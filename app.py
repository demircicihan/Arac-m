import streamlit as st
from datetime import datetime
import os

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="DriveNow Premium",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- KLASÖR VE DOSYA KONTROLÜ ---
LOG_FILE = "kayitlar.txt"
UPLOAD_DIR = "yuklemeler"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8-sig") as f:
        f.write("")

ADMIN_SIFRE = "cihan123"

# --- ARAÇ FİLOSU ---
ARACLAR = [
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "vites": "Otomatik", "yakit": "Dizel", "fiyat": 1500, "puan": "4.9", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "vites": "Manuel", "yakit": "Benzin", "fiyat": 900, "puan": "4.7", "koltuk": "5 Koltuk", "bagaj": "1 Valiz"},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "vites": "Otomatik", "yakit": "Benzin", "fiyat": 1200, "puan": "4.8", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "vites": "Manuel", "yakit": "Dizel", "fiyat": 850, "puan": "4.6", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "vites": "Otomatik", "yakit": "Elektrik", "fiyat": 2500, "puan": "5.0", "koltuk": "5 Koltuk", "bagaj": "3 Valiz"}
]

# --- KRİTİK CSS DÜZELTMESİ (GÖRÜNTÜ SORUNU İÇİN) ---
st.markdown("""
    <style>
    /* Genel Arkaplan */
    .stApp {
        background: #F8FAFC !important;
    }

    /* TÜM METİNLERİ ZORLA SİYAH YAP (GHOST TEXT ENGELLEME) */
    * {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
    }

    /* GÖRSELDEKİ HATALI SELECTBOX VE INPUT DÜZELTMESİ */
    /* Selectbox (Seçim Kutusu) Dış ve İç Kutusu */
    div[data-baseweb="select"], div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #C7D2FE !important;
    }
    
    /* Sayı Girişi (Number Input) Düzeltmesi */
    div[data-testid="stNumberInput"] div[data-baseweb="base-input"],
    [data-testid="stNumberInputContainer"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #C7D2FE !important;
    }

    /* Sayı Girişi Artı/Eksi Butonlarını Görünür Yap */
    button[tabindex="0"] {
        background-color: #F1F5F9 !important;
        border-radius: 8px !important;
        color: #0F172A !important;
    }

    /* Arama Kartı (Mavi Çerçeveli Alan) */
    .search-card {
        background: #FFFFFF !important;
        padding: 18px !important;
        border-radius: 20px !important;
        border: 1px solid #C7D2FE !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.05) !important;
        margin-bottom: 20px !important;
    }

    /* Araç Kartları */
    .car-card-detailed {
        background: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 15px !important;
    }

    /* Mavi/Turuncu Buton Metin Rengi (Beyaz Kalmalı) */
    div.stButton > button, div.stFormSubmitButton > button {
        background: #FF6B00 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        border: none !important;
    }

    /* Etiketler (Badges) */
    .tag-vites { background: #EFF6FF !important; color: #1D4ED8 !important; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; margin-right: 4px; border: 1px solid #BFDBFE; }
    .tag-yakit { background: #FEF3C7 !important; color: #B45309 !important; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; margin-right: 4px; border: 1px solid #FDE68A; }
    </style>
""", unsafe_allow_html=True)

# --- KAYIT FONKSİYONLARI ---
def kaydet(tip, mesaj):
    zaman = datetime.now().strftime('%d.%m.%Y %H:%M')
    with open(LOG_FILE, "a", encoding="utf-8-sig") as f:
        f.write(f"{zaman} | {tip} | {mesaj}\n")

# --- OTURUM ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'user' not in st.session_state: st.session_state['user'] = {}
if 'secili' not in st.session_state: st.session_state['secili'] = None

