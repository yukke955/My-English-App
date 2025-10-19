# 実行
# 開発・本番の両方を起動
import sys
import os

# Flask_main.py のパスを明示的に追加
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from Flask_main import app  # ← ここはそのままでOK

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
