# learner.py
# 結果をもとに重みを学習するモジュール

class Learner:
    def __init__(self):
        pass

    def learn(self, race_result):
        """
        race_result: dict
            - exhibition_score
            - motor_score
            - pair_score
            - actual_rank
        """

        # 仮の学習ロジック（実際はもっと高度になる）
        base = 0.05

        new_weights = {
            "exhibition": 0.4 + (0.1 if race_result["exhibition_score"] > 0.7 else -0.05),
            "motor": 0.3 + (0.1 if race_result["motor_score"] > 0.6 else -0.05),
            "pair": 0.3 + (0.1 if race_result["pair_score"] > 0.55 else -0.05),
        }

        # 正規化（合計1.0にする）
        total = sum(new_weights.values())
        for key in new_weights:
            new_weights[key] /= total

        return new_weights
