import streamlit as st
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
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "vites": "Otomatik", "yakit": "Dizel", "fiyat": 1500},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "vites": "Manuel", "yakit": "Benzin", "fiyat": 900},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "vites": "Otomatik", "yakit": "Benzin", "fiyat": 1200},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "vites": "Manuel", "yakit": "Dizel", "fiyat": 850},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "vites": "Otomatik", "yakit": "Elektrik", "fiyat": 2500}
]

# --- KARANLIK MODU EZEN VE GÖRÜNÜRLÜĞÜ ZORLAYAN CSS ---
st.markdown("""
    <style>
    /* 1. TÜM ARKA PLANI BEYAZA ZORLA */
    .stApp {
        background-color: #F8FAFC !important;
    }

    /* 2. TÜM YAZILARI KOYU LACİVERT/SİYAH YAP */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small {
        color: #0F172A !important;
        font-family: -apple-system, sans-serif !important;
    }

    /* 3. INPUT KUTULARINI BEYAZ YAP VE YAZISINI NETLEŞTİR */
    input, div[data-baseweb="select"], .stNumberInput div, div[data-baseweb="base-input"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
        -webkit-text-fill-color: #0F172A !important; /* iOS için */
    }

    /* 4. BUTONLARI TURUNCU YAP VE YAZISINI BEYAZA ZORLA */
    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #FF6B00 0%, #FF5F00 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        height: 54px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(255, 95, 0, 0.3) !important;
        opacity: 1 !important;
    }
    
    /* Butonun içindeki metni ekstra zorla */
    div.stButton > button p, div.stFormSubmitButton > button p {
        color: #FFFFFF !important;
    }

    /* 5. KARTLARI BEYAZ YAP */
    .custom-card {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 2px solid #E2E8F0 !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }

    /* 6. TABLARI DÜZENLE */
    div[data-baseweb="tab-list"] {
        background-color: #E2E8F0 !important;
        border-radius: 15px !important;
        padding: 5px !important;
    }
    div[aria-selected="true"] {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
    }

    /* 7. ADMIN PANELİ METİN KUTUSU */
    .admin-text-area {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        padding: 15px !important;
        border-radius: 12px !important;
        border: 1px solid #CBD5E1 !important;
        font-family: monospace !important;
        font-size: 12px !important;
        max-height: 300px;
        overflow-y: auto;
    }

    /* Header'ı gizle */
    header {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

# --- DOSYA İŞLEMLERİ ---
LOG_FILE = "kayitlar.txt"

def kaydet(mesaj):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%d.%m.%Y %H:%M')} | {mesaj}\n")

def kayitlari_oku():
    if not os.path.exists(LOG_FILE):
        return "Henüz bir işlem yapılmadı."
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read()

# --- OTURUM MANTIĞI ---
if 'giris_yapti' not in st.session_state:
    st.session_state['giris_yapti'] = False
    st.session_state['kullanici'] = {}

# --- GİRİŞ EKRANI ---
if not st.session_state['giris_yapti']:
    st.markdown("<h1 style='text-align:center;'>DriveNow</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        ad = st.text_input("Ad Soyad", placeholder="Örn: Cihan Demirci")
        tc = st.text_input("TC Kimlik No", max_chars=11, placeholder="11 haneli")
        tel = st.text_input("Telefon", max_chars=10, placeholder="5XXXXXXXXX")
        
        submit = st.form_submit_button("SİSTEME GİRİŞ YAP")
        if submit:
            if ad and len(tc) == 11:
                st.session_state['giris_yapti'] = True
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                kaydet(f"GİRİŞ: {ad} - TC: {tc} - TEL: {tel}")
                st.rerun()
            else:
                st.error("Lütfen bilgileri eksiksiz girin.")
else:
    # --- ANA UYGULAMA ---
    tab1, tab2, tab3 = st.tabs(["🚗 ARAÇLAR", "📋 KAYITLARIM", "⚙️ YÖNETİCİ"])

    with tab1:
        st.markdown(f"<h4>Hoş geldin, {st.session_state['kullanici']['ad']}</h4>", unsafe_allow_html=True)
        loc = st.selectbox("Teslimat Noktası", ["İstanbul HL", "Sabiha Gökçen HL", "Ankara Esenboğa"])
        days = st.number_input("Gün Sayısı", min_value=1, value=1)

        for a in ARACLAR:
            total = a['fiyat'] * days
            st.markdown(f"""
            <div class="custom-card">
                <b style="font-size:22px;">{a['ad']}</b><br>
                <span style="color:#2563EB; font-weight:800; font-size:12px;">{a['kat']}</span>
                <div style="margin-top:15px; display:flex; justify-content:space-between; align-items:center;">
                    <div><small>GÜNLÜK</small><br><b style="font-size:18px;">{a['fiyat']} ₺</b></div>
                    <div style="text-align:right;"><small style="color:#FF6B00;">TOPLAM</small><br><b style="font-size:22px;">{total} ₺</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"HEMEN KİRALA: {a['ad']}", key=a['ad']):
                kaydet(f"KİRALAMA: {st.session_state['kullanici']['ad']} | Araç: {a['ad']} | Gün: {days} | Toplam: {total} ₺ | Yer: {loc}")
                st.success(f"{a['ad']} başarıyla kiralandı!")

    with tab2:
        st.subheader("İşlem Geçmişiniz")
        logs = kayitlari_oku().split("\n")
        sayac = 0
        for log in logs:
            if st.session_state['kullanici']['ad'] in log:
                st.markdown(f"<div class='custom-card'>{log}</div>", unsafe_allow_html=True)
                sayac += 1
        if sayac == 0:
            st.info("Henüz bir işleminiz bulunmuyor.")

    with tab3:
        # KULLANICI KARTI
        st.markdown(f"""
        <div style="background:#FFFFFF; border:2px solid #0F172A; padding:20px; border-radius:15px; margin-bottom:20px;">
            <b style="font-size:18px;">Aktif Sürücü</b><br>
            {st.session_state['kullanici']['ad']}<br>
            TC: {st.session_state['kullanici']['tc']}
        </div>
        """, unsafe_allow_html=True)

        # ADMIN PANELİ
        if st.checkbox("Yönetici Panelini Göster"):
            st.write("---")
            st.markdown("<b>Tüm Sistem Logları:</b>", unsafe_allow_html=True)
            st.markdown(f"<div class='admin-text-area'>{kayitlari_oku()}</div>", unsafe_allow_html=True)
            
            st.download_button(
                label="📥 KAYITLARI İNDİR (.TXT)",
                data=kayitlari_oku(),
                file_name="drive_now_kayitlar.txt",
                mime="text/plain"
            )
            
            if st.button("🚨 SİSTEMİ SIFIRLA"):
                if os.path.exists(LOG_FILE):
                    os.remove(LOG_FILE)
                    st.rerun()

        if st.button("ÇIKIŞ YAP"):
            st.session_state['giris_yapti'] = False
            st.rerun()
