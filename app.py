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

# --- ARAÇ LİSTESİ (FOTOĞRAFLARI BURADAN DEĞİŞTİREBİLİRSİN) ---
# 'resim' kısmına kendi dosya yolunu veya URL'ni tırnak içinde yazman yeterli.
ARACLAR = [
    {
        "ad": "Peugeot 508 GT", 
        "kat": "SEDAN • PREMİUM", 
        "vites": "Otomatik", 
        "yakit": "Dizel", 
        "fiyat": 1500, 
        "puan": "4.9", 
        "koltuk": "5 Koltuk", 
        "bagaj": "2 Valiz", 
        "resim": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=800" # Burayı değiştir
    },
    {
        "ad": "Renault Clio", 
        "kat": "HATCHBACK • EKONOMİK", 
        "vites": "Manuel", 
        "yakit": "Benzin", 
        "fiyat": 900, 
        "puan": "4.7", 
        "koltuk": "5 Koltuk", 
        "bagaj": "1 Valiz", 
        "resim": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800" # Burayı değiştir
    },
    {
        "ad": "Ford Focus", 
        "kat": "COMPACT • KONFOR", 
        "vites": "Otomatik", 
        "yakit": "Benzin", 
        "fiyat": 1200, 
        "puan": "4.8", 
        "koltuk": "5 Koltuk", 
        "bagaj": "2 Valiz", 
        "resim": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800" # Burayı değiştir
    },
    {
        "ad": "Fiat Egea Cross", 
        "kat": "CROSSOVER • EKONOMİK", 
        "vites": "Manuel", 
        "yakit": "Dizel", 
        "fiyat": 850, 
        "puan": "4.6", 
        "koltuk": "5 Koltuk", 
        "bagaj": "2 Valiz", 
        "resim": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800" # Burayı değiştir
    },
    {
        "ad": "Tesla Model 3", 
        "kat": "LÜKS • %100 ELEKTRİK", 
        "vites": "Otomatik", 
        "yakit": "Elektrik", 
        "fiyat": 2500, 
        "puan": "5.0", 
        "koltuk": "5 Koltuk", 
        "bagaj": "3 Valiz", 
        "resim": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800" # Burayı değiştir
    }
]

