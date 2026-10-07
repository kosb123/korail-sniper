"""Mock demonstration of Korail client usage with sample seed data."""

import json
from korail_sniper.korail_client import KorailClient

def main():
    print("=== Korail Client Mock Demo ===")
    
    # Sample seed data mimicking what might be exported from browser
    sample_seed = {
        "trains": [
            {
                "runDt": "20240101",
                "trnNo": "101",
                "trnClsfCd": "10",
                "trnGpCd": "01",
                "dptRsStnCd": "0001",
                "arvRsStnCd": "0020",
                "dptStnRunOrdr": "0",
                "arvStnRunOrdr": "15",
                "trnClsfNm": "KTX",
                "dptTm": "060000",
                "arvTm": "090000",
                "totPsgCnt": "1000",
                "srcarNo": "01",
                "langCode": "ko",
                "gdNo": "12345",
                "psrmClCd": "1",
                "seatAttCd": "015"
            },
            {
                "runDt": "20240101",
                "trnNo": "102",
                "trnClsfCd": "10",
                "trnGpCd": "01",
                "dptRsStnCd": "0001",
                "arvRsStnCd": "0020",
                "dptStnRunOrdr": "0",
                "arvStnRunOrdr": "15",
                "trnClsfNm": "KTX",
                "dptTm": "070000",
                "arvTm": "100000",
                "totPsgCnt": "1000",
                "srcarNo": "01",
                "langCode": "ko",
                "gdNo": "12345",
                "psrmClCd": "1",
                "seatAttCd": "015"
            }
        ]
    }
    
    # Save sample seed to file
    seed_path = "examples/korail_seed_sample.json"
    with open(seed_path, "w", encoding="utf-8") as f:
        json.dump(sample_seed, f, ensure_ascii=False, indent=2)
    print(f"Sample seed saved to {seed_path}")
    
    # Load trains from seed
    trains = KorailClient.load_seed(seed_path)
    print(f"Loaded {len(trains)} trains from seed")
    
    # Create client (won't actually make real requests in this mock)
    client = KorailClient()
    print("KorailClient initialized")
    
    # Show how to check seats would work
    print("\n--- Seat checking would work like this ---")
    for i, train in enumerate(trains, 1):
        print(f"Train {i}: {train.label}")
        print(f"  Query data keys: {list(train.seat_query_data().keys())[:5]}...")
        print("  To check: result = client.check_seats(train)")
        print("  Then: available = KorailClient.has_available_seat(result)")
        print()
    
    print("Demo complete.")
    print("Note: Actual seat checking requires network access and may be blocked by WAF.")

if __name__ == "__main__":
    main()