# version_up_judger.py
# バージョンアップの判定を行う

class VersionUpJudger:
    def __init__(self):
        pass

    def judge(self, new_weights):
        """
        重みの変化が大きい場合にバージョンアップとする
        """
        threshold = 0.08  # 8% 以上変化したらバージョンアップ

        diffs = [
            abs(new_weights["exhibition"] - 0.4),
            abs(new_weights["motor"] - 0.3),
            abs(new_weights["pair"] - 0.3),
        ]

        return any(d > threshold for d in diffs)
