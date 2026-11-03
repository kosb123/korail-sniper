# -*- coding: utf-8 -*-
"""SRT 취소표 sniper: poll schedule, reserve the first free SRT seat, KEEP it.

Usage:
    .venv/Scripts/python.exe sniper.py <출발역> <도착역> [YYYYMMDD] [HHMMSS] [--interval 2]

Behavior:
- Polls the SRT schedule every `interval` seconds.
- On the first SRT train (live code 0A) with a general seat, reserves it and
  prints/logs the PNR, then stops. The reservation is kept (payment pending
  until its deadline) — cancel it in the app or with SRTClient.cancel().
- Without .env credentials it runs watch-only: logs availability, no booking.

Log: sniper.log (JSONL, one line per poll).
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from korail_sniper.constants import TRAIN_NAMES
from korail_sniper.srt_client import SRTClient, SRTError, SeatType

SRT_LIVE_CODE = "0A"
LOG_PATH = Path(__file__).parent / "sniper.log"


def log(step: str, **kw):
    rec = {"ts": datetime.now().isoformat(timespec="seconds"), "step": step}
    rec.update(kw)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def main():
    raw = sys.argv[1:]
    interval = 2
    if "--interval" in raw:
        i = raw.index("--interval")
        interval = float(raw[i + 1])
        raw = raw[:i] + raw[i + 2:]
    args = raw
    if len(args) < 3:
        print(__doc__)
        sys.exit(1)
    dep, arr, date = args[0], args[1], args[2]
    tm = args[3] if len(args) > 3 else "000000"

    load_env()
    uid = os.environ.get("SRT_ID")
    pwd = os.environ.get("SRT_PW")

    c = SRTClient(verbose=False)
    if uid and pwd:
        c.user_id, c.password = uid, pwd
        try:
            c.login()
            log("LOGIN", ok=True, name=c.user_name)
            mode = "arm"
            print(f"ARMED: {dep}->{arr} {date} from {tm}, interval {interval}s, account {c.user_name}")
        except SRTError as e:
            log("LOGIN", ok=False, error=str(e))
            print(f"WARN: 로그인 실패, 관측 전용으로 진행: {e}")
            mode = "watch"
    else:
        mode = "watch"
        print(f"WATCH-ONLY: {dep}->{arr} {date} from {tm} (.env 없으면 예약 불가)")

    n = 0
    while True:
        n += 1
        try:
            trains = c.search_trains(dep, arr, date, tm)
        except SRTError as e:
            log("SEARCH_ERR", error=str(e), n=n)
            time.sleep(interval * 3)
            continue

        free = [t for t in trains if t.train_code == SRT_LIVE_CODE and t.has_general_seat()]
        log("POLL", n=n, total=len(trains), srt_free=len(free),
            free=[f"{t.train_number} {t.dep_time[:4]}" for t in free][:10])

        if free and mode == "arm":
            train = free[0]
            print(f">> 좌석 발견: {train}  -> 예약 시도")
            try:
                res = c.reserve(train, SeatType.GENERAL_ONLY)
                log("RESERVE", ok=True, pnr=res.reservation_number,
                    train=train.train_number, fare=res.total_cost,
                    limit=f"{res.limit_date} {res.limit_time}")
                print(f"=== GRABBED === pnr={res.reservation_number} fare={res.total_cost}")
                print(f"결제기한: {res.limit_date} {res.limit_time[:2]}:{res.limit_time[2:4]}")
                print("예약은 유지됩니다. 취소하려면 앱 또는 SRTClient.cancel(pnr) 사용.")
                return
            except SRTError as e:
                log("RESERVE", ok=False, error=str(e), train=train.train_number)
                print(f"!! 예약 실패: {e} (다음 폴링 재시도)")

        time.sleep(interval)


if __name__ == "__main__":
    main()
