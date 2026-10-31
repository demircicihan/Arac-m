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

# --- ARAÇ LİSTESİ (FOTOĞRAFLAR KALDIRILDI) ---
ARACLAR = [
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "vites": "Otomatik", "yakit": "Dizel", "fiyat": 1500, "puan": "4.9", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "vites": "Manuel", "yakit": "Benzin", "fiyat": 900, "puan": "4.7", "koltuk": "5 Koltuk", "bagaj": "1 Valiz"},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "vites": "Otomatik", "yakit": "Benzin", "fiyat": 1200, "puan": "4.8", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "vites": "Manuel", "yakit": "Dizel", "fiyat": 850, "puan": "4.6", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "vites": "Otomatik", "yakit": "Elektrik", "fiyat": 2500, "puan": "5.0", "koltuk": "5 Koltuk", "bagaj": "3 Valiz"}
]

# --- TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(160deg, #E0E7FF 0%, #F8FAFC 100%) !important; }
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span {
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
    }

    div[data-baseweb="tab-list"] {
        background-color: rgba(199, 210, 254, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        padding: 5px !important;
        border: 1px solid rgba(255,255,255,0.8) !important;
        margin-bottom: 20px;
    }
    div[aria-selected="true"] {
        background: white !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }

    .car-card-modern {
        background: white !important;
        padding: 24px !important;
        border-radius: 26px !important;
        box-shadow: 0 10px 30px rgba(30, 27, 75, 0.05) !important;
        border: 1.5px solid #E2E8F0 !important;
        margin-bottom: 20px !important;
    }

    .tag-vites { background: #EFF6FF !important; color: #1D4ED8 !important; padding: 6px 12px; border-radius: 10px; font-weight: 800; font-size: 12px; margin-right: 6px; }
    .tag-yakit { background: #FEF3C7 !important; color: #B45309 !important; padding: 6px 12px; border-radius: 10px; font-weight: 800; font-size: 12px; margin-right: 6px; }
    .tag-koltuk { background: #F3E8FF !important; color: #6B21A8 !important; padding: 6px 12px; border-radius: 10px; font-weight: 800; font-size: 12px; margin-right: 6px; }
    .tag-bagaj { background: #ECFDF5 !important; color: #047857 !important; padding: 6px 12px; border-radius: 10px; font-weight: 800; font-size: 12px; }

    .price-row {
        background: #F8FAFC !important;
        padding: 16px !important;
        border-radius: 20px !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 15px;
        border: 1px solid #F1F5F9;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #FF6B00 0%, #FF5F00 100%) !important;
        color: white !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: 900 !important;
        height: 52px !important;
        box-shadow: 0 8px 20px rgba(255, 95, 0, 0.3) !important;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- VERİ TABANI ---
DATA_FILE = "rezervasyonlar.csv"
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"]).to_csv(DATA_FILE, index=False)

# --- OTURUM YÖNETİMİ ---
if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

if st.session_state['kullanici'] is None:
    st.markdown('<div style="text-align: center; padding: 30px 20px;"><h1 style="font-weight: 900; font-size: 42px; margin-bottom: 5px;">DriveNow</h1><p style="opacity: 0.7; font-weight: 600;">Hızlı ve Güvenli Araç Kiralama</p></div>', unsafe_allow_html=True)
    with st.form("login_form"):
        ad = st.text_input("Ad Soyad", placeholder="Örn: Cihan Demir")
        tc = st.text_input("TC Kimlik No", max_chars=11, placeholder="11 haneli")
        tel = st.text_input("Telefon", max_chars=10, placeholder="5XXXXXXXXX")
        if st.form_submit_button("ARAÇLARI GÖR"):
            if ad and len(tc) == 11:
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                st.rerun()
else:
    tab1, tab2, tab3 = st.tabs(["🚗 Araç Seçimi", "📋 Rezervasyonlarım", "👤 Profilim"])

    with tab1:
        st.markdown("<h4 style='font-weight: 900; margin-bottom: 15px;'>Mevcut Araçlar</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            konum = st.selectbox("Lokasyon", ["İstanbul HL", "Sabiha Gökçen HL", "Ankara HL", "İzmir HL"])
        with c2:
            gun = st.number_input("Gün Sayısı", min_value=1, value=1)

        for arac in ARACLAR:
            total = arac['fiyat'] * gun
            card_html = f"""
            <div class="car-card-modern">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div style="font-size: 11px; font-weight: 900; color: #2563EB; letter-spacing: 0.5px;">{arac['kat']}</div>
                        <div style="font-size: 24px; font-weight: 900; margin: 4px 0;">{arac['ad']}</div>
                    </div>
                    <div style="background: #FEF3C7; color: #B45309; padding: 4px 10px; border-radius: 10px; font-weight: 900; font-size: 13px;">★ {arac['puan']}</div>
                </div>
                <div style="margin: 15px 0;">
                    <span class="tag-vites">{arac['vites']}</span>
                    <span class="tag-yakit">{arac['yakit']}</span>
                    <span class="tag-koltuk">{arac['koltuk']}</span>
                </div>
                <div class="price-row">
                    <div>
                        <div style="font-size: 10px; color: #64748B; font-weight: 700;">GÜNLÜK</div>
                        <div style="font-size: 18px; font-weight: 900; color: #0F172A;">{arac['fiyat']} ₺</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 10px; color: #64748B; font-weight: 700;">TOPLAM ÖDEME</div>
                        <div style="font-size: 20px; font-weight: 900; color: #FF6B00;">{total} ₺</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            if st.button(f"Hemen Kirala: {arac['ad']}", key=arac['ad']):
                yeni_kayit = pd.DataFrame([[datetime.now().strftime("%d.%m.%Y"), st.session_state['kullanici']['ad'], st.session_state['kullanici']['tc'], st.session_state['kullanici']['tel'], konum, arac['ad'], gun, total]], 
                                    columns=["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"])
                yeni_kayit.to_csv(DATA_FILE, mode='a', header=False, index=False)
                st.success(f"Tebrikler! {arac['ad']} rezerve edildi.")

    with tab2:
        df = pd.read_csv(DATA_FILE)
        user_df = df[df['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
        if not user_df.empty:
            for _, row in user_df.iterrows():
                st.markdown(f"""
                <div style="background: white; padding: 20px; border-radius: 20px; border: 1.5px solid #E2E8F0; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-weight: 900; font-size: 18px;">{row['Arac']}</span>
                        <span style="color: #059669; font-weight: 800; font-size: 14px;">Aktif</span>
                    </div>
                    <div style="font-size: 13px; color: #64748B; margin: 8px 0;">{row['Tarih']} • {row['Konum']}</div>
                    <div style="font-weight: 900; font-size: 16px; color: #0F172A;">{row['ToplamTutar']} ₺</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Henüz bir kiralama yapmadınız.")

    with tab3:
        k = st.session_state['kullanici']
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 30px; border-radius: 24px; color: white !important; box-shadow: 0 15px 35px rgba(0,0,0,0.2);">
            <div style="font-size: 12px; opacity: 0.6; letter-spacing: 2px; color: white !important;">VIP SÜRÜCÜ KARTI</div>
            <div style="font-size: 26px; font-weight: 900; margin: 15px 0; color: white !important;">{k['ad']}</div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 15px;">
                <div style="font-size: 13px; color: white !important;">TC: {k['tc']}</div>
                <div style="font-size: 13px; color: white !important;">TEL: +90 {k['tel']}</div>
            </div>
            <div style="margin-top: 25px; border-top: 1px dashed rgba(255,255,255,0.3); padding-top: 20px; text-align: center; font-family: monospace; font-size: 20px; letter-spacing: 5px; color: white !important;">
                || ||| | || |||| |
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Sistemden Çıkış Yap"):
            st.session_state['kullanici'] = None
            st.rerun()
