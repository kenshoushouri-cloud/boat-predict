# main.py

from predict_engine.predictor import predict_race
from supabase_client.predictions import insert_prediction
from supabase_client.system_status import load_system_status
from nightly_learning.fetch_results import process_results
from nightly_learning.learner import nightly_learning
from nightly_learning.summary_generator import generate_summary

import datetime


def morning_prediction(race_data: list, place: str):
    """
    朝の予測処理
    - predict_engine で予測
    - Supabase に保存
    - LINE 通知用のデータを返す
    """

    results = []

    for race in race_data:
        race_id = race["race_id"]
        players = race["players"]

        pred = predict_race(players, place)

        insert_prediction(
            race_id=race_id,
            place=place,
            race_no=race["race_no"],
            honmei=pred["honmei"],
            taikou=pred["taikou"],
            ana=pred["ana"],
            scenario=pred["scenarios"][pred["honmei"]]
        )

        results.append({
            "race_id": race_id,
            "honmei": pred["honmei"],
            "taikou": pred["taikou"],
            "ana": pred["ana"],
            "scenario": pred["scenarios"][pred["honmei"]]
        })

    return results


def night_learning_process(today_race_ids: list):
    """
    夜の学習処理
    - 結果取得
    - 学習
    - バージョンアップ
    - 成長レポート生成
    """

    # 結果取得 → Supabase 保存
    results = process_results(today_race_ids)

    # 学習処理
    nightly_learning(today_race_ids)

    # 最新の状態を取得
    status = load_system_status()

    # 成長レポート生成
    summary = generate_summary(
        old_weights=status["factor_weights_before"],
        new_weights=status["factor_weights"],
        old_pair_profile=status["pair_profile_before"],
        new_pair_profile=status["pair_profile"],
        version_up_places=status["version_up_places"]
    )

    return summary


def main():
    """
    AI の1日を管理するメイン関数
    """

    now = datetime.datetime.now().hour

    if 6 <= now <= 10:
        # 朝の予測
        race_data = []  # 実際はAPIから取得
        place = "徳山"
        predictions = morning_prediction(race_data, place)
        print("朝の予測完了:", predictions)

    elif 22 <= now <= 23:
        # 夜の学習
        today_race_ids = []  # 実際はAPIから取得
        summary = night_learning_process(today_race_ids)
        print("夜の学習完了:", summary)


if __name__ == "__main__":
    main()
