# 📊 Dashboard MBG Analyst
Aplikasi web untuk menganalisis data, memantau indikator, dan memberikan insight mendalam terkait Program Makan Bergizi Gratis (MBG), dibangun dengan framework Streamlit.
🔗 Live Demo: mbg-analyst.streamlit.app
---
## 📌 Tentang Project
Project ini dikembangkan sebagai alat bantu analisis (analyst tool) untuk memantau performa dan dampak program Makan Bergizi Gratis (MBG). Aplikasi ini menyediakan visualisasi data yang intuitif untuk membantu pemangku kepentingan dalam memahami distribusi, kualitas, dan efektivitas program di lapangan secara real-time atau berdasarkan dataset historis.
---
## 🎯 Tujuan Analisis
    • Monitoring Program: Memantau ketercapaian target distribusi makan bergizi.
    • Analisis Kualitas: Mengevaluasi metrik kualitas layanan dan pemenuhan gizi.
    • Visualisasi Geospasial: Memetakan jangkauan program berdasarkan wilayah.
    • Pengambilan Keputusan: Menyediakan data pendukung untuk perbaikan strategi distribusi dan operasional.
---
## 🗂️ Struktur Project
Plaintext
mbg-analyst/
├── app.py                        # Entry point aplikasi Streamlit
├── model.pkl                # model ML – Random Forest
├── vectorizer.pkl     # TF-IDF atau frekuensi kata
├── requirements.txt       # Daftar dependensi library
└── README.md
---
## ⚙️ Fitur Dashboard
Fitur	Keterangan
Executive Summary	Ringkasan KPI utama program MBG
Data Explorer	Eksplorasi dataset mentah melalui video youtube
Trend Analysis	Visualisasi tren distribusi mbg
Quality Control	Pemantauan standar kualitas makanan
Interactive Filters	Filter dinamis berdasarkan waktu, wilayah, dan kategori
---
## 📊 Metode yang Digunakan
    1. Exploratory Data Analysis (EDA): Mengolah dataset mentah untuk menemukan pola distribusi dan anomali data.
    2. Data Visualization: Menggunakan Plotly dan Altair untuk menyajikan data yang kompleks menjadi grafik yang mudah dipahami.
    3. Statistical Profiling: Menghitung rata-rata, tren, dan korelasi antar variabel untuk mengukur efektivitas program.
---
## 🌐 Deploy
Aplikasi dideploy menggunakan Streamlit Community Cloud, yang memungkinkan akses online langsung melalui browser tanpa memerlukan konfigurasi server tambahan.
🛠️ Tech Stack
    • Python
    • Streamlit (UI Framework)
    • Pandas & NumPy (Data Processing)
    • Plotly / Matplotlib (Visualization)
    • Streamlit Cloud (Deployment)
---
## 📈 Manfaat Bisnis
    • Mempercepat pelaporan kinerja program secara paperless.
    • Meningkatkan transparansi data bagi pihak terkait.
    • Mengidentifikasi area dengan kendala distribusi secara cepat.
    • Mendukung evaluasi berbasis data (data-driven evaluation).
.
## ⚠️ Catatan
    • Akurasi analisis sangat bergantung pada kualitas data input yang diunggah.
    • Project ini bersifat sebagai alat bantu visualisasi dan analisis data untuk mendukung pengambilan keputusan.
