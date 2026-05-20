import os
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient
import uuid

app = Flask(__name__)

# =========================
# TAMBAHAN: DEBUG TOKEN
# =========================
HF_TOKEN = os.getenv("HF_TOKEN")
print("=" * 50)
print("🔑 CEK TOKEN HUGGINGFACE")
print("=" * 50)
if HF_TOKEN:
    print(f"✅ TOKEN DITEMUKAN: {HF_TOKEN[:15]}...")
else:
    print("❌ TOKEN TIDAK DITEMUKAN!")
    print("Pastikan file .env berisi: HF_TOKEN=hf_xxxxxxxxx")
print("=" * 50)

# =========================
# HUGGINGFACE
# =========================

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)

# =========================
# CHAT STORAGE
# =========================

chat_sessions = {}

current_chat_id = None

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# NEW CHAT
# =========================

@app.route("/new_chat", methods=["POST"])
def new_chat():

    global current_chat_id

    chat_id = str(uuid.uuid4())

    current_chat_id = chat_id

    chat_sessions[chat_id] = []

    return jsonify({
        "chat_id": chat_id
    })

# =========================
# GET CHATS
# =========================

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

    return jsonify(chats)

# =========================
# LOAD CHAT
# =========================

@app.route("/load_chat/<chat_id>")
def load_chat(chat_id):

    messages = chat_sessions.get(chat_id, [])

    return jsonify(messages)

# =========================
# CHAT API
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    global current_chat_id

    data = request.get_json()

    user_message = data.get("message")

    if not current_chat_id:

        current_chat_id = str(uuid.uuid4())

        chat_sessions[current_chat_id] = []

    messages = chat_sessions[current_chat_id]

    messages.append({
        "role": "user",
        "content": user_message
    })

    try:

        # =========================
        # TAMBAHAN: CETAK PESAN KE TERMINAL
        # =========================
        print(f"\n💬 USER: {user_message}")

        completion = client.chat.completions.create(

            model="meta-llama/Llama-3.3-70B-Instruct",

            messages=messages,

            max_tokens=700,
        )

        bot_reply = completion.choices[0].message.content

        messages.append({
            "role": "assistant",
            "content": bot_reply
        })

        # =========================
        # TAMBAHAN: CETAK BALASAN KE TERMINAL
        # =========================
        print(f"🤖 BOT: {bot_reply[:100]}...")

        return jsonify({
            "reply": bot_reply,
            "chat_id": current_chat_id
        })

    except Exception as e:

        # =========================
        # TAMBAHAN: CETAK ERROR LEBIH DETAIL
        # =========================
        print("=" * 50)
        print("❌ ERROR DETAIL:")
        print(str(e))
        print("=" * 50)

        return jsonify({
            "reply": f"Error: {str(e)}"
        })

# =========================
# RUN
# =========================

if __name__ == "__main__":

    print("=" * 50)
    print("🐱 ChibiCat AI Server Started")
    print("=" * 50)

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )