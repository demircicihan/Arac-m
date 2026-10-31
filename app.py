import streamlit as st
from datetime import datetime
import os

# --- AYARLAR ---
st.set_page_config(page_title="DriveNow Premium", page_icon="🚗", layout="centered")

# ---ADMİN ŞİFRE BELİRLE (Burayı istediğin şifreyle değiştirebilirsin) ---
ADMIN_SIFRE = "cihan123" 

# --- ARAÇLAR ---
ARACLAR = [
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "fiyat": 1500},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "fiyat": 900},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "fiyat": 1200},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "fiyat": 850},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "fiyat": 2500}
]

# --- KARANLIK MODU TAMAMEN DEVRE DIŞI BIRAKAN CSS ---
st.markdown("""
    <style>
    /* Arka planı beyaza zorla */
    .stApp { background-color: #F8FAFC !important; }
    
    /* Tüm yazıları koyu lacivert/siyah yap */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small {
        color: #0F172A !important;
        font-family: -apple-system, sans-serif !important;
    }

    /* Giriş kutuları ve butonlar - iOS Karanlık Modu ezer */
    input, div[data-baseweb="select"], .stNumberInput div, div[data-baseweb="base-input"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
        -webkit-text-fill-color: #0F172A !important;
    }

    /* Butonları Turuncu yap ve yazısını beyazda kilitle */
    div.stButton > button, div.stFormSubmitButton > button {
        background: #FF6B00 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        height: 52px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.3) !important;
    }
    
    div.stButton > button p, div.stFormSubmitButton > button p {
        color: #FFFFFF !important;
    }

    /* Kartlar ve Tablar */
    .custom-card {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 2px solid #E2E8F0 !important;
        margin-bottom: 15px !important;
    }
    div[data-baseweb="tab-list"] { background-color: #E2E8F0 !important; border-radius: 15px; padding: 5px; }
    div[aria-selected="true"] { background-color: #FFFFFF !important; border-radius: 10px; }

    header {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

# --- DOSYA SİSTEMİ ---
LOG_FILE = "kayitlar.txt"
def kaydet(mesaj):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%d.%m.%Y %H:%M')} | {mesaj}\n")

def kayitlari_oku():
    if not os.path.exists(LOG_FILE): return "Henüz kayıt yok."
    with open(LOG_FILE, "r", encoding="utf-8") as f: return f.read()

# --- OTURUM ---
if 'login' not in st.session_state:
    st.session_state['login'] = False
    st.session_state['user'] = {}

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
                kaydet(f"GİRİŞ: {ad} - TC: {tc} - TEL: {tel}")
                st.rerun()
else:
    tab1, tab2, tab3 = st.tabs(["🚗 ARAÇLAR", "📋 KAYITLARIM", "⚙️ PROFİL"])

    with tab1:
        st.write(f"Merhaba, **{st.session_state['user']['ad']}**")
        loc = st.selectbox("Alış Yeri", ["İstanbul Havalimanı", "Sabiha Gökçen HL", "Ankara Esenboğa"])
        days = st.number_input("Gün", min_value=1, value=1)

        for a in ARACLAR:
            total = a['fiyat'] * days
            st.markdown(f"""
            <div class="custom-card">
                <b style="font-size:20px;">{a['ad']}</b><br>
                <div style="display:flex; justify-content:space-between; margin-top:10px;">
                    <span>Günlük: <b>{a['fiyat']} ₺</b></span>
                    <span style="color:#FF6B00;">Toplam: <b>{total} ₺</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"KİRALA: {a['ad']}", key=a['ad']):
                kaydet(f"KİRALAMA: {st.session_state['user']['ad']} | Araç: {a['ad']} | Gün: {days} | Toplam: {total} ₺ | Yer: {loc}")
                st.success("Rezervasyon kaydedildi!")

    with tab2:
        st.subheader("İşlemleriniz")
        logs = kayitlari_oku().split("\n")
        sayac = 0
        for log in logs:
            if st.session_state['user']['ad'] in log:
                st.markdown(f"<div class='custom-card'>{log}</div>", unsafe_allow_html=True)
                sayac += 1
        if sayac == 0: st.info("Kaydınız bulunamadı.")

    with tab3:
        # KİŞİSEL BİLGİ
        st.markdown(f"""<div style="background:white; border:2px solid #0F172A; padding:15px; border-radius:12px;">
        <b>İsim:</b> {st.session_state['user']['ad']}<br>
        <b>TC:</b> {st.session_state['user']['tc']}</div>""", unsafe_allow_html=True)
        
        st.write("---")
        
        # SADECE SENİN GÖREBİLECEĞİN ŞİFRELİ PANEL
        admin_check = st.checkbox("🔑 Yönetici Panelini Aç")
        if admin_check:
            sifre = st.text_input("Admin Şifresini Girin", type="password")
            if sifre == ADMIN_SIFRE:
                st.success("Yetki Onaylandı. Hoş geldin Cihan.")
                st.markdown("### Tüm Sistem Kayıtları")
                st.text_area("Loglar", kayitlari_oku(), height=200)
                
                st.download_button("📥 Kayıtları TXT Olarak İndir", kayitlari_oku(), "sistem_kayit.txt")
                
                if st.button("🚨 Verileri Sıfırla"):
                    if os.path.exists(LOG_FILE):
                        os.remove(LOG_FILE)
                        st.rerun()
            elif sifre != "":
                st.error("Hatalı Şifre! Bu alana erişim yetkiniz yok.")

        if st.button("ÇIKIŞ YAP"):
            st.session_state['login'] = False
            st.rerun()
