import json
import math

from engine.scoring import (
    calc_scores,
    get_teppan_threshold,
    get_buy_threshold,
    pair_score,
    select_best_hole_pattern
)

# ===== パラメータ読み込み =====
with open("params.json", "r", encoding="utf-8") as f:
    PARAMS = json.load(f)


def predict(race):
    # スコア計算
    scores = calc_scores(race)

    # 本線（スコア上位3艇）
    sorted_boats = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top3 = [b[0] for b in sorted_boats[:3]]

    # 穴（5号艇を絡めたパターン）
    hole_pattern = select_best_hole_pattern(top3[0], top3[1], top3[2], scores)

    # EV計算（安全版）
    ev_main = scores[top3[0]] / 100
    ev_ana = scores[5] / 100 if 5 in scores else 0

    return {
        "main": f"{top3[0]}-{top3[1]}-{top3[2]}",
        "ana": hole_pattern,
        "ev_main": ev_main,
        "ev_ana": ev_ana
    }
