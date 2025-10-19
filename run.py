# 実行
# 開発・本番の両方を起動
import sys
import os

# run.py のあるディレクトリを基準に app をパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from Flask_main import app  # これで Flask_main.py が見えるはず

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
