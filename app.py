import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Sayfa Ayarları
st.set_page_config(
    page_title="DriveNow Premium",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ULTRA MODERN iOS GLASSMORPHISM & GRADIENT CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #E0E7FF 0%, #F1F5F9 35%, #F8FAFC 100%) !important;
        background-attachment: fixed !important;
    }
    
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stDeployButton {display:none !important;}

    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span {
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", Roboto, sans-serif !important;
    }

    .hero-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        padding: 22px 20px !important;
        border-radius: 24px !important;
        color: #FFFFFF !important;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.18) !important;
        margin-bottom: 20px !important;
    }
    
    .hero-header h1, .hero-header p, .hero-header span {
        color: #FFFFFF !important;
    }

    .status-badge {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        padding: 4px 12px !important;
        border-radius: 20px !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        display: inline-block !important;
        margin-bottom: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    .search-glass {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        padding: 16px !important;
        border-radius: 22px !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.08) !important;
        margin-bottom: 20px !important;
    }

    /* MODERN SADE ARAÇ KARTI TASARIMI (FOTOĞRAFSIZ) */
    .car-card-modern {
        background-color: #FFFFFF !important;
        padding: 18px !important;
        border-radius: 24px !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06) !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 12px !important;
    }

    .car-cat {
        font-size: 11px !important;
        font-weight: 800 !important;
        color: #2563EB !important;
        letter-spacing: 1px !important;
    }

    .rating-pill {
        background: #FEF3C7 !important;
        color: #D97706 !important;
        font-weight: 800 !important;
        font-size: 12px !important;
        padding: 4px 10px !important;
        border-radius: 10px !important;
    }

    .car-title-text {
        font-size: 20px !important;
        font-weight: 900 !important;
        color: #0F172A !important;
        margin: 4px 0 8px 0 !important;
    }

    .pill-box {
        display: flex !important;
        gap: 6px !important;
        flex-wrap: wrap !important;
        margin-bottom: 10px !important;
    }

    .tag-item {
        background: #F1F5F9 !important;
        color: #334155 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        padding: 5px 10px !important;
        border-radius: 8px !important;
    }

    .guarantee-tag {
        color: #059669 !important;
        background: #ECFDF5 !important;
        font-weight: 700 !important;
        font-size: 11px !important;
        padding: 4px 8px !important;
        border-radius: 6px !important;
        display: inline-block !important;
        margin-bottom: 8px !important;
    }

    .price-row {
        border-top: 1px dashed #E2E8F0 !important;
        padding-top: 10px !important;
        margin-top: 6px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
    }

    div.stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #FF6B00 0%, #FF5F00 100%) !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        border-radius: 16px !important;
        border: none !important;
        padding: 14px !important;
        box-shadow: 0 6px 20px rgba(255, 95, 0, 0.35) !important;
        margin-bottom: 16px !important;
    }

    div.stFormSubmitButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        border-radius: 16px !important;
        border: none !important;
        padding: 14px !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35) !important;
    }

    .stTextInput>div>div>input, .stNumberInput>div>div>input, div[data-baseweb="select"]>div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border-radius: 12px !important;
        border: 1px solid #CBD5E1 !important;
        font-weight: 700 !important;
    }
    
    button[data-baseweb="tab"] p {
        font-size: 15px !important;
        font-weight: 800 !important;
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "rezervasyonlar.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)
    if 'Konum' not in df.columns:
        df['Konum'] = "İstanbul • Sabiha Gökçen HL"
        df.to_csv(DATA_FILE, index=False)

# ARAÇ FLOSU (FOTOĞRAFSIZ)
ARACLAR = [
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "vites": "Otomatik", "yakit": "Dizel", "fiyat": 1500, "puan": "4.9", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "vites": "Manuel", "yakit": "Benzin", "fiyat": 900, "puan": "4.7", "koltuk": "5 Koltuk", "bagaj": "1 Valiz"},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "vites": "Otomatik", "yakit": "Benzin", "fiyat": 1200, "puan": "4.8", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "vites": "Manuel", "yakit": "Dizel", "fiyat": 850, "puan": "4.6", "koltuk": "5 Koltuk", "bagaj": "2 Valiz"},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "vites": "Otomatik", "yakit": "Elektrik", "fiyat": 2500, "puan": "5.0", "koltuk": "5 Koltuk", "bagaj": "3 Valiz"}
]

