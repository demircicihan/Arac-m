import streamlit as st
import pandas as pd
from datetime import datetime
import os
import io

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

# --- YÜKSEK KONTRASTLI VE MOBİL UYUMLU CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #F1F5F9 !important; }
    header, footer {visibility: hidden !important;}

    /* TÜM YAZILAR KOYU LACİVERT */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small, input {
        color: #0F172A !important;
        font-family: -apple-system, sans-serif !important;
    }

    /* KUTULAR VE GİRDİ ALANLARI */
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
        box-shadow: 0 4px 10px rgba(0,0,0,0.04) !important;
    }

    .car-title { font-size: 24px !important; font-weight: 900 !important; margin: 5px 0 !important; }

    .tag-item {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 800;
        background: #F1F5F9;
        margin-right: 5px;
    }

    div.stButton > button {
        background: #FF6B00 !important;
        color: white !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        width: 100% !important;
        height: 48px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.25) !important;
    }

    .vip-card { background: #1E293B !important; padding: 25px !important; border-radius: 20px; }
    .vip-card * { color: #FFFFFF !important; }

    div[data-baseweb="tab-list"] { background-color: #E2E8F0 !important; border-radius: 15px; padding: 4px; }
    div[aria-selected="true"] { background: #FFFFFF !important; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- STANDART VERİTABANI YÖNETİMİ ---
DATA_FILE = "rezervasyonlar.csv"
COLUMNS = ["Tarih", "Musteri", "TC", "Telefon", "Konum", "Arac", "Gun", "ToplamTutar"]

def veritabanini_oku_ve_duzelt():
    """Bozuk veya eski formattaki dosyayı otomatik olarak tespit eder, temizler ve duzeltir."""
    if not os.path.exists(DATA_FILE):
        df_empty = pd.DataFrame(columns=COLUMNS)
        df_empty.to_csv(DATA_FILE, index=False, sep=';', encoding='utf-8-sig')
        return df_empty

    try:
        # Öncelik: Noktalı virgül ile oku
        df = pd.read_csv(DATA_FILE, sep=';', encoding='utf-8-sig')
        if 'TC' not in df.columns:
            # Virgül ile oku
            df = pd.read_csv(DATA_FILE, sep=',', encoding='utf-8-sig')
        if 'TC' not in df.columns:
            # Otomatik ayırıcı denemesi
            df = pd.read_csv(DATA_FILE, sep=None, engine='python', encoding='utf-8-sig')

        # Eksik sütun kontrolü ve düzeltme
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""

        return df[COLUMNS]
    except Exception:
        df_empty = pd.DataFrame(columns=COLUMNS)
        df_empty.to_csv(DATA_FILE, index=False, sep=';', encoding='utf-8-sig')
        return df_empty

def rezervasyon_ekle(yeni_kayit_dict):
    df_mevcut = veritabanini_oku_ve_duzelt()
    df_yeni = pd.DataFrame([yeni_kayit_dict])
    df_toplam = pd.concat([df_mevcut, df_yeni], ignore_index=True)
    # Excel'in kusursuz açması için utf-8-sig ve ';' ile kaydet
    df_toplam.to_csv(DATA_FILE, index=False, sep=';', encoding='utf-8-sig')

# --- OTURUM ---
if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

# --- GİRİŞ EKRANI ---
if st.session_state['kullanici'] is None:
    st.markdown("<h1 style='text-align:center; font-weight:900;'>DriveNow</h1>", unsafe_allow_html=True)
    with st.form("giris_formu"):
        ad = st.text_input("Ad Soyad", placeholder="Örn: Cihan Demir")
        tc = st.text_input("TC Kimlik No", max_chars=11, placeholder="11 haneli TC No")
        tel = st.text_input("Telefon No", max_chars=10, placeholder="5XXXXXXXXX")
        if st.form_submit_button("SİSTEME GİRİŞ YAP"):
            if ad and len(tc) == 11 and len(tel) == 10:
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                st.rerun()
            else:
                st.error("Lütfen bilgileri eksiksiz ve doğru formatta girin.")
else:
    tab1, tab2, tab3 = st.tabs(["🚗 ARAÇLAR", "📋 KAYITLARIM", "👤 PROFİL"])

    with tab1:
        st.markdown("<h4 style='font-weight:800;'>Müsait Araçlar</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            loc = st.selectbox("Teslimat Noktası", ["İstanbul HL", "Sabiha Gökçen HL", "Ankara HL", "İzmir HL", "Antalya HL"])
        with col2:
            days = st.number_input("Süre (Gün)", min_value=1, value=1)

        for a in ARACLAR:
            total = a['fiyat'] * days
            st.markdown(f"""
            <div class="car-card">
                <div style="font-size:11px; font-weight:900; color:#2563EB;">★ {a['puan']} • {a['kat']}</div>
                <div class="car-title">{a['ad']}</div>
                <div style="margin: 8px 0;">
                    <span class="tag-item">🔀 {a['vites']}</span>
                    <span class="tag-item">⛽ {a['yakit']}</span>
                </div>
                <div style="background:#F8FAFC; padding:12px; border-radius:12px; display:flex; justify-content:space-between; align-items:center;">
                    <div><small>GÜNLÜK</small><br><b>{a['fiyat']:,} ₺</b></div>
                    <div style="text-align:right;"><small style="color:#FF6B00;">TOPLAM</small><br><b style="font-size:20px;">{total:,} ₺</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Hemen Kirala: {a['ad']}", key=f"krl_{a['ad']}"):
                yeni_kayit = {
                    "Tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "Musteri": st.session_state['kullanici']['ad'],
                    "TC": str(st.session_state['kullanici']['tc']),
                    "Telefon": str(st.session_state['kullanici']['tel']),
                    "Konum": loc,
                    "Arac": a['ad'],
                    "Gun": days,
                    "ToplamTutar": total
                }
                rezervasyon_ekle(yeni_kayit)
                st.success("🎉 Rezervasyonunuz başarıyla kaydedildi!")

    with tab2:
        st.markdown("<h4 style='font-weight:800;'>Kayıtlarınız</h4>", unsafe_allow_html=True)
        df_db = veritabanini_oku_ve_duzelt()
        if not df_db.empty:
            user_records = df_db[df_db['TC'].astype(str) == str(st.session_state['kullanici']['tc'])]
            if not user_records.empty:
                for _, r in user_records.iterrows():
                    st.markdown(f"""
                    <div class="car-card" style="border-left: 6px solid #059669;">
                        <b style="font-size:18px;">{r['Arac']}</b><br>
                        <small style="color:#64748B;">📅 {r['Tarih']} | 📍 {r['Konum']}</small><br>
                        <div style="color:#059669; font-weight:900; font-size:16px; margin-top:5px;">💰 {r['ToplamTutar']} ₺ (Onaylandı)</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Henüz kiralama yapmadınız.")
        else:
            st.info("Henüz sistemde kayıt yok.")

    with tab3:
        k = st.session_state['kullanici']
        st.markdown(f"""
        <div class="vip-card">
            <div style="font-size:10px; opacity:0.7; letter-spacing:2px;">VIP SÜRÜCÜ KARTI</div>
            <div style="font-size:24px; font-weight:900; margin:15px 0;">{k['ad']}</div>
            <div style="font-size:14px;">TC: {k['tc']}</div>
            <div style="font-size:14px;">TEL: +90 {k['tel']}</div>
            <div style="margin-top:20px; text-align:center; font-size:20px; letter-spacing:8px; opacity:0.5;">|| ||| | || ||||</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        if st.checkbox("⚙️ Yönetici Paneli"):
            st.markdown("<b>Tüm Rezervasyonları Excel İçin İndir:</b>", unsafe_allow_html=True)
            df_full = veritabanini_oku_ve_duzelt()
            
            # Excel için daha anlaşılır Türkçe başlıklar hazırlayalım
            df_excel = df_full.rename(columns={
                "Tarih": "Kayıt Tarihi",
                "Musteri": "Müşteri Ad Soyad",
                "TC": "T.C. Kimlik No",
                "Telefon": "Telefon No",
                "Konum": "Lokasyon",
                "Arac": "Kiralanan Araç",
                "Gun": "Süre (Gün)",
                "ToplamTutar": "Toplam Tutar (TL)"
            })
            
            # UTF-8 BOM ve Noktalı Virgül ile Excel çıktısı oluştur
            csv_data = df_excel.to_csv(index=False, sep=';', encoding='utf-8-sig')
            
            st.download_button(
                label="📥 EXCEL DOSYASINI İNDİR (.csv)",
                data=csv_data,
                file_name=f"DriveNow_Rezervasyonlar_{datetime.now().strftime('%d_%m_%Y')}.csv",
                mime="text/csv"
            )
            
            if st.button("🚨 Veritabanını Temizle / Sıfırla"):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                    st.warning("Veritabanı sıfırlandı. Sayfayı yenileyin.")
                    st.rerun()

        if st.button("Çıkış Yap"):
            st.session_state['kullanici'] = None
            st.rerun()
