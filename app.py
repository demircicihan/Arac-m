import streamlit as st
from datetime import datetime
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="DriveNow Premium", page_icon="🚗", layout="centered")

# --- KLASÖRLER VE DOSYALAR ---
UPLOAD_DIR = "yuklemeler"
LOG_FILE = "kayitlar.txt"

if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "a", encoding="utf-8") as f: f.write("")

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

# --- KARANLIK MODU VE HAYALET YAZILARI YOK EDEN CSS ---
st.markdown("""
    <style>
    /* 1. UYGULAMA ZEMİNİ BEMBEYAZ */
    .stApp { background-color: #FFFFFF !important; }

    /* 2. TÜM YAZILARI ZORLA SİYAHA ÇEK (Karanlık Modda Bile) */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small, strong {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-family: -apple-system, sans-serif !important;
    }

    /* 3. GİRİŞ KUTULARI VE SELECTBOXLAR */
    input, div[data-baseweb="select"], .stNumberInput div, div[data-baseweb="base-input"], textarea {
        background-color: #F1F5F9 !important;
        color: #000000 !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* 4. BUTONLAR: TURUNCU ARKA PLAN, BEYAZ YAZI (YAZIYI ZORLA BEYAZ YAP) */
    div.stButton > button, div.stFormSubmitButton > button {
        background: #FF6B00 !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 900 !important;
        height: 52px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.3) !important;
    }
    
    /* Buton içindeki metin beyaz kalsın */
    div.stButton > button p, div.stFormSubmitButton > button p {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* 5. KARTLAR VE TABLAR */
    .custom-card {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 2px solid #E2E8F0 !important;
        margin-bottom: 15px !important;
    }

    /* Header gizleme */
    header {visibility: hidden !important;}
    </style>
""", unsafe_allow_html=True)

# --- KAYIT FONKSİYONLARI ---
def kaydet(mesaj):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%d.%m.%Y %H:%M')} | {mesaj}\n")
    except:
        st.error("Dosyaya yazılamadı!")

def kayitlari_oku():
    if not os.path.exists(LOG_FILE): return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return [line.strip() for line in lines if line.strip()]
    except:
        return []

# --- OTURUM MANTIĞI ---
if 'giris' not in st.session_state: st.session_state['giris'] = False
if 'kullanici' not in st.session_state: st.session_state['kullanici'] = {}
if 'secili_arac' not in st.session_state: st.session_state['secili_arac'] = None

# --- GİRİŞ EKRANI ---
if not st.session_state['giris']:
    st.markdown("<h1 style='text-align:center;'>DriveNow</h1>", unsafe_allow_html=True)
    with st.form("giris_ekrani"):
        ad = st.text_input("Ad Soyad")
        tc = st.text_input("TC Kimlik No", max_chars=11)
        tel = st.text_input("Telefon", max_chars=10)
        
        if st.form_submit_button("GİRİŞ YAP"):
            if ad and len(tc) == 11:
                st.session_state['giris'] = True
                st.session_state['kullanici'] = {"ad": ad, "tc": tc, "tel": tel}
                kaydet(f"GİRİŞ: {ad} (TC:{tc})")
                st.rerun()
            else:
                st.error("Lütfen bilgileri eksiksiz girin.")
