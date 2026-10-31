import streamlit as st
from datetime import datetime
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="DriveNow Premium", page_icon="🚗", layout="centered")

# --- DOSYA SİSTEMİ ---
LOG_FILE = "kayitlar.txt"
UPLOAD_DIR = "yuklemeler"
if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8-sig") as f: f.write("")

ADMIN_SIFRE = "cihan123"

# --- ARAÇLAR ---
ARACLAR = [
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "fiyat": 1500},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "fiyat": 900},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "fiyat": 1200},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "fiyat": 850},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "fiyat": 2500}
]

# --- GÖRÜNÜR KISIMLARI DÜZELTEN CSS ---
st.markdown("""
    <style>
    /* 1. TÜM ZEMİN VE YAZI KONTROLÜ */
    .stApp { background-color: #FFFFFF !important; }
    
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small, strong, textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* 2. DOSYA YÜKLEYİCİ (FILE UPLOADER) DÜZELTME */
    /* Siyah kutuyu beyaza çevirir */
    [data-testid="stFileUploader"] section {
        background-color: #F8FAFC !important;
        border: 2px dashed #CBD5E1 !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }
    
    /* Dosya yükleyici içindeki küçük yazılar ve 'upload' yazısı */
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] div, [data-testid="stFileUploader"] small {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* 3. İNDİRME BUTONLARI (DOWNLOAD BUTTON) DÜZELTME */
    /* Kararan butonları turuncu veya beyaz yapalım */
    [data-testid="stDownloadButton"] > button {
        background-color: #FFFFFF !important;
        color: #FF6B00 !important;
        border: 2px solid #FF6B00 !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        width: 100% !important;
        margin-top: 5px !important;
    }
    
    [data-testid="stDownloadButton"] > button:hover {
        background-color: #FF6B00 !important;
        color: #FFFFFF !important;
    }

    /* 4. GENEL GİRİŞ KUTULARI (INPUTLAR) */
    input, .stNumberInput div, div[data-baseweb="base-input"] {
        background-color: #F8FAFC !important;
        color: #000000 !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 10px !important;
    }

    /* 5. ANA TURUNCU BUTON (KİRALAMAYI TAMAMLA) */
    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #FF6B00 0%, #FF5F00 100%) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        height: 52px !important;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.3) !important;
    }

    /* Kartlar */
    .custom-card {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 2px solid #F1F5F9 !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }

    header {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

# --- FONKSİYONLAR ---
def kaydet(tip, mesaj):
    zaman = datetime.now().strftime('%d.%m.%Y %H:%M')
    with open(LOG_FILE, "a", encoding="utf-8-sig") as f:
        f.write(f"{zaman} | {tip} | {mesaj}\n")

def kayitlari_ayristir():
    if not os.path.exists(LOG_FILE): return "", ""
    girisler = []
    kiralama = []
    with open(LOG_FILE, "r", encoding="utf-8-sig") as f:
        for satir in f:
            if "| GİRİŞ |" in satir: girisler.append(satir.strip())
            if "| KİRALAMA |" in satir: kiralama.append(satir.strip())
    return "\n".join(girisler), "\n".join(kiralama)

# --- UYGULAMA MANTIĞI ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'user' not in st.session_state: st.session_state['user'] = {}
if 'secili' not in st.session_state: st.session_state['secili'] = None

if not st.session_state['auth']:
    st.markdown("<h1 style='text-align:center;'>DriveNow</h1>", unsafe_allow_html=True)
    with st.form("login"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("TC Kimlik No", max_chars=11)
        tel = st.text_input("Telefon", max_chars=10)
        if st.form_submit_button("DEVAM ET"):
            if ad and len(tc) == 11:
                st.session_state['auth'] = True
                st.session_state['user'] = {"ad": ad, "tc": tc, "tel": tel}
                kaydet("GİRİŞ", f"Ad: {ad} - TC: {tc} - Tel: {tel}")
                st.rerun()
else:
    t1, t2, t3 = st.tabs(["🚗 Araçlar", "📋 Kayıtlarım", "👤 Admin"])

    with t1:
        if st.session_state['secili'] is None:
            st.markdown(f"<h3>Hoş geldin, {st.session_state['user']['ad']}</h3>", unsafe_allow_html=True)
            gun = st.number_input("Gün", min_value=1, value=1)
            for a in ARACLAR:
                fiyat = a['fiyat'] * gun
                st.markdown(f"<div class='custom-card'><b>{a['ad']}</b><br>{fiyat} ₺</div>", unsafe_allow_html=True)
                if st.button(f"SEÇ: {a['ad']}", key=a['ad']):
                    st.session_state['secili'] = {"ad": a['ad'], "fiyat": fiyat}
                    st.rerun()
        else:
            with st.form("kiralama_onay"):
                st.write(f"Araç: {st.session_state['secili']['ad']}")
                ehliyet = st.text_input("Ehliyet No")
                dosya = st.file_uploader("Ehliyet Fotoğrafı", type=['jpg','png'])
                if st.form_submit_button("KİRALAMAYI TAMAMLA"):
                    if ehliyet and dosya:
                        foto_ad = f"{st.session_state['user']['tc']}_{datetime.now().strftime('%H%M%S')}.jpg"
                        with open(os.path.join(UPLOAD_DIR, foto_ad), "wb") as f:
                            f.write(dosya.getbuffer())
                        kaydet("KİRALAMA", f"Müşteri: {st.session_state['user']['ad']} | Araç: {st.session_state['secili']['ad']} | Ehliyet: {ehliyet} | Tutar: {st.session_state['secili']['fiyat']} ₺")
                        st.success("Kiralama Başarılı!")
                        st.session_state['secili'] = None
                        st.rerun()
            if st.button("Vazgeç"):
                st.session_state['secili'] = None
                st.rerun()

    with tab2:
        st.subheader("İşlemleriniz")
        u_ad = st.session_state['user']['ad']
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8-sig") as f:
                for satir in f:
                    if u_ad in satir:
                        st.markdown(f"<div class='custom-card'>{satir}</div>", unsafe_allow_html=True)

    with tab3:
        lock = st.checkbox("🔒 Yönetici Girişi")
        if lock:
            sifre = st.text_input("Şifre", type="password")
            if sifre == ADMIN_SIFRE:
                st.success("Admin Yetkisi Aktif.")
                g_logs, k_logs = kayitlari_ayristir()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("📥 Giriş Kayıtlarını İndir", g_logs, "giris_yapanlar.txt")
                with col2:
                    st.download_button("📥 Kiralama Kayıtlarını İndir", k_logs, "kiralama_kayitlari.txt")
                
                st.markdown("<b>Yüklenen Resimler:</b>", unsafe_allow_html=True)
                fotolar = os.listdir(UPLOAD_DIR)
                for f in fotolar:
                    with open(os.path.join(UPLOAD_DIR, f), "rb") as file:
                        st.image(os.path.join(UPLOAD_DIR, f), width=100)
                        st.download_button(f"İndir: {f}", file, file_name=f)
                
                if st.button("🚨 Verileri Sıfırla"):
                    if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
                    for f in os.listdir(UPLOAD_DIR): os.remove(os.path.join(UPLOAD_DIR, f))
                    st.rerun()
        if st.button("ÇIKIŞ"):
            st.session_state['auth'] = False
            st.rerun()
