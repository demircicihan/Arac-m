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
    }
    .car-title { font-size: 24px !important; font-weight: 900 !important; }
    .tag-item { display: inline-block; padding: 5px 10px; border-radius: 8px; font-size: 12px; font-weight: 800; background: #F1F5F9; margin-right:5px;}
    div.stButton > button {
        background: #FF6B00 !important;
        color: white !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        width: 100% !important;
        height: 48px !important;
        border: none !important;
    }
    .vip-card { background: #1E293B !important; padding: 25px !important; border-radius: 20px; }
    .vip-card * { color: #FFFFFF !important; }
    div[data-baseweb="tab-list"] { background-color: #E2E8F0 !important; border-radius: 15px; padding: 4px; }
    div[aria-selected="true"] { background: #FFFFFF !important; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- VERİ DOSYASI KONTROLÜ VE TAMİRİ ---
DATA_FILE = "rezervasyonlar.csv"
COLUMNS = ["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"]

def dosyayi_yukle():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=COLUMNS)
    try:
        # Önce noktalı virgül ile dene
        df = pd.read_csv(DATA_FILE, sep=';', encoding='utf-8-sig')
        if 'TC' not in df.columns:
            # Sütun yoksa virgül ile dene
            df = pd.read_csv(DATA_FILE, sep=',', encoding='utf-8-sig')
        # Eğer hala sütunlar eksikse boşalt (tamir et)
        if 'TC' not in df.columns:
            return pd.DataFrame(columns=COLUMNS)
        return df
    except:
        return pd.DataFrame(columns=COLUMNS)

def veriyi_kaydet(yeni_satir_df):
    if not os.path.exists(DATA_FILE):
        yeni_satir_df.to_csv(DATA_FILE, index=False, sep=';', encoding='utf-8-sig')
    else:
        yeni_satir_df.to_csv(DATA_FILE, mode='a', index=False, sep=';', encoding='utf-8-sig', header=False)

# --- OTURUM YÖNETİMİ ---
if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

if st.session_state['kullanici'] is None:
    st.markdown("<h1 style='text-align:center; font-weight:900;'>DriveNow</h1>", unsafe_allow_html=True)
    with st.form("giris"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("TC No (11 Hane)", max_chars=11)
        tel = st.text_input("Telefon", max_chars=10)
        if st.form_submit_button("GİRİŞ YAP"):
            if ad and len(tc) == 11:
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                st.rerun()
else:
    tab1, tab2, tab3 = st.tabs(["🚗 ARAÇLAR", "📋 KAYITLARIM", "👤 PROFİL"])

    with tab1:
        st.markdown("<h4 style='font-weight:800;'>Müsait Araçlar</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            loc = st.selectbox("Teslimat", ["İstanbul HL", "Sabiha Gökçen HL", "Ankara HL", "İzmir HL"])
        with c2:
            days = st.number_input("Gün Sayısı", min_value=1, value=1)

        for a in ARACLAR:
            total = a['fiyat'] * days
            st.markdown(f"""
            <div class="car-card">
                <div style="font-size:11px; font-weight:900; color:#2563EB;">{a['puan']} ★</div>
                <div class="car-title">{a['ad']}</div>
                <div style="margin: 8px 0;">
                    <span class="tag-item">{a['vites']}</span>
                    <span class="tag-item">{a['yakit']}</span>
                </div>
                <div style="background:#F8FAFC; padding:10px; border-radius:12px; display:flex; justify-content:space-between;">
                    <div><small>GÜNLÜK</small><br><b>{a['fiyat']} ₺</b></div>
                    <div style="text-align:right;"><small style="color:#FF6B00;">TOPLAM</small><br><b>{total} ₺</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Kirala: {a['ad']}", key=f"krl_{a['ad']}"):
                yeni = pd.DataFrame([{
                    "Tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "Musteri": st.session_state['kullanici']['ad'],
                    "TC": st.session_state['kullanici']['tc'],
                    "Telefon": st.session_state['kullanici']['tel'],
                    "Konum": loc,
                    "Arac": a['ad'],
                    "Gun": days,
                    "ToplamTutar": total
                }])
                veriyi_kaydet(yeni)
                st.success("Rezervasyon Alındı!")

    with tab2:
        st.markdown("<h4 style='font-weight:800;'>Kayıtlarınız</h4>", unsafe_allow_html=True)
        df_read = dosyayi_yukle()
        if not df_read.empty:
            # TC sütununa göre filtrele (güvenli okuma)
            user_recs = df_read[df_read['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
            if not user_recs.empty:
                for _, r in user_recs.iterrows():
                    st.markdown(f"""<div class="car-card"><b>{r['Arac']}</b><br><small>{r['Tarih']} | {r['Konum']}</small><br><b>{r['ToplamTutar']} ₺</b></div>""", unsafe_allow_html=True)
            else:
                st.info("Henüz kaydınız yok.")
        else:
            st.info("Sistemde kayıtlı veri bulunamadı.")

    with tab3:
        k = st.session_state['kullanici']
        st.markdown(f"""<div class="vip-card"><div style="font-size:10px; opacity:0.7;">PREMIUM ÜYE</div><div style="font-size:24px; font-weight:900; margin:15px 0;">{k['ad']}</div><div style="font-size:14px;">TC: {k['tc']}</div><div style="margin-top:20px; text-align:center; font-size:20px; letter-spacing:8px; opacity:0.5;">|| ||| | || ||||</div></div>""", unsafe_allow_html=True)
        
        st.write("---")
        if st.checkbox("Yönetici Ayarları"):
            # Tüm dosyayı indir
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "rb") as f:
                    st.download_button("Excel/CSV Dosyasını İndir", f, "rezervasyonlar.csv", "text/csv")
            
            # Veritabanını Sıfırla (Eğer çok karışırsa)
            if st.button("VERİTABANINI SIFIRLA (DİKKAT!)"):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                    st.warning("Dosya silindi, sayfayı yenileyin.")

        if st.button("Çıkış Yap"):
            st.session_state['kullanici'] = None
            st.rerun()
