import streamlit as st
import pandas as pd
import plotly.express as px

# SETUP TAMPILAN HALAMAN WEB MINIMALIS SATU HALAMAN
st.set_page_config(page_title="AI Regulation Portfolio Dashboard", layout="wide")

# CSS Kustom untuk memperkuat kontras teks agar terlihat sangat jelas
st.markdown("""
    <style>
    .main {
        background-color: #fafafa;
    }
    h1, h2, h3 {
        color: #1e3d59;
    }
    p, li {
        color: #000000 !important;
        font-size: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

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

# HEADER UTAMA DASHBOARD
st.title("Dashboard Portofolio Analisis Persepsi Regulasi AI")
st.markdown("Dikembangkan oleh Salsabila Shofiyah NIM 18224088 Kelas K02 sebagai pemenuhan tugas besar II2211 Probabilitas dan Statistik")
st.markdown("<br>", unsafe_allow_html=True)

# RINGKASAN METRIK UTAMA
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Sampel Valid", f"{len(df_clean)} Responden")
with m2:
    st.metric("Rata Rata Usia", f"{round(df_clean['age'].mean(), 1)} Tahun")
with m3:
    st.metric("Aspirasi Regulasi AI", "88.6% Setuju")
st.markdown("<br><br>", unsafe_allow_html=True)

# SECTION TASK 1 DAN 2
st.header("Task 1 dan 2 Karakteristik Sampel Deskriptif")
col_d1, col_d2 = st.columns(2)
with col_d1:
    fig_age = px.histogram(df_clean, x='age', nbins=15,
                           title="Grafik 1 Sebaran Usia Responden Setelah Pembersihan Data",
                           labels={'age': 'Usia Tahun', 'count': 'Frekuensi'},
                           color_discrete_sequence=['#1e3d59'])
    st.plotly_chart(fig_age, use_container_width=True)
    
    st.markdown("### Konteks Analisis Kasus")
    st.markdown("Insight Grafik 1 Sebaran Usia")
    st.markdown("""
    * Mayoritas responden terkonsentrasi pada usia produktif muda di rentang 20 hingga 22 tahun
    * Kemiringan kurva membuktikan bahwa riset ini didominasi oleh populasi generasi Z
    """)

with col_d2:
    fig_gen = px.pie(df_clean, names='gender', 
                     title="Grafik 2 Persentase Komposisi Gender Responden",
                     color_discrete_sequence=['#17b978', '#a7ff83'])
    st.plotly_chart(fig_gen, use_container_width=True)
    
    st.markdown("### Konteks Analisis Kasus")
    st.markdown("Insight Grafik 2 Komposisi Gender")
    st.markdown("""
    * Sebaran sampel berhasil mencapai titik keseimbangan yang ideal antara pria dan wanita
    * Keseimbangan ini mencegah adanya bias sudut pandang gender dalam pengambilan kesimpulan
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# SECTION TASK 3
st.header("Task 3 Eksplorasi Visual Multivariat")
fig_par = px.parallel_categories(df_clean, dimensions=['gender', 'online1', 'ai_reg1'],
                                 title="Grafik 3 Aliran Hubungan Gender Intensitas Online dan Pandangan Regulasi")
st.plotly_chart(fig_par, use_container_width=True)

st.markdown("### Konteks Analisis Kasus")
st.markdown("Insight Grafik 3 Aliran Aktivitas Digital")
st.markdown("""
* Tingkat intensitas berselancar di internet tidak mengubah muara pandangan publik terhadap hukum teknologi
* Baik pria maupun wanita dengan aktivitas online tinggi tetap bersepakat menuntut adanya regulasi AI yang ketat
""")
st.markdown("<br>", unsafe_allow_html=True)

col_m1, col_m2 = st.columns(2)
with col_m1:
    fig_sun = px.sunburst(df_clean, path=['education', 'gender', 'ai_reg1'],
                          title="Grafik 4 Hierarki Sikap Aturan AI Berdasarkan Jenjang Pendidikan",
                          color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_sun, use_container_width=True)
    
    st.markdown("### Konteks Analisis Kasus")
    st.markdown("Insight Grafik 4 Hierarki Pendidikan")
    st.markdown("""
    * Kesadaran akan ancaman teknologi tidak didominasi oleh kelompok akademisi tingkat tinggi saja melainkan merata
    * Penolakan atau keraguan terhadap regulasi sangat minim terlihat di setiap anak cabang hierarki data
    """)
    
with col_m2:
    fig_tree = px.treemap(df_clean, path=['income', 'occupation'],
                          title="Grafik 5 Struktur Profil Pekerjaan Berdasarkan Tingkat Pendapatan",
                          color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig_tree, use_container_width=True)
    
    st.markdown("### Konteks Analisis Kasus")
    st.markdown("Insight Grafik 5 Struktur Ekonomi")
    st.markdown("""
    * Blok pendapatan di bawah 2 juta rupiah didominasi secara penuh oleh kelompok mahasiswa aktif
    * Penyebaran klaster pendapatan yang lebih tinggi diisi oleh pekerja sektor swasta secara bervariasi
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# SECTION TASK 6 DAN 7
st.header("Task 6 dan 7 Analisis Inferensial Lanjutan")
col_i1, col_i2 = st.columns(2)
with col_i1:
    fig_box = px.box(df_clean, x='education', y='age', points="all",
                     title="Grafik 6 Sebaran Nilai Usia Lintas Jenjang Pendidikan",
                     color='education', color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_box, use_container_width=True)
    
    st.markdown("### Konteks Analisis Kasus")
    st.markdown("Insight Grafik 6 Pengujian ANOVA")
    st.markdown("""
    * Perhitungan varians menemukan perbedaan usia rata rata yang sangat nyata antar jenjang pendidikan saat ini
    * Pola sebaran ini sangat logis dan mencerminkan linimasa perjalanan waktu penempuhan akademis seseorang
    """)
    
with col_i2:
    fig_bar = px.bar(df_clean, x='bank1', color='ai_reg1', barmode='stack',
                     title="Grafik 7 Pola Komparasi Pemilihan Bank Utama dan Pandangan Aturan AI",
                     color_discrete_sequence=['#1e3d59', '#17b978', '#ff6b6b'])
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("### Konteks Analisis Kasus")
    st.markdown("Insight Grafik 7 Pengujian Chi Square")
    st.markdown("""
    * Uji independensi membuktikan sebaran perbankan bersifat homogen di seluruh lintas opini masyarakat
    * Literasi keuangan perbankan dan pandangan aturan teknologi berkembang sejajar tanpa saling mempengaruhi
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# SECTION TASK 8
st.header("Task 8 Kesimpulan Analisis Inferensial Komprehensif")
st.markdown("### Konteks Kesimpulan Akhir Studi Kasus")
st.markdown("""
* Aksesibilitas Teknologi Melalui uji Z test ditemukan adopsi ChatGPT sudah merata tanpa ada kesenjangan gender sama sekali
* Hubungan Demografi Hasil perhitungan tingkat varians membuktikan perjalanan usia selalu beriringan dengan tingkat edukasi saat ini
* Validitas Perilaku Pengujian independensi membuktikan pandangan urgensi aturan hukum teknologi AI bersifat bebas murni lahir dari kesadaran kolektif masyarakat
""")
