from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv
import random

# --- APIキー設定 ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-pro")

# --- Flaskアプリ開始 ---
app = Flask(__name__)
app.secret_key = "secret_key_for_flash"

# ===== 選択ルール (ジャンル → セクション → フォーマット) =====
rules = {
    "TOEIC": {
        "Listening": ["conversation_2", "conversation_3", "business_explanation"],
        "Reading": ["conversation_2", "business_long_text"]
    },
    "TOEFL": {
        "Listening": ["conversation_2", "lecture"],
        "Reading": ["academic_explanation"],
        "Writing": ["writing_task"],
        "Speaking": ["speaking_task"]
    },
    "IELTS": {
        "Listening": ["conversation_2", "explanation"],
        "Reading": ["academic_explanation"],
        "Writing": ["writing_task"],
        "Speaking": ["speaking_task"]
    },
    "Native conversation": {
        "default": []
    }
}

# ===== 生成関数 (ダミーの例文) =====
def generate_conversation(num_speakers=2, vocab="word"):
    if num_speakers == 2:
        return f"A: Hi, how are you?\nB: I'm good, thanks. I just learned '{vocab}'."
    elif num_speakers == 3:
        return f"A: Are we ready for the meeting?\nB: Yes, almost.\nC: Don’t forget the '{vocab}'."

def generate_explanation(context="business", vocab="word"):
    if context == "business":
        return f"This is a short business announcement including '{vocab}'."
    elif context == "academic":
        return f"This passage explains an academic concept of '{vocab}'."
    else:
        return f"This is a general explanation about '{vocab}'."

def generate_long_reading(context="business", vocab="word"):
    return f"This is a longer business text with more detail. The topic is '{vocab}'."

def generate_writing_task(vocab="word"):
    return f"Write an essay about how '{vocab}' influences modern society."

def generate_speaking_task(vocab="word"):
    return f"Describe a situation where '{vocab}' was important in your daily life."


#＝＝＝　ルーティング　＝＝＝
@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    vocab = ""
    if request.method == "POST":
        genre = request.form.get("genre")
        section = request.form.get("section")
        chosen_format = request.form.get("format")
        vocab = request.form.get("vocab", "").strip()

        # --- 単語未入力チェック ---
        if not vocab:
            flash("単語を入力してください。")
            return render_template("index.html", prompt="", rules=rules)

        # --- プロンプト組み立て ---
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


if __name__ == "__main__":
    app.run(debug=True)

    #     # --- Geminiで生成 ---
    #     response = model.generate_content([prompt])
    #     text = response.text

    #     # --- 教科書風に先頭修正 ---
    #     lines = text.splitlines()
    #     if lines and lines[0].lower().startswith("of course"):
    #         lines = lines[1:]
    #     intro = f"The following example illustrates the word '{word}' in {genre} {subgenre} context."
    #     lines.insert(0, intro)
    #     result = "\n".join(lines)

    # return render_template("index.html", result=result)

