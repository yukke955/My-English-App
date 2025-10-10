

# 例文生成import random
# #ランダムいらない

# ===== 選択ルール =====
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

# ===== ダミー生成関数 =====
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