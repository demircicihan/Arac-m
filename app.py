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

# --- TASARIM (YÜKSEK KONTRASTLI CSS) ---
st.markdown("""
    <style>
    /* Arka plan */
    .stApp { background: linear-gradient(160deg, #E2E8F0 0%, #F8FAFC 100%) !important; }
    
    /* GİZLENECEK ALANLAR */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    /* TÜM METİNLERİ NETLEŞTİR (KOYU LACİVERT) */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div {
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
    }

    /* Input ve Selectbox yazılarını netleştir */
    input, select, textarea {
        color: #0F172A !important;
        font-weight: 700 !important;
    }

    /* Tab Menüsü Tasarımı */
    div[data-baseweb="tab-list"] {
        background-color: #CBD5E1 !important;
        border-radius: 15px !important;
        padding: 5px !important;
        margin-bottom: 20px;
    }
    div[aria-selected="true"] {
        background: #FFFFFF !important;
        border-radius: 12px !important;
    }
    div[aria-selected="true"] p {
        color: #2563EB !important;
        font-weight: 900 !important;
    }

    /* Araç Kartları */
    .car-card-modern {
        background: #FFFFFF !important;
        padding: 24px !important;
        border-radius: 24px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
        border: 2px solid #CBD5E1 !important;
        margin-bottom: 20px !important;
    }

    /* Renkli Tagler (Yazıları kalın ve koyu) */
    .tag-vites { background: #DBEAFE !important; color: #1E40AF !important; padding: 6px 12px; border-radius: 8px; font-weight: 900; font-size: 13px; margin-right: 6px; border: 1px solid #BFDBFE; }
    .tag-yakit { background: #FEF3C7 !important; color: #92400E !important; padding: 6px 12px; border-radius: 8px; font-weight: 900; font-size: 13px; margin-right: 6px; border: 1px solid #FDE68A; }
    .tag-koltuk { background: #F3E8FF !important; color: #6B21A8 !important; padding: 6px 12px; border-radius: 8px; font-weight: 900; font-size: 13px; border: 1px solid #E9D5FF; }

    /* Fiyat Alanı */
    .price-row {
        background: #F1F5F9 !important;
        padding: 16px !important;
        border-radius: 18px !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 15px;
        border: 1px solid #E2E8F0;
    }

    /* Buton Tasarımı */
    div.stButton > button {
        background: #FF6B00 !important;
        color: #FFFFFF !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        height: 54px !important;
        width: 100% !important;
        box-shadow: 0 6px 15px rgba(255, 107, 0, 0.3) !important;
        margin-top: 5px;
    }
    
    /* Input kutuları */
    .stTextInput>div>div>input {
        background-color: white !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
        height: 45px !important;
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
    st.markdown('<div style="text-align: center; padding: 30px 10px;"><h1 style="font-weight: 900; font-size: 46px; color: #0F172A !important;">DriveNow</h1><p style="font-weight: 800; color: #475569 !important;">Premium Araç Kiralama</p></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div style='background: white; padding: 25px; border-radius: 20px; border: 2px solid #CBD5E1;'>", unsafe_allow_html=True)
        with st.form("giris"):
            ad = st.text_input("Ad Soyad")
            tc = st.text_input("TC Kimlik No (11 Hane)", max_chars=11)
            tel = st.text_input("Telefon (5xx)", max_chars=10)
            if st.form_submit_button("SİSTEME GİRİŞ YAP"):
                if ad and len(tc) == 11:
                    st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # Sekmeler
    tab1, tab2, tab3 = st.tabs(["🚗 ARAÇLAR", "📋 KİRALAMALARIM", "👤 PROFİL"])

    with tab1:
        st.markdown("<h3 style='font-weight: 900; margin-bottom: 20px;'>Müsait Araçlar</h3>", unsafe_allow_html=True)
        
        # Filtre Alanı
        col1, col2 = st.columns(2)
        with col1:
            konum = st.selectbox("Alış Noktası", ["İstanbul Havalimanı", "Sabiha Gökçen HL", "Ankara Esenboğa HL", "İzmir Adnan Menderes HL"])
        with col2:
            gun = st.number_input("Gün Sayısı", min_value=1, value=1)

        for arac in ARACLAR:
            total = arac['fiyat'] * gun
            card_html = f"""
            <div class="car-card-modern">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-size: 12px; font-weight: 900; color: #2563EB;">{arac['kat']}</span>
                    <span style="background: #FEF3C7; color: #92400E; padding: 2px 8px; border-radius: 6px; font-weight: 900;">★ {arac['puan']}</span>
                </div>
                <div style="font-size: 26px; font-weight: 900; margin: 8px 0;">{arac['ad']}</div>
                <div style="margin: 15px 0;">
                    <span class="tag-vites">{arac['vites']}</span>
                    <span class="tag-yakit">{arac['yakit']}</span>
                    <span class="tag-koltuk">{arac['koltuk']}</span>
                </div>
                <div class="price-row">
                    <div>
                        <div style="font-size: 11px; font-weight: 800; color: #64748B;">GÜNLÜK</div>
                        <div style="font-size: 20px; font-weight: 900;">{arac['fiyat']} ₺</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 11px; font-weight: 800; color: #64748B;">TOPLAM</div>
                        <div style="font-size: 22px; font-weight: 900; color: #FF6B00;">{total} ₺</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            if st.button(f"HEMEN KİRALA: {arac['ad']}", key=arac['ad']):
                yeni = pd.DataFrame([[datetime.now().strftime("%d.%m.%Y"), st.session_state['kullanici']['ad'], st.session_state['kullanici']['tc'], st.session_state['kullanici']['tel'], konum, arac['ad'], gun, total]], 
                                    columns=["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"])
                yeni.to_csv(DATA_FILE, mode='a', header=False, index=False)
                st.success(f"Rezervasyon Tamamlandı: {arac['ad']}")

    with tab2:
        st.markdown("<h3 style='font-weight: 900;'>Geçmiş Kiralamalar</h3>", unsafe_allow_html=True)
        df = pd.read_csv(DATA_FILE)
        user_df = df[df['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
        
        if not user_df.empty:
            for _, row in user_df.iterrows():
                st.markdown(f"""
                <div style="background: white; padding: 20px; border-radius: 20px; border: 2px solid #CBD5E1; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-weight: 900; font-size: 20px;">{row['Arac']}</div>
                        <div style="color: #059669; font-weight: 900;">ONAYLANDI</div>
                    </div>
                    <div style="font-size: 14px; font-weight: 700; color: #475569; margin-top: 5px;">{row['Tarih']} • {row['Konum']}</div>
                    <div style="margin-top: 10px; font-size: 18px; font-weight: 900;">{row['ToplamTutar']} ₺</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Henüz bir arac kiralamadınız.")

    with tab3:
        k = st.session_state['kullanici']
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 35px 25px; border-radius: 25px; box-shadow: 0 15px 30px rgba(0,0,0,0.3);">
            <div style="color: #94A3B8 !important; font-size: 12px; font-weight: 900; letter-spacing: 2px;">DRIVENOW VIP CARD</div>
            <div style="color: #FFFFFF !important; font-size: 28px; font-weight: 900; margin: 20px 0;">{k['ad']}</div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.2);">
                <div style="color: #FFFFFF !important; font-weight: 700;">TC: {k['tc']}</div>
                <div style="color: #FFFFFF !important; font-weight: 700;">TEL: +90 {k['tel']}</div>
            </div>
            <div style="margin-top: 30px; border-top: 1px dashed rgba(255,255,255,0.4); padding-top: 20px; text-align: center; color: white !important; font-size: 24px; letter-spacing: 6px;">
                ||| || |||| || |||
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("ÇIKIŞ YAP"):
            st.session_state['kullanici'] = None
            st.rerun()
