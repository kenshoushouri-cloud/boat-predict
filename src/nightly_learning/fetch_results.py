# fetch_results.py
# レース結果を取得し、Supabase に保存する

import requests
from supabase_client.results import insert_result


def fetch_race_result(race_id):
    """
    単一レースの結果をAPIから取得する
    実際のAPI仕様に合わせて修正可能
    """

    url = f"https://api.example.com/race/{race_id}/result"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        return {
            "race_id": race_id,
            "winning_boat": data.get("winning_boat"),
            "payout": data.get("payout"),
            "raw": data
        }

    except Exception as e:
        print(f"結果取得エラー: {race_id}, {e}")
        return None


def process_results(race_ids):
    """
    複数レースの結果を取得し、Supabase に保存する
    """

    results = []

    for race_id in race_ids:
        result = fetch_race_result(race_id)

        if result:
            insert_result(
                race_id=result["race_id"],
                winning_boat=result["winning_boat"],
                payout=result["payout"],
                raw=result["raw"]
            )
            results.append(result)

    return results
