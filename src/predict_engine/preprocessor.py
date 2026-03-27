# preprocessor.py
# 展示タイム・モーター・相性などの前処理を行う

import numpy as np


def z_score(value, mean, std):
    """Zスコアを計算（標準偏差0対策あり）"""
    if std == 0:
        return 0
    return (value - mean) / std


def preprocess_exhibition(players):
    """
    展示タイムのZスコアを計算して返す
    players: [{ "id": 1, "exhibition": 6.78 }, ...]
    """
    times = [p["exhibition"] for p in players]
    mean = np.mean(times)
    std = np.std(times)

    for p in players:
        p["exhibition_score"] = z_score(p["exhibition"], mean, std)

    return players


def preprocess_motor(players):
    """
    モーター2連率を正規化してスコア化
    players: [{ "id": 1, "motor_rate": 32.5 }, ...]
    """
    rates = [p["motor_rate"] for p in players]
    mean = np.mean(rates)
    std = np.std(rates)

    for p in players:
        p["motor_score"] = z_score(p["motor_rate"], mean, std)

    return players


def preprocess_pair_profile(players, pair_profile):
    """
    選手同士の相性スコアを付与
    pair_profile: { "1-2": 0.12, "1-3": -0.03, ... }
    """
    for p in players:
        p["pair_score"] = 0

    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            key = f"{players[i]['id']}-{players[j]['id']}"
            rev = f"{players[j]['id']}-{players[i]['id']}"

            score = pair_profile.get(key) or pair_profile.get(rev) or 0

            players[i]["pair_score"] += score
            players[j]["pair_score"] += score

    return players


def preprocess_all(players, pair_profile):
    """
    すべての前処理をまとめて実行
    """
    players = preprocess_exhibition(players)
    players = preprocess_motor(players)
    players = preprocess_pair_profile(players, pair_profile)

    return players
