# ai_versions.py
# AI のバージョンアップ履歴を Supabase に保存する

from .client import supabase


def save_version_up(new_version):
    """
    バージョンアップを Supabase に記録する
    """

    data = {
        "version": new_version
    }

    supabase.table("ai_versions").insert(data).execute()
