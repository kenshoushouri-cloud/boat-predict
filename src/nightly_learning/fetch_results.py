# fetch_results.py
# レース結果を取得するモジュール（本来はスクレイピング or API）

class ResultFetcher:
    def __init__(self):
        pass

    def fetch(self):
        """
        本来はレース結果を取得する。
        今はテスト用の固定データを返す。
        """
        result = {
            "exhibition_score": 0.75,
            "motor_score": 0.62,
            "pair_score": 0.58,
            "actual_rank": 2  # 仮の結果
        }
        return result
