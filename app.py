import os
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient
import uuid

app = Flask(__name__)

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

        return jsonify({
            "reply": bot_reply,
            "chat_id": current_chat_id
        })

    except Exception as e:

        return jsonify({
            "reply": f"Error: {str(e)}"
        })

# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )