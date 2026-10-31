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

# ULTRA MODERN CANLI RENKLİ iOS GLASSMORPHISM CSS
st.markdown("""
    <style>
    /* Arka Plan Degradesi */
    .stApp {
        background: linear-gradient(160deg, #E0E7FF 0%, #EEF2FF 40%, #F8FAFC 100%) !important;
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

    /* iOS Segmented Control Sekme Menüsü */
    div[data-baseweb="tab-list"] {
        background-color: rgba(199, 210, 254, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 20px !important;
        padding: 6px !important;
        gap: 4px !important;
        margin-bottom: 20px !important;
        border: 1px solid rgba(255,255,255,0.8) !important;
    }
    div[data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 14px !important;
        padding: 10px 16px !important;
        border: none !important;
        margin: 0 !important;
    }
    div[aria-selected="true"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%) !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.15) !important;
    }
    div[aria-selected="true"] p {
        color: #2563EB !important;
        font-weight: 900 !important;
    }
    div[aria-selected="false"] p {
        color: #475569 !important;
        font-weight: 700 !important;
    }

    .hero-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        padding: 24px 20px !important;
        border-radius: 24px !important;
        color: #FFFFFF !important;
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.22) !important;
        margin-bottom: 20px !important;
        position: relative;
        overflow: hidden;
    }

    .status-badge {
        background: rgba(255, 255, 255, 0.18) !important;
        backdrop-filter: blur(10px) !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        display: inline-block !important;
        margin-bottom: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: #FFFFFF !important;
    }

    /* RENKLENDİRİLMİŞ ARAMA PANANELİ */
    .search-glass {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(238,242,255,0.95) 100%) !important;
        backdrop-filter: blur(16px) !important;
        padding: 20px !important;
        border-radius: 24px !important;
        border: 1.5px solid #C7D2FE !important;
        box-shadow: 0 12px 35px rgba(37, 99, 235, 0.1) !important;
        margin-bottom: 20px !important;
    }

    /* RENKLENDİRİLMİŞ ÖZEL LÜKS ARAÇ KARTI (Düz beyaz yerine canlı geçiş) */
    .car-card-modern {
        background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 60%, #EEF2FF 100%) !important;
        padding: 22px !important;
        border-radius: 26px !important;
        box-shadow: 0 14px 35px rgba(30, 27, 75, 0.07) !important;
        border: 1.5px solid #E0E7FF !important;
        margin-bottom: 18px !important;
    }

    /* RENKLİ AVATAR KUTUSU */
    .car-avatar-container {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 16px;
        padding-bottom: 14px;
        border-bottom: 1.5px solid #E2E8F0;
    }
    .car-avatar {
        font-size: 38px;
        background: linear-gradient(135deg, #E0E7FF 0%, #C7D2FE 100%);
        width: 72px;
        height: 72px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 22px;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.15);
        border: 1px solid #A5B4FC;
    }

    .car-cat {
        font-size: 11px !important;
        font-weight: 900 !important;
        color: #2563EB !important;
        letter-spacing: 1px !important;
        text-transform: uppercase;
    }

    .rating-pill {
        background: #FEF3C7 !important;
        color: #B45309 !important;
        font-weight: 900 !important;
        font-size: 12px !important;
        padding: 4px 10px !important;
        border-radius: 12px !important;
        border: 1px solid #FDE68A;
        display: inline-block;
        margin-top: 4px;
    }

    .car-title-text {
        font-size: 21px !important;
        font-weight: 900 !important;
        color: #0F172A !important;
        margin-bottom: 2px !important;
    }

    /* RENKLİ ÖZEL ROZETLER (PASTEL TAGS) */
    .pill-box {
        display: flex !important;
        gap: 8px !important;
        flex-wrap: wrap !important;
        margin-bottom: 14px !important;
    }

    .tag-vites {
        background: #EFF6FF !important;
        color: #1D4ED8 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        padding: 6px 12px !important;
        border-radius: 10px !important;
        border: 1px solid #BFDBFE !important;
    }

    .tag-yakit {
        background: #FEF3C7 !important;
        color: #B45309 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        padding: 6px 12px !important;
        border-radius: 10px !important;
        border: 1px solid #FDE68A !important;
    }

    .tag-koltuk {
        background: #F3E8FF !important;
        color: #6B21A8 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        padding: 6px 12px !important;
        border-radius: 10px !important;
        border: 1px solid #E9D5FF !important;
    }

    .tag-bagaj {
        background: #ECFDF5 !important;
        color: #047857 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        padding: 6px 12px !important;
        border-radius: 10px !important;
        border: 1px solid #A7F3D0 !important;
    }

    .guarantee-tag {
        color: #047857 !important;
        background: #D1FAE5 !important;
        font-weight: 800 !important;
        font-size: 12px !important;
        padding: 6px 12px !important;
        border-radius: 10px !important;
        display: inline-flex !important;
        align-items: center;
        gap: 4px;
        margin-bottom: 14px !important;
        border: 1px solid #6EE7B7;
    }

    /* RENKLİ FİYAT KUTUSU (SAFİR MAVİSİ ŞERİT) */
    .price-row {
        background: linear-gradient(135deg, #EFF6FF 0%, #E0E7FF 100%) !important;
        padding: 14px 18px !important;
        border-radius: 18px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        border: 1px solid #BFDBFE !important;
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
        box-shadow: 0 8px 25px rgba(255, 95, 0, 0.35) !important;
        margin-top: 12px !important;
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
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.35) !important;
    }

    .stTextInput>div>div>input, .stNumberInput>div>div>input, div[data-baseweb="select"]>div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border-radius: 14px !important;
        border: 1.5px solid #C7D2FE !important;
        font-weight: 800 !important;
        padding: 10px !important;
    }
    
    .trust-badges {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-top: 16px;
        flex-wrap: wrap;
    }
    .trust-pill {
        background-color: #E2E8F0;
        color: #334155;
        font-size: 11px;
        font-weight: 800;
        padding: 6px 12px;
        border-radius: 20px;
    }
    
    .wallet-barcode {
        font-size: 26px;
        letter-spacing: 3px;
        color: #FFFFFF;
        opacity: 0.6;
        text-align: center;
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px dashed rgba(255,255,255,0.2);
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

ARACLAR = [
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "vites": "Otomatik", "yakit": "Dizel", "fiyat": 1500, "puan": "4.9", "koltuk": "5 Koltuk", "bagaj": "2 Valiz", "ikon": "🚘"},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "vites": "Manuel", "yakit": "Benzin", "fiyat": 900, "puan": "4.7", "koltuk": "5 Koltuk", "bagaj": "1 Valiz", "ikon": "🚗"},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "vites": "Otomatik", "yakit": "Benzin", "fiyat": 1200, "puan": "4.8", "koltuk": "5 Koltuk", "bagaj": "2 Valiz", "ikon": "🚙"},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "vites": "Manuel", "yakit": "Dizel", "fiyat": 850, "puan": "4.6", "koltuk": "5 Koltuk", "bagaj": "2 Valiz", "ikon": "🚕"},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "vites": "Otomatik", "yakit": "Elektrik", "fiyat": 2500, "puan": "5.0", "koltuk": "5 Koltuk", "bagaj": "3 Valiz", "ikon": "⚡"}
]

if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

# ==================== 1. GİRİŞ EKRANI ====================
if st.session_state['kullanici'] is None:
    hero_html = """<div class="hero-header" style="text-align: center;"><div class="status-badge">📍 Türkiye Geneli 7/24 Hizmet</div><h1 style="font-size: 34px; font-weight: 900; margin: 4px 0; color: #FFF;">DriveNow</h1><p style="font-size: 15px; opacity: 0.9; color: #FFF;">Premium & Ekonomik Araç Kiralama</p></div>"""
    st.markdown(hero_html, unsafe_allow_html=True)

    with st.form("giris_formu"):
        st.markdown("<p style='font-size: 18px; font-weight: 800; margin-bottom: 10px;'>👋 Sisteme Giriş Yapın</p>", unsafe_allow_html=True)
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
    
    trust_html = """<div class="trust-badges"><span class="trust-pill">⚡ Anında Onay</span><span class="trust-pill">🛡️ Tam Kasko</span><span class="trust-pill">🚫 Gizli Ücret Yok</span></div>"""
    st.markdown(trust_html, unsafe_allow_html=True)

# ==================== 2. ANA UYGULAMA ====================
else:
    col_user, col_logout = st.columns([3, 1])
    with col_user:
        st.markdown(f"<div style='font-size: 18px; font-weight: 900; color: #0F172A; padding-top: 8px;'>👋 Merhaba, {st.session_state['kullanici']['ad']}</div>", unsafe_allow_html=True)
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
            
            # RENKLENDİRİLMİŞ CANLI KART HTML YAPISI
            card_html = f"""<div class="car-card-modern"><div class="car-avatar-container"><div class="car-avatar">{arac['ikon']}</div><div><div class="car-title-text">{arac['ad']}</div><div class="car-cat">{arac['kat']}</div><div class="rating-pill">★ {arac['puan']} Müşteri Puanı</div></div></div><div class="pill-box"><span class="tag-vites">🔀 {arac['vites']}</span><span class="tag-yakit">⛽ {arac['yakit']}</span><span class="tag-koltuk">👥 {arac['koltuk']}</span><span class="tag-bagaj">🧳 {arac['bagaj']}</span></div><div><span class="guarantee-tag">✓ Sınırsız KM & Ücretsiz İptal Güvencesi</span></div><div class="price-row"><div><div style="font-size: 11px; color: #475569; font-weight: 800;">GÜNLÜK ÜCRET</div><div style="font-size: 18px; font-weight: 900; color: #2563EB;">{arac['fiyat']:,} ₺</div></div><div style="text-align: right;"><div style="font-size: 11px; color: #475569; font-weight: 800;">{gun} GÜNLÜK TOPLAM</div><div style="font-size: 20px; font-weight: 900; color: #0F172A;">{toplam_fiyat:,} ₺</div></div></div></div>"""
            
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
        st.markdown("<h3 style='font-size: 20px; font-weight: 900; margin-bottom: 16px;'>Geçmiş Rezervasyonlar</h3>", unsafe_allow_html=True)
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            user_df = df[df['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
            if not user_df.empty:
                for idx, row in user_df.iterrows():
                    konum_yazisi = row['Konum'] if 'Konum' in df.columns else "İstanbul • Sabiha Gökçen HL"
                    
                    rec_html = f"""<div class="car-card-modern" style="border-left: 8px solid #059669 !important;"><div style="display: flex; justify-content: space-between; align-items: center;"><div style="font-size: 12px; color: #059669; font-weight: 900; background: #D1FAE5; padding: 4px 8px; border-radius: 8px;">✓ ONAYLANDI</div><div style="font-size: 12px; color: #64748B; font-weight: 700;">📅 {row['Tarih']}</div></div><div style="font-size: 20px; font-weight: 900; color: #0F172A; margin: 12px 0 4px 0;">🚗 {row['Arac']}</div><div style="font-size: 13px; color: #475569; font-weight: 600; margin-bottom: 12px;">📍 {konum_yazisi}</div><div class="price-row" style="padding: 10px !important;"><div style="font-size: 14px; font-weight: 800; color: #64748B;">⏱ {row['Gun']} Günlük Kiralama</div><div style="font-size: 16px; font-weight: 900; color: #0F172A;">💰 {row['ToplamTutar']:,} ₺</div></div></div>"""
                    st.markdown(rec_html, unsafe_allow_html=True)
            else:
                st.info("Aktif veya geçmiş bir kiralamanız bulunmuyor.")

    # ---------- TAB 3: DİJİTAL SÜRÜCÜ KARTI ----------
    with tab3:
        k = st.session_state['kullanici']
        card_driver = f"""<div class="hero-header" style="padding: 24px !important;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;"><span style="font-size: 14px; font-weight: 900; letter-spacing: 2px; color:#93C5FD; background: rgba(255,255,255,0.1); padding: 6px 12px; border-radius: 20px;">DRIVENOW PREMIUM</span><span style="font-size: 28px; background: #FFF; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">💎</span></div><div style="margin-bottom: 20px;"><div style="font-size: 11px; font-weight: 800; opacity: 0.7; color:#FFF; letter-spacing: 1px;">SÜRÜCÜ AD SOYAD</div><div style="font-size: 24px; font-weight: 900; color:#FFF; text-transform: uppercase;">{k['ad']}</div></div><div style="display: flex; justify-content: space-between; background: rgba(0,0,0,0.2); padding: 16px; border-radius: 16px;"><div><div style="font-size: 11px; font-weight: 800; opacity: 0.7; color:#FFF; letter-spacing: 1px;">T.C. KİMLİK NO</div><div style="font-size: 16px; font-weight: 800; color:#FFF;">{k['tc']}</div></div><div><div style="font-size: 11px; opacity: 0.7; color:#FFF;">TELEFON</div><div style="font-size: 16px; font-weight: 800; color:#FFF;">+90 {k['tel']}</div></div></div><div class="wallet-barcode">||| |||| || ||| || |||| |</div></div>"""
        st.markdown(card_driver, unsafe_allow_html=True)
