# ========  Geminiを用いた例文・会話生成（試験名なし版）  =========
from flask import current_app
import re
import random


# --- Gemini呼び出し関数 ---
def _generate_from_gemini(prompt: str) -> str:
    """Geminiモデルにプロンプトを送信してテキストを取得"""
    try:
        model = current_app.model
        response = model.generate_content(prompt)
        text = response.text.strip()
        return clean_generated_text(text)
    
    except Exception as e:
        return f"[Error] Gemini API 呼び出し失敗: {e}"


# ===== 単語の意味生成 =====
def generate_word_meanings(vocab="word"):
    prompt = f"""
You are an expert bilingual English-Japanese lexicographer.

Provide a concise and clear explanation of the English word "{vocab}" in Japanese, including:
- its part(s) of speech (noun, verb, adjective, etc.)
- 2–4 major meanings , numbered (1), (2), (3)...

⚠️ Output only in this structured Japanese format, without any English introductions or meta explanations.
⚠️ Do not include phrases like "Of course" or "Here are the meanings".
Format example:

単語の意味
(1) 【名詞】革新、新しい考え
(2) 【名詞】新しい製品・発明

"""
    return _generate_from_gemini(prompt)

# ===== 各分野別 生成関数 =====

## --- Business ---
def generate_business_examples(vocab="word"):
    prompt = f"""
Generate three English example sentences for a business context using the word "{vocab}".
Use a formal and concise tone suitable for workplace communication.
After each English sentence, provide a natural Japanese translation starting with "→".
"""
    return _generate_from_gemini(prompt)



## --- Academic ---
def generate_academic_examples(vocab="word"):
    prompt = f"""
Generate three academic English sentences that use the word "{vocab}".
Use formal and objective language similar to research or academic writing.
After each English sentence, include a Japanese translation starting with "→".
"""
    return _generate_from_gemini(prompt)



NAMES = ["Alice", "Bob", "Charlie", "David", "Emma", "Fiona", "George", "Hannah", "Jack", "Lily"]
## --- Daily ---
def generate_daily_examples(vocab="word"):

    
        # ランダムに2〜3人選ぶ
    speakers = random.sample(NAMES, k=random.choice([2, 3]))
    speakers_str = ", ".join(speakers)

    prompt = f"""
Create a daily-life conversation that naturally includes the word "{vocab}".
- Include 2 or 3 speakers: {speakers_str}.
- Each line should be short, casual, and sound like natural spoken Japanese/English.
- The scene or situation should be random and everyday (no need to specify in advance).
- After each English line, provide a Japanese translation starting with "→".

Example output format:
{speakers[0]}: Hello! How are you?
→ こんにちは！元気？
{speakers[1]}: I'm good, thanks. Did you try the new cafe?
→ 元気だよ。新しいカフェ行った？
{speakers[2] if len(speakers) == 3 else ""}: Not yet, but I want to!
→ まだ行ってないけど、行きたい！

"""
    return _generate_from_gemini(prompt)




## --- Native Casual Conversation ---
def generate_native_casual_conversation(vocab="word"):
    # ランダムに2〜3人選ぶ
    speakers = random.sample(NAMES, k=random.choice([2, 3]))
    speakers_str = ", ".join(speakers)

    prompt = f"""
Write a natural, casual conversation between 2 or 3 native English speakers that includes the word "{vocab}".
- Include 2 or 3 speakers: {speakers_str}.
- Use relaxed tone, contractions, and idiomatic phrases typical of spoken English.
- The scene or situation should be random.
- After each English line, provide a Japanese translation starting with "→".

Example output format:
{speakers[0]}: Hey, have you seen the latest episode?
→ ねえ、最新のエピソード見た？
{speakers[1]}: Yeah! It was amazing!
→ 見たよ！めっちゃ良かった！
{speakers[2] if len(speakers) == 3 else ""}: I need to catch up soon.
→ すぐ追いつかないと！
"""
    return _generate_from_gemini(prompt)


