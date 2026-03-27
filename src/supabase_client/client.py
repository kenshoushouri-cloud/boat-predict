# client.py
# Supabase との接続を管理する中心ファイル

from supabase import create_client
from dotenv import load_dotenv
import os

# .env の読み込み
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase の URL または KEY が設定されていません (.env を確認してください)")

# Supabase クライアント作成
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
