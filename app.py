from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

import os
import uuid

# ====================================
# LOAD ENV
# ====================================

load_dotenv()

# ====================================
# FLASK
# ====================================

app = Flask(__name__)

CORS(app)

# ====================================
# TOKEN
# ====================================

HF_TOKEN = os.getenv("HF_TOKEN")

# ====================================
# HUGGINGFACE CLIENT
# ====================================

client = InferenceClient(
    token=HF_TOKEN
)

# ====================================
# MODEL
# ====================================

MODEL = "NousResearch/Meta-Llama-3-8B-Instruct"

# ====================================
# CHAT STORAGE
# ====================================

chat_sessions = {}

current_chat_id = None

# ====================================
# START LOG
# ====================================

print("=" * 50)
print("🚀 ChibiCat AI")
print("=" * 50)
print(f"🦙 MODEL : {MODEL}")
print("✅ AI READY")
print("=" * 50)

# ====================================
# HOME
# ====================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

# ====================================
# NEW CHAT
# ====================================

@app.route(
    "/new_chat",
    methods=["POST"]
)
def new_chat():

    global current_chat_id

    chat_id = str(
        uuid.uuid4()
    )

    current_chat_id = chat_id

    chat_sessions[chat_id] = []

    return jsonify({

        "chat_id": chat_id
    })

# ====================================
# GET CHAT LIST
# ====================================

@app.route("/get_chats")
def get_chats():

    chats = []

    for chat_id, messages in chat_sessions.items():

        title = "New Chat"

        for msg in messages:

            if msg["role"] == "user":

                title = msg["content"][:30]

                break

        chats.append({

            "chat_id": chat_id,

            "title": title
        })

    chats.reverse()

    return jsonify(chats)

# ====================================
# LOAD CHAT
# ====================================

@app.route("/load_chat/<chat_id>")
def load_chat(chat_id):

    messages = chat_sessions.get(
        chat_id,
        []
    )

    return jsonify(messages)

# ====================================
# CHAT API
# ====================================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    global current_chat_id

    try:

        data = request.get_json()

        print("📩 DATA:", data)

        user_message = data.get(
            "message",
            ""
        ).strip()

        if user_message == "":

            return jsonify({

                "reply":
                "Pesan kosong 🥺"
            })

        # ====================================
        # CREATE CHAT
        # ====================================

        if not current_chat_id:

            current_chat_id = str(
                uuid.uuid4()
            )

            chat_sessions[current_chat_id] = []

        messages = chat_sessions[
            current_chat_id
        ]

        # ====================================
        # SAVE USER MESSAGE
        # ====================================

        messages.append({

            "role": "user",

            "content": user_message
        })

        print(f"\n💬 USER: {user_message}")

        # ====================================
        # PROMPT
        # ====================================

        prompt = f"""
Kamu adalah ChibiCat 🐱💕

Karakteristik:
- Lucu
- Ceria
- Ramah
- Santai
- Bahasa Indonesia sehari-hari
- Gunakan emoji lucu
- Jawaban pendek dan hangat

User: {user_message}

Assistant:
"""

        print("🔥 REQUEST AI")

        # ====================================
        # AI RESPONSE
        # ====================================

        bot_reply = client.text_generation(

            prompt,

            model=MODEL,

            max_new_tokens=300,

            temperature=0.7,

            return_full_text=False
        )

        bot_reply = bot_reply.strip()

        print(f"🤖 BOT: {bot_reply}")

        # ====================================
        # SAVE BOT MESSAGE
        # ====================================

        messages.append({

            "role": "assistant",

            "content": bot_reply
        })

        return jsonify({

            "reply": bot_reply,

            "chat_id": current_chat_id
        })

    except Exception as e:

        print("=" * 50)
        print("❌ FULL ERROR")
        print(e)
        print("=" * 50)

        return jsonify({

            "reply":
            f"ERROR SERVER:\n{str(e)}"
        })

# ====================================
# HEALTH CHECK
# ====================================

@app.route("/health")
def health():

    return jsonify({

        "status": "online",

        "model": MODEL
    })

# ====================================
# RUN
# ====================================

if __name__ == "__main__":

    print("=" * 50)
    print("🐱 ChibiCat AI Server")
    print("=" * 50)

    print("🌐 LOCAL:")
    print("http://127.0.0.1:5000")

    print("")
    print("☁️ RENDER:")
    print("https://chibichat.onrender.com")

    print("=" * 50)

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000
    )