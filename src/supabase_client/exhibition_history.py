# exhibition_history.py
# 展示タイムの履歴を Supabase に保存・取得する

from .client import supabase


def insert_exhibition(race_id, player_id, exhibition_time):
    """
    展示タイムを Supabase に保存する
    """

    data = {
        "race_id": race_id,
        "player_id": player_id,
        "exhibition_time": exhibition_time
    }

    supabase.table("exhibition_history").insert(data).execute()


def load_exhibition_by_player(player_id, limit=20):
    """
    選手ごとの展示タイム履歴を取得する（最新20件など）
    """

    response = (
        supabase.table("exhibition_history")
        .select("*")
        .eq("player_id", player_id)
        .order("race_id", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data or []
