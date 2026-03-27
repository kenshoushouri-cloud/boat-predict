# scenario_analyzer.py
# 予測ロジックの「シナリオ分析」部分を担当

class ScenarioAnalyzer:
    def __init__(self):
        pass

    def analyze(self, features):
        """
        features: dict
            - exhibition_score（展示評価）
            - motor_score（モーター評価）
            - pair_score（相性評価）
        """
        score = 0.0

        # 展示タイム（速いほどプラス）
        if "exhibition_score" in features:
            score += features["exhibition_score"] * 0.4

        # モーター評価
        if "motor_score" in features:
            score += features["motor_score"] * 0.3

        # 選手相性
        if "pair_score" in features:
            score += features["pair_score"] * 0.3

        return score
