def calc_scores(race):
    scores = {}

    for b in race.boats:
        # ST（速いほど高評価）
        # 0.15 → 高得点、0.30 → 低得点 になるように調整
        st_score = max(0.0, 0.30 - b.st) * 200  # 0〜30点程度

        # 将来の拡張に備えて、他の項目も加点方式で残す
        base = (
            st_score +
            b.win_rate * 10 +
            b.local_win_rate * 8 +
            (1 - b.accident_rate) * 5 +
            b.motor_score +
            b.boat_score +
            b.local_score +
            b.course_score
        )

        scores[b.number] = base

    return scores


def get_teppan_threshold(place):
    return 75


def get_buy_threshold(place):
    return 65


def pair_score(boat_a, boat_b):
    # 将来 pair_stats を入れる場合に備えて残す
    if boat_b.player_id in boat_a.pair_stats:
        return boat_a.pair_stats[boat_b.player_id]["score"]
    return 50


def select_best_hole_pattern(b1, b2, b3, scores):
    if 5 not in scores:
        return f"{b1}-{b2}-{b3}"

    patterns = {
        f"5-{b1}-{b2}": scores[5] + 15,
        f"{b1}-5-{b2}": scores[5] + 10,
        f"{b1}-{b2}-5": scores[5] + 5,
    }
    return max(patterns, key=patterns.get)
