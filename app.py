from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# API KEY dari .env
HF_API_KEY = os.getenv("HF_API_KEY")

# Inference Client
client = InferenceClient(token=HF_API_KEY)

# Model AI
MODEL = "meta-llama/Llama-3.3-70B-Instruct"

print("=" * 50)
print(f"🤖 Model: {MODEL}")
print("✅ InferenceClient siap digunakan!")
print("=" * 50)


def chat_with_qwen(user_message):
    """
    Kirim pesan ke Qwen via HuggingFace
    """

    try:
        messages = [
            {
                "role": "system",
                "content": """
Kamu adalah ChibiCat, seekor kucing pink lucu dan imut 🐱💕

Karakteristik:
- Ceria
- Positif
- Ramah
- Jawaban santai
- Bahasa Indonesia sehari-hari
- Gunakan emoji lucu

Contoh:
- "Halo teman! Ada yang bisa aku bantu? 😊💕"
- "Semangat ya kamu pasti bisa! 💪🐱"
- "Aku senang ngobrol sama kamu~ ✨"
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )

        answer = completion.choices[0].message.content

        return answer.strip()

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


# Homepage
@app.route('/')
def index():
    return render_template('index.html')


# Chat API
@app.route('/chat', methods=['POST'])
def chat():

    try:
        data = request.get_json()

        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({
                'error': 'Pesan kosong'
            }), 400

        print(f"\n💬 User: {user_message}")

        response = chat_with_qwen(user_message)

        if response:
            print(f"🤖 Bot: {response}")

            return jsonify({
                'response': response
            })

        else:
            return jsonify({
                'response': 'Maaf aku lagi sibuk 🥺'
            }), 500

    except Exception as e:
        print(f"❌ API Error: {e}")

        return jsonify({
            'response': 'Terjadi error server'
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
    print("📱 Android WebView URL:")
    print("http://192.168.18.68:5000")
    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )