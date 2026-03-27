# learner.py
# 夜の学習処理（重み更新・相性更新・場別バージョンアップ判定）

from supabase_client.results import load_results_by_race_ids
from supabase_client.predictions import load_predictions_by_race_ids
from supabase_client.system_status import load_system_status, save_system_status
from supabase_client.pair_profiles import load_pair_profile, save_pair_profile
from supabase_client.ai_versions import save_version_up

import numpy as np


def update_factor_weights(old_weights, accuracy):
    """
    予測精度に応じて重みを微調整する
    accuracy: 0〜1
    """

    new_weights = old_weights.copy()

    # 精度が高いほど展示の比重を上げる例
    new_weights["exhibition"] += (accuracy - 0.5) * 0.05
    new_weights["motor"] += (accuracy - 0.5) * 0.03
    new_weights["pair"] += (accuracy - 0.5) * 0.02

    # 正規化
    total = sum(new_weights.values())
    for k in new_weights:
        new_weights[k] /= total

    return new_weights


def update_pair_profile(pair_profile, predictions, results):
    """
    選手同士の相性データを更新する
    """

    for pred, res in zip(predictions, results):
        win = res["winning_boat"]

        # 本命が当たったら相性を強化
        if pred["honmei"] == win:
            key = f"{pred['honmei']}-{pred['taikou']}"
            pair_profile[key] = pair_profile.get(key, 0) + 0.01

        # 外れたら少し弱める
        else:
            key = f"{pred['honmei']}-{pred['taikou']}"
            pair_profile[key] = pair_profile.get(key, 0) - 0.005

    return pair_profile


def nightly_learning(race_ids):
    """
    夜の学習処理のメイン関数
    """

    # データ取得
    predictions = load_predictions_by_race_ids(race_ids)
    results = load_results_by_race_ids(race_ids)
    status = load_system_status()
    pair_profile = load_pair_profile()

    # 精度計算
    correct = 0
    for pred, res in zip(predictions, results):
        if pred["honmei"] == res["winning_boat"]:
            correct += 1

    accuracy = correct / len(predictions) if predictions else 0.5

    # 重み更新
    new_weights = update_factor_weights(status["factor_weights"], accuracy)

    # 相性更新
    new_pair_profile = update_pair_profile(pair_profile, predictions, results)

    # バージョンアップ判定（精度が一定以上なら）
    version_up_places = []
    if accuracy >= 0.55:
        save_version_up(status["current_version"] + 1)
        version_up_places.append(status["place"])

    # 状態保存
    save_system_status(
        factor_weights=new_weights,
        pair_profile=new_pair_profile,
        version_up_places=version_up_places
    )
