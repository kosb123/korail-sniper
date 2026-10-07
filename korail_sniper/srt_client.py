# -*- coding: utf-8 -*-
"""SRT (Super Rapid Train) Client implementation."""

import json
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

try:
    import curl_cffi.requests as curl_req
    HAS_CURL_CFFI = True
except ImportError:
    import requests as curl_req
    HAS_CURL_CFFI = False

from .constants import SRT_STATIONS, TRAIN_NAMES, SeatType, USER_AGENTS
from .netfunnel import NetFunnelHelper

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
PHONE_REGEX = re.compile(r"(\d{3})-?(\d{3,4})-?(\d{4})")

SRT_MOBILE = "https://app.srail.or.kr:443"
API_ENDPOINTS = {
    "main": f"{SRT_MOBILE}/main/main.do",
    "login": f"{SRT_MOBILE}/apb/selectListApb01080_n.do",
    "logout": f"{SRT_MOBILE}/login/loginOut.do",
    "search_schedule": f"{SRT_MOBILE}/ara/selectListAra10007_n.do",
    "reserve": f"{SRT_MOBILE}/arc/selectListArc05013_n.do",
    "tickets": f"{SRT_MOBILE}/atc/selectListAtc14016_n.do",
    "ticket_info": f"{SRT_MOBILE}/ard/selectListArd02019_n.do",
    "cancel": f"{SRT_MOBILE}/ard/selectListArd02045_n.do",
    "reserve_info": f"{SRT_MOBILE}/atc/getListAtc14087.do",
}


class SRTError(Exception):
    pass


class SRTLoginError(SRTError):
    pass


class SRTTrain:
    """Represents an SRT Train entry."""

    def __init__(self, data: dict):
        self.raw = data
        self.train_code = data.get("stlbTrnClsfCd", "17")
        self.train_name = TRAIN_NAMES.get(self.train_code, "SRT")
        self.train_number = data.get("trnNo", "")

        self.dep_date = data.get("dptDt", "")
        self.dep_time = data.get("dptTm", "")
        self.dep_station_code = data.get("dptRsStnCd", "")
        self.dep_station_name = data.get("dptRsStnNm", "")

        self.arr_date = data.get("arvDt", "")
        self.arr_time = data.get("arvTm", "")
        self.arr_station_code = data.get("arvRsStnCd", "")
        self.arr_station_name = data.get("arvRsStnNm", "")

        self.dep_order = data.get("dptStnRunOrdr", "")
        self.arr_order = data.get("arvStnRunOrdr", "")

        self.general_seat_state = data.get("gnrmRsvPsbStr", "")
        self.special_seat_state = data.get("sprmRsvPsbStr", "")
        self.reserve_wait_name = data.get("rsvWaitPsbCdNm", "")
        self.reserve_wait_code = data.get("rsvWaitPsbCd", "-1")

    def has_general_seat(self) -> bool:
        return "예약하기" in self.general_seat_state or "가능" in self.general_seat_state

    def has_special_seat(self) -> bool:
        return "예약하기" in self.special_seat_state or "가능" in self.special_seat_state

    def has_seat(self, seat_type: SeatType = SeatType.GENERAL_FIRST) -> bool:
        if seat_type == SeatType.GENERAL_ONLY:
            return self.has_general_seat()
        elif seat_type == SeatType.SPECIAL_ONLY:
            return self.has_special_seat()
        return self.has_general_seat() or self.has_special_seat()

    def has_waiting_list(self) -> bool:
        return str(self.reserve_wait_code) == "9" or "신청하기" in self.reserve_wait_name

    def __repr__(self) -> str:
        dep_fmt = f"{self.dep_time[:2]}:{self.dep_time[2:4]}" if len(self.dep_time) >= 4 else self.dep_time
        arr_fmt = f"{self.arr_time[:2]}:{self.arr_time[2:4]}" if len(self.arr_time) >= 4 else self.arr_time
        gen = "일반실 [가능]" if self.has_general_seat() else "일반실 [매진]"
        spe = "특실 [가능]" if self.has_special_seat() else "특실 [매진]"
        wait = " 대기 [가능]" if self.has_waiting_list() else ""
        return f"[{self.train_name} {self.train_number:>4s}] {self.dep_station_name}→{self.arr_station_name} ({dep_fmt}~{arr_fmt}) | {gen}, {spe}{wait}"


class SRTReservation:
    """Represents a successful SRT reservation."""

    def __init__(self, data: dict):
        self.raw = data
        self.reservation_number = data.get("pnrNo", "")
        self.total_cost = data.get("rcvdAmt", "")
        self.seat_count = data.get("totPrnb", "1")
        self.train_number = data.get("trnNo", "")
        self.dep_time = data.get("dptTm", "")
        self.arr_time = data.get("arvTm", "")
        self.limit_date = data.get("ntisuLmtDt", "")
        self.limit_time = data.get("ntisuLmtTm", "")

    def __repr__(self) -> str:
        lim = f"{self.limit_date} {self.limit_time[:2]}:{self.limit_time[2:4]}" if self.limit_time else "확인요망"
        return f"[SRT 예약완료] 예약번호: {self.reservation_number} | 열차: {self.train_number}호 | 금액: {self.total_cost}원 | 결제기한: {lim}"


