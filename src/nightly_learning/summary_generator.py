# summary_generator.py
# 夜の学習後の成長レポートを生成する

class SummaryGenerator:
    def __init__(self):
        pass

    def generate(self, new_weights, version_up):
        """
        new_weights: dict
        version_up: bool
        """

        summary = "【夜の学習レポート】\n"
        summary += f"展示重み: {new_weights['exhibition']:.3f}\n"
        summary += f"モーター重み: {new_weights['motor']:.3f}\n"
        summary += f"相性重み: {new_weights['pair']:.3f}\n"

        if version_up:
            summary += "\nAIが成長し、新しいバージョンに進化しました！🚀"
        else:
            summary += "\n本日はバージョン据え置きです。"

        return summary
