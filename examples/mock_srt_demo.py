"""Mock demonstration of SRT client usage without real network calls."""

from korail_sniper.srt_client import SRTClient, SRTTrain, SeatType

def main():
    print("=== SRT Client Mock Demo ===")
    # Create client (no credentials needed for mock)
    client = SRTClient()
    
    # Show how to create a fake train object (as if from search results)
    fake_train_data = {
        "stlbTrnClsfCd": "05",
        "trnNo": "123",
        "dptDt": "20240101",
        "dptTm": "050000",
        "dptRsStnCd": "0001",  # 서울
        "dptRsStnNm": "서울",
        "arvDt": "20240101",
        "arvTm": "080000",
        "arvRsStnCd": "0020",  # 부산
        "arvRsStnNm": "부산",
        "dptStnRunOrdr": "0",
        "arvStnRunOrdr": "10",
        "gnrmRsvPsbStr": "예약하기",
        "sprmRsvPsbStr": "예약하기",
        "rsvWaitPsbCd": "-1",
        "rsvWaitPsbCdNm": "예약하기"
    }
    
    train = SRTTrain(fake_train_data)
    print(f"Fake train: {train}")
    print(f"Has general seat: {train.has_general_seat()}")
    print(f"Has special seat: {train.has_special_seat()}")
    print(f"Has waiting list: {train.has_waiting_list()}")
    
    # Show reservation attempt would require login
    print("\n--- Reservation would require login ---")
    print("To reserve, you need to call client.login(id, pwd) first")
    print("Then: reservation = client.reserve(train, SeatType.GENERAL_FIRST)")
    
    print("\nDemo complete.")

if __name__ == "__main__":
    main()