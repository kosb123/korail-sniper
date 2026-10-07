# -*- coding: utf-8 -*-
"""NetFunnel token helper and queue solver for Korail / SRT systems."""

import re
import time
from typing import Optional, Tuple

try:
    import curl_cffi.requests as curl_req
    HAS_CURL_CFFI = True
except ImportError:
    import requests as curl_req
    HAS_CURL_CFFI = False


class NetFunnelHelper:
    """Helper to bypass or acquire valid NetFunnel queuing tokens."""

    WAIT_STATUS_PASS = "200"
    WAIT_STATUS_FAIL = "201"
    ALREADY_COMPLETED = "502"

    OP_CODE = {
        "getTidchkEnter": "5101",
        "chkEnter": "5002",
        "setComplete": "5004",
    }

    DEFAULT_HEADERS = {
        "Host": "nf.letskorail.com",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "sec-ch-ua-platform": "Android",
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 15; SM-S912N Build/AP3A.240905.015.A2; wv) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/136.0.7103.125 Mobile Safari/537.36SRT-APP-Android V.2.0.38"
        ),
        "Accept": "*/*",
        "X-Requested-With": "kr.co.srail.newapp",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Referer": "https://app.srail.or.kr/",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    def __init__(self, host: str = "nf.letskorail.com", debug: bool = False):
        self.host = host
        self.debug = debug
        if HAS_CURL_CFFI:
            self._session = curl_req.Session(impersonate="chrome")
        else:
            self._session = curl_req.Session()
        self._session.headers.update(self.DEFAULT_HEADERS)
        self._cached_key: Optional[str] = None
        self._last_fetch_time: float = 0
        self._cache_ttl: float = 45.0  # 45 seconds TTL

    def run(self) -> Optional[str]:
        """Obtain a valid NetFunnel pass key."""
        current_time = time.time()
        if self._cached_key and (current_time - self._last_fetch_time) < self._cache_ttl:
            return self._cached_key

        try:
            status, self._cached_key, nwait, ip = self._start()
            self._last_fetch_time = current_time

            # In case of waiting queue
            while status == self.WAIT_STATUS_FAIL:
                if self.debug:
                    print(f"[*] NetFunnel queue waiting: {nwait} ahead...")
                time.sleep(1.0)
                status, self._cached_key, nwait, ip = self._check(ip)

            status, *_ = self._complete(ip)
            if status in (self.WAIT_STATUS_PASS, self.ALREADY_COMPLETED):
                return self._cached_key

            self.clear()
            return None
        except Exception as ex:
            if self.debug:
                print(f"[!] NetFunnel error: {ex}")
            self.clear()
            return None

    def clear(self):
        self._cached_key = None
        self._last_fetch_time = 0

    def _start(self) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        return self._make_request("getTidchkEnter")

    def _check(self, ip: Optional[str] = None) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        return self._make_request("chkEnter", ip)

    def _complete(self, ip: Optional[str] = None) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        return self._make_request("setComplete", ip)

    def _make_request(self, opcode: str, ip: Optional[str] = None) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        url = f"https://{ip or self.host}/ts.wseq"
        params = self._build_params(self.OP_CODE[opcode])
        try:
            r = self._session.get(url, params=params, timeout=5)
            response = self._parse(r.text)
            return response.get("status"), response.get("key"), response.get("nwait"), response.get("ip")
        except Exception:
            return None, None, None, None

    def _build_params(self, opcode: str, key: Optional[str] = None) -> dict:
        params = {
            "opcode": opcode,
            "nfid": "0",
            "prefix": f"NetFunnel.gRtype={opcode};",
            "js": "true",
            str(int(time.time() * 1000)): "",
        }
        if opcode in (self.OP_CODE["getTidchkEnter"], self.OP_CODE["chkEnter"]):
            params.update({"sid": "service_1", "aid": "act_10"})
            if opcode == self.OP_CODE["chkEnter"]:
                params.update({"key": key or self._cached_key, "ttl": "1"})
        elif opcode == self.OP_CODE["setComplete"]:
            params["key"] = key or self._cached_key
        return params

    def _parse(self, response: str) -> dict:
        result_match = re.search(r"NetFunnel\.gControl\.result='([^']+)'", response)
        if not result_match:
            return {}
        parts = result_match.group(1).split(":", 2)
        if len(parts) < 3:
            return {}
        code, status, params_str = parts[0], parts[1], parts[2]
        params = dict(param.split("=", 1) for param in params_str.split("&") if "=" in param)
        params.update({"code": code, "status": status})
        return params
