# predictions.py
# 朝の予測結果を Supabase に保存・取得する

from .client import supabase


def insert_prediction(race_id, place, race_no, honmei, taikou, ana, scenario):
    """
    予測結果を Supabase に保存する
    """

    data = {
        "race_id": race_id,
        "place": place,
        "race_no": race_no,
        "honmei": honmei,
        "taikou": taikou,
        "ana": ana,
        "scenario": scenario
    }

    supabase.table("predictions").insert(data).execute()


def load_predictions_by_race_ids(race_ids):
    """
    race_id のリストから予測データをまとめて取得する
    """

    if not race_ids:
        return []

    response = (
        supabase.table("predictions")
        .select("*")
        .in_("race_id", race_ids)
        .execute()
    )

    return response.data or []