else:
    # --- UYGULAMA ARAYÜZÜ ---
    tab1, tab2, tab3 = st.tabs(["🚗 ARAÇLAR", "📋 KAYITLARIM", "⚙️ YÖNETİCİ"])

    with tab1:
        if st.session_state['secili_arac'] is None:
            st.markdown(f"<h3>Hoş geldin, {st.session_state['kullanici']['ad']}</h3>", unsafe_allow_html=True)
            konum = st.selectbox("Teslimat Yeri", ["İstanbul Havalimanı", "Sabiha Gökçen HL", "Ankara HL"])
            gun = st.number_input("Gün Sayısı", min_value=1, value=1)
            
            for a in ARACLAR:
                toplam = a['fiyat'] * gun
                st.markdown(f"""<div class='custom-card'><b style='font-size:20px;'>{a['ad']}</b><br>Fiyat: {toplam} ₺</div>""", unsafe_allow_html=True)
                if st.button(f"SEÇ: {a['ad']}", key=a['ad']):
                    st.session_state['secili_arac'] = {"ad": a['ad'], "toplam": toplam, "gun": gun, "konum": konum}
                    st.rerun()
        else:
            # EHLİYET YÜKLEME
            st.warning(f"Seçilen: {st.session_state['secili_arac']['ad']}")
            with st.form("ehliyet_formu"):
                ehliyet_no = st.text_input("Ehliyet Belge No")
                dosya = st.file_uploader("Ehliyet Fotoğrafı (Zorunlu)", type=['jpg','png'])
                
                if st.form_submit_button("KİRALAMAYI ONAYLA"):
                    if ehliyet_no and dosya:
                        # Kaydet
                        foto_ad = f"{st.session_state['kullanici']['tc']}_{datetime.now().strftime('%H%M%S')}.jpg"
                        with open(os.path.join(UPLOAD_DIR, foto_ad), "wb") as f:
                            f.write(dosya.getbuffer())
                        
                        s = st.session_state['secili_arac']
                        kaydet(f"KİRALAMA: {st.session_state['kullanici']['ad']} | Araç: {s['ad']} | Ehliyet: {ehliyet_no} | Tutar: {s['toplam']} ₺")
                        
                        st.success("Rezervasyon başarıyla oluşturuldu!")
                        st.session_state['secili_arac'] = None
                        st.rerun()
                    else:
                        st.error("Lütfen tüm alanları doldurun.")
            if st.button("⬅️ Geri Dön"):
                st.session_state['secili_arac'] = None
                st.rerun()

    with tab2:
        st.subheader("İşlem Geçmişiniz")
        tum_kayitlar = kayitlari_oku()
        
        # Kullanıcının sadece kendi kayıtlarını görmesi için filtre
        kullanici_adi = st.session_state['kullanici']['ad']
        sayac = 0
        
        if not tum_kayitlar:
            st.info("Henüz sistemde hiç kayıt yok.")
        else:
            for satir in tum_kayitlar:
                if kullanici_adi in satir:
                    st.markdown(f"<div class='custom-card'>{satir}</div>", unsafe_allow_html=True)
                    sayac += 1
            
            if sayac == 0:
                st.info("Adınıza kayıtlı bir işlem bulunamadı.")

    with tab3:
        # ŞİFRELİ YÖNETİCİ PANELİ
        admin_onay = st.checkbox("🔑 Yönetici Paneli Girişi")
        if admin_onay:
            sifre = st.text_input("Şifre", type="password")
            if sifre == ADMIN_SIFRE:
                st.success("Yetkili Girişi Başarılı.")
                
                # Rezervasyonları Listele
                st.markdown("### Tüm Rezervasyon Listesi")
                st.text_area("Sistem Kayıtları", "\n".join(kayitlari_oku()), height=250)
                
                # Ehliyet Fotoğrafları
                st.markdown("### Yüklenen Ehliyetler")
                fotolar = os.listdir(UPLOAD_DIR)
                for f in fotolar:
                    with open(os.path.join(UPLOAD_DIR, f), "rb") as file:
                        st.download_button(f"İndir: {f}", file, file_name=f)
                        st.image(os.path.join(UPLOAD_DIR, f), width=150)
                
                if st.button("🚨 Verileri Sıfırla"):
                    if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
                    for f in os.listdir(UPLOAD_DIR): os.remove(os.path.join(UPLOAD_DIR, f))
                    st.rerun()
            elif sifre != "":
                st.error("Hatalı Şifre!")

        if st.button("GÜVENLİ ÇIKIŞ"):
            st.session_state['giris'] = False
            st.rerun()
