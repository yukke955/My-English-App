# ルーティング処理
# WEBリクエストの処理

from flask import Blueprint, render_template, request, flash
from app.generators import (
    rules,
    generate_conversation,
    generate_explanation,
    generate_long_reading,
    generate_writing_task,
    generate_speaking_task
)

main = Blueprint("main", __name__, template_folder='../templates')

@main.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    vocab = ""

    if request.method == "POST":
        genre = request.form.get("genre")
        section = request.form.get("section")
        chosen_format = request.form.get("format")
        vocab = request.form.get("vocab", "").strip()

        if not vocab:
            flash("単語を入力してください。")
            return render_template("index.html", prompt="", rules=rules)

        # === フォーマットに応じた生成 ===
        if genre == "Native conversation":
            prompt = generate_conversation(num_speakers=2, vocab=vocab)
        elif chosen_format == "conversation_2":
            prompt = generate_conversation(num_speakers=2, vocab=vocab)
        elif chosen_format == "conversation_3":
            prompt = generate_conversation(num_speakers=3, vocab=vocab)
        elif chosen_format == "business_explanation":
            prompt = generate_explanation(context="business", vocab=vocab)
        elif chosen_format == "business_long_text":
            prompt = generate_long_reading(context="business", vocab=vocab)
        elif chosen_format == "lecture":
            prompt = generate_explanation(context="academic", vocab=vocab)
        elif chosen_format == "academic_explanation":
            prompt = generate_explanation(context="academic", vocab=vocab)
        elif chosen_format == "writing_task":
            prompt = generate_writing_task(vocab=vocab)
        elif chosen_format == "speaking_task":
            prompt = generate_speaking_task(vocab=vocab)
        else:
            prompt = "Please select valid options."

    return render_template("index.html", prompt=prompt, rules=rules, vocab=vocab)