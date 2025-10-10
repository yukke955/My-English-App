# 実行
# 開発・本番の両方を起動
from app.Falsk_main import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render が指定するポート
    app.run(host="0.0.0.0", port=port, debug=False)
