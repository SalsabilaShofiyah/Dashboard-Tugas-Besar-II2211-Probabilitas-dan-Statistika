import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETUP HALAMAN WEB
st.set_page_config(page_title="AI Regulation Dashboard", page_icon="🤖", layout="wide")

# 2. LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("18224088.csv")
    # Pembersihan Data (Task 1)
    df_clean = df[(df['age'] >= 15) & (df['age'] <= 80)].copy()
    return df_clean

df_clean = load_data()

# 3. HEADER & DESKRIPSI (UI Minimalis)
st.title("🤖 Dashboard Analisis: Persepsi Publik Terhadap Regulasi AI")
st.markdown("Portofolio Analisis Data oleh **Salsabila Shofiyah (18224088)** | Mata Kuliah Probabilitas & Statistika")
st.markdown("---")

# 4. MEMBUAT LAYOUT KOLOM (Biar rapi seperti referensi)
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Konsensus Regulasi Lintas Pendidikan")
    fig1 = px.sunburst(df_clean, path=['education', 'gender', 'ai_reg1'])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("2. Demografi Ekonomi Responden")
    fig2 = px.treemap(df_clean, path=['income', 'occupation'])
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# 5. GRAFIK FULL WIDTH
st.subheader("3. Interaksi Gender, Aktivitas Online & Regulasi AI")
fig6 = px.parallel_categories(df_clean, dimensions=['gender', 'online1', 'ai_reg1'])
st.plotly_chart(fig6, use_container_width=True)

# 6. BAGIAN INSIGHTS (Storyline)
st.success("""
**Key Insights dari Analisis Statistik Inferensial:**
* Tuntutan regulasi kecerdasan buatan (AI) disetujui secara mutlak lintas kelompok (88.64% sepakat).
* Uji Interval Kepercayaan (95%) membuktikan tidak ada kesenjangan penggunaan ChatGPT antara pria dan wanita.
* Uji Chi-Square membuktikan bahwa perspektif moral terkait regulasi bersifat independen dan murni dari kesadaran kolektif masyarakat.
""") 
