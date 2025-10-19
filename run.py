# 実行
# 開発・本番の両方を起動
import sys
import os
from pathlib import Path

# appディレクトリをPythonパスに追加
sys.path.append(str(Path(__file__).resolve().parent / "app"))

# Flaskアプリをインポート
from Flask_main import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