# --- EKRAN AKIŞI ---
if not st.session_state['auth']:
    st.markdown("<h2 style='text-align:center;'>DriveNow Premium</h2>", unsafe_allow_html=True)
    with st.form("giris"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("T.C. Kimlik No", max_chars=11)
        tel = st.text_input("Telefon", max_chars=10)
        if st.form_submit_button("DEVAM ET ➔"):
            if ad and len(tc) == 11 and len(tel) == 10:
                st.session_state['auth'] = True
                st.session_state['user'] = {"ad": ad, "tc": tc, "tel": tel}
                kaydet("GİRİŞ", f"{ad} - {tc}")
                st.rerun()
            else:
                st.error("Bilgileri kontrol edin.")
else:
    t1, t2, t3 = st.tabs(["🚗 Araçlar", "📋 Kayıtlarım", "👤 Profil"])

    with t1:
        if st.session_state['secili'] is None:
            # GÖRSELDEKİ SORUNLU KISIM BURASI - CSS İLE DÜZELTİLDİ
            st.markdown(f'<div class="search-card"><div style="font-weight:900; margin-bottom:10px;">👋 Merhaba, {st.session_state["user"]["ad"]}</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns([2, 1.5, 1])
            with c1: konum = st.selectbox("📍 Teslimat Noktası", ["İstanbul Havalimanı", "Sabiha Gökçen HL", "Ankara Esenboğa", "İzmir Adnan Menderes"])
            with c2: vites = st.selectbox("🔀 Vites", ["Tümü", "Otomatik", "Manuel"])
            with c3: gun = st.number_input("⏱ Gün", 1, 30, 1)
            st.markdown('</div>', unsafe_allow_html=True)

            for a in ARACLAR:
                if vites != "Tümü" and a["vites"] != vites: continue
                toplam = a["fiyat"] * gun
                st.markdown(f"""
                <div class="car-card-detailed">
                    <div style="font-size:12px; font-weight:800; color:#2563EB;">{a['kat']}</div>
                    <div style="font-size:22px; font-weight:900;">{a['ad']}</div>
                    <div style="margin: 8px 0;">
                        <span class="tag-vites">{a['vites']}</span>
                        <span class="tag-yakit">{a['yakit']}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; background:#F8FAFC; padding:10px; border-radius:12px;">
                        <div><small>Günlük</small><br><b>{a['fiyat']} ₺</b></div>
                        <div style="text-align:right;"><small>Toplam</small><br><b style="font-size:18px; color:#FF6B00;">{toplam} ₺</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Rezerve Et: {a['ad']}", key=a['ad']):
                    st.session_state['secili'] = {"ad": a['ad'], "toplam": toplam, "gun": gun, "konum": konum}
                    st.rerun()
        else:
            s = st.session_state['secili']
            st.markdown(f"### 🔒 Rezervasyon: {s['ad']}")
            with st.form("onay"):
                seri = st.text_input("Ehliyet Seri No")
                sinif = st.selectbox("Ehliyet Sınıfı", ["B", "B1", "A", "C", "D"])
                foto = st.file_uploader("Ehliyet Fotoğrafı", type=['jpg', 'png'])
                if st.form_submit_button("KİRALAMAYI TAMAMLA"):
                    if seri and foto:
                        fname = f"{st.session_state['user']['tc']}_{datetime.now().strftime('%H%M%S')}.jpg"
                        with open(os.path.join(UPLOAD_DIR, fname), "wb") as f:
                            f.write(foto.getbuffer())
                        kaydet("KİRALAMA", f"{s['ad']} | {s['konum']} | {s['toplam']} TL | Foto: {fname}")
                        st.success("İşlem Başarılı!")
                        st.session_state['secili'] = None
                        st.rerun()
            if st.button("⬅️ Geri Dön"):
                st.session_state['secili'] = None
                st.rerun()

    with t2:
        st.markdown("### 📋 Rezervasyonlarınız")
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8-sig") as f:
                for satir in f:
                    if st.session_state['user']['tc'] in satir:
                        st.info(satir)

    with t3:
        if st.checkbox("Yönetici Paneli"):
            sifre = st.text_input("Şifre", type="password")
            if sifre == ADMIN_SIFRE:
                if st.button("Verileri Sıfırla"):
                    open(LOG_FILE, "w").close()
                    st.rerun()
                st.text(open(LOG_FILE, "r").read())
        if st.button("Çıkış Yap"):
            st.session_state['auth'] = False
            st.rerun()
