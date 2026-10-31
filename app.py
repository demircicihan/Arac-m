import streamlit as st
from datetime import datetime
import os

# --- AYARLAR ---
st.set_page_config(page_title="DriveNow Premium", page_icon="🚗", layout="centered")

# --- KLASÖR KONTROLÜ ---
UPLOAD_DIR = "yuklemeler"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- ADMİN ŞİFRE ---
ADMIN_SIFRE = "cihan123" 

# --- ARAÇLAR ---
ARACLAR = [
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "fiyat": 1500},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "fiyat": 900},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "fiyat": 1200},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "fiyat": 850},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "fiyat": 2500}
]

# --- CSS (GÖRÜNÜRLÜK AYARI) ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; }
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small {
        color: #0F172A !important;
        font-family: -apple-system, sans-serif !important;
    }
    input, div[data-baseweb="select"], .stNumberInput div, div[data-baseweb="base-input"], div[data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
    }
    div.stButton > button {
        background: #FF6B00 !important;
        color: #FFFFFF !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        height: 52px !important;
        width: 100% !important;
    }
    .custom-card {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 2px solid #E2E8F0 !important;
        margin-bottom: 15px !important;
    }
    header {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

# --- DOSYA İŞLEMLERİ ---
LOG_FILE = "kayitlar.txt"
def kaydet(mesaj):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%d.%m.%Y %H:%M')} | {mesaj}\n")

def kayitlari_oku():
    if not os.path.exists(LOG_FILE): return "Henüz kayıt yok."
    with open(LOG_FILE, "r", encoding="utf-8") as f: return f.read()

# --- OTURUM ---
if 'login' not in st.session_state: st.session_state['login'] = False
if 'user' not in st.session_state: st.session_state['user'] = {}
if 'secilen_arac' not in st.session_state: st.session_state['secilen_arac'] = None

# --- GİRİŞ EKRANI ---
if not st.session_state['login']:
    st.markdown("<h1 style='text-align:center;'>DriveNow</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("TC Kimlik No", max_chars=11)
        tel = st.text_input("Telefon", max_chars=10)
        if st.form_submit_button("GİRİŞ YAP"):
            if ad and len(tc) == 11:
                st.session_state['login'] = True
                st.session_state['user'] = {"ad": ad, "tc": tc, "tel": tel}
                kaydet(f"SİSTEME GİRİLDİ: {ad} (TC:{tc})")
                st.rerun()
else:
    tab1, tab2, tab3 = st.tabs(["🚗 ARAÇLAR", "📋 KAYITLARIM", "⚙️ YÖNETİCİ"])

    with tab1:
        if st.session_state['secilen_arac'] is None:
            st.write(f"Hoş geldin, **{st.session_state['user']['ad']}**")
            loc = st.selectbox("Lokasyon", ["İstanbul HL", "Sabiha Gökçen HL", "Ankara Esenboğa"])
            days = st.number_input("Gün", min_value=1, value=1)
            for a in ARACLAR:
                total = a['fiyat'] * days
                st.markdown(f"<div class='custom-card'><b style='font-size:18px;'>{a['ad']}</b><br>Toplam: {total} ₺</div>", unsafe_allow_html=True)
                if st.button(f"SEÇ: {a['ad']}", key=a['ad']):
                    st.session_state['secilen_arac'] = {"ad": a['ad'], "toplam": total, "gün": days, "konum": loc}
                    st.rerun()
        else:
            # --- FOTOĞRAF YÜKLEME VE ONAY FORMU ---
            st.warning(f"Seçilen Araç: {st.session_state['secilen_arac']['ad']}")
            with st.form("onay_formu"):
                ehliyet_no = st.text_input("Ehliyet Belge No")
                uploaded_file = st.file_uploader("Ehliyet Fotoğrafını Yükleyin", type=['jpg', 'jpeg', 'png'])
                
                if st.form_submit_button("KİRALAMAYI TAMAMLA"):
                    if ehliyet_no and uploaded_file:
                        # 1. Dosyayı Kaydet
                        dosya_adi = f"{st.session_state['user']['tc']}_{st.session_state['secilen_arac']['ad']}_{datetime.now().strftime('%d%m%H%M')}.jpg"
                        dosya_yolu = os.path.join(UPLOAD_DIR, dosya_adi)
                        with open(dosya_yolu, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # 2. Log Kaydet
                        s = st.session_state['secilen_arac']
                        u = st.session_state['user']
                        kaydet(f"KİRALAMA: {u['ad']} | Araç: {s['ad']} | Foto: {dosya_adi} | Tutar: {s['toplam']} ₺")
                        
                        st.success("İşlem Başarılı! Ehliyetiniz kaydedildi ve kiralama onaylandı.")
                        st.session_state['secilen_arac'] = None
                    else:
                        st.error("Lütfen ehliyet numaranızı girin ve fotoğrafı yükleyin.")

    with tab2:
        logs = kayitlari_oku().split("\n")
        for log in logs:
            if st.session_state['user']['ad'] in log:
                st.markdown(f"<div class='custom-card'>{log}</div>", unsafe_allow_html=True)

    with tab3:
        admin_check = st.checkbox("🔑 Yönetici Paneli")
        if admin_check:
            sifre = st.text_input("Admin Şifresi", type="password")
            if sifre == ADMIN_SIFRE:
                st.success("Hoş geldin Yönetici.")
                
                # Kayıtlar
                st.markdown("### 📄 Rezervasyon Kayıtları")
                st.text_area("Loglar", kayitlari_oku(), height=200)
                
                # Fotoğraflar
                st.markdown("### 📷 Yüklenen Ehliyet Fotoğrafları")
                fotolar = os.listdir(UPLOAD_DIR)
                if fotolar:
                    for foto in fotolar:
                        with open(os.path.join(UPLOAD_DIR, foto), "rb") as file:
                            st.download_button(label=f"İndir: {foto}", data=file, file_name=foto)
                            st.image(os.path.join(UPLOAD_DIR, foto), width=200)
                else:
                    st.info("Henüz fotoğraf yüklenmedi.")
                
                if st.button("🚨 Sistemi Sıfırla"):
                    for f in os.listdir(UPLOAD_DIR): os.remove(os.path.join(UPLOAD_DIR, f))
                    if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
                    st.rerun()
            elif sifre != "": st.error("Yetkisiz Giriş!")

        if st.button("ÇIKIŞ YAP"):
            st.session_state['login'] = False
            st.rerun()
