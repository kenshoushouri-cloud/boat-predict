# results.py
# レース結果を Supabase に保存・取得する

from .client import supabase


def insert_result(race_id, winning_boat, payout, raw):
    """
    レース結果を Supabase に保存する
    """

    data = {
        "race_id": race_id,
        "winning_boat": winning_boat,
        "payout": payout,
        "raw": raw
    }

    supabase.table("results").insert(data).execute()


def load_results_by_race_ids(race_ids):
    """
    race_id のリストから結果データをまとめて取得する
    """

    if not race_ids:
        return []

    response = (
        supabase.table("results")
        .select("*")
        .in_("race_id", race_ids)
        .execute()
    )

    return response.data or []
