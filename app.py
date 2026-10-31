import streamlit as st
from datetime import datetime
import os

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="DriveNow Yönetici Paneli",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ARAÇ LİSTESİ ---
ARACLAR = [
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "vites": "Otomatik", "yakit": "Dizel", "fiyat": 1500},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "vites": "Manuel", "yakit": "Benzin", "fiyat": 900},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "vites": "Otomatik", "yakit": "Benzin", "fiyat": 1200},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "vites": "Manuel", "yakit": "Dizel", "fiyat": 850},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "vites": "Otomatik", "yakit": "Elektrik", "fiyat": 2500}
]

# --- KRİTİK GÖRÜNÜRLÜK AYARLARI (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; }
    header, footer {visibility: hidden !important;}
    
    /* YAZILARI NETLEŞTİR */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small, input {
        color: #0F172A !important;
        font-family: sans-serif !important;
    }

    input, div[data-baseweb="select"], .stNumberInput div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
    }

    .card {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 2px solid #E2E8F0 !important;
        margin-bottom: 15px !important;
    }

    div.stButton > button {
        background: #FF6B00 !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        height: 50px !important;
        width: 100% !important;
        border: none !important;
    }
    
    .admin-box {
        background-color: #F1F5F9 !important;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #0F172A;
        font-family: monospace;
        white-space: pre-wrap;
    }
    </style>
""", unsafe_allow_html=True)

# --- METİN DOSYASI İŞLEMLERİ (TXT) ---
LOG_FILE = "kayitlar.txt"

def kaydet(mesaj):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%d.%m.%Y %H:%M')} | {mesaj}\n")

def kayitlari_oku():
    if not os.path.exists(LOG_FILE):
        return "Henüz kayıt bulunmuyor."
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read()

# --- OTURUM BAŞLATMA ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- GİRİŞ EKRANI ---
if st.session_state['user'] is None:
    st.markdown("<h1 style='text-align:center;'>DriveNow</h1>", unsafe_allow_html=True)
    with st.form("giris"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("TC Kimlik No", max_chars=11)
        tel = st.text_input("Telefon", max_chars=10)
        if st.form_submit_button("GİRİŞ YAP"):
            if ad and len(tc) == 11:
                st.session_state['user'] = {"ad": ad, "tc": tc, "tel": tel}
                kaydet(f"GİRİŞ: {ad} - TC: {tc} - TEL: {tel}")
                st.rerun()
else:
    t1, t2, t3 = st.tabs(["🚗 Araçlar", "📋 Kayıtlarım", "👤 Profil & Admin"])

    with t1:
        st.write(f"Hoş geldin, **{st.session_state['user']['ad']}**")
        loc = st.selectbox("Alış Yeri", ["İstanbul Havalimanı", "Sabiha Gökçen HL", "Ankara Esenboğa"])
        days = st.number_input("Gün Sayısı", min_value=1, value=1)

        for a in ARACLAR:
            total = a['fiyat'] * days
            st.markdown(f"""
            <div class="card">
                <b style="font-size:20px;">{a['ad']}</b><br>
                <small>{a['kat']}</small><br><br>
                <div style="display:flex; justify-content:space-between;">
                    <span>Günlük: <b>{a['fiyat']} ₺</b></span>
                    <span style="color:#FF6B00;">Toplam: <b>{total} ₺</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Hemen Kirala: {a['ad']}", key=a['ad']):
                bilgi = f"KİRALAMA: {st.session_state['user']['ad']} | Araç: {a['ad']} | Gün: {days} | Tutar: {total} ₺ | Yer: {loc}"
                kaydet(bilgi)
                st.success("Rezervasyonunuz kaydedildi!")

    with t2:
        st.subheader("İşlemleriniz")
        tum_kayitlar = kayitlari_oku().split("\n")
        sayac = 0
        for k in tum_kayitlar:
            if st.session_state['user']['ad'] in k:
                st.markdown(f"<div class='card'>{k}</div>", unsafe_allow_html=True)
                sayac += 1
        if sayac == 0:
            st.info("Size ait bir kiralama kaydı bulunamadı.")

    with t3:
        # KULLANICI BİLGİSİ
        st.markdown(f"""<div style="background:#1E293B; color:white; padding:20px; border-radius:15px;">
        <b>Sürücü:</b> {st.session_state['user']['ad']}<br>
        <b>TC:</b> {st.session_state['user']['tc']}</div>""", unsafe_allow_html=True)
        
        st.write("---")
        
        # YÖNETİCİ PANELİ (GİRENLERİ GÖRMEK İÇİN)
        if st.checkbox("⚙️ Yönetici Paneli (Girenleri Gör)"):
            st.write("**Tüm Sistem Kayıtları (.txt formatı):**")
            st.markdown(f"<div class='admin-box'>{kayitlari_oku()}</div>", unsafe_allow_html=True)
            
            # TXT olarak indir
            st.download_button(
                label="📥 Tüm Kayıtları .txt Olarak İndir",
                data=kayitlari_oku(),
                file_name="admin_kayitlar.txt",
                mime="text/plain"
            )
            
            if st.button("🚨 Kayıtları Sıfırla"):
                if os.path.exists(LOG_FILE):
                    os.remove(LOG_FILE)
                    st.rerun()

        if st.button("Çıkış Yap"):
            st.session_state['user'] = None
            st.rerun()
