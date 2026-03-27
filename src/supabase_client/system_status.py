# system_status.py
# AI の現在状態（重み・相性・バージョン・場）を保存・取得する

from .client import supabase


def load_system_status():
    """
    システム状態を1件取得する
    """

    response = (
        supabase.table("system_status")
        .select("*")
        .limit(1)
        .execute()
    )

    data = response.data

    if not data:
        # 初期状態が存在しない場合はデフォルト値を返す
        return {
            "current_version": 1,
            "place": "unknown",
            "factor_weights": {
                "exhibition": 0.4,
                "motor": 0.3,
                "pair": 0.3
            }
        }

    return data[0]


def save_system_status(factor_weights=None, pair_profile=None, version_up_places=None):
    """
    システム状態を更新する
    """

    # 現在の状態を取得
    current = load_system_status()

    update_data = {}

    if factor_weights is not None:
        update_data["factor_weights"] = factor_weights

    if pair_profile is not None:
        update_data["pair_profile"] = pair_profile

    if version_up_places is not None:
        update_data["version_up_places"] = version_up_places

    # 更新
    supabase.table("system_status").update(update_data).neq("place", "").execute()
