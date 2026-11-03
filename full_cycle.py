# -*- coding: utf-8 -*-
"""Full SRT cycle test: login -> search -> reserve -> verify -> cancel -> verify.

Credentials: SRT_ID / SRT_PW from .env (repo root) or environment variables.
Usage:
    .venv/Scripts/python.exe full_cycle.py <출발역> <도착역> [YYYYMMDD] [HHMMSS]

Example:
    .venv/Scripts/python.exe full_cycle.py 수서 평택지제 20261104
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from korail_sniper.constants import TRAIN_NAMES
from korail_sniper.srt_client import SRTClient, SRTError, SeatType

SRT_LIVE_CODE = "0A"  # stlbTrnClsfCd for SRT trains in the live app API

LOG_PATH = Path(__file__).parent / "full_cycle.log"


def log(step: str, **kw):
    rec = {"ts": datetime.now().isoformat(timespec="seconds"), "step": step}
    rec.update(kw)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"[{rec['ts'][11:]}] {step}", {k: v for k, v in kw.items() if k != "raw"})


def load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def pnr_in_res_list(resp, pnr: str) -> bool:
    return pnr in json.dumps(resp, ensure_ascii=False)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    dep, arr = sys.argv[1], sys.argv[2]
    date = sys.argv[3] if len(sys.argv) > 3 else datetime.now().strftime("%Y%m%d")
    tm = sys.argv[4] if len(sys.argv) > 4 else "000000"

    load_env()
    uid = os.environ.get("SRT_ID")
    pwd = os.environ.get("SRT_PW")
    if not uid or not pwd:
        print("FAIL: .env에 SRT_ID/SRT_PW가 없습니다.")
        sys.exit(2)

    c = SRTClient(user_id=uid, password=pwd, verbose=True)

    # 1. login
    c.login()
    log("LOGIN", ok=True, name=c.user_name, mbCrNo=c.membership_number)

    # 2. search
    trains = c.search_trains(dep, arr, date, tm)
    log("SEARCH", count=len(trains), dep=dep, arr=arr, date=date)
    for t in trains:
        print("   ", t)

    srt_trains = [t for t in trains if t.train_code == SRT_LIVE_CODE and t.has_general_seat()]
    if not srt_trains:
        print("FAIL: 좌석 있는 SRT 열차 없음 (이 시간대/날짜는 취소표 없음 가능)")
        sys.exit(3)

    train = srt_trains[0]
    print("선택:", train)

    # 3. reserve
    try:
        res = c.reserve(train, SeatType.GENERAL_ONLY)
    except SRTError as e:
        print(f"FAIL: 예약 실패: {e}")
        sys.exit(4)
    pnr = res.reservation_number
    log("RESERVE", ok=True, pnr=pnr, fare=res.total_cost, limit=res.limit_date + " " + res.limit_time)
    print("예약완료:", res)

    # 4. verify in my reservation list
    try:
        rl = c.get_my_reservations()
        found = pnr_in_res_list(rl, pnr)
        log("VERIFY_LIST", pnr=pnr, found=found, raw_len=len(json.dumps(rl)))
        print("예약조회 원문(절대):", json.dumps(rl, ensure_ascii=False)[:400])
    except SRTError as e:
        print(f"WARN: 예약조회 실패 (취소는 시도): {e}")
        found = None

    # 5. cancel
    try:
        cx = c.cancel(pnr, train)
        log("CANCEL", ok=True, raw=json.dumps(cx, ensure_ascii=False)[:300])
    except SRTError as e:
        print(f"FAIL: 취소 실패: {e}")
        log("CANCEL", ok=False, error=str(e))
        sys.exit(5)

    # 6. verify gone
    time.sleep(2)
    try:
        rl2 = c.get_my_reservations()
        still = pnr_in_res_list(rl2, pnr)
        log("VERIFY_GONE", pnr=pnr, still_present=still)
    except SRTError as e:
        print(f"WARN: 취소 후 조회 실패: {e}")
        still = None

    print()
    print("=== RESULT ===")
    print(f"예약: pnr={pnr} fare={res.total_cost}")
    print(f"예약조회에 존재: {found}")
    print(f"취소: 성공")
    print(f"취소 후 여전히 존재: {still}")
    if found is not False and still is False:
        print("PASS: 전체 사이클 확인 (예약 -> 조회 -> 취소 -> 소멸)")
    else:
        print("PARTIAL: 사이클은 완료됐지만 조회 검증이 불확실 (필드 구조 확인 필요)")


if __name__ == "__main__":
    main()
