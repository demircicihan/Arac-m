import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Sayfa Ayarları
st.set_page_config(
    page_title="DriveNow | Araç Kiralama",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ULTRA MODERN CAR RENTAL UI & LIGHT MODE CSS
st.markdown("""
    <style>
    /* Global Arka Plan - iOS Cool Grey */
    .stApp {
        background-color: #F4F5F7 !important;
    }
    
    /* Streamlit Varsayılan Elemanları Gizleme */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stDeployButton {display:none !important;}

    /* Tipografi Sıfırlama ve Yüksek Kontrast */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span {
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif !important;
    }

    /* Input Kutuları & Selectbox Tasarımı */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, div[data-baseweb="select"]>div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }

    /* Üst Arama / Filtreleme Paneli */
    .search-panel {
        background-color: #FFFFFF !important;
        padding: 16px !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 20px !important;
    }

    /* Professionally Styled Car Cards (Sixt / Avis Inspired) */
    .rental-card {
        background-color: #FFFFFF !important;
        padding: 18px !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05) !important;
        border: 1px solid #EDF2F7 !important;
        margin-bottom: 14px !important;
        position: relative;
    }

    .category-badge {
        font-size: 11px !important;
        font-weight: 800 !important;
        color: #64748B !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
    }

    .rating-badge {
        background-color: #FEF3C7 !important;
        color: #D97706 !important;
        font-weight: 700 !important;
        font-size: 12px !important;
        padding: 3px 8px !important;
        border-radius: 8px !important;
        float: right;
    }

    .car-name {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        margin: 4px 0 10px 0 !important;
    }

    /* Specs Pills Row */
    .specs-row {
        display: flex !important;
        gap: 6px !important;
        flex-wrap: wrap !important;
        margin-bottom: 12px !important;
    }

    .spec-pill {
        background-color: #F8FAFC !important;
        color: #475569 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        padding: 6px 10px !important;
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
    }

    .badge-guarantee {
        color: #059669 !important;
        background-color: #ECFDF5 !important;
        font-weight: 700 !important;
        font-size: 12px !important;
        padding: 4px 10px !important;
        border-radius: 8px !important;
        display: inline-block !important;
        margin-bottom: 12px !important;
    }

    /* Price Section */
    .price-container {
        border-top: 1px dashed #E2E8F0 !important;
        padding-top: 12px !important;
        margin-top: 8px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: flex-end !important;
    }

    .price-sub {
        font-size: 12px !important;
        color: #64748B !important;
        font-weight: 500 !important;
    }

    .price-main {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #2563EB !important;
    }

    .price-total-text {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
    }

    /* Sixt Style Vibrant Orange CTA Button */
    div.stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #FF6B00 0%, #FF5F00 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px !important;
        box-shadow: 0 4px 14px rgba(255, 95, 0, 0.35) !important;
        margin-top: 6px !important;
        transition: transform 0.1s ease !important;
    }

    div.stButton > button:active {
        transform: scale(0.98) !important;
    }

    /* Giriş Yap Form Butonu */
    div.stFormSubmitButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 14px !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }

    /* Tab Başlıkları */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
    }
    
    button[data-baseweb="tab"] p {
        font-size: 15px !important;
        font-weight: 800 !important;
        color: #475569 !important;
    }

    button[aria-selected="true"] p {
        color: #FF5F00 !important;
    }

    /* Sürücü Kartı Profil Stili */
    .driver-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        color: #FFFFFF !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15) !important;
        margin-top: 10px !important;
    }

    .driver-card div, .driver-card span, .driver-card p {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "rezervasyonlar.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Tarih", "Musteri", "TC", "Telefon", "Arac", "Gun", "ToplamTutar"])
    df.to_csv(DATA_FILE, index=False)

# PROFESYONEL ARAÇ FLOSU VERİLERİ
ARACLAR = [
    {
        "ad": "Peugeot 508", "kat": "SEDAN • PREMİUM", "vites": "Otomatik", 
        "yakit": "Dizel", "fiyat": 1500, "puan": "4.9", "koltuk": "5 Koltuk", 
        "bagaj": "2 Valiz", "foto": "🚘"
    },
    {
        "ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "vites": "Manuel", 
        "yakit": "Benzin", "fiyat": 900, "puan": "4.7", "koltuk": "5 Koltuk", 
        "bagaj": "1 Valiz", "foto": "🚗"
    },
    {
        "ad": "Ford Focus", "kat": "COMPACT • KONFOR", "vites": "Otomatik", 
        "yakit": "Benzin", "fiyat": 1200, "puan": "4.8", "koltuk": "5 Koltuk", 
        "bagaj": "2 Valiz", "foto": "🚙"
    },
    {
        "ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "vites": "Manuel", 
        "yakit": "Dizel", "fiyat": 850, "puan": "4.6", "koltuk": "5 Koltuk", 
        "bagaj": "2 Valiz", "foto": "🚕"
    },
    {
        "ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "vites": "Otomatik", 
        "yakit": "Elektrik", "fiyat": 2500, "puan": "5.0", "koltuk": "5 Koltuk", 
        "bagaj": "3 Valiz", "foto": "⚡"
    }
]

if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

# ==================== 1. GİRİŞ EKRANI ====================
if st.session_state['kullanici'] is None:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0 10px 0;">
            <span style="font-size: 42px;">🚗</span>
            <h1 style="font-size: 28px; font-weight: 900; margin-top: 8px; color: #0F172A !important;">DriveNow</h1>
            <p style="font-size: 14px; color: #64748B !important; font-weight: 600;">Hızlı ve Güvenilir Araç Kiralama</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("giris_formu"):
        ad = st.text_input("Ad Soyad", placeholder="Örn: Cihan Demir")
        tc = st.text_input("T.C. Kimlik No", max_chars=11, placeholder="11 Haneli T.C. No")
        tel = st.text_input("Telefon No", max_chars=10, placeholder="5XXXXXXXXX")
        submit = st.form_submit_button("ARAÇLARI SORGULA ➔")

        if submit:
            if ad and len(tc) == 11 and len(tel) == 10:
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                st.success("Giriş Başarılı!")
                st.rerun()
            else:
                st.error("Lütfen bilgileri eksiksiz girin (TC: 11 hane, Tel: 10 hane).")

# ==================== 2. ANA UYGULAMA ====================
else:
    # Üst Bilgi Barı
    col_user, col_logout = st.columns([3, 1])
    with col_user:
        st.markdown(f"👋 **Hoş Geldin, {st.session_state['kullanici']['ad']}**")
    with col_logout:
        if st.button("Çıkış"):
            st.session_state['kullanici'] = None
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["🚗 Araç Bul", "📋 Kiralamalarım", "👤 Sürücü Kartı"])

    # ---------- TAB 1: ARAÇ KİRALAMA EKRANI ----------
    with tab1:
        # Arama ve Filtreleme Paneli
        st.markdown('<div class="search-panel">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            vites_filtre = st.selectbox("Vites Tipi", ["Tümü", "Otomatik", "Manuel"])
        with c2:
            gun = st.number_input("Süre (Gün)", min_value=1, max_value=30, value=1)
        st.markdown('</div>', unsafe_allow_html=True)

        # Araç Kartları Listesi
        for arac in ARACLAR:
            if vites_filtre != "Tümü" and arac["vites"] != vites_filtre:
                continue

            toplam_fiyat = arac["fiyat"] * gun
            
            # Sixt / Avis İlhamlı Tasarım Kartı
            st.markdown(f"""
            <div class="rental-card">
                <div>
                    <span class="category-badge">{arac['kat']}</span>
                    <span class="rating-badge">★ {arac['puan']}</span>
                </div>
                <div class="car-name">{arac['foto']} {arac['ad']}</div>
                
                <div class="specs-row">
                    <span class="spec-pill">🔀 {arac['vites']}</span>
                    <span class="spec-pill">⛽ {arac['yakit']}</span>
                    <span class="spec-pill">👥 {arac['koltuk']}</span>
                    <span class="spec-pill">🧳 {arac['bagaj']}</span>
                </div>

                <div>
                    <span class="badge-guarantee">✓ Sınırsız KM & Ücretsiz İptal</span>
                </div>

                <div class="price-container">
                    <div>
                        <div class="price-sub">Günlük Fiyat</div>
                        <div class="price-main">{arac['fiyat']:,} ₺</div>
                    </div>
                    <div style="text-align: right;">
                        <div class="price-sub">{gun} Günlük Toplam</div>
                        <div class="price-total-text">{toplam_fiyat:,} ₺</div>
                    </div>
                </div>
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
                st.success(f"🎉 Rezervasyon Başarılı! {arac['ad']} ({gun} Gün) - {toplam_fiyat:,} ₺")

    # ---------- TAB 2: GEÇMİŞ KİRALAMALAR ----------
    with tab2:
        st.markdown("<h3 style='font-size: 18px; font-weight: 800;'>Kiralama Geçmişiniz</h3>", unsafe_allow_html=True)
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            user_df = df[df['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
            if not user_df.empty:
                for idx, row in user_df.iterrows():
                    st.markdown(f"""
                    <div class="rental-card" style="border-left: 5px solid #2563EB !important;">
                        <div style="font-size: 12px; color: #64748B; font-weight: 700;">REZERVASYON ONAYLANDI</div>
                        <div style="font-size: 18px; font-weight: 800; color: #0F172A; margin: 4px 0;">🚗 {row['Arac']}</div>
                        <div style="font-size: 13px; color: #475569; margin-bottom: 8px;">📅 İşlem Tarihi: {row['Tarih']}</div>
                        <div style="font-size: 14px; font-weight: 700; color: #2563EB;">
                            ⏱ {row['Gun']} Günlük Kiralama | 💰 Toplam: {row['ToplamTutar']:,} ₺
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Aktif veya geçmiş bir kiralamanız bulunmuyor.")

    # ---------- TAB 3: DİJİTAL SÜRÜCÜ KARTI ----------
    with tab3:
        st.markdown("<h3 style='font-size: 18px; font-weight: 800;'>Dijital Sürücü Profiliniz</h3>", unsafe_allow_html=True)
        k = st.session_state['kullanici']
        
        st.markdown(f"""
        <div class="driver-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <span style="font-size: 18px; font-weight: 900; letter-spacing: 1px;">DriveNow DRIVER</span>
                <span style="font-size: 22px;">💳</span>
            </div>
            <div style="margin-bottom: 12px;">
                <div style="font-size: 11px; text-transform: uppercase; opacity: 0.7;">Sürücü Ad Soyad</div>
                <div style="font-size: 18px; font-weight: 800;">{k['ad']}</div>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <div style="font-size: 11px; text-transform: uppercase; opacity: 0.7;">T.C. Kimlik No</div>
                    <div style="font-size: 14px; font-weight: 700;">{k['tc']}</div>
                </div>
                <div>
                    <div style="font-size: 11px; text-transform: uppercase; opacity: 0.7;">İletişim</div>
                    <div style="font-size: 14px; font-weight: 700;">+90 {k['tel']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
