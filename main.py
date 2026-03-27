import requests
import json
import datetime
import sys

# ---------------------------------------------------------
# Supabase REST API 設定
# ---------------------------------------------------------
SUPABASE_URL = "https://xxxxxxxx.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_SERVICE_ROLE_KEY"

def supabase_insert(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    return requests.post(url, headers=headers, data=json.dumps(data))

def supabase_select(table, query="*"):
    url = f"{SUPABASE_URL}/rest/v1/{table}?select={query}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    return requests.get(url, headers=headers).json()

# ---------------------------------------------------------
# LINE Notify
# ---------------------------------------------------------
LINE_TOKEN = "YOUR_LINE_NOTIFY_TOKEN"

def line_notify(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)

# ---------------------------------------------------------
# 予想エンジン（本番ロジックに差し替え可能）
# ---------------------------------------------------------
def predict_engine(race_data):
    return {
        "race_id": race_data["race_id"],
        "prediction": "1-2-3",
        "confidence": 0.82,
        "scenario": "nige"
    }

# ---------------------------------------------------------
# 夜中の学習処理
# ---------------------------------------------------------
def learning_engine(result, pred):
    accuracy = 1.0 if result["result"] == pred["prediction"] else 0.0
    return {
        "date": str(datetime.date.today()),
        "accuracy": accuracy,
        "scenario": pred["scenario"]
    }

# ---------------------------------------------------------
# 朝モード（予想）
# ---------------------------------------------------------
def morning_mode():
    today = datetime.date.today()
    race_ids = [
        f"{today}_hiru_1",
        f"{today}_hiru_2",
        f"{today}_hiru_3",
        f"{today}_yoru_1",
        f"{today}_yoru_2",
        f"{today}_yoru_3",
    ]

    for rid in race_ids:
        race_data = {"race_id": rid}
        pred = predict_engine(race_data)
        supabase_insert("predictions", pred)

    line_notify("本日の6場の予想が完了しました。")

# ---------------------------------------------------------
# 夜中モード（学習）
# ---------------------------------------------------------
def night_mode():
    today = str(datetime.date.today())
    preds = supabase_select("predictions", "*")

    for pred in preds:
        result = {"race_id": pred["race_id"], "result": "1-2-3"}  # 本来は結果取得
        learning = learning_engine(result, pred)
        supabase_insert("learning_logs", learning)

    line_notify("夜間学習が完了しました。成長レポートを保存しました。")

# ---------------------------------------------------------
# メイン処理（引数でモード切替）
# ---------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "morning":
            morning_mode()
        elif mode == "night":
            night_mode()
    else:
        print("引数が必要です： morning / night")
