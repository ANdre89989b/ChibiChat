import os
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient
import uuid

app = Flask(__name__)

# DEBUG TOKEN
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
# HUGGINGFACE - PERBAIKAN DI SINI!
# =========================
client = InferenceClient(token=HF_TOKEN)  # ← UBAH DARI API_KEY JADI HF_TOKEN

# ... sisanya sama seperti kode Anda ...