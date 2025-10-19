import os, shutil, re
from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def create_app():
    base_dir = os.path.dirname(__file__)
    template_path = os.path.join(base_dir, "templates")
    session_dir = os.path.join(base_dir, "flask_session")
    
    app = Flask(__name__, template_folder=template_path)

    # --- セッション設定を「サーバー側保存」に変更 ---
    app.config["SESSION_TYPE"] = "filesystem"
    session_dir = os.path.join(base_dir, "flask_session") 
    app.config["SESSION_FILE_DIR"] = session_dir         

    app.config["SESSION_PERMANENT"] = False
    app.secret_key = os.getenv("SECRET_KEY", "dev_key")

    Session(app)  # ✅ これが重要
    
        # ✅ この位置でリセットする（Session初期化の後！）
    if os.path.exists(session_dir):
        shutil.rmtree(session_dir)
    os.makedirs(session_dir, exist_ok=True)

    print("🧹 セッション履歴をリセットしました")
       

    # --- Gemini設定 ---
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    try:
        app.model = genai.GenerativeModel("models/gemini-2.5-flash")

        print("✅ Gemini モデル初期化完了（gemini-2.5-flash）")
    except Exception as e:
        print(f"❌ Gemini モデル初期化エラー: {e}")
        app.model = None
    
    # --- ルート登録 ---
    from app.routes import main
    app.register_blueprint(main)
        
    @app.template_filter('nl2br')
    def nl2br(value):
        """改行文字を <br> に変換して HTML で改行を維持"""
        if not value:
            return ""
        return value.replace("\n", "<br>\n")
        
    @app.template_filter("highlight_vocab")
    def highlight_vocab(text, vocab):
        """
        例文内の入力単語を太字にする
        - 大文字小文字も無視してすべての出現箇所を <b> で囲む
        """
        if not text or not vocab:
            return text
        pattern = re.compile(re.escape(vocab), re.IGNORECASE)
        return pattern.sub(lambda m: f"<b>{m.group(0)}</b>", text)

    return app

app = create_app()
    