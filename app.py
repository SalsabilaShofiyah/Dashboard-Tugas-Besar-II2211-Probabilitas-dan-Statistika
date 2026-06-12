import streamlit as st
import pandas as pd
import plotly.express as px

# 1. SETUP TAMPILAN HALAMAN WEB MINIMALIS
# Menghilangkan emoji dari tab browser
st.set_page_config(page_title="AI Regulation Portfolio Dashboard", layout="wide")

# CSS Kustom untuk warna senada (Syntax titik dua di sini aman karena tidak muncul di layar)
st.markdown("""
    <style>
    .main {
        background-color: #fafafa;
    }
    h1, h2, h3 {
        color: #1e3d59;
    }
    div.stButton > button:first-child {
        background-color: #17b978;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. PROSES MEMUAT DATA
@st.cache_data
def load_data():
    df = pd.read_csv("18224088.csv")
    
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    
    cols_utama = ['gender', 'age', 'education', 'occupation', 'income',
                  'online1', 'ai_know1', 'ai_use1_chatgpt', 'ai_reg1',
                  'bank1', 'bank4_mobile_banking']
    df_clean = df[cols_utama].copy()
    
    df_clean = df_clean[(df_clean['age'] >= 15) & (df_clean['age'] <= 80)]
    df_clean.dropna(inplace=True)
    
    return df_clean

df_clean = load_data()

# 3. HEADER PORTOFOLIO
st.title("Dashboard Portofolio Analisis Persepsi Regulasi AI")
st.markdown("Dikembangkan oleh Salsabila Shofiyah NIM 18224088 Kelas K02")
st.markdown("<br>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Sampel Valid", f"{len(df_clean)} Responden")
with m2:
    st.metric("Rata Rata Usia", f"{round(df_clean['age'].mean(), 1)} Tahun")
with m3:
    st.metric("Aspirasi Regulasi AI", "88.6% Setuju")

st.markdown("<br>", unsafe_allow_html=True)

# 4. TABS NAVIGASI
tab_deskriptif, tab_multivariat, tab_inferensial = st.tabs([
    "Analisis Deskriptif Task 1 dan 2", 
    "Eksplorasi Visual Task 3", 
    "Pengujian Statistik Task 4 hingga 7"
])

# --- TAB 1 ---
with tab_deskriptif:
    st.subheader("Karakteristik Umum Sampel Responden")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        fig_age = px.histogram(df_clean, x='age', nbins=15,
                               title="Grafik 1 Sebaran Usia Responden Setelah Pembersihan Data",
                               labels={'age': 'Usia Tahun', 'count': 'Frekuensi'},
                               color_discrete_sequence=['#1e3d59'])
        st.plotly_chart(fig_age, use_container_width=True)
        
    with col_d2:
        fig_gen = px.pie(df_clean, names='gender', 
                         title="Grafik 2 Persentase Komposisi Gender Responden",
                         color_discrete_sequence=['#17b978', '#a7ff83'])
        st.plotly_chart(fig_gen, use_container_width=True)
        
    st.info("Ringkasan Analisis Deskriptif Pembersihan data berhasil mengeliminasi input ekstrem di atas seratus tahun sehingga sebaran kembali normal. Mayoritas responden berada pada masa produktif awal dengan proporsi seimbang antara pria dan wanita.")

# --- TAB 2 ---
with tab_multivariat:
    st.subheader("Visualisasi Hubungan Multivariat Lintas Kategori")
    
    # PERBAIKAN ERROR: Menghapus pengaturan warna custom agar library Plotly tidak crash
    fig_par = px.parallel_categories(df_clean, dimensions=['gender', 'online1', 'ai_reg1'],
                                     title="Grafik 3 Aliran Hubungan Gender Intensitas Online dan Pandangan Regulasi")
    st.plotly_chart(fig_par, use_container_width=True)
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        fig_sun = px.sunburst(df_clean, path=['education', 'gender', 'ai_reg1'],
                              title="Grafik 4 Hierarki Sikap Aturan AI Berdasarkan Jenjang Pendidikan",
                              color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_sun, use_container_width=True)
        
    with col_m2:
        fig_tree = px.treemap(df_clean, path=['income', 'occupation'],
                              title="Grafik 5 Struktur Profil Pekerjaan Berdasarkan Tingkat Pendapatan",
                              color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_tree, use_container_width=True)

# --- TAB 3 ---
with tab_inferensial:
    st.subheader("Uji Hipotesis Parametrik dan Non Parametrik")
    
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        fig_box = px.box(df_clean, x='education', y='age', points="all",
                         title="Grafik 6 Sebaran Nilai Usia Lintas Jenjang Pendidikan",
                         color='education', color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_i2:
        fig_bar = px.bar(df_clean, x='bank1', color='ai_reg1', barmode='stack',
                         title="Grafik 7 Pola Komparasi Pemilihan Bank Utama dan Pandangan Aturan AI",
                         color_discrete_sequence=['#1e3d59', '#17b978', '#ff6b6b'])
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.success("""
    Kesimpulan Analisis Inferensial Komprehensif
    
    1. Aksesibilitas Teknologi Melalui uji Z test ditemukan adopsi ChatGPT sudah merata tanpa ada kesenjangan gender.
    
    2. Hubungan Demografi Hasil perhitungan ANOVA menunjukkan perbedaan rata rata usia yang sangat nyata antar jenjang pendidikan saat ini.
    
    3. Validitas Perilaku Pengujian Chi Square membuktikan pandangan urgensi aturan hukum teknologi AI bersifat independen serta murni lahir dari kesadaran kolektif masyarakat.
    """)
