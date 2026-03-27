# main.py
# AI 全体の実行エントリーポイント（朝の予測・夜の学習）

from predict_engine.predictor import run_prediction
from nightly_learning.fetch_results import process_results
from nightly_learning.learner import nightly_learning
from nightly_learning.summary_generator import generate_summary
from supabase_client.system_status import load_system_status
from line_notifier.line_notifier import send_morning_prediction, send_nightly_summary


def morning_cycle():
    """
    朝の予測処理
    """

    # 予測実行
    prediction = run_prediction()

    # Supabase 保存は predictor 内で実行済み
    # LINE 通知
    send_morning_prediction(
        place=prediction["place"],
        race_no=prediction["race_no"],
        honmei=prediction["honmei"],
        taikou=prediction["taikou"],
        ana=prediction["ana"],
        scenario_text=prediction["scenario_text"]
    )


def nightly_cycle():
    """
    夜の学習処理
    """

    # 今日のレースID一覧（predictor が保存している想定）
    status = load_system_status()
    race_ids = status.get("today_race_ids", [])

    # 結果取得
    results = process_results(race_ids)

    # 学習
    nightly_learning(race_ids)

    # 成長レポート生成
    new_status = load_system_status()
    summary = generate_summary(
        old_weights=status["factor_weights"],
        new_weights=new_status["factor_weights"],
        old_pair_profile=status.get("pair_profile", {}),
        new_pair_profile=new_status.get("pair_profile", {}),
        version_up_places=new_status.get("version_up_places", [])
    )

    # LINE 通知
    send_nightly_summary(summary)


if __name__ == "__main__":
    # Railway / Cron などで morning_cycle と nightly_cycle を呼び分ける
    pass
