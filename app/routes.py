from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from app.generators import (
    generate_word_meanings,
    generate_business_examples,
    generate_academic_examples,
    generate_daily_examples,
    generate_native_casual_conversation,
    refine_expression,
    rules,
    _generate_from_gemini,
    clean_generated_text

    
)

main = Blueprint("main", __name__, template_folder='../templates')


@main.route("/", methods=["GET", "POST"])
def chat():
    """チャット画面（履歴あり）"""
    # セッションに履歴がなければ初期化
    if "history" not in session:
        session["history"] = []

    # POST送信された場合（新しい単語入力）
    if request.method == "POST":
        vocab = request.form.get("vocab", "").strip()
        genre = request.form.get("genre", "")

        if not vocab:
            flash("単語を入力してください。")
            return redirect(url_for("main.chat"))

        # ===== ① 単語の意味 =====
        meaning_text = generate_word_meanings(vocab=vocab)

        # ===== ② ジャンル別例文 =====
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

        # ===== ③ 履歴に追加 =====
        session["history"].append({
            "user": f"「{vocab}」を使った{genre}の例文を作って",
            "meaning": meaning_text,
            "ai": prompt,
            "ai_vocab": vocab
        })
        session.modified = True  # 明示的に保存

        return redirect(url_for("main.chat"))

    # 履歴をテンプレートに渡す
    return render_template("chat.html", history=session["history"])


@main.route("/refine", methods=["POST"])
def refine():
    print("🔥 refineルート呼び出し検出")
    print("POST内容:", request.form)
    
    """AI出力をリライトして履歴に追記"""
    text = request.form.get("original_text", "")
    mode = request.form.get("mode", "")

    if not text:
        flash("再生成するテキストがありません。")
        return redirect(url_for("main.chat"))

    # リライト実行
    refined_text = refine_expression(text, mode)

    # モードの日本語表記
    mode_labels = {
        "polite": "もう少し丁寧に",
        "casual": "カジュアルに",
        "alternative": "他の言い方で",
        "followup": "追加で質問する"
    }
    
        # followupの場合はユーザーが再質問できるように履歴に追加
    if mode == "followup":
        session["history"].append({
            "user": f"🧑‍🎓 🔍 追加で質問：{question}",
            "meaning": None,
            "ai": answer,  # Geminiの回答をそのまま格納
            "ai_vocab": None  # 単語例文用ではないためNone
        })
    else:
        refined_text = refine_expression(text, mode)
        session["history"].append({
            "user": f"🔁 {mode_labels.get(mode, 'リライト')}",
            "meaning": None,
            "ai": refined_text
        })

    session.modified = True

    return redirect(url_for("main.chat"))



@main.route("/followup_question", methods=["POST"])
def followup_question():
    """ユーザーが入力した単語の追加質問に答える"""
    vocab = request.form.get("original_vocab", "").strip()
    question = request.form.get("question", "").strip()

    if not vocab or not question:
        flash("単語と質問を入力してください。")
        return redirect(url_for("main.chat"))

    from app.generators import generate_followup_answer

    # 生成AIで回答
    answer = generate_followup_answer(vocab, question)

    # 履歴に追加
    session["history"].append({
        "user": f"🧑‍🎓 🔍 追加で質問：{question}",
        "meaning": None,
        "ai": answer,
        "ai_vocab": vocab
    })
    session.modified = True

    return redirect(url_for("main.chat"))
