# predictor.py
# 予測ロジックの中心部分

from .preprocessor import preprocess_all


def score_player(player, weights):
    """
    各選手の総合スコアを計算する
    weights = {
        "exhibition": 0.4,
        "motor": 0.3,
        "pair": 0.3
    }
    """

    return (
        player["exhibition_score"] * weights["exhibition"]
        + player["motor_score"] * weights["motor"]
        + player["pair_score"] * weights["pair"]
    )


def predict_race(players, place, pair_profile=None, weights=None):
    """
    レース予測のメイン関数
    players: [{id, exhibition, motor_rate}, ...]
    """

    # デフォルトの重み（学習で更新される）
    if weights is None:
        weights = {
            "exhibition": 0.4,
            "motor": 0.3,
            "pair": 0.3
        }

    # 相性データがない場合は空で処理
    if pair_profile is None:
        pair_profile = {}

    # 前処理
    players = preprocess_all(players, pair_profile)

    # スコア計算
    for p in players:
        p["score"] = score_player(p, weights)

    # スコア順に並べる
    sorted_players = sorted(players, key=lambda x: x["score"], reverse=True)

    honmei = sorted_players[0]["id"]
    taikou = sorted_players[1]["id"]
    ana = sorted_players[2]["id"]

    # シナリオ文生成
    scenarios = {
        honmei: f"{honmei}号艇が展示・モーターともに優勢。軸として信頼。",
        taikou: f"{taikou}号艇が対抗。展開次第で頭も十分。",
        ana: f"{ana}号艇が穴候補。相性スコアが高く一発あり。"
    }

    return {
        "honmei": honmei,
        "taikou": taikou,
        "ana": ana,
        "scenarios": scenarios
    }
