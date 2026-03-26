import os
import requests
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from supabase import create_client, Client

from engine.data_models import Boat, Race
from engine.predict_engine import predict

# ============================================================
#  Supabase 接続
# ============================================================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# JST
JST = timezone(timedelta(hours=9))

# ============================================================
#  対象場
# ============================================================
TARGET_PLACES = {
    "12": "住之江",
    "19": "下関",
    "24": "大村",
}

# ============================================================
#  安定した GET リクエスト（timeout + retry）
# ============================================================
def safe_get(url, timeout=30, retries=3):
    for i in range(retries):
        try:
            return requests.get(url, timeout=timeout)
        except requests.exceptions.Timeout:
            print(f"[Timeout] {url}  ({i+1}/{retries})")
        except Exception as e:
            print(f"[Error] {url} : {e}")

    print(f"[Failed] {url} → スキップ")
    return None


# ============================================================
#  開催チェック
# ============================================================
def is_race_held(place_code: str, date: str) -> bool:
    url = f"https://www.boatrace.jp/owpc/pc/race/index?jcd={place_code}&hd={date}"
    res = safe_get(url)

    if res is None:
        return False

    return ("開催" in res.text) or ("レース" in res.text)


# ============================================================
#  出走表取得
# ============================================================
def fetch_race_data(place_code: str, race_number: int, date: str) -> Race | None:
    url = (
        "https://www.boatrace.jp/owpc/pc/race/racelist"
        f"?rno={race_number}&jcd={place_code}&hd={date}"
    )

    res = safe_get(url)
    if res is None:
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("table tbody tr")
    if not rows or len(rows) < 6:
        return None

    boats = []

    for idx, row in enumerate(rows[:6], start=1):
        cols = row.find_all("td")
        if len(cols) < 9:
            continue

        raw_name = cols[2].get_text(strip=True)
        name = raw_name.split()[-1]

        raw_st = cols[4].get_text(strip=True).split()
        try:
            st = float(raw_st[-1])
        except:
            st = 0.0

        boat = Boat(
            number=idx,
            name=name,
            st=st,
            motor=0.0,
            win_rate=0.0,
        )
        boats.append(boat)

    if len(boats) != 6:
        return None

    race_id = f"{date}_{place_code}_{race_number}R"
    race = Race(race_id=race_id, boats=boats, metadata={"place_code": place_code})

    return race


# ============================================================
#  Supabase 保存
# ============================================================
def save_prediction(race: Race, pred: dict, date: str):
    data = {
        "race_id": race.race_id,
        "place": race.metadata["place_code"],
        "race_number": int(race.race_id.split("_")[-1].replace("R", "")),
        "date": date,
        "prediction": pred,
        "result": None,
        "odds": None,
        "evaluation": None,
        "saved_at": datetime.now(JST).isoformat(),
    }

    supabase.table("predictions").upsert(data).execute()


# ============================================================
#  メイン処理
# ============================================================
def main():
    today = datetime.now(JST).strftime("%Y%m%d")

    for place_code, place_name in TARGET_PLACES.items():
        print(f"=== {place_name}（{place_code}）開催チェック ===")

        if not is_race_held(place_code, today):
            print(f"{place_name} は本日開催なし")
            continue

        print(f"{place_name} は本日開催 → 予測開始")

        for r in range(1, 13):
            race = fetch_race_data(place_code, r, today)
            if race is None:
                print(f"{place_name}{r}R：出走表なし or 取得失敗")
                continue

            pred = predict(race)
            save_prediction(race, pred, today)

            print(f"{place_name}{r}R：保存完了")

    print("=== 自動予測完了 ===")
