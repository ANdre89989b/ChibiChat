from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

# Flask app
app = Flask(__name__)
CORS(app)

# HuggingFace API KEY
HF_API_KEY = os.getenv("HF_API_KEY")

# HuggingFace Client
client = InferenceClient(
    token=HF_API_KEY
)

# MODEL AI
MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"

print("=" * 50)
print(f"🤖 MODEL: {MODEL}")
print("✅ Nyara AI siap digunakan!")
print("=" * 50)


def chat_with_ai(user_message):

    try:

        messages = [

            {
                "role": "system",

                "content": """
Kamu adalah Nyara AI 🐱✨

Karakteristik:
- Ramah
- Santai
- Ceria
- Natural
- Bahasa Indonesia sehari-hari
- Gunakan emoji secukupnya
- Jawaban tidak terlalu formal
- Jangan terlalu panjang

Contoh:
- "Halo teman 😊"
- "Aku bantu ya ✨"
- "Wah menarik banget 🐱"
- "Semangat ya 💪"
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


# Chat Endpoint
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

        print(f"\n💬 USER: {user_message}")

        response = chat_with_ai(
            user_message
        )

        print(f"🤖 BOT: {response}")

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
            f'❌ Server Error:\n{str(e)}'

        }), 500


# Health Check
@app.route('/health')
def health():

    return jsonify({

        'status': 'online',

        'model': MODEL
    })


# Run Server
if __name__ == '__main__':

    print("=" * 50)
    print("🐱 Nyara AI Server")
    print("=" * 50)

    print("🌐 Local URL:")
    print("http://127.0.0.1:5000")

    print("")
    print("📱 Android URL:")
    print("http://192.168.18.68:5000")

    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )