import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# ---------------------- HELPER FUNCTIONS ----------------------
def compute_ratios(df):
    df = df.copy()
    df['Current Ratio'] = df['aset_lancar'] / df['liabilitas_lancar']
    df['DER'] = df['total_utang'] / df['ekuitas']
    df['DSCR'] = df['ebitda'] / df['angsuran']
    df['ROA'] = df['laba_bersih'] / df['total_aset']
    return df[['tahun', 'Current Ratio', 'DER', 'DSCR', 'ROA']]

def forecast_cashflow(df):
    df = df[['tahun', 'cashflow']].dropna()
    df = df.reset_index(drop=True).copy()
    df['x'] = range(len(df))
    model = LinearRegression().fit(df[['x']], df['cashflow'])
    future = pd.DataFrame({'x': range(len(df), len(df) + 14)})
    future['cashflow'] = model.predict(future[['x']])
    future['tanggal'] = pd.date_range(start=pd.to_datetime('today'), periods=14)
    return future

# ---------------------- MAIN APP ----------------------
st.set_page_config(layout="wide")
st.title("📊 Dashboard Kinerja Keuangan - PT ASDP Indonesia Ferry")

# Sidebar menu
st.sidebar.title("📁 Menu Navigasi")
menu = st.sidebar.radio("Pilih Halaman:", [
    "Ringkasan Kinerja",
    "Rasio Keuangan",
    "Forecast Cashflow",
    "Profil Utang",
    "Maturitas Utang",
    "Rekomendasi Strategi"
])

# Upload CSV
st.sidebar.subheader("📤 Upload Data CSV")
lk_file = st.sidebar.file_uploader("Laporan Keuangan (lk.csv)", type=["csv"])
lt_file = st.sidebar.file_uploader("Laporan Tahunan (laporan_tahunan.csv)", type=["csv"])

if lk_file:
    lk_data = pd.read_csv(lk_file)
else:
    st.warning("Harap unggah file lk.csv")

if lt_file:
    lt_data = pd.read_csv(lt_file)
else:
    lt_data = pd.DataFrame()  # optional

if lk_file:

    # Ringkasan KPI
    if menu == "Ringkasan Kinerja":
        st.header("📈 Ringkasan Kinerja Keuangan")
        columns_to_show = [col for col in ['tahun', 'pendapatan', 'ebitda', 'fixed_cost', 'laba_bersih', 'debt'] if col in lk_data.columns]
        st.dataframe(lk_data[columns_to_show])

    # Rasio Keuangan
    elif menu == "Rasio Keuangan":
        st.header("📉 Rasio Keuangan")
        if all(col in lk_data.columns for col in ['aset_lancar', 'liabilitas_lancar', 'total_utang', 'ekuitas', 'ebitda', 'angsuran', 'laba_bersih', 'total_aset']):
            ratio_df = compute_ratios(lk_data)
            st.dataframe(ratio_df)
        else:
            st.error("Beberapa kolom untuk menghitung rasio tidak tersedia.")

    # Forecast Cashflow
    elif menu == "Forecast Cashflow":
        st.header("🔮 Forecast Cashflow 2 Minggu")
        if 'cashflow' in lk_data.columns:
            forecast_df = forecast_cashflow(lk_data)
            st.line_chart(forecast_df.set_index('tanggal')['cashflow'])
        else:
            st.warning("Kolom cashflow tidak ditemukan pada data.")

    # Profil Utang
    elif menu == "Profil Utang":
        st.header("💳 Profil Utang")
        columns = [col for col in ['tahun', 'debt', 'tipe_utang'] if col in lk_data.columns]
        if columns:
            st.dataframe(lk_data[columns])
        else:
            st.warning("Data utang tidak lengkap.")

    # Maturitas Utang
    elif menu == "Maturitas Utang":
        st.header("📅 Maturitas Utang")
        if 'maturity_date' in lk_data.columns:
            maturitas_df = lk_data.groupby('maturity_date')['debt'].sum().reset_index()
            st.bar_chart(maturitas_df.set_index('maturity_date'))
        else:
            st.warning("Kolom maturity_date belum tersedia dalam data.")

    # Strategi Perusahaan
    elif menu == "Rekomendasi Strategi":
        st.header("🚀 Rekomendasi Strategi Perusahaan")
        st.markdown(\"\"\"
        **1. Diversifikasi Sumber Pendapatan**  
        Mengembangkan layanan baru yang berbasis logistik dan pariwisata.

        **2. Efisiensi Operasional**  
        Optimalisasi penggunaan bahan bakar dan digitalisasi operasional pelabuhan.

        **3. Refinancing Utang Jangka Pendek**  
        Reprofiling utang menjadi tenor yang lebih panjang dengan bunga rendah.

        **4. Optimalisasi Rute dan Tarif**  
        Menyesuaikan rute kapal dan harga berdasarkan demand dan profitabilitas.

        **5. Peningkatan Layanan Digital**  
        Penguatan pemesanan tiket dan integrasi sistem manajemen pelabuhan.
        \"\"\")