# ===== 再生成（リライト）機能 =====
def refine_expression(text: str, mode: str = "polite") -> str:
    """
    生成済みテキストをもとに再生成する。
    mode: "polite"（丁寧に）, "casual"（カジュアルに）, "alternative"（他の言い方）
    """
    if mode == "polite":
        prompt = f"""
Rewrite the following English and Japanese examples in a **more polite and natural tone**.
Keep the same meaning, but make both the English and Japanese versions smoother and more formal.
Do not include any explanations, introductions, or headings — output only the rewritten examples.
Each line must follow the same format as the original (English line + "→" Japanese translation).
---
{text}
"""
    elif mode == "casual":
        prompt = f"""
Rewrite the following English and Japanese examples in a **more casual, friendly, and natural spoken style**.
Avoid formal expressions. Use contractions and conversational tone.
Do not include any explanations, introductions, or headings — output only the rewritten examples.
Each line must follow the same format as the original (English line + "→" Japanese translation).
---
{text}
"""
    elif mode == "alternative":
        prompt = f"""
Provide 2–3 **alternative English and Japanese phrasings** for the following examples.
Each should sound natural and contextually appropriate.
Do not include any explanations, introductions, or headings — output only the alternative examples.
Each line must follow this format:
EN: [English sentence]
JA: → [Japanese translation]
---
{text}
"""
    else:
        return "[Error] 無効なモードです。'polite', 'casual', 'alternative' のいずれかを指定してください。"

    return _generate_from_gemini(prompt)


# ===== 追加質問（followup）用 =====
def generate_followup_answer(vocab: str, question: str) -> str:
    """
    vocab: 単語
    question: ユーザーの質問（日本語）
    簡潔に日本語で回答、必要に応じて短く英語補足
    """
    prompt = f"""

The target word is "{vocab}".
Answer the following user question.
適宜英語を使うこと
単語の前には「・」をつけること

User Question: {question}
"""
    from flask import current_app
    return _generate_from_gemini(prompt)


# ===== 共通ルール説明 =====
rules = {
    "business": "ビジネス：フォーマルで職場向けの例文を生成。",
    "academic": "アカデミック：論文・研究向けの表現を生成。",
    "daily": "日常会話：カジュアルで自然な表現を生成。",
    "native": "ネイティブ会話：自然でリアルな英会話表現を生成。"
}


# --- 整形関数（アスタリスク・空白削除など） ---
def clean_generated_text(text: str, term: str = None) -> str:
    """
    Geminiで生成された文章を整形
    - 不要な冒頭文削除
    - アスタリスク削除
    - 見出しを固定
    """
    lines = text.splitlines()
    filtered_lines = [line for line in lines if not line.startswith("Of course")]
    cleaned_lines = [line.replace("*", "") for line in filtered_lines]

    if term:
        formatted_text = f"### Explanation of {term}\n\n" + "\n".join(cleaned_lines)
    else:
        formatted_text = "\n".join(cleaned_lines)

    import re

    # 不要な冒頭文削除
    lines = text.splitlines()
    lines = [line for line in lines if not line.startswith("Of course")]

    # アスタリスク削除
    text = "\n".join(lines).replace("*", "")

    # すべての # を削除
    text = text.replace("#", "")

    # **bold** のアスタリスク除去
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

    # 行頭の空白削除
    text = re.sub(r"^[ \t]+", "", text, flags=re.MULTILINE)

    # --- 区切り削除
    text = re.sub(r"^---$", "", text, flags=re.MULTILINE)

    # 連続空行をまとめる
    text = re.sub(r"\n{3,}", "\n\n", text)

    # 定型文削除
    text = re.sub(r"(?i)\b(Of course!|Here are|Sure!|Let’s see,|Okay,)\b.*", "", text)

    # 両端の空白除去
    text = text.strip()


    return text
