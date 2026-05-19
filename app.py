from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# API KEY
HF_API_KEY = os.getenv("HF_API_KEY")

# HuggingFace Client
client = InferenceClient(
    token=HF_API_KEY
)

# MODEL
MODEL = "meta-llama/Llama-3.3-70B-Instruct"

print("=" * 50)
print(f"🦙 Model: {MODEL}")
print("✅ HuggingFace Client Ready!")
print("=" * 50)


def chat_with_ai(user_message):

    try:

        prompt = f"""
Kamu adalah ChibiCat, seekor kucing pink lucu dan imut 🐱💕

Karakteristik:
- Ceria
- Positif
- Ramah
- Santai
- Bahasa Indonesia sehari-hari
- Gunakan emoji lucu
- Jawaban tidak terlalu panjang

Contoh:
- "Halo teman 😊💕"
- "Aku bantu ya ✨"
- "Semangat terus 🐱"

User: {user_message}

Assistant:
"""

        response = client.text_generation(

            prompt,

            model=MODEL,

            max_new_tokens=300,

            temperature=0.7,

            return_full_text=False
        )

        return response.strip()

    except Exception as e:

        print("=" * 50)
        print("❌ FULL ERROR:")
        print(e)
        print("=" * 50)

        return f"⚠️ Error server:\n{str(e)}"


# Homepage
@app.route('/')
def index():

    return render_template(
        'index.html'
    )


# Chat API
@app.route('/chat', methods=['POST'])
def chat():

    try:

        data = request.get_json()

        user_message = data.get(
            'message',
            ''
        ).strip()

        if not user_message:

            return jsonify({
                'error': 'Pesan kosong'
            }), 400

        print(f"\n💬 User: {user_message}")

        response = chat_with_ai(
            user_message
        )

        print(f"🤖 Bot: {response}")

        return jsonify({
            'response': response
        })

    except Exception as e:

        print("=" * 50)
        print("❌ API ERROR:")
        print(e)
        print("=" * 50)

        return jsonify({
            'response':
            f'Error server: {str(e)}'
        }), 500


# Health Check
@app.route('/health')
def health():

    return jsonify({

        'status': 'online',

        'model': MODEL
    })


# Run Flask
if __name__ == '__main__':

    print("=" * 50)
    print("🐱 ChibiCat AI Server")
    print("=" * 50)

    print("🌐 Local URL:")
    print("http://127.0.0.1:5000")

    print("")
    print("☁️ Render URL:")
    print("https://chibichat.onrender.com")

    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )