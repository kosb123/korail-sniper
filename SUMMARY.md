# korail-sniper 프로젝트 요약

## 완료된 작업
1. **패키지 구조화**
   - `korail_sniper/__init__.py` 생성
   - SRT 클라이언트 (`korail_sniper/srt_client.py`)
   - Korail 클라이언트 (`korail_sniper/korail_client.py`)
   - 상수 모듈 (`korail_sniper/constants.py`)
   - NetFunnel 헬퍼 (`korail_sniper/netfunnel.py`)
   - 유틸리티 모듈 (`korail_sniper/utils.py`) - 재시도 데코레이터 추가

2. **예시 및 테스트 스크립트**
   - `examples/mock_srt_demo.py`: SRT 클라이언트 모의 시연
   - `examples/mock_korail_demo.py`: Korail 클라이언트 모의 시연
   - `examples/korail_seed_sample.json`: 샘플 시드 데이터
   - `examples/ptj_to_sd_seed.json`: 평택지제→증평 샘플 시드 데이터
   - `waitlist_watcher.py`: 특정 구간의 대기열을 주기적으로 확인하는 스크립트
   - `test_waitlist.py`: waitlist_watcher의 테스트 버전 (한 번만 실행)

3. **Git 및 GitHub 연동**
   - 로컬 저장소 초기화 및 초기 커밋
   - GitHub 저장소 생성 및 푸시 (https://github.com/kosb123/korail-sniper)
   - 여러 차례의 업데이트 푸시

4. **최적화 및 안정성 향상**
   - 재시도 데코레이터 추가 (`utils.retry`)
   - SRT 클라이언트의 `login`, `search_trains`, `reserve` 메서드에 재시도 로직 적용
   - Korail 클라이언트의 `check_seats` 메서드에 재시도 로직 적용
   - 지수 백오프 전략으로 네트워크 오류에 대한 내성 향상

5. **문서화**
   - `README.md`에 설치 및 사용 방법 설명
   - `SUMMARY.md` (이 파일)에 프로젝트 요약

## 현재 상태
- 작업 디렉터리: `C:/Users/jun/projects/korail-sniper`
- Git 브랜치: master
- 원격 저장소: origin (GitHub)
- Python 패키지로서 설치 가능: `pip install -e .`
- 필수 의존성: `requests`, `curl_cffi`

## 사용 예시
### SRT 클라이언트 (인증 필요)
```python
from korail_sniper.srt_client import SRTClient, SeatType
client = SRTClient()
# client.login("your_id", "your_password")
# trains = client.search_trains("서울", "부산", "20240101", "050000")
```

### Korail 클라이언트 (시드 기반)
```python
from korail_sniper.korail_client import KorailClient
trains = KorailClient.load_seed("examples/korail_seed_sample.json")
client = KorailClient()
for train in trains:
    try:
        result = client.check_seats(train)
        if KorailClient.has_available_seat(result):
            print(f"{train.label}: seats available")
    except Exception as e:
        print(f"{train.label}: {e}")
```

### 대기열 감시 (예: 평택지제→증평)
```bash
python waitlist_watcher.py examples/ptj_to_sd_seed.json 20261009 평택지제 증평
```

## 향후 개선 방향
1. 실제 인증을 통한 SRT/Korail 예약 자동화 테스트
2. 더 정교한 대기열 알림 (데스크톱 알림, 음성 알림 등)
3. 여러 구간 동시 모니터링 지원
4. 브라우저 자동화 (Playwright)를 통한 시드 자동 수집
5. Docker 이미지화로 배포 용이성 향상
6. GitHub Actions를 통한 CI/CD 파이프라인 구축

---
마지막 업데이트: 2026-10-08