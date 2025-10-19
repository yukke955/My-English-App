# 実行
# 開発・本番の両方を起動
import sys
import os
from pathlib import Path

# 現在のファイル(run.py)のディレクトリを取得
BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"

# appディレクトリをPythonパスに追加
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Flask_mainをインポート
from Flask_main import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
