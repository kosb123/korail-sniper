#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor Korail residual seats (waitlist) for a given route and date.
Usage:
    python waitlist_watcher.py <seed.json> <YYYYMMDD> <start_station_name> <end_station_name>
Example:
    python waitlist_watcher.py examples/korail_seed_sample.json 20240101 평택지제 증평
The script will poll every 30 seconds and print when a waitlist opens (rsvWaitPsbCd != '-1').

"""
import json
import sys
import time
from pathlib import Path
from korail_sniper.korail_client import KorailClient, KorailTrain

def load_station_codes():
    """Load station_codes.json fallback."""
    try:
        with open(Path(__file__).parent / "station_codes.json", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def get_station_code(name: str) -> str:
    codes = load_station_codes()
    # exact match first
    if name in codes:
        return codes[name]
    # fallback: contains
    for k, v in codes.items():
        if name in k or name in v:
            return v
    raise ValueError(f"역 이름을 찾을 수 없습니다: {name}")

def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)
    seed_path, date_str, start_name, end_name = sys.argv[1:]
    try:
        start_code = get_station_code(start_name)
        end_code = get_station_code(end_name)
    except ValueError as e:
        print(e)
        sys.exit(1)

    # Load seed
    try:
        trains = KorailClient.load_seed(seed_path)
    except Exception as e:
        print(f"시드 파일 로드 실패: {e}")
        sys.exit(1)

    # Filter trains for date and stations
    candidates = [
        t for t in trains
        if t.raw.get("runDt") == date_str
        and t.raw.get("dptRsStnCd") == start_code
        and t.raw.get("arvRsStnCd") == end_code
    ]
    if not candidates:
        print(f"시드에 해당 조건({date_str} {start_name}->{end_name}) 열차가 없습니다.")
        print("시드에 있는 열차 수:", len(trains))
        # show first few for debugging
        for t in trains[:5]:
            print(f"  {t.label} ({t.raw.get('runDt')} {t.raw.get('dptRsStnCd')}->{t.raw.get('arvRsStnCd')})")
        sys.exit(1)

    print(f"대상 열차 {len(candidates)}개 발견. 30초 간격으로 대기열 확인 시작...")
    client = KorailClient(verbose=False)
    try:
        while True:
            for train in candidates:
                try:
                    result = client.check_seats(train)
                    # parse waitlist flag
                    wait_flag = result.get("rsvWaitPsbCd", "-1")
                    if wait_flag != "-1":
                        # also check if any seat available
                        avail = KorailClient.has_available_seat(result)
                        print(f"\n[{time.strftime('%H:%M:%S')}] {train.label}")
                        print(f"  대기열 플래그: {wait_flag} (좌석 예약가능: {avail})")
                        # optionally show full result
                        # print(json.dumps(result, ensure_ascii=False, indent=2))
                except Exception as e:
                    if client.verbose:
                        print(f"오류 ({train.label}): {e}")
                # small delay between requests to be gentle
                time.sleep(0.5)
            print(f"[{time.strftime('%H:%M:%S')}] 주기 완료, 30초 후 재시작...")
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n중지됨.")

if __name__ == "__main__":
    main()