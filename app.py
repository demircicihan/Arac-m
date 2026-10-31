import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="DriveNow Premium",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ARAÇ LİSTESİ ---
ARACLAR = [
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "vites": "Otomatik", "yakit": "Dizel", "fiyat": 1500, "puan": "4.9", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "vites": "Manuel", "yakit": "Benzin", "fiyat": 900, "puan": "4.7", "koltuk": "5 Koltuk", "bagaj": "1 Valiz"},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "vites": "Otomatik", "yakit": "Benzin", "fiyat": 1200, "puan": "4.8", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "vites": "Manuel", "yakit": "Dizel", "fiyat": 850, "puan": "4.6", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "vites": "Otomatik", "yakit": "Elektrik", "fiyat": 2500, "puan": "5.0", "koltuk": "5 Koltuk", "bagaj": "3 Valiz"}
]

# --- KRİTİK GÖRÜNÜRLÜK AYARLARI (CSS) ---
st.markdown("""
    <style>
    /* Genel Arka Plan */
    .stApp { background-color: #F1F5F9 !important; }
    header, footer {visibility: hidden !important;}

    /* TÜM YAZILARI KOYU LACİVERT YAP (KARANLIK MODU EZER) */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small {
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* GİRİŞ KUTULARI VE SELECTBOX GÖRÜNÜRLÜĞÜ */
    input, div[data-baseweb="select"], .stNumberInput div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
    }
    
    /* ARAÇ KARTI TASARIMI */
    .car-card {
        background-color: #FFFFFF !important;
        padding: 22px !important;
        border-radius: 24px !important;
        border: 2px solid #E2E8F0 !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }

    /* ARAÇ İSMİ - ÖZELLİKLE BURAYI KİLİTLEDİK */
    .car-title {
        font-size: 26px !important;
        font-weight: 900 !important;
        color: #0F172A !important;
        margin: 5px 0 12px 0 !important;
        display: block !important;
    }

    /* ETİKETLER */
    .tag-box {
        display: flex;
        gap: 6px;
        margin-bottom: 15px;
    }
    .tag-item {
        padding: 6px 12px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 800;
        border: 1px solid rgba(0,0,0,0.05);
    }

    /* FİYAT ALANI */
    .price-container {
        background-color: #F8FAFC !important;
        padding: 15px !important;
        border-radius: 16px !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #F1F5F9;
    }

    /* BUTONLAR */
    div.stButton > button {
        background: linear-gradient(135deg, #FF6B00 0%, #FF5F00 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 16px !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        height: 52px !important;
        width: 100% !important;
        margin-top: 10px !important;
        box-shadow: 0 6px 15px rgba(255, 95, 0, 0.3) !important;
    }

    /* TAB MENÜSÜ */
    div[data-baseweb="tab-list"] {
        background-color: #E2E8F0 !important;
        border-radius: 15px !important;
        padding: 5px !important;
    }
    div[aria-selected="true"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
    }
    
    /* PROFIL KARTI */
    .driver-card {
        background: #1E293B !important;
        padding: 25px !important;
        border-radius: 20px !important;
    }
    .driver-card * { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# --- VERİ İŞLEMLERİ ---
DATA_FILE = "rezervasyonlar.csv"
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"]).to_csv(DATA_FILE, index=False)

if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

# --- UYGULAMA AKIŞI ---
if st.session_state['kullanici'] is None:
    st.markdown("<h1 style='text-align:center; font-weight:900;'>DriveNow</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("TC Kimlik No", max_chars=11)
        tel = st.text_input("Telefon", max_chars=10)
        if st.form_submit_button("DEVAM ET"):
            if ad and len(tc) == 11:
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                st.rerun()
else:
    tab1, tab2, tab3 = st.tabs(["🚗 Araç Seç", "📋 Kiralamalarım", "👤 Profil"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            loc = st.selectbox("Lokasyon", ["İstanbul HL", "Sabiha Gökçen HL", "Ankara HL", "İzmir HL"])
        with c2:
            days = st.number_input("Gün", min_value=1, value=1)

        for a in ARACLAR:
            total = a['fiyat'] * days
            # HTML Kart Yapısı
            st.markdown(f"""
            <div class="car-card">
                <div style="font-size:11px; font-weight:900; color:#2563EB;">{a['kat']}</div>
                <div class="car-title">{a['ad']}</div>
                <div class="tag-box">
                    <span class="tag-item" style="background:#DBEAFE; color:#1E40AF;">{a['vites']}</span>
                    <span class="tag-item" style="background:#FEF3C7; color:#92400E;">{a['yakit']}</span>
                    <span class="tag-item" style="background:#F3E8FF; color:#6B21A8;">{a['koltuk']}</span>
                </div>
                <div class="price-container">
                    <div>
                        <small style="font-weight:700; opacity:0.6;">GÜNLÜK</small><br>
                        <b style="font-size:18px;">{a['fiyat']} ₺</b>
                    </div>
                    <div style="text-align:right;">
                        <small style="font-weight:700; color:#FF6B00;">TOPLAM</small><br>
                        <b style="font-size:22px;">{total} ₺</b>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Hemen Kirala: {a['ad']}", key=a['ad']):
                yeni = pd.DataFrame([[datetime.now().strftime("%d.%m.%Y"), st.session_state['kullanici']['ad'], st.session_state['kullanici']['tc'], st.session_state['kullanici']['tel'], loc, a['ad'], days, total]], 
                                    columns=["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"])
                yeni.to_csv(DATA_FILE, mode='a', header=False, index=False)
                st.success(f"Başarılı! {a['ad']} ayrıldı.")

    with tab2:
        df = pd.read_csv(DATA_FILE)
        user_df = df[df['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
        if not user_df.empty:
            for _, row in user_df.iterrows():
                st.markdown(f"""
                <div class="car-card">
                    <b style="font-size:20px;">{row['Arac']}</b>
                    <div style="font-size:13px; margin:5px 0;">{row['Tarih']} • {row['Konum']}</div>
                    <div style="font-weight:900; color:#059669;">{row['ToplamTutar']} ₺ - ONAYLANDI</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Henüz kiralama yapmadınız.")

    with tab3:
        k = st.session_state['kullanici']
        st.markdown(f"""
        <div class="driver-card">
            <div style="font-size:10px; letter-spacing:2px; opacity:0.7;">PREMIUM SÜRÜCÜ</div>
            <div style="font-size:24px; font-weight:900; margin:15px 0;">{k['ad']}</div>
            <div style="font-size:14px; opacity:0.9;">TC: {k['tc']}</div>
            <div style="font-size:14px; opacity:0.9;">TEL: +90 {k['tel']}</div>
            <div style="margin-top:20px; border-top:1px dashed rgba(255,255,255,0.3); padding-top:15px; text-align:center; font-size:20px; letter-spacing:5px;">
                ||| || |||| ||
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Çıkış Yap"):
            st.session_state['kullanici'] = None
            st.rerun()
