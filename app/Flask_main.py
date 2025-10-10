# Flask本体
# アプリ設定やGemini接続を一元化
from flask import Flask
from dotenv import load_dotenv
import os
import google.generativeai as genai

# --- APIキー設定 ---
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="app/templates")
    app.secret_key = os.getenv("SECRET_KEY", "secret_key_for_flash")

    # === Gemini設定 ===
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    app.model = genai.GenerativeModel("models/gemini-2.5-pro")

    # --- Blueprint登録 ---
    from app.routes import main
    app.register_blueprint(main)

    return app

app=create_app()
