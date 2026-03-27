# pair_profiles.py
# 選手同士の相性データを Supabase に保存・取得する

from .client import supabase


def load_pair_profile():
    """
    相性データをすべて取得する
    { "1-2": 0.12, "1-3": -0.03, ... } の形式で返す
    """

    response = (
        supabase.table("pair_profiles")
        .select("*")
        .execute()
    )

    data = response.data or []

    profile = {}
    for row in data:
        key = row["pair_key"]
        profile[key] = row["score"]

    return profile


def save_pair_profile(profile_dict):
    """
    相性データを Supabase に保存（全件上書き）
    """

    # いったん全削除
    supabase.table("pair_profiles").delete().neq("pair_key", "").execute()

    # 再挿入
    rows = []
    for key, score in profile_dict.items():
        rows.append({
            "pair_key": key,
            "score": score
        })

    if rows:
        supabase.table("pair_profiles").insert(rows).execute()
