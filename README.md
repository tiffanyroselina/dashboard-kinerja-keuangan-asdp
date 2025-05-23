# 📊 Dashboard Kinerja Keuangan - PT ASDP Indonesia Ferry

Aplikasi Streamlit ini digunakan untuk menampilkan dashboard analisis keuangan dari PT ASDP Indonesia Ferry berbasis laporan keuangan dan tahunan.

## 📁 Struktur Folder
```
├── app.py
├── requirements.txt
├── README.md
└── data/
    ├── lk.csv
    └── laporan_tahunan.csv
```

## 🚀 Cara Menjalankan

### 🔹 Lokal
1. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

2. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```

### 🔹 Streamlit Cloud
1. Upload seluruh folder ke GitHub
2. Deploy via https://streamlit.io/cloud
3. Pastikan:
   - `app.py` di root repo
   - `requirements.txt` juga di root

---

## 📈 Fitur Dashboard
- Ringkasan kinerja: pendapatan, ebitda, laba bersih, dsb
- Rasio keuangan: Current Ratio, DER, DSCR, ROA
- Forecast cashflow 2 minggu
- Profil dan maturitas utang
- Rekomendasi strategi bisnis
