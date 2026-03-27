# predictor.py
# 予測ロジックのメイン処理

from .scenario_analyzer import ScenarioAnalyzer
from .weight_manager import WeightManager

class Predictor:
    def __init__(self):
        self.scenario_analyzer = ScenarioAnalyzer()
        self.weight_manager = WeightManager()

    def predict(self, features):
        """
        features: dict
            - exhibition_score
            - motor_score
            - pair_score
        """

        # シナリオ分析スコア
        scenario_score = self.scenario_analyzer.analyze(features)

        # 重み適用スコア
        weighted_score = self.weight_manager.apply_weights(features)

        # 最終スコア（将来拡張可能）
        final_score = (scenario_score + weighted_score) / 2

        return {
            "scenario_score": scenario_score,
            "weighted_score": weighted_score,
            "final_score": final_score
        }