if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

# ==================== 1. GİRİŞ EKRANI ====================
if st.session_state['kullanici'] is None:
    st.markdown("""<div class="hero-header" style="text-align: center;"><div class="status-badge">📍 Türkiye Geneli 7/24 Hizmet</div><h1 style="font-size: 32px; font-weight: 900; margin: 4px 0;">DriveNow</h1><p style="font-size: 14px; opacity: 0.8;">Lüks & Ekonomik Araç Kiralama</p></div>""", unsafe_allow_html=True)

    with st.form("giris_formu"):
        ad = st.text_input("Ad Soyad", placeholder="Örn: Cihan Demir")
        tc = st.text_input("T.C. Kimlik No", max_chars=11, placeholder="11 Haneli T.C. No")
        tel = st.text_input("Telefon No", max_chars=10, placeholder="5XXXXXXXXX")
        submit = st.form_submit_button("ARAÇLARI LİSTELE ➔")

        if submit:
            if ad and len(tc) == 11 and len(tel) == 10:
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                st.success("Giriş Başarılı!")
                st.rerun()
            else:
                st.error("Lütfen bilgileri eksiksiz girin (TC: 11 hane, Tel: 10 hane).")

# ==================== 2. ANA UYGULAMA ====================
else:
    col_user, col_logout = st.columns([3, 1])
    with col_user:
        st.markdown(f"👋 **{st.session_state['kullanici']['ad']}**")
    with col_logout:
        if st.button("Çıkış"):
            st.session_state['kullanici'] = None
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["🚗 Araç Bul", "📋 Kiralamalarım", "👤 Sürücü Kartı"])

    # ---------- TAB 1: ARAÇ KİRALAMA EKRANI ----------
    with tab1:
        st.markdown('<div class="search-glass">', unsafe_allow_html=True)
        secilen_konum = st.selectbox("📍 Alış ve Teslim Noktası", [
            "İstanbul • Sabiha Gökçen HL",
            "İstanbul • İstanbul Havalimanı",
            "Ankara • Esenboğa HL",
            "İzmir • Adnan Menderes HL",
            "Antalya • Havalimanı",
            "Muğla • Dalaman HL",
            "Bursa • Şehir Merkezi"
        ])
        
        c1, c2 = st.columns(2)
        with c1:
            vites_filtre = st.selectbox("🔀 Vites Tipi", ["Tümü", "Otomatik", "Manuel"])
        with c2:
            gun = st.number_input("⏱ Süre (Gün)", min_value=1, max_value=30, value=1)
        st.markdown('</div>', unsafe_allow_html=True)

        for arac in ARACLAR:
            if vites_filtre != "Tümü" and arac["vites"] != vites_filtre:
                continue

            toplam_fiyat = arac["fiyat"] * gun
            
            # SADE VE FOTOĞRAFSIZ KART YAPISI
            card_html = f"""<div class="car-card-modern"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;"><span class="car-cat">{arac['kat']}</span><span class="rating-pill">★ {arac['puan']}</span></div><div class="car-title-text">{arac['ad']}</div><div class="pill-box"><span class="tag-item">🔀 {arac['vites']}</span><span class="tag-item">⛽ {arac['yakit']}</span><span class="tag-item">👥 {arac['koltuk']}</span><span class="tag-item">🧳 {arac['bagaj']}</span></div><div><span class="guarantee-tag">✓ Sınırsız KM & Ücretsiz İptal</span></div><div class="price-row"><div><div style="font-size: 10px; color: #64748B; font-weight: 700;">GÜNLÜK</div><div style="font-size: 17px; font-weight: 800; color: #2563EB;">{arac['fiyat']:,} ₺</div></div><div style="text-align: right;"><div style="font-size: 10px; color: #64748B; font-weight: 700;">{gun} GÜNLÜK TOPLAM</div><div style="font-size: 17px; font-weight: 900; color: #0F172A;">{toplam_fiyat:,} ₺</div></div></div></div>"""
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            if st.button(f"Hemen Kirala - {arac['ad']}", key=arac['ad']):
                yeni_kayit = pd.DataFrame([{
                    "Tarih": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Musteri": st.session_state['kullanici']['ad'],
                    "TC": st.session_state['kullanici']['tc'],
                    "Telefon": st.session_state['kullanici']['tel'],
                    "Konum": secilen_konum,
                    "Arac": arac['ad'],
                    "Gun": gun,
                    "ToplamTutar": toplam_fiyat
                }])
                yeni_kayit.to_csv(DATA_FILE, mode='a', header=False, index=False)
                st.balloons()
                st.success(f"🎉 Rezervasyon Başarılı! {arac['ad']} ({secilen_konum}) - {toplam_fiyat:,} ₺")

    # ---------- TAB 2: GEÇMİŞ KİRALAMALAR ----------
    with tab2:
        st.markdown("<h3 style='font-size: 18px; font-weight: 800;'>Kiralama Geçmişiniz</h3>", unsafe_allow_html=True)
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            user_df = df[df['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
            if not user_df.empty:
                for idx, row in user_df.iterrows():
                    konum_yazisi = row['Konum'] if 'Konum' in df.columns else "İstanbul • Sabiha Gökçen HL"
                    
                    rec_html = f"""<div class="car-card-modern" style="border-left: 6px solid #2563EB !important;"><div style="font-size: 11px; color: #2563EB; font-weight: 800;">REZERVASYON ONAYLANDI</div><div style="font-size: 18px; font-weight: 900; color: #0F172A; margin: 4px 0;">🚗 {row['Arac']}</div><div style="font-size: 12px; color: #64748B; margin-bottom: 8px;">📍 {konum_yazisi} &nbsp;|&nbsp; 📅 {row['Tarih']}</div><div style="font-size: 14px; font-weight: 800; color: #0F172A;">⏱ {row['Gun']} Günlük | 💰 Toplam: {row['ToplamTutar']:,} ₺</div></div>"""
                    st.markdown(rec_html, unsafe_allow_html=True)
            else:
                st.info("Aktif veya geçmiş bir kiralamanız bulunmuyor.")

    # ---------- TAB 3: DİJİTAL SÜRÜCÜ KARTI ----------
    with tab3:
        k = st.session_state['kullanici']
        card_driver = f"""<div class="hero-header"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;"><span style="font-size: 16px; font-weight: 900; letter-spacing: 1px; color:#FFF;">DriveNow VIP</span><span style="font-size: 22px;">💳</span></div><div style="margin-bottom: 12px;"><div style="font-size: 11px; opacity: 0.7; color:#FFF;">SÜRÜCÜ AD SOYAD</div><div style="font-size: 20px; font-weight: 900; color:#FFF;">{k['ad']}</div></div><div style="display: flex; justify-content: space-between;"><div><div style="font-size: 11px; opacity: 0.7; color:#FFF;">T.C. KİMLİK NO</div><div style="font-size: 14px; font-weight: 700; color:#FFF;">{k['tc']}</div></div><div><div style="font-size: 11px; opacity: 0.7; color:#FFF;">TELEFON</div><div style="font-size: 14px; font-weight: 700; color:#FFF;">+90 {k['tel']}</div></div></div></div>"""
        st.markdown(card_driver, unsafe_allow_html=True)
