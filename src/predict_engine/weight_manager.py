# weight_manager.py
# 予測ロジックの「重み管理」部分を担当

class WeightManager:
    def __init__(self):
        # 初期重み（夜の学習で更新される）
        self.weights = {
            "exhibition": 0.4,
            "motor": 0.3,
            "pair": 0.3,
        }

    def apply_weights(self, features):
        """
        features: dict
        """
        score = 0.0

        if "exhibition_score" in features:
            score += features["exhibition_score"] * self.weights["exhibition"]

        if "motor_score" in features:
            score += features["motor_score"] * self.weights["motor"]

        if "pair_score" in features:
            score += features["pair_score"] * self.weights["pair"]

        return score

    def update_weights(self, new_weights):
        """
        nightly_learning から渡される更新後の重みを反映
        """
        for key, value in new_weights.items():
            if key in self.weights:
                self.weights[key] = value
