# version_up_judger.py
# バージョンアップ判定の補助ロジック

def judge_version_up(accuracy, threshold=0.55):
    """
    精度に応じてバージョンアップするか判定する
    accuracy: 0〜1
    threshold: バージョンアップ基準
    """

    if accuracy >= threshold:
        return True
    return False
