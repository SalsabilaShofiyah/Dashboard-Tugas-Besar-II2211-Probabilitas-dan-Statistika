import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETUP TAMPILAN HALAMAN WEB MINIMALIS
st.set_page_config(page_title="AI Regulation Dashboard", page_icon="📊", layout="wide")

# 2. PROSES PEMBERSIHAN DATA SESUAI LAPORAN
@st.cache_data
def load_data():
    df = pd.read_csv("18224088.csv")
    # Pembersihan Data: Filter usia produktif (15-80 tahun)
    df_clean = df[(df['age'] >= 15) & (df['age'] <= 80)].copy()
    return df_clean

df_clean = load_data()

# 3. HEADER PORTOFOLIO
st.title("📊 Dashboard Analisis: Persepsi Publik Terhadap Regulasi AI")
st.markdown("Disusun oleh **Salsabila Shofiyah (18224088)** | Portofolio Analisis Data")
st.markdown("---")

# 4. ROW 1: VISUALISASI UTAMA (MEMBAGI 2 KOLOM)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Konsensus Regulasi Lintas Pendidikan")
    # Sunburst Chart dari Task 3
    fig1 = px.sunburst(df_clean, path=['education', 'gender', 'ai_reg1'], 
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Demografi Pendidikan & Pendapatan")
    # Treemap Chart dari Task 3
    fig2 = px.treemap(df_clean, path=['income', 'education'], 
                      color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# 5. ROW 2: VISUALISASI FULL WIDTH & INSIGHTS
st.subheader("Interaksi Gender, Aktivitas Online & Dukungan Regulasi")
# Parallel Categories dari Task 3
fig3 = px.parallel_categories(df_clean, dimensions=['gender', 'online1', 'ai_reg1'],
                              color_continuous_scale=px.colors.sequential.Inferno)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("### 💡 Ringkasan Insights Eksekutif")
st.info("""
* **Karakteristik Sampel:** Mayoritas merupakan *Digital Natives* muda (20-22 tahun), berstatus pelajar dengan pendapatan di bawah Rp 2 juta.
* **Konsensus Publik:** Terdapat dorongan untuk meregulasi teknologi kecerdasan buatan (AI) yang disetujui secara mutlak lintas latar belakang sosial, gender, maupun tingkat ekonomi.
* **Aksesibilitas Merata:** Uji statistik membuktikan bahwa pemanfaatan AI (seperti ChatGPT) telah diadopsi secara merata tanpa adanya kesenjangan gender (*gender digital divide*).
""")
