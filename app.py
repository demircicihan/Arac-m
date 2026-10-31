import streamlit as st
from datetime import datetime
import os

# --- AYARLAR ---
st.set_page_config(page_title="DriveNow Premium", page_icon="🚗", layout="centered")

# --- ADMİN ŞİFRE ---
ADMIN_SIFRE = "cihan123" 

# --- ARAÇLAR ---
ARACLAR = [
    {"ad": "Peugeot 508 GT", "kat": "SEDAN • PREMİUM", "fiyat": 1500},
    {"ad": "Renault Clio", "kat": "HATCHBACK • EKONOMİK", "fiyat": 900},
    {"ad": "Ford Focus", "kat": "COMPACT • KONFOR", "fiyat": 1200},
    {"ad": "Fiat Egea Cross", "kat": "CROSSOVER • EKONOMİK", "fiyat": 850},
    {"ad": "Tesla Model 3", "kat": "LÜKS • %100 ELEKTRİK", "fiyat": 2500}
]

# --- KARANLIK MODU EZEN CSS (YÜKSEK GÖRÜNÜRLÜK) ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; }
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small {
        color: #0F172A !important;
        font-family: -apple-system, sans-serif !important;
    }
    input, div[data-baseweb="select"], .stNumberInput div, div[data-baseweb="base-input"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
        -webkit-text-fill-color: #0F172A !important;
    }
    div.stButton > button, div.stFormSubmitButton > button {
        background: #FF6B00 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        height: 52px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.3) !important;
    }
    .custom-card {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 2px solid #E2E8F0 !important;
        margin-bottom: 15px !important;
    }
    header {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

# --- DOSYA SİSTEMİ ---
LOG_FILE = "kayitlar.txt"
def kaydet(mesaj):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%d.%m.%Y %H:%M')} | {mesaj}\n")

def kayitlari_oku():
    if not os.path.exists(LOG_FILE): return "Henüz kayıt yok."
    with open(LOG_FILE, "r", encoding="utf-8") as f: return f.read()

# --- OTURUM ---
if 'login' not in st.session_state:
    st.session_state['login'] = False
    st.session_state['user'] = {}
if 'secilen_arac' not in st.session_state:
    st.session_state['secilen_arac'] = None

# --- GİRİŞ EKRANI ---
if not st.session_state['login']:
    st.markdown("<h1 style='text-align:center;'>DriveNow</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("TC Kimlik No", max_chars=11)
        tel = st.text_input("Telefon", max_chars=10)
        if st.form_submit_button("GİRİŞ YAP"):
            if ad and len(tc) == 11:
                st.session_state['login'] = True
                st.session_state['user'] = {"ad": ad, "tc": tc, "tel": tel}
                kaydet(f"GİRİŞ YAPILDI: {ad} - TC: {tc} - TEL: {tel}")
                st.rerun()
else:
    tab1, tab2, tab3 = st.tabs(["🚗 ARAÇLAR", "📋 KAYITLARIM", "⚙️ PROFİL"])

    with tab1:
        # Araç Seçimi veya Kimlik Onayı
        if st.session_state['secilen_arac'] is None:
            st.write(f"Hoş geldin, **{st.session_state['user']['ad']}**")
            loc = st.selectbox("Alış Yeri", ["İstanbul Havalimanı", "Sabiha Gökçen HL", "Ankara Esenboğa"])
            days = st.number_input("Gün Sayısı", min_value=1, value=1)

            for a in ARACLAR:
                total = a['fiyat'] * days
                st.markdown(f"""
                <div class="custom-card">
                    <b style="font-size:20px;">{a['ad']}</b><br>
                    <span>Günlük: {a['fiyat']} ₺ | Toplam: <b style="color:#FF6B00;">{total} ₺</b></span>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"SEÇ VE İLERLE: {a['ad']}", key=a['ad']):
                    st.session_state['secilen_arac'] = {"ad": a['ad'], "toplam": total, "gün": days, "konum": loc}
                    st.rerun()
        else:
            # KİMLİK VE EHLİYET BİLGİLERİ FORMU
            st.warning(f"Seçilen Araç: {st.session_state['secilen_arac']['ad']}")
            st.markdown("### 🛡️ Kiralama İçin Kimlik Doğrulama")
            with st.form("kimlik_onay"):
                ehliyet_no = st.text_input("Ehliyet Seri No (Belge No)")
                ehliyet_sinif = st.selectbox("Ehliyet Sınıfı", ["B", "B1", "A", "C", "D"])
                st.info("Lütfen Ehliyetinizin ön yüzünün fotoğrafını yükleyin (Opsiyonel)")
                ehliyet_foto = st.file_uploader("Ehliyet Görseli Seç", type=['jpg','png','jpeg'])
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button("KİRALAMAYI ONAYLA"):
                        if ehliyet_no:
                            s = st.session_state['secilen_arac']
                            u = st.session_state['user']
                            bilgi = (f"KİRALAMA: {u['ad']} (TC:{u['tc']}) | Araç: {s['ad']} | "
                                    f"Ehliyet No: {ehliyet_no} | Sınıf: {ehliyet_sinif} | "
                                    f"Tutar: {s['toplam']} ₺ | Yer: {s['konum']}")
                            kaydet(bilgi)
                            st.success("Tebrikler! Kiralama işleminiz başarıyla tamamlandı.")
                            st.session_state['secilen_arac'] = None # Formu sıfırla
                        else:
                            st.error("Ehliyet Seri No girmek zorunludur.")
                with c2:
                    if st.form_submit_button("İPTAL ET"):
                        st.session_state['secilen_arac'] = None
                        st.rerun()

    with tab2:
        st.subheader("Rezervasyonlarınız")
        logs = kayitlari_oku().split("\n")
        sayac = 0
        for log in logs:
            if st.session_state['user']['ad'] in log and "KİRALAMA" in log:
                st.markdown(f"<div class='custom-card'>{log}</div>", unsafe_allow_html=True)
                sayac += 1
        if sayac == 0: st.info("Kaydınız bulunamadı.")

    with tab3:
        st.markdown(f"""<div style="background:white; border:2px solid #0F172A; padding:15px; border-radius:12px;">
        <b>Kullanıcı:</b> {st.session_state['user']['ad']}<br>
        <b>TC:</b> {st.session_state['user']['tc']}</div>""", unsafe_allow_html=True)
        
        st.write("---")
        admin_check = st.checkbox("🔑 Yönetici Paneli")
        if admin_check:
            sifre = st.text_input("Şifre", type="password")
            if sifre == ADMIN_SIFRE:
                st.success("Yetkili Girişi Yapıldı.")
                st.text_area("Tüm Sistem Kayıtları", kayitlari_oku(), height=300)
                st.download_button("📥 Kayıtları İndir", kayitlari_oku(), "drive_now_admin.txt")
                if st.button("🚨 Verileri Temizle"):
                    if os.path.exists(LOG_FILE): os.remove(LOG_FILE); st.rerun()
            elif sifre != "": st.error("Hatalı Giriş!")

        if st.button("ÇIKIŞ YAP"):
            st.session_state['login'] = False
            st.rerun()
