# line_notifier.py
# LINE Messaging API を使って通知を送る

import os
import requests
from dotenv import load_dotenv

load_dotenv()

LINE_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

if not LINE_TOKEN:
    raise ValueError("LINE_NOTIFY_TOKEN が .env に設定されていません")


def send_line_message(message: str):
    """
    LINE にメッセージを送信する（共通関数）
    """

    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    data = {
        "message": message
    }

    try:
        requests.post(url, headers=headers, data=data, timeout=10)
    except Exception as e:
        print(f"LINE送信エラー: {e}")


def send_morning_prediction(place, race_no, honmei, taikou, ana, scenario_text):
    """
    朝の予測通知
    """

    message = (
        f"【本日の予測】\n"
        f"{place} {race_no}R\n\n"
        f"本命: {honmei}\n"
        f"対抗: {taikou}\n"
        f"穴: {ana}\n\n"
        f"{scenario_text}"
    )

    send_line_message(message)


def send_nightly_summary(summary_text):
    """
    夜の成長レポート通知
    """

    message = f"【AI成長レポート】\n{summary_text}"
    send_line_message(message)
