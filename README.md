# Korail/SRT sniper

A Python package for searching and reserving tickets on Korail and SRT (Super Rapid Train) systems.

## Features

- SRT client for searching trains and making reservations
- Korail client for checking seat availability on pre-seeded train schedules
- Helper modules for station codes, NetFunnel token handling, and more

## Installation

```bash
pip install .
```

## Usage

### SRT Client

```python
from korail_sniper.srt_client import SRTClient, SeatType

# Initialize client (optional: set verbose=True for debug output)
client = SRTClient()

# Login with your credentials
# client.login("your_id", "your_password")

# Search for trains (example: Seoul to Busan on 2024-01-01)
# trains = client.search_trains("서울", "부산", "20240101", "050000")
# for train in trains:
#     print(train)

# Reserve a seat on a selected train
# reservation = client.reserve(train, SeatType.GENERAL_FIRST)
# print(reservation)
```

### Korail Client

```python
from korail_sniper.korail_client import KorailClient

# Load train seeds from a JSON file (exported from browser)
# trains = KorailClient.load_seed("korail_trains.json")
# client = KorailClient()
# for train in trains:
#     try:
#         result = client.check_seats(train)
#         if KorailClient.has_available_seat(result):
#             print(f"{train.label}: seats available")
#     except Exception as e:
#         print(f"{train.label}: {e}")
```

## Station Codes

Station codes are available in `korail_sniper/constants.py` as `SRT_STATIONS` dictionary.

## License

MIT