class SRTClient:
    """SRT API Client for searching and reserving tickets."""

    def __init__(self, user_id: Optional[str] = None, password: Optional[str] = None, verbose: bool = False):
        self.user_id = user_id
        self.password = password
        self.verbose = verbose
        self.is_logged_in = False
        self.membership_number: Optional[str] = None
        self.user_name: Optional[str] = None

        if HAS_CURL_CFFI:
            self._session = curl_req.Session(impersonate="chrome")
        else:
            self._session = curl_req.Session()

        self._session.headers.update({
            "User-Agent": USER_AGENTS["ANDROID_SRT"],
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        })
        self._netfunnel = NetFunnelHelper(host="nf.letskorail.com", debug=verbose)

    def _log(self, msg: str):
        if self.verbose:
            print(f"[SRT] {msg}")

    def login(self, user_id: Optional[str] = None, password: Optional[str] = None) -> bool:
        uid = user_id or self.user_id
        pwd = password or self.password
        if not uid or not pwd:
            raise SRTLoginError("아이디/비밀번호가 지정되지 않았습니다.")

        login_type = "2" if EMAIL_REGEX.match(uid) else ("3" if PHONE_REGEX.match(uid) else "1")
        if login_type == "3":
            uid = re.sub(r"-", "", uid)

        data = {
            "auto": "Y",
            "check": "Y",
            "page": "menu",
            "deviceKey": "-",
            "customerYn": "",
            "login_referer": API_ENDPOINTS["main"],
            "srchDvCd": login_type,
            "srchDvNm": uid,
            "hmpgPwdCphd": pwd,
        }

        try:
            r = self._session.post(API_ENDPOINTS["login"], data=data, timeout=10)
            self._log(f"Login status: {r.status_code}")
            if "존재하지않는" in r.text or "비밀번호 오류" in r.text:
                raise SRTLoginError("로그인 실패: 회원번호 또는 비밀번호가 올바르지 않습니다.")

            try:
                j = json.loads(r.text)
                user_info = j.get("userMap", [{}])[0]
                self.membership_number = user_info.get("mbCrNo", uid)
                self.user_name = user_info.get("custNm", "")
                self.is_logged_in = True
                self._log(f"로그인 성공: {self.user_name} ({self.membership_number})")
                return True
            except Exception:
                if r.status_code == 200 and "FAIL" not in r.text:
                    self.is_logged_in = True
                    return True
                raise SRTLoginError(f"로그인 응답 파싱 실패: {r.text[:150]}")
        except Exception as e:
            raise SRTLoginError(f"SRT 로그인 오류: {e}")

    def search_trains(
        self,
        dep: str,
        arr: str,
        date: Optional[str] = None,
        time_str: Optional[str] = None,
        seat_type: SeatType = SeatType.GENERAL_FIRST,
        available_only: bool = False,
    ) -> List[SRTTrain]:
        """Search trains between dep and arr stations."""
        dep_code = SRT_STATIONS.get(dep)
        arr_code = SRT_STATIONS.get(arr)
        if not dep_code or not arr_code:
            raise SRTError(f"SRT 정차역이 아닙니다: {dep} 또는 {arr}")

        if not date:
            date = datetime.now().strftime("%Y%m%d")
        if not time_str:
            time_str = "000000"

        netfunnel_key = self._netfunnel.run() or ""

        data = {
            "chtnDvCd": "1",
            "arriveTime": "N",
            "seatAttCd": "015",
            "psgNum": "1",
            "trnGpCd": "109",
            "stlbTrnClsfCd": "05",
            "dptDt": date,
            "dptTm": time_str,
            "arvRsStnCd": arr_code,
            "dptRsStnCd": dep_code,
            "netfunnelKey": netfunnel_key,
        }

        r = self._session.post(API_ENDPOINTS["search_schedule"], data=data, timeout=10)
        self._log(f"Schedule response length: {len(r.text)}")

        try:
            j = json.loads(r.text)
            out_sets = j.get("outDataSets", {}).get("dsOutput1", [])
            trains = [SRTTrain(item) for item in out_sets]

            if available_only:
                trains = [t for t in trains if t.has_seat(seat_type)]

            return trains
        except Exception as e:
            self._log(f"Search parse error: {e}")
            return []

    def reserve(
        self,
        train: SRTTrain,
        seat_type: SeatType = SeatType.GENERAL_FIRST,
    ) -> SRTReservation:
        """Reserve a seat on the selected train."""
        if not self.is_logged_in:
            self.login()

        psrm_cd = "2" if (seat_type == SeatType.SPECIAL_ONLY or (seat_type == SeatType.SPECIAL_FIRST and train.has_special_seat())) else "1"

        data = {
            "stlbTrnClsfCd": train.train_code,
            "trnGpCd": "300",
            "trnNo": train.train_number,
            "dptDt": train.dep_date,
            "dptTm": train.dep_time,
            "dptRsStnCd": train.dep_station_code,
            "arvRsStnCd": train.arr_station_code,
            "dptStnRunOrdr": train.dep_order,
            "arvStnRunOrdr": train.arr_order,
            "jobId": "1101",  # 개인예약
            "totPrnb": "1",
            "psgGridcnt": "1",
            "psgTpCd1": "1",  # 어른
            "psgInfoPerPrnb1": "1",
            "psrmClCd1": psrm_cd,
            "locSeatAttCd1": "000",
            "rqSeatAttCd1": "015",
            "dirSeatAttCd1": "009",
            "smkSeatAttCd1": "000",
            "etcSeatAttCd1": "000",
        }

        r = self._session.post(API_ENDPOINTS["reserve"], data=data, timeout=10)
        self._log(f"Reserve response: {r.text[:200]}")

        try:
            j = json.loads(r.text)
            output = j.get("outDataSets", {}).get("dsOutput1", [{}])[0]
            if not output or output.get("strResult") == "FAIL":
                msg = output.get("msgTxt") or j.get("msgTxt") or "예약 실패"
                raise SRTError(f"예약 실패: {msg}")
            return SRTReservation(output)
        except Exception as e:
            if isinstance(e, SRTError):
                raise
            raise SRTError(f"예약 응답 오류: {e}")
