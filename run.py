# 実行
# 開発・本番の両方を起動
from app import Flask_main
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render が指定するポート
    Flask_main.app.run(host="0.0.0.0", port=port, debug=True)
