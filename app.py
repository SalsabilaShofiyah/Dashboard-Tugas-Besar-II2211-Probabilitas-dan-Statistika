import streamlit as st
import pandas as pd
import plotly.express as px

# SETUP TAMPILAN HALAMAN WEB MINIMALIS SATU HALAMAN
st.set_page_config(page_title="AI Regulation Portfolio Dashboard", layout="wide")

# CSS Kustom Premium menggunakan Font Plus Jakarta Sans dan UI Kontras Tinggi
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"], .main {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #fafafa;
    }
    
    h1 {
        font-weight: 800 !important;
        color: #1e3d59 !important;
        font-size: 36px !important;
        letter-spacing: -0.5px;
    }
    
    h2 {
        font-weight: 700 !important;
        color: #1e3d59 !important;
        font-size: 24px !important;
        letter-spacing: -0.3px;
        margin-top: 35px !important;
        border-bottom: 2px solid #eef5f9;
        padding-bottom: 12px;
    }
    
    p {
        color: #2d3748 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    
    [data-testid="stMetricLabel"] p {
        color: #718096 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #1e3d59 !important;
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

# Helper untuk merender Komponen UI/UX Kotak Sorot Biru Interaktif Highlight Card
def render_insight_card(title_text, points_list):
    items_html = ""
    for pt in points_list:
        items_html += f"<li style='margin-bottom: 10px; line-height: 1.6; color: #2d3748;'>{pt}</li>"
        
    card_html = f"""
    <div style="background-color: #eef7fc; border-left: 6px solid #1e3d59; padding: 22px; border-radius: 12px; margin-top: 15px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(30,61,89,0.04);">
        <p style="color: #1e3d59 !important; font-weight: 700 !important; font-size: 17px !important; margin-top: 0px; margin-bottom: 14px; letter-spacing: -0.2px;">Konteks Analisis Kasus {title_text}</p>
        <ul style="margin-left: 0px; padding-left: 18px; font-size: 15px !important;">
            {items_html}
        </ul>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# HEADER UTAMA DASHBOARD
st.title("Dashboard Portofolio Analisis Persepsi Regulasi AI")
st.markdown("<b>Dikembangkan oleh Salsabila Shofiyah NIM 18224088 Kelas K02 sebagai pemenuhan tugas besar II2211 Probabilitas dan Statistik</b>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# RINGKASAN METRIK UTAMA
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Sampel Valid", f"{len(df_clean)} Responden")
with m2:
    st.metric("Rata Rata Usia", f"{round(df_clean['age'].mean(), 1)} Tahun")
with m3:
    st.metric("Aspirasi Regulasi AI", "88.6% Setuju")
st.markdown("<br>", unsafe_allow_html=True)

# SECTION TASK 1 DAN 2
st.header("Task 1 dan 2 Karakteristik Sampel Deskriptif")
col_d1, col_d2 = st.columns(2)
with col_d1:
    fig_age = px.histogram(df_clean, x='age', nbins=15,
                           title="Grafik 1 Sebaran Usia Responden Setelah Pembersihan Data",
                           labels={'age': 'Usia Tahun', 'count': 'Frekuensi'},
                           color_discrete_sequence=['#1e3d59'])
    st.plotly_chart(fig_age, use_container_width=True)
    
    render_insight_card("Insight Grafik 1 Sebaran Usia", [
        "Mayoritas responden terkonsentrasi pada usia produktif muda di rentang <b>20 hingga 22 tahun</b>",
        "Riset ini didominasi oleh populasi <b>generasi Z</b>"
    ])

with col_d2:
    fig_gen = px.pie(df_clean, names='gender', 
                     title="Grafik 2 Persentase Komposisi Gender Responden",
                     color_discrete_sequence=['#17b978', '#a7ff83'])
    st.plotly_chart(fig_gen, use_container_width=True)
    
    render_insight_card("Insight Grafik 2 Komposisi Gender", [
        "Sebaran sampel berhasil mencapai titik keseimbangan yang ideal antara <b>pria dan wanita</b>",
        "Keseimbangan ini mencegah adanya <b>bias sudut pandang gender</b> dalam pengambilan kesimpulan"
    ])

# SECTION TASK 3
st.header("Task 3 Eksplorasi Visual Multivariat")
fig_par = px.parallel_categories(df_clean, dimensions=['gender', 'online1', 'ai_reg1'],
                                 title="Grafik 3 Aliran Hubungan Gender Intensitas Online dan Pandangan Regulasi")
st.plotly_chart(fig_par, use_container_width=True)

render_insight_card("Insight Grafik 3 Aliran Aktivitas Digital", [
    "Tingkat intensitas menggunakan internet <b>tidak mengubah</b> pandangan publik terhadap hukum teknologi",
    "Baik pria maupun wanita yang beraktivitas online tinggi, bersepakat terkait adanya <b>regulasi AI yang ketat</b>"
])
st.markdown("<br>", unsafe_allow_html=True)

col_m1, col_m2 = st.columns(2)
with col_m1:
    fig_sun = px.sunburst(df_clean, path=['education', 'gender', 'ai_reg1'],
                          title="Grafik 4 Hierarki Sikap Aturan AI Berdasarkan Jenjang Pendidikan",
                          color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_sun, use_container_width=True)
    
    render_insight_card("Insight Grafik 4 Hierarki Pendidikan", [
        "Kesadaran akan ancaman teknologi merata dan <b>tidak didominasi</b> oleh kelompok akademisi tingkat tinggi saja ",
        "Penolakan atau keraguan terhadap regulasi <b>sangat minim terlihat</b> "
    ])
    
with col_m2:
    fig_tree = px.treemap(df_clean, path=['income', 'occupation'],
                          title="Grafik 5 Struktur Profil Pekerjaan Berdasarkan Tingkat Pendapatan",
                          color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig_tree, use_container_width=True)
    
    render_insight_card("Insight Grafik 5 Struktur Ekonomi", [
        "Blok pendapatan di bawah 2 juta rupiah didominasi secara penuh oleh kelompok <b>mahasiswa aktif</b>",
        "Penyebaran kelompok pendapatan yang lebih tinggi mayoritas diisi oleh pekerja sektor swasta secara <b>variatif</b>"
    ])

# SECTION TASK 6 DAN 7
st.header("Task 6 dan 7 Analisis Inferensial Lanjutan")
col_i1, col_i2 = st.columns(2)
with col_i1:
    fig_box = px.box(df_clean, x='education', y='age', points="all",
                     title="Grafik 6 Sebaran Nilai Usia Lintas Jenjang Pendidikan",
                     color='education', color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_box, use_container_width=True)
    
    render_insight_card("Insight Grafik 6 Pengujian ANOVA", [
        "Perhitungan varians menemukan <b>perbedaan usia rata rata</b> yang sangat variatif antar jenjang pendidikan saat ini",
        "Pola sebaran ini mencerminkan linimasa perjalanan waktu <b>penempuhan akademis</b> seorang responden"
    ])
    
with col_i2:
    fig_bar = px.bar(df_clean, x='bank1', color='ai_reg1', barmode='stack',
                     title="Grafik 7 Pola Komparasi Pemilihan Bank Utama dan Pandangan Aturan AI",
                     color_discrete_sequence=['#1e3d59', '#17b978', '#ff6b6b'])
    st.plotly_chart(fig_bar, use_container_width=True)
    
    render_insight_card("Insight Grafik 7 Pengujian Chi Square", [
        "Uji independensi membuktikan sebaran perbankan bersifat <b>homogen</b> di seluruh lintas opini masyarakat",
        "Literasi keuangan perbankan dan pandangan aturan teknologi berkembang sejajar tanpa <b>saling mempengaruhi</b>"
    ])

# SECTION TASK 8
st.header("Task 8 Kesimpulan Analisis Inferensial Komprehensif")
render_insight_card("Kesimpulan Akhir Studi Kasus", [
    "<b>Aksesibilitas Teknologi</b> Uji Z test menemukan insight bahwa adopsi ChatGPT sudah merata tanpa adanya kesenjangan gender",
    "<b>Hubungan Demografi</b> Hasil perhitungan tingkat varians membuktikan bahwa perjalanan usia selalu beriringan dengan tingkat edukasi saat ini",
    "<b>Validitas Perilaku</b> Pengujian independensi membuktikan pandangan urgensi aturan hukum teknologi AI bersifat bebas dan lahir dari kesadaran kolektif masyarakat, bukan hanya sekelompok golongan saja"
])
