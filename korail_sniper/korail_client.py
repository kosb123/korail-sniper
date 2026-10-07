# -*- coding: utf-8 -*-
"""Korail client using officially exposed web endpoints where available.

The current Korail web search endpoint is WAF-protected. To avoid repeated
search requests, this client accepts a one-time schedule seed exported from a
normal browser session, then checks availability only for those known trains.

"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from .constants import USER_AGENTS
from .utils import retry

KORAIL_BASE = "https://www.korail.com"
SEAT_ENDPOINT = f"{KORAIL_BASE}/classes/com.korail.mobile.research.TResidualSeatsResearch.do"


class KorailError(Exception):
    pass


class KorailTrain:
    """Known Korail train metadata required for a residual-seat query."""

    REQUIRED = {
        "runDt", "trnNo", "trnClsfCd", "trnGpCd", "dptRsStnCd",
        "arvRsStnCd", "dptStnRunOrdr", "arvStnRunOrdr",
    }

    def __init__(self, data: Dict[str, Any]):
        missing = self.REQUIRED - set(data)
        if missing:
            raise KorailError(f"열차 시드에 필요한 값이 없습니다: {', '.join(sorted(missing))}")
        self.raw = data
        for key, value in data.items():
            setattr(self, key, str(value) if value is not None else "")

    @property
    def label(self) -> str:
        name = self.raw.get("trnClsfNm") or self.raw.get("trainName") or "열차"
        dep = self.raw.get("dptTm") or ""
        arr = self.raw.get("arvTm") or ""
        return f"{name} {self.trnNo}호 {dep[:2]}:{dep[2:4]}~{arr[:2]}:{arr[2:4]}"

    def seat_query_data(self) -> Dict[str, str]:
        return {
            "runDt": self.runDt,
            "trnNo": self.trnNo,
            "trnClsfCd": self.trnClsfCd,
            "trnGpCd": self.trnGpCd,
            "dptRsStnCd": self.dptRsStnCd,
            "arvRsStnCd": self.arvRsStnCd,
            "psrmClCd": self.raw.get("psrmClCd", "1"),
            "seatAttCd": self.raw.get("seatAttCd", "015"),
            "dptStnRunOrdr": self.dptStnRunOrdr,
            "arvStnRunOrdr": self.arvStnRunOrdr,
            "totPsgCnt": self.raw.get("totPsgCnt", "1"),
            "srcarNo": self.raw.get("srcarNo", ""),
            "langCode": self.raw.get("langCode", "ko"),
            "gdNo": self.raw.get("gdNo", ""),
            "Device": "BH",
            "Version": "999999999",
        }


class KorailClient:
    """Availability client for a pre-seeded Korail train list."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": USER_AGENTS["CHROME_DESKTOP"],
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
            "Origin": KORAIL_BASE,
            "Referer": f"{KORAIL_BASE}/ticket/search/list",
        })

    @staticmethod
    def load_seed(path: str | Path) -> List[KorailTrain]:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        entries = data.get("trains", data) if isinstance(data, dict) else data
        if not isinstance(entries, list):
            raise KorailError("시드 파일은 열차 목록(JSON 배열 또는 {trains: [...]})이어야 합니다.")
        return [KorailTrain(entry) for entry in entries]

    @retry(max_attempts=3, initial_delay=1.0, backoff_factor=2.0, exceptions=(KorailError,))
    def check_seats(self, train: KorailTrain) -> Dict[str, Any]:
        """Check a known train. Does not initiate booking or payment."""
        r = self._session.post(SEAT_ENDPOINT, data=train.seat_query_data(), timeout=10)
        try:
            result = r.json()
        except Exception:
            raise KorailError(f"좌석 조회 응답 해석 실패 ({r.status_code}): {r.text[:180]}")

        if result.get("strResult") != "SUCC":
            msg = result.get("h_msg_txt") or result.get("errMsg") or "알 수 없는 오류"
            raise KorailError(f"{train.label} 좌석 조회 실패: {msg}")
        return result

    @staticmethod
    def has_available_seat(result: Dict[str, Any]) -> bool:
        """Interpret variable response payloads conservatively."""
        # Common explicit counts / availability values from Korail responses
        text = json.dumps(result, ensure_ascii=False)
        unavailable = ("매진", "불가", "없음")
        available_markers = ("예약가능", "좌석 있음", "가능")
        return any(marker in text for marker in available_markers) and not all(marker in text for marker in unavailable)
