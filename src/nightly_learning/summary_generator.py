# summary_generator.py
# 夜の学習後の成長レポートを生成する

def format_weights(weights):
    """重みを見やすい形に整形"""
    return (
        f"展示:{weights['exhibition']:.3f} / "
        f"モーター:{weights['motor']:.3f} / "
        f"相性:{weights['pair']:.3f}"
    )


def generate_summary(old_weights, new_weights, old_pair_profile, new_pair_profile, version_up_places):
    """
    成長レポートを生成する
    """

    summary = []

    # 重みの変化
    summary.append("【重みの変化】")
    summary.append(f"Before → {format_weights(old_weights)}")
    summary.append(f"After  → {format_weights(new_weights)}")
    summary.append("")

    # 相性データの変化（大きく変わった上位5件）
    summary.append("【相性データの変化（上位5件）】")

    diffs = []
    for key in new_pair_profile:
        before = old_pair_profile.get(key, 0)
        after = new_pair_profile[key]
        diffs.append((key, after - before))

    diffs_sorted = sorted(diffs, key=lambda x: abs(x[1]), reverse=True)[:5]

    for key, diff in diffs_sorted:
        summary.append(f"{key}: {diff:+.3f}")

    summary.append("")

    # バージョンアップ
    if version_up_places:
        summary.append("【バージョンアップ】")
        for place in version_up_places:
            summary.append(f"- {place} のモデルがアップデートされました")
    else:
        summary.append("【バージョンアップ】なし")

    return "\n".join(summary)