# --- TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(160deg, #E0E7FF 0%, #F8FAFC 100%) !important; }
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    /* Metin Renkleri - Koyu Lacivert */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span {
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
    }

    /* iOS Segmented Control */
    div[data-baseweb="tab-list"] {
        background-color: rgba(199, 210, 254, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        padding: 5px !important;
        border: 1px solid rgba(255,255,255,0.8) !important;
    }
    div[aria-selected="true"] {
        background: white !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }

    /* Kart Tasarımı */
    .car-card-modern {
        background: white !important;
        padding: 20px !important;
        border-radius: 26px !important;
        box-shadow: 0 10px 30px rgba(30, 27, 75, 0.05) !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 20px !important;
    }

    .car-photo-main {
        width: 100% !important;
        height: 200px !important;
        object-fit: cover !important;
        border-radius: 18px !important;
        margin: 12px 0 !important;
    }

    /* Tagler */
    .tag-vites { background: #EFF6FF !important; color: #1D4ED8 !important; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 12px; margin-right: 5px; }
    .tag-yakit { background: #FEF3C7 !important; color: #B45309 !important; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 12px; margin-right: 5px; }
    .tag-koltuk { background: #F3E8FF !important; color: #6B21A8 !important; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 12px; margin-right: 5px; }
    .tag-bagaj { background: #ECFDF5 !important; color: #047857 !important; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 12px; }

    .price-row {
        background: #F8FAFC !important;
        padding: 15px !important;
        border-radius: 18px !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 10px;
    }

    /* Butonlar */
    div.stButton > button {
        background: linear-gradient(135deg, #FF6B00 0%, #FF5F00 100%) !important;
        color: white !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: 900 !important;
        height: 50px !important;
        box-shadow: 0 8px 20px rgba(255, 95, 0, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- VERİ TABANI ---
DATA_FILE = "rezervasyonlar.csv"
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"]).to_csv(DATA_FILE, index=False)

# --- UYGULAMA MANTIĞI ---
if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

if st.session_state['kullanici'] is None:
    # Giriş Ekranı
    st.markdown('<div style="text-align: center; padding: 20px;"><h1 style="font-weight: 900; font-size: 40px;">DriveNow</h1><p>Premium Araç Deneyimi</p></div>', unsafe_allow_html=True)
    with st.form("login"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("TC No", max_chars=11)
        tel = st.text_input("Telefon", max_chars=10)
        if st.form_submit_button("DEVAM ET"):
            if ad and len(tc)==11:
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                st.rerun()
else:
    # Ana Uygulama
    tab1, tab2, tab3 = st.tabs(["🚗 Araçlar", "📋 Kiralamalar", "👤 Kartım"])

    with tab1:
        st.markdown("<h4 style='font-weight: 900;'>Senin İçin En İyileri</h4>", unsafe_allow_html=True)
        konum = st.selectbox("Teslim Noktası", ["İstanbul Havalimanı", "Sabiha Gökçen HL", "Ankara Esenboğa", "İzmir Adnan Menderes"])
        gun = st.number_input("Kaç Gün?", min_value=1, value=1)

        for arac in ARACLAR:
            total = arac['fiyat'] * gun
            card = f"""
            <div class="car-card-modern">
                <div style="font-size: 11px; font-weight: 900; color: #2563EB;">{arac['kat']}</div>
                <div style="font-size: 22px; font-weight: 900; margin-bottom: 5px;">{arac['ad']}</div>
                <img src="{arac['resim']}" class="car-photo-main">
                <div style="margin-bottom: 15px;">
                    <span class="tag-vites">{arac['vites']}</span>
                    <span class="tag-yakit">{arac['yakit']}</span>
                    <span class="tag-koltuk">{arac['koltuk']}</span>
                    <span class="tag-bagaj">{arac['bagaj']}</span>
                </div>
                <div class="price-row">
                    <div>
                        <div style="font-size: 10px; color: #64748B;">GÜNLÜK</div>
                        <div style="font-size: 18px; font-weight: 900;">{arac['fiyat']} ₺</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 10px; color: #64748B;">TOPLAM</div>
                        <div style="font-size: 20px; font-weight: 900; color: #FF6B00;">{total} ₺</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(card, unsafe_allow_html=True)
            if st.button(f"Rezerve Et: {arac['ad']}", key=arac['ad']):
                yeni = pd.DataFrame([[datetime.now().strftime("%d/%m/%Y"), st.session_state['kullanici']['ad'], st.session_state['kullanici']['tc'], st.session_state['kullanici']['tel'], konum, arac['ad'], gun, total]], 
                                    columns=["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"])
                yeni.to_csv(DATA_FILE, mode='a', header=False, index=False)
                st.success("Rezervasyon Alındı!")

    with tab2:
        df = pd.read_csv(DATA_FILE)
        user_df = df[df['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
        if not user_df.empty:
            for _, row in user_df.iterrows():
                st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 15px; border: 1px solid #E2E8F0; margin-bottom: 10px;">
                    <div style="font-weight: 900;">{row['Arac']}</div>
                    <div style="font-size: 12px; color: #64748B;">{row['Tarih']} - {row['Konum']}</div>
                    <div style="font-weight: 800; color: #059669;">{row['ToplamTutar']} ₺</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Henüz rezervasyonunuz yok.")

    with tab3:
        k = st.session_state['kullanici']
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 25px; border-radius: 20px; color: white !important;">
            <div style="font-size: 12px; opacity: 0.6; color: white !important;">PREMIUM MEMBER</div>
            <div style="font-size: 24px; font-weight: 900; margin: 10px 0; color: white !important;">{k['ad']}</div>
            <div style="font-size: 14px; color: white !important;">TC: {k['tc']}</div>
            <div style="margin-top: 20px; border-top: 1px dashed rgba(255,255,255,0.2); padding-top: 10px; text-align: center; font-family: monospace; color: white !important;">
                |||||| || |||| ||| ||||
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Çıkış Yap"):
            st.session_state['kullanici'] = None
            st.rerun()
