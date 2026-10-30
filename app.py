import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- SAYFA AYARLARI (Mobil Uyumlu) ---
st.set_page_config(
    page_title="Rent a Car",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS İLE MOBİL GÖRÜNÜM GÜZELLEŞTİRME ---
st.markdown("""
    <style>
    .main { background-color: #F2F2F7; }
    .stButton>button {
        width: 100%;
        background-color: #007AFF;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 3em;
    }
    .car-card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- VERİTABANI DOSYASI ---
DATA_FILE = "rezervasyonlar.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Tarih", "Musteri", "TC", "Telefon", "Arac", "Gun", "ToplamTutar"])
    df.to_csv(DATA_FILE, index=False)

# --- ARAÇ VERİLERİ ---
ARACLAR = [
    {"ad": "Peugeot 508", "vites": "Otomatik", "yakit": "Dizel", "fiyat": 1500, "foto": "🚘"},
    {"ad": "Renault Clio", "vites": "Manuel", "yakit": "Benzin", "fiyat": 900, "foto": "🚗"},
    {"ad": "Ford Focus", "vites": "Otomatik", "yakit": "Benzin", "fiyat": 1200, "foto": "🚙"},
    {"ad": "Fiat Egea", "vites": "Manuel", "yakit": "Dizel", "fiyat": 800, "foto": "🚕"},
    {"ad": "Tesla Model 3", "vites": "Otomatik", "yakit": "Elektrik", "fiyat": 2500, "foto": "⚡"}
]

# --- OTURUM YÖNETİMİ ---
if 'kullanici' not in st.session_state:
    st.session_state['kullanici'] = None

# ==========================================
# EKRAN 1: GİRİŞ EKRANI
# ==========================================
if st.session_state['kullanici'] is None:
    st.title("🚗 Rent a Car")
    st.subheader("Hoş Geldiniz 👋")
    st.write("Araç kiralamak için bilgilerinizi girin.")

    with st.form("giris_formu"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("T.C. Kimlik No", max_chars=11)
        tel = st.text_input("Telefon No (5XX)", max_chars=10)
        submit = st.form_submit_button("Giriş Yap ➔")

        if submit:
            if ad and len(tc) == 11 and len(tel) == 10:
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                st.success("Giriş Başarılı!")
                st.rerun()
            else:
                st.error("Lütfen bilgileri doğru ve eksiksiz girin (TC: 11 hane, Tel: 10 hane).")

# ==========================================
# EKRAN 2: ANA UYGULAMA (GİRİŞ YAPILDIYSA)
# ==========================================
else:
    # Üst Bilgi Barı
    col_user, col_logout = st.columns([3, 1])
    with col_user:
        st.write(f"👤 **{st.session_state['kullanici']['ad']}**")
    with col_logout:
        if st.button("Çıkış"):
            st.session_state['kullanici'] = None
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["🚗 Araç Kirala", "📋 Geçmişim", "👤 Profil"])

    # --- TAB 1: ARAÇ KİRALAMA ---
    with tab1:
        st.markdown("### Uygun Araçlar")
        
        # Filtreler & Gün Seçimi
        c1, c2 = st.columns(2)
        with c1:
            vites_filtre = st.selectbox("Vites Tipi", ["Tümü", "Otomatik", "Manuel"])
        with c2:
            gun = st.number_input("Kiralama Süresi (Gün)", min_value=1, max_value=30, value=1)

        # Araç Listeleme
        for arac in ARACLAR:
            if vites_filtre != "Tümü" and arac["vites"] != vites_filtre:
                continue

            toplam_fiyat = arac["fiyat"] * gun
            
            with st.container():
                st.markdown(f"""
                <div class="car-card">
                    <h3>{arac['foto']} {arac['ad']}</h3>
                    <p>⛽ <b>Yakıt:</b> {arac['yakit']} | 🔀 <b>Vites:</b> {arac['vites']}</p>
                    <p style="color: #34C759; font-weight: bold;">✓ Ücretsiz İptal</p>
                    <h4 style="color: #007AFF;">Günlük: {arac['fiyat']} ₺</h4>
                    <h5>Toplam ({gun} Gün): {toplam_fiyat:,} ₺</h5>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Hemen Kirala - {arac['ad']}", key=arac['ad']):
                    # Kayıt Yap
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
                    st.success(f"🎉 {arac['ad']} başarıyla kiralandı! Toplam: {toplam_fiyat} ₺")

    # --- TAB 2: GEÇMİŞ REZERVASYONLAR ---
    with tab2:
        st.markdown("### Kiralama Geçmişiniz")
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            user_df = df[df['TC'] == int(st.session_state['kullanici']['tc'])]
            if not user_df.empty:
                for idx, row in user_df.iterrows():
                    st.info(f"🚗 **{row['Arac']}**\n\n📅 Tarih: {row['Tarih']}\n\n⏱ Süre: {row['Gun']} Gün\n\n💰 Tutar: {row['ToplamTutar']} ₺")
            else:
                st.write("Henüz bir kiralama yapmadınız.")

    # --- TAB 3: PROFİL ---
    with tab3:
        st.markdown("### Profil Bilgileri")
        st.json(st.session_state['kullanici'])