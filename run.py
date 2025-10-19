# 実行
# 開発・本番の両方を起動
from app.Flask_main import app

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
