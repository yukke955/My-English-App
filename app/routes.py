# ===============================
# routes.py（ジャンル別会話生成版・修正版）
# ===============================
from flask import Blueprint, render_template, request, flash
from app.generators import (
    generate_word_meanings,
    generate_business_examples,
    generate_academic_examples,
    generate_daily_examples,
    generate_native_casual_conversation,
    rules
)

# Flask Blueprint 設定
main = Blueprint("main", __name__, template_folder='../templates')

@main.route("/", methods=["GET", "POST"])
def index():
    vocab = ""
    meaning_text = ""
    prompt = ""
    
    # 🔹 ページ上で使うルール説明など（例: セレクトボックスやヘルプ文）
    rules = {
        "business": "ビジネス：フォーマルで職場向けの例文を生成します。",
        "academic": "アカデミック：論文・研究向けの表現を生成します。",
        "daily": "日常会話：カジュアルで自然な表現を生成します。",
        "native": "ネイティブ会話：自然でリアルな英会話表現を生成します。"
    }

    if request.method == "POST":
        genre = request.form.get("genre")
        vocab = request.form.get("vocab", "").strip()

        if not vocab:
            flash("単語を入力してください。")
            return render_template(
                "index.html",
                vocab=vocab,
                meaning_text=meaning_text,
                prompt=prompt,
                rules=rules
            )

        # ===== ① 単語の意味（多義語対応）を生成 =====
        meaning_text = generate_word_meanings(vocab=vocab)

        # ===== ② ジャンル別の例文・会話を生成 =====
        if genre == "business":
            prompt = generate_business_examples(vocab=vocab)
        elif genre == "academic":
            prompt = generate_academic_examples(vocab=vocab)
        elif genre == "daily":
            prompt = generate_daily_examples(vocab=vocab)
        elif genre == "native":
            prompt = generate_native_casual_conversation(vocab=vocab)
        else:
            prompt = "Please select a valid genre."

    # 🔹 語義＋例文を両方テンプレートへ
    return render_template(
        "index.html",
        vocab=vocab,
        meaning_text=meaning_text,
        prompt=prompt,
        rules=rules
    )