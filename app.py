import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Sayfa Ayarları
st.set_page_config(
    page_title="Araç Kiralama",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# iOS Light Mode ve Yüksek Kontrast Tasarım CSS Overrides
st.markdown("""
    <style>
    /* Arka planı iOS Gri yap */
    .stApp {
        background-color: #F2F2F7 !important;
    }
    
    /* Üst ve alt varsayılan Streamlit çubuklarını gizle */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stDeployButton {display:none !important;}

    /* Genel Yazı Renklerini Siyah/Koyu Griye Zorla */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span {
        color: #1C1C1E !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* Form Etiketleri (Input üstündeki yazılar) */
    label p, label span {
        color: #1C1C1E !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Input kutuları stili */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 10px !important;
        border: 1px solid #C7C7CC !important;
        font-weight: 500 !important;
    }

    /* iOS Tarzı Beyaz Kart Tasarımı */
    .ios-card {
        background-color: #FFFFFF !important;
        padding: 16px !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
        margin-bottom: 12px !important;
        border: 1px solid #E5E5EA !important;
    }

    .car-title {
        color: #000000 !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        margin-bottom: 6px !important;
    }

    .car-info {
        color: #3A3A3C !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
        font-weight: 500 !important;
    }

    .badge-green {
        color: #34C759 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        background-color: #E8F9ED !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        display: inline-block !important;
        margin-bottom: 8px !important;
    }

    .price-daily {
        color: #007AFF !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin: 2px 0 !important;
    }

    .price-total {
        color: #1C1C1E !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }

    /* GİRİŞ YAP VE FORMLAR İÇİN MAVİ BUTON */
    div.stFormSubmitButton > button {
        width: 100% !important;
        background-color: #007AFF !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px !important;
        box-shadow: 0 2px 8px rgba(0, 122, 255, 0.3) !important;
    }

    /* KİRALAMA İÇİN TURUNCU BUTON */
    div.stButton > button {
        width: 100% !important;
        background-color: #FF9500 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px !important;
        box-shadow: 0 2px 8px rgba(255, 149, 0, 0.3) !important;
    }

    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        opacity: 0.9 !important;
        color: #FFFFFF !important;
    }
    
    /* Tab Menü Başlıkları */
    button[data-baseweb="tab"] p {
        font-size: 15px !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "rezervasyonlar.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Tarih", "Musteri", "TC", "Telefon", "Arac", "Gun", "ToplamTutar"])
    df.to_csv(DATA_FILE, index=False)

ARACLAR = [
    {"ad": "Peugeot 508", "vites": "Otomatik", "yakit": "Dizel", "fiyat": 1500, "foto": "🚘"},
    {"ad": "Renault Clio", "vites": "Manuel", "yakit": "Benzin", "fiyat": 900, "foto": "🚗"},
    {"ad": "Ford Focus", "vites": "Otomatik", "yakit": "Benzin", "fiyat": 1200, "foto": "🚙"},
    {"ad": "Fiat Egea", "vites": "Manuel", "yakit": "Dizel", "fiyat": 800, "foto": "🚕"},
    {"ad": "Tesla Model 3", "vites": "Otomatik", "yakit": "Elektrik", "fiyat": 2500, "foto": "⚡"}
]

if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

# 1. GİRİŞ EKRANI
if st.session_state['kullanici'] is None:
    st.markdown("<h1 style='text-align: center; color: #000000 !important;'>🚗 Rent a Car</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #8E8E93 !important;'>Sisteme Giriş Yapın</h4>", unsafe_allow_html=True)
    st.write("")

    with st.form("giris_formu"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("T.C. Kimlik No", max_chars=11)
        tel = st.text_input("Telefon No (5XX)", max_chars=10)
        submit = st.form_submit_button("GİRİŞ YAP ➔")

        if submit:
            if ad and len(tc) == 11 and len(tel) == 10:
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                st.success("Giriş Başarılı!")
                st.rerun()
            else:
                st.error("Lütfen bilgileri doğru girin (TC: 11 hane, Tel: 10 hane).")

# 2. ANA UYGULAMA EKRANI
else:
    col_user, col_logout = st.columns([3, 1])
    with col_user:
        st.markdown(f"👤 **{st.session_state['kullanici']['ad']}**")
    with col_logout:
        if st.button("Çıkış"):
            st.session_state['kullanici'] = None
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["🚗 Araç Kirala", "📋 Geçmişim", "👤 Profil"])

    # SEKME 1: ARAÇLAR
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            vites_filtre = st.selectbox("Vites Tipi", ["Tümü", "Otomatik", "Manuel"])
        with c2:
            gun = st.number_input("Kiralama Süresi (Gün)", min_value=1, max_value=30, value=1)

        for arac in ARACLAR:
            if vites_filtre != "Tümü" and arac["vites"] != vites_filtre:
                continue

            toplam_fiyat = arac["fiyat"] * gun
            
            st.markdown(f"""
            <div class="ios-card">
                <div class="car-title">{arac['foto']} {arac['ad']}</div>
                <div class="car-info">⛽ <b>Yakıt:</b> {arac['yakit']} &nbsp;|&nbsp; 🔀 <b>Vites:</b> {arac['vites']}</div>
                <div class="badge-green">✓ Ücretsiz İptal</div>
                <div class="price-daily">Günlük: {arac['fiyat']} ₺</div>
                <div class="price-total">Toplam ({gun} Gün): {toplam_fiyat:,} ₺</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Hemen Kirala - {arac['ad']}", key=arac['ad']):
                yeni_kayit = pd.DataFrame([{
                    "Tarih": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Musteri": st.session_state['kullanici']['ad'],
                    "TC": st.session_state['kullanici']['tc'],
                    "Telefon": st.session_state['kullanici']['tel'],
                    "Arac": arac['ad'],
                    "Gun": gun,
                    "ToplamTutar": toplam_fiyat
                }])
                yeni_kayit.to_csv(DATA_FILE, mode='a', header=False, index=False)
                st.balloons()
                st.success(f"🎉 {arac['ad']} kiralandı! Toplam: {toplam_fiyat} ₺")

    # SEKME 2: GEÇMİŞ
    with tab2:
        st.markdown("<h3 style='color: #000000 !important;'>Kiralama Geçmişiniz</h3>", unsafe_allow_html=True)
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            user_df = df[df['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
            if not user_df.empty:
                for idx, row in user_df.iterrows():
                    st.markdown(f"""
                    <div class="ios-card">
                        <div style="font-size: 16px; font-weight: 700; color: #007AFF;">🚗 {row['Arac']}</div>
                        <div style="font-size: 13px; color: #8E8E93; margin-top: 4px;">📅 Tarih: {row['Tarih']}</div>
                        <div style="font-size: 14px; color: #1C1C1E; font-weight: 600; margin-top: 6px;">
                            ⏱ Süre: {row['Gun']} Gün | 💰 Toplam: {row['ToplamTutar']} ₺
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Henüz kiralama yapmadınız.")

    # SEKME 3: PROFİL (NET İOS KART TASARIMI)
    with tab3:
        st.markdown("<h3 style='color: #000000 !important;'>Profil Bilgileri</h3>", unsafe_allow_html=True)
        k = st.session_state['kullanici']
        st.markdown(f"""
        <div class="ios-card">
            <div style="font-size: 15px; color: #1C1C1E; margin-bottom: 8px;"><b>👤 Ad Soyad:</b> {k['ad']}</div>
            <div style="font-size: 15px; color: #1C1C1E; margin-bottom: 8px;"><b>🪪 T.C. Kimlik No:</b> {k['tc']}</div>
            <div style="font-size: 15px; color: #1C1C1E;"><b>📞 Telefon:</b> {k['tel']}</div>
        </div>
        """, unsafe_allow_html=True)
