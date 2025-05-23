import streamlit as st
import pandas as pd
from utils.analytics import compute_ratios
from utils.forecast import forecast_cashflow

# Load data
lk_data = pd.read_csv('data/lk.csv')
lt_data = pd.read_csv('data/laporan_tahunan.csv')

# Sidebar
st.sidebar.title("Menu")
menu = st.sidebar.radio("Pilih Halaman:", [
    "Ringkasan Kinerja",
    "Rasio Keuangan",
    "Forecast Cashflow",
    "Profil Utang",
    "Maturitas Utang",
    "Rekomendasi Strategi"
])

st.title("Dashboard Kinerja Keuangan - PT ASDP Indonesia Ferry")

# Ringkasan KPI
if menu == "Ringkasan Kinerja":
    st.header("Ringkasan Kinerja Keuangan")
    st.dataframe(lk_data[['tahun', 'pendapatan', 'ebitda', 'fixed_cost', 'laba_bersih', 'debt']])

# Rasio
elif menu == "Rasio Keuangan":
    st.header("Rasio Keuangan")
    ratio_df = compute_ratios(lk_data)
    st.dataframe(ratio_df)

# Forecast Cashflow
elif menu == "Forecast Cashflow":
    st.header("Forecast Cashflow 2 Minggu")
    forecast_df = forecast_cashflow(lk_data)
    st.line_chart(forecast_df.set_index('tanggal')['cashflow'])

# Profil Utang
elif menu == "Profil Utang":
    st.header("Profil Utang")
    st.dataframe(lk_data[['tahun', 'debt', 'tipe_utang']])

# Maturitas Utang
elif menu == "Maturitas Utang":
    st.header("Maturitas Utang")
    if 'maturity_date' in lk_data.columns:
        maturitas_df = lk_data.groupby('maturity_date').debt.sum().reset_index()
        st.bar_chart(maturitas_df.set_index('maturity_date'))
    else:
        st.warning("Kolom maturity_date belum tersedia dalam data.")

# Strategi
elif menu == "Rekomendasi Strategi":
    st.header("Strategi Perusahaan")
    st.markdown("""
    - Diversifikasi sumber pendapatan
    - Efisiensi operasional
    - Refinancing utang jangka pendek
    - Optimalisasi rute dan tarif
    - Peningkatan layanan digital
    """)
