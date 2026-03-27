# main.py
# AIシステム全体の統合制御

from src.predict_engine.predictor import Predictor
from src.supabase_client.client import SupabaseClient
from src.supabase_client.predictions import save_prediction
from src.supabase_client.results import save_result
from src.supabase_client.ai_versions import update_ai_version
from src.supabase_client.system_status import update_system_status
from src.line_notifier.line_notifier import LineNotifier

from src.nightly_learning.fetch_results import ResultFetcher
from src.nightly_learning.learner import Learner
from src.nightly_learning.version_up_judger import VersionUpJudger
from src.nightly_learning.summary_generator import SummaryGenerator


# ---------------------------------------------------------
# 朝の予測処理
# ---------------------------------------------------------
def morning_cycle():
    notifier = LineNotifier()
    supabase = SupabaseClient()
    predictor = Predictor()

    # 予測に必要な特徴量（本来はスクレイピング or DB から取得）
    features = {
        "exhibition_score": 0.75,
        "motor_score": 0.62,
        "pair_score": 0.58,
    }

    # 予測実行
    prediction = predictor.predict(features)

    # Supabase に保存
    save_prediction(supabase, prediction)

    # LINE 通知
    message = (
        "【朝の予測完了】\n"
        f"展開スコア: {prediction['scenario_score']:.3f}\n"
        f"重みスコア: {prediction['weighted_score']:.3f}\n"
        f"最終スコア: {prediction['final_score']:.3f}"
    )
    notifier.send(message)

    print("Morning cycle completed.")


# ---------------------------------------------------------
# 夜の学習処理
# ---------------------------------------------------------
def nightly_cycle():
    notifier = LineNotifier()
    supabase = SupabaseClient()

    # 結果取得
    fetcher = ResultFetcher()
    race_result = fetcher.fetch()

    # 結果保存
    save_result(supabase, race_result)

    # 学習処理
    learner = Learner()
    new_weights = learner.learn(race_result)

    # バージョンアップ判定
    judger = VersionUpJudger()
    version_up = judger.judge(new_weights)

    if version_up:
        update_ai_version(supabase)

    # システムステータス更新
    update_system_status(supabase, new_weights)

    # 成長レポート生成
    summary = SummaryGenerator().generate(new_weights, version_up)

    # LINE 通知
    notifier.send(summary)

    print("Nightly cycle completed.")


# ---------------------------------------------------------
# CLI 実行用
# ---------------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py [morning|nightly]")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "morning":
        morning_cycle()
    elif mode == "nightly":
        nightly_cycle()
    else:
        print("Unknown mode:", mode)
