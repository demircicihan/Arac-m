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
    /* Arka Plan */
    .stApp {
        background: #F1F5F9 !important;
    }

    header, footer {visibility: hidden !important;}

    /* TÜM YAZILAR: Koyu Lacivert ve Net */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span {
        color: #0F172A !important;
        font-family: -apple-system, sans-serif !important;
    }

    /* GİRİŞ KUTULARI (Selectbox, Input, Number) - KARANLIK MODU EZER */
    input, div[data-baseweb="select"], div[data-baseweb="base-input"], .stNumberInput div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border-radius: 12px !important;
        border: 2px solid #CBD5E1 !important;
    }
    
    /* Input içerisindeki metinler */
    input {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-weight: 700 !important;
    }

    /* Dropdown (Açılır Menü) Seçenekleri */
    div[role="listbox"] ul {
        background-color: white !important;
        color: #0F172A !important;
    }

    /* TURUNCU BUTONLAR VE BEYAZ YAZI */
    div.stButton > button, div.stFormSubmitButton > button {
        background: #FF6B00 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        height: 50px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.2) !important;
    }
    
    /* Mavi giriş butonu özel */
    div.stFormSubmitButton > button {
        background: #2563EB !important;
    }

    /* Tab Menüsü */
    div[data-baseweb="tab-list"] {
        background-color: #E2E8F0 !important;
        border-radius: 15px !important;
        padding: 4px !important;
    }
    div[aria-selected="true"] {
        background: #FFFFFF !important;
        border-radius: 12px !important;
    }

    /* Araç Kartları */
    .car-card {
        background: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 1px solid #CBD5E1 !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
    }

    .tag {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        margin-right: 5px;
        border: 1px solid rgba(0,0,0,0.1);
    }
    
    /* PROFIL KARTI (VIP) - Yazıların Beyaz Kalması İçin Zorla */
    .vip-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important;
        padding: 25px !important;
        border-radius: 20px !important;
        color: #FFFFFF !important;
    }
    .vip-card * {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- VERİ VE LOGIC ---
DATA_FILE = "rezervasyonlar.csv"
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"]).to_csv(DATA_FILE, index=False)

if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

# --- GİRİŞ EKRANI ---
if st.session_state['kullanici'] is None:
    st.markdown("<h1 style='text-align:center; margin-bottom:0;'>DriveNow</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.7; margin-bottom:30px;'>Premium Rent a Car</p>", unsafe_allow_html=True)
    
    with st.form("login"):
        ad = st.text_input("Ad Soyad", placeholder="Adınızı giriniz")
        tc = st.text_input("TC Kimlik No", max_chars=11, placeholder="11 hane")
        tel = st.text_input("Telefon", max_chars=10, placeholder="5XXXXXXXXX")
        if st.form_submit_button("DEVAM ET ➔"):
            if ad and len(tc) == 11:
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                st.rerun()
else:
    # --- ANA UYGULAMA ---
    t1, t2, t3 = st.tabs(["🚗 Araçlar", "📋 Kiralamalarım", "👤 Profil"])

    with t1:
        st.markdown("<h4 style='font-weight:800;'>Kiralık Araçlar</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            loc = st.selectbox("Lokasyon", ["İstanbul HL", "Sabiha Gökçen HL", "Ankara HL", "İzmir HL"])
        with c2:
            days = st.number_input("Gün", min_value=1, value=1)

        for a in ARACLAR:
            total = a['fiyat'] * days
            st.markdown(f"""
            <div class="car-card">
                <div style="font-size:11px; color:#2563EB; font-weight:800;">{a['kat']}</div>
                <div style="font-size:22px; font-weight:900; margin-bottom:10px;">{a['ad']}</div>
                <div style="margin-bottom:15px;">
                    <span class="tag" style="background:#DBEAFE; color:#1E40AF;">{a['vites']}</span>
                    <span class="tag" style="background:#FEF3C7; color:#92400E;">{a['yakit']}</span>
                </div>
                <div style="background:#F8FAFC; padding:12px; border-radius:12px; display:flex; justify-content:space-between; align-items:center;">
                    <div><small>GÜNLÜK</small><br><b>{a['fiyat']} ₺</b></div>
                    <div style="text-align:right; color:#FF6B00;"><small>TOPLAM</small><br><b style="font-size:18px;">{total} ₺</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Hemen Kirala: {a['ad']}", key=a['ad']):
                yeni = pd.DataFrame([[datetime.now().strftime("%d.%m.%Y"), st.session_state['kullanici']['ad'], st.session_state['kullanici']['tc'], st.session_state['kullanici']['tel'], loc, a['ad'], days, total]], 
                                    columns=["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"])
                yeni.to_csv(DATA_FILE, mode='a', header=False, index=False)
                st.success("Rezervasyon Başarılı!")

    with t2:
        st.markdown("<h4 style='font-weight:800;'>Rezervasyon Geçmişi</h4>", unsafe_allow_html=True)
        df = pd.read_csv(DATA_FILE)
        user_df = df[df['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
        if not user_df.empty:
            for _, row in user_df.iterrows():
                st.markdown(f"""
                <div class="car-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="font-size:18px;">{row['Arac']}</b>
                        <span style="color:#059669; font-size:12px; font-weight:800;">ONAYLANDI</span>
                    </div>
                    <div style="font-size:13px; opacity:0.7;">{row['Tarih']} | {row['Konum']}</div>
                    <div style="margin-top:8px; font-weight:800;">{row['ToplamTutar']} ₺</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Henüz kaydınız yok.")

    with t3:
        k = st.session_state['kullanici']
        st.markdown(f"""
        <div class="vip-card">
            <div style="font-size:11px; letter-spacing:2px; opacity:0.8; margin-bottom:15px;">DRIVENOW VIP SÜRÜCÜ KARTI</div>
            <div style="font-size:26px; font-weight:900; text-transform:uppercase; margin-bottom:20px;">{k['ad']}</div>
            <div style="background:rgba(255,255,255,0.1); padding:15px; border-radius:15px;">
                <div style="font-size:13px;">TC: {k['tc']}</div>
                <div style="font-size:13px;">TEL: +90 {k['tel']}</div>
            </div>
            <div style="margin-top:30px; text-align:center; font-size:24px; letter-spacing:8px; opacity:0.5;">
                || ||| | || ||||
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("ÇIKIŞ YAP"):
            st.session_state['kullanici'] = None
            st.rerun()
