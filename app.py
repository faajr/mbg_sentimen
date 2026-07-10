import streamlit as st
import pickle
import re
import string
import matplotlib.pyplot as plt
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(page_title="Sentiment Analysis MBG", page_icon="🍽️", layout="wide")

# --- Custom CSS (Tema Dark, Glassmorphism & Vibrant Gradient) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #05161A, #0B3C49, #137752, #FF8E00, #E62A76);
        background-size: 300% 300%;
        animation: gradientBG 15s ease infinite;
        color: white;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    h1, h2, h3, h4, h5, h6, p, span, label, li { color: #ffffff !important; }
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 30, 0.4) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 2px solid rgba(0, 255, 255, 0.6) !important;
        color: white !important;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
    }
    .stTextArea textarea:focus {
        border: 2px solid #00FFFF !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff6b00, #ff4000) !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(255, 107, 0, 0.5) !important;
        transition: 0.3s ease-in-out !important;
        width: 250px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 0, 0.8) !important;
    }
    .glass-panel {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    .status-text { font-size: 20px; font-weight: bold; }
    .status-pos { color: #00FF87; }
    .status-neg { color: #FF4B4B; }
    .status-neu { color: #4B9BFF; }
    </style>
""", unsafe_allow_html=True)

# --- Load Resource (Di-cache agar Load Awal Cepat) ---
@st.cache_resource
def get_sastrawi_tools():
    factory_stemmer = StemmerFactory()
    stemmer = factory_stemmer.create_stemmer()
    factory_stopword = StopWordRemoverFactory()
    stopword = factory_stopword.create_stop_word_remover()
    return stemmer, stopword

@st.cache_resource
def load_models():
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except FileNotFoundError:
        return None, None

stemmer, stopword = get_sastrawi_tools()
model, vectorizer = load_models()

# --- OPTIMASI: Fungsi Utama Dipisah & Di-Cache (st.cache_data) ---
@st.cache_data(show_spinner=False)
def process_and_predict(text):
    # 1. Cleaning Dasar
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.encode('ascii', 'ignore').decode('ascii').strip()
    
    # 2. Stopword & Stemming 
    stop_removed = stopword.remove(text)
    stemmed_text = stemmer.stem(stop_removed)
    
    if stemmed_text == "":
        return None, None, None
        
    # 3. Prediksi
    text_vector = vectorizer.transform([stemmed_text])
    pred = model.predict(text_vector)[0]
    prob = model.predict_proba(text_vector)[0]
    
    return pred, prob, stemmed_text

# --- Sidebar Menu ---
with st.sidebar:
    st.markdown("### 📋 MENU")
    menu = st.radio("", ["Analisis Sentimen", "Panduan Pengguna"])
    st.write("---")
    st.caption("Aplikasi ini menggunakan Machine Learning untuk memprediksi sentimen ulasan pengguna terhadap Program MBG. Didesain dengan Streamlit 👑 Sumber dataset: https://s.id/5QP31")

# --- MENU 1: ANALISIS SENTIMEN ---
if menu == "Analisis Sentimen":
    st.markdown("<h1 style='text-align: center; font-size: 3em;'>🍱 Analisis Sentimen Program MBG</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; opacity: 0.8;'>Ketahui prediksi sentimen ulasan - komentar masyarakat terkait program <b>Makan Bergizi Gratis (MBG) dengan visual yang menarik!</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    if model is None or vectorizer is None:
        st.error("⚠️ Model atau Vectorizer tidak ditemukan! Pastikan file `model.pkl` dan `vectorizer.pkl` tersedia.")
        st.stop()

    st.markdown("<br>", unsafe_allow_html=True)
    user_input = st.text_area("💬 Masukkan Ulasan/Komentar di sini ya:", 
                              placeholder="Contoh: Program makan bergizi ini sangat membantu pertumbuhan anak! Terima kasih...", 
                              height=120)

    if st.button("🚀 PREDIKSI SENTIMEN"):
        if user_input.strip() == "":
            st.warning("Silakan masukkan teks terlebih dahulu!")
        else:
            with st.spinner('Memproses teks (Mencari kata dasar Sastrawi)... ⏳'):
                prediction, probabilities, processed_text = process_and_predict(user_input)
                
                if prediction is None:
                    st.warning("Teks tidak mengandung kata valid setelah dibersihkan.")
                else:
                    confidence = max(probabilities) * 100
                    
                    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
                    st.markdown(f"### ✔️**Confidence Score:** {confidence:.2f}%")
                    st.write("---")
                    
                   # --- HASIL ANALISIS ---
                    st.markdown("### 📊 Hasil Prediksi")
                    
                    # Kotak Alert Sentimen
                    if prediction == 'Positive':
                        st.success(f"### 🤩 SENTIMEN: POSITIF")
                    elif prediction == 'Negative':
                        st.error(f"### 😡 SENTIMEN: NEGATIF")
                    else:
                        st.info(f"### 😐 SENTIMEN: NETRAL")
                    
                    st.write("---")
                    
                    # --- GRAFIK PROBABILITAS ---
                    st.subheader("Grafik Probabilitas Sentimen")
                    classes = model.classes_
                    fig, ax = plt.subplots(figsize=(8, 3.5))
                    fig.patch.set_alpha(0.0)
                    ax.set_facecolor('none')
                    
                    colors = ['#FF4B4B' if c=='Negative' else '#00E676' if c=='Positive' else '#4B9BFF' for c in classes]
                    bars = ax.bar(classes, probabilities * 100, color=colors, edgecolor='none')
                    
                    ax.set_ylim(0, 100)
                    ax.set_ylabel('Probabilitas (%)', color='white', fontweight='bold')
                    ax.tick_params(colors='white')
                    ax.spines['bottom'].set_color('white')
                    ax.spines['left'].set_color('white')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.yaxis.grid(True, color='white', alpha=0.1, linestyle='-')
                    
                    for i, v in enumerate(probabilities * 100):
                        ax.text(i, v + 2, f"{v:.2f}%", ha='center', color='white', fontweight='bold')
                    
                    st.pyplot(fig)
                    plt.close(fig) 
                    
# --- MENU 2: PANDUAN PENGGUNA ---
elif menu == "Panduan Pengguna":
    st.markdown("<h1>📖 Panduan Pengguna</h1>", unsafe_allow_html=True)
    st.write("1. Masuk ke menu **Analisis Sentimen**.")
    st.write("2. Ketikkan kalimat pada kotak teks yang tersedia.")
    st.write("3. Klik tombol **Analisis Sentimen**.")
    st.info("Catatan: Analisis kalimat pertama kali mungkin memakan waktu beberapa detik karena sistem sedang mengenali kamus bahasa Indonesia. Kalimat berikutnya akan diproses jauh lebih cepat.")
