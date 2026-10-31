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
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "vites": "Otomatik", "yakit": "Dizel", "fiyat": 1500, "puan": "4.9"},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "vites": "Manuel", "yakit": "Benzin", "fiyat": 900, "puan": "4.7"},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "vites": "Otomatik", "yakit": "Benzin", "fiyat": 1200, "puan": "4.8"},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "vites": "Manuel", "yakit": "Dizel", "fiyat": 850, "puan": "4.6"},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "vites": "Otomatik", "yakit": "Elektrik", "fiyat": 2500, "puan": "5.0"}
]

# --- KRİTİK GÖRÜNÜRLÜK AYARLARI (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F5F9 !important; }
    header, footer {visibility: hidden !important;}
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small, input {
        color: #0F172A !important;
        font-family: -apple-system, sans-serif !important;
    }
    input, div[data-baseweb="select"], .stNumberInput div {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
    }
    .car-card {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 22px !important;
        border: 2px solid #E2E8F0 !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
    }
    .car-title { font-size: 24px !important; font-weight: 900 !important; margin: 5px 0 !important; }
    .tag-item { display: inline-block; padding: 5px 10px; border-radius: 8px; font-size: 12px; font-weight: 800; margin-right: 5px; background: #F1F5F9; }
    .price-box { background-color: #F8FAFC !important; padding: 12px !important; border-radius: 14px; display: flex; justify-content: space-between; align-items: center; margin-top: 10px; }
    div.stButton > button {
        background: #FF6B00 !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        font-weight: 900 !important;
        height: 48px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.2) !important;
    }
    .vip-card { background: #1E293B !important; padding: 25px !important; border-radius: 20px; }
    .vip-card * { color: #FFFFFF !important; }
    div[data-baseweb="tab-list"] { background-color: #E2E8F0 !important; border-radius: 15px; padding: 4px; }
    div[aria-selected="true"] { background: #FFFFFF !important; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- VERİ DOSYASI KONTROLÜ (EXCEL DOSTU FORMAT) ---
DATA_FILE = "rezervasyonlar.csv"
def veriyi_kaydet(yeni_satir_df):
    if not os.path.exists(DATA_FILE):
        # İlk kez oluştururken Excel için BOM (utf-8-sig) ve noktalı virgül kullanıyoruz
        yeni_satir_df.to_csv(DATA_FILE, index=False, sep=';', encoding='utf-8-sig')
    else:
        # Üzerine eklerken aynı formatı koruyoruz
        yeni_satir_df.to_csv(DATA_FILE, mode='a', index=False, sep=';', encoding='utf-8-sig', header=False)

if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

# --- GİRİŞ EKRANI ---
if st.session_state['kullanici'] is None:
    st.markdown("<h1 style='text-align:center; font-weight:900;'>DriveNow</h1>", unsafe_allow_html=True)
    with st.form("giris_formu"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("TC Kimlik No", max_chars=11)
        tel = st.text_input("Telefon", max_chars=10)
        if st.form_submit_button("SİSTEME GİRİŞ YAP"):
            if ad and len(tc) == 11:
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                st.rerun()
else:
    tab1, tab2, tab3 = st.tabs(["🚗 ARAÇLAR", "📋 KAYITLARIM", "👤 PROFİL"])

    with tab1:
        st.markdown("<h4 style='font-weight:800;'>Müsait Araçlar</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            loc = st.selectbox("Teslimat", ["İstanbul HL", "Sabiha Gökçen HL", "Ankara HL", "İzmir HL"])
        with col2:
            days = st.number_input("Gün", min_value=1, value=1)

        for a in ARACLAR:
            total = a['fiyat'] * days
            st.markdown(f"""
            <div class="car-card">
                <div style="font-size:11px; font-weight:900; color:#2563EB;">{a['puan']} ★ {a['kat']}</div>
                <div class="car-title">{a['ad']}</div>
                <div style="margin: 10px 0;">
                    <span class="tag-item">🔀 {a['vites']}</span>
                    <span class="tag-item">⛽ {a['yakit']}</span>
                </div>
                <div class="price-box">
                    <div><small>GÜNLÜK</small><br><b>{a['fiyat']} ₺</b></div>
                    <div style="text-align:right;"><small style="color:#FF6B00;">TOPLAM</small><br><b style="font-size:20px;">{total} ₺</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Hemen Kirala: {a['ad']}", key=f"btn_{a['ad']}"):
                yeni_veri = pd.DataFrame([{
                    "Tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "Musteri": st.session_state['kullanici']['ad'],
                    "TC": st.session_state['kullanici']['tc'],
                    "Telefon": st.session_state['kullanici']['tel'],
                    "Konum": loc,
                    "Arac": a['ad'],
                    "Gun": days,
                    "ToplamTutar": total
                }])
                veriyi_kaydet(yeni_veri)
                st.success(f"Rezervasyon Tamamlandı!")

    with tab2:
        if os.path.exists(DATA_FILE):
            df_read = pd.read_csv(DATA_FILE, sep=';', encoding='utf-8-sig')
            user_recs = df_read[df_read['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
            if not user_recs.empty:
                for _, r in user_recs.iterrows():
                    st.markdown(f"""<div class="car-card"><b>{r['Arac']}</b><br><small>{r['Tarih']} | {r['Konum']}</small><br><div style="color:#059669; font-weight:900;">{r['ToplamTutar']} ₺</div></div>""", unsafe_allow_html=True)
            else:
                st.info("Kayıt bulunamadı.")

    with tab3:
        k = st.session_state['kullanici']
        st.markdown(f"""<div class="vip-card"><div style="font-size:10px; letter-spacing:2px; opacity:0.7;">VIP KART</div><div style="font-size:24px; font-weight:900; margin:15px 0;">{k['ad']}</div><div style="font-size:14px;">TC: {k['tc']}</div><div style="margin-top:20px; text-align:center; font-size:20px; letter-spacing:8px; opacity:0.5;">|| ||| | || ||||</div></div>""", unsafe_allow_html=True)
        
        st.write("---")
        if st.checkbox("Yönetici Panelini Aç"):
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "rb") as file:
                    st.download_button(
                        label="📥 TÜM VERİLERİ EXCEL OLARAK İNDİR",
                        data=file,
                        file_name="rezervasyonlar.csv",
                        mime="text/csv"
                    )
        
        if st.button("Çıkış Yap"):
            st.session_state['kullanici'] = None
            st.rerun()
