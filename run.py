# 実行
# 開発・本番の両方を起動
from app.Flask_main import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

