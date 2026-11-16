
import streamlit as st
import json
import os
from google import genai

# =========================
# KONFIGURASI HALAMAN
# =========================

st.set_page_config(
    page_title="AI Disaster Assistant",
    page_icon="🌪️",
    layout="wide"
)

# =========================
# DESAIN TAMPILAN
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FA;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.header {
    background: linear-gradient(120deg, #173B59, #2B6685);
    padding: 28px;
    border-radius: 14px;
    color: white;
    margin-bottom: 22px;
}

.header-label {
    color: #C8DCEB;
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: 600;
}

.header h1 {
    color: white;
    font-size: 29px;
    margin: 10px 0 8px 0;
}

.header p {
    color: #E0EAF1;
    font-size: 14px;
    margin: 0;
}

.section-title {
    color: #173B59;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 5px;
}

.info-card {
    background: white;
    border: 1px solid #DCE5EC;
    border-radius: 12px;
    padding: 16px;
    min-height: 95px;
}

.info-label {
    color: #718096;
    font-size: 12px;
}

.info-value {
    color: #173B59;
    font-size: 23px;
    font-weight: 700;
    margin-top: 5px;
}

.stChatMessage {
    background-color: white;
    border: 1px solid #E1E8EF;
    border-radius: 12px;
    padding: 12px;
}

.stChatInput {
    background-color: white;
}

div.stButton > button {
    background-color: white;
    color: #173B59;
    border: 1px solid #D5E0E8;
    border-radius: 9px;
    text-align: left;
    min-height: 48px;
    font-size: 13px;
}

div.stButton > button:hover {
    border-color: #2B6685;
    color: #2B6685;
    background-color: #EDF4F8;
}

.footer {
    text-align: center;
    color: #8795A3;
    font-size: 11px;
    padding-top: 25px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# MEMBACA DATA
# =========================

with open("/content/ringkasan_ai.json", encoding="utf-8") as f:
    data = json.load(f)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API Key belum tersedia.")
    st.stop()

client = genai.Client(api_key=api_key)

# =========================
# HEADER
# =========================

st.markdown("""
<div class="header">
    <div class="header-label">COGNITIVE ANALYTICS</div>
    <h1>🌪️ AI Disaster Assistant</h1>
    <p>
    Asisten kecerdasan buatan untuk membantu
    mengeksplorasi dan memahami data kebencanaan Indonesia.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# INFORMASI DATA
# =========================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <div class="info-label">Total Baris Dataset</div>
        <div class="info-value">35.113</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-label">Periode Analisis</div>
        <div class="info-value">2018–2024*</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <div class="info-label">Wilayah Analisis</div>
        <div class="info-value">Indonesia</div>
    </div>
    """, unsafe_allow_html=True)

st.caption("*Perbandingan tahunan menggunakan tahun dengan kode identitas lengkap.")

st.divider()

# =========================
# PERTANYAAN
# =========================

st.markdown(
    '<div class="section-title">Jelajahi Data Kebencanaan</div>',
    unsafe_allow_html=True
)

st.write(
    "Pilih contoh pertanyaan atau ketik pertanyaanmu sendiri."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""

col1, col2 = st.columns(2)

with col1:
    if st.button("🌧️ Jenis bencana paling dominan", use_container_width=True):
        st.session_state.pending_question = "Jenis bencana apa yang paling dominan?"

    if st.button("📍 Provinsi dengan kejadian terbanyak", use_container_width=True):
        st.session_state.pending_question = "Provinsi mana dengan kejadian bencana terbanyak?"

with col2:
    if st.button("📊 Perbandingan kejadian tahunan", use_container_width=True):
        st.session_state.pending_question = "Bagaimana perbandingan kejadian bencana setiap tahun?"

    if st.button("🏘️ Kabupaten dengan kejadian terbanyak", use_container_width=True):
        st.session_state.pending_question = "Kabupaten mana dengan kejadian bencana terbanyak?"

st.divider()

st.markdown(
    '<div class="section-title">Percakapan dengan AI</div>',
    unsafe_allow_html=True
)

# =========================
# RIWAYAT CHAT
# =========================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Tanyakan sesuatu tentang data kebencanaan..."
)

if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = ""

# =========================
# PROSES JAWABAN AI
# =========================

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    instructions = f"""
    Kamu adalah AI Disaster Assistant untuk analisis
    data kebencanaan Indonesia.

    Gunakan hanya data berikut sebagai sumber angka
    dan fakta:

    {json.dumps(data, ensure_ascii=False)}

    ATURAN:
    1. Jawab dalam Bahasa Indonesia yang mudah dipahami.
    2. Gunakan angka sesuai data.
    3. Jangan mengarang angka atau fakta.
    4. Ringkasan tahunan hanya mencakup 2018 dan 2020–2024.
    5. Jangan membuat kesimpulan tren untuk tahun tidak lengkap.
    6. Jika informasi tidak tersedia, katakan bahwa data belum tersedia.
    7. Berikan interpretasi yang relevan.
    8. Bedakan jumlah baris dan jumlah kejadian unik.
    9. Jawab ringkas, jelas, dan langsung.
    """

    riwayat = ""
    for message in st.session_state.messages:
        riwayat += (
            f"\n{message['role']}: {message['content']}"
        )

    with st.chat_message("assistant"):
        try:

            def generate_response():
                response = client.models.generate_content_stream(
                    model="gemini-3.5-flash-lite",
                    contents=instructions + "\n\nRiwayat percakapan:" + riwayat
                )

                for chunk in response:
                    if chunk.text:
                        yield chunk.text

            answer = st.write_stream(generate_response())

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# =========================
# FOOTER
# =========================

st.markdown("""
<div class="footer">
    AI DISASTER ASSISTANT | COGNITIVE ANALYTICS
    <br>
    Disaster Prediction & Decision Support
</div>
""", unsafe_allow_html=True)
