# 実行
# 開発・本番の両方を起動
from app.Falsk_main import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
