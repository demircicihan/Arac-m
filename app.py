import os
import re
from datetime import datetime
import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="DriveNow | Araç Kiralama",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- SECRETS MANAGEMENT ---
ADMIN_SIFRE = st.secrets.get("ADMIN_SIFRE", "cihan123")

# --- KLASÖR VE DOSYA KONTROLÜ ---
LOG_FILE = "kayitlar.txt"
UPLOAD_DIR = "yuklemeler"

os.makedirs(UPLOAD_DIR, exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8-sig") as f:
        f.write("")

# --- MOBİL UYGULAMA BİREBİR ARAÇ FİLOSU (GÖRSELLİ) ---
ARACLAR = [
    {
        "ad": "Peugeot 301",
        "alt_baslik": "veya benzeri",
        "kat": "SEDAN • EKONOMİK",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "fiyat": 1500,
        "km": "2000km",
        "resim": "https://raw.githubusercontent.com/raymond-design/car-images/main/peugeot301.png",
        "motor": "1.2 PureTech (82 HP)",
        "sanziman": "5 İleri Otomatik",
        "tuketim": "5.1 Lt / 100km",
        "hizlanma": "0-100 km/s: 12.9 sn",
        "donanimlar": ["Klima", "Bluetooth", "Park Sensörü", "ABS / ESP"],
    },
    {
        "ad": "Renault Clio",
        "alt_baslik": "veya benzeri",
        "kat": "HATCHBACK • EKONOMİK",
        "vites": "Manuel",
        "yakit": "Benzin",
        "fiyat": 1350,
        "km": "Sınırsız KM",
        "resim": "https://raw.githubusercontent.com/raymond-design/car-images/main/clio.png",
        "motor": "1.0 TCe (90 HP)",
        "sanziman": "6 İleri Manuel",
        "tuketim": "5.0 Lt / 100km",
        "hizlanma": "0-100 km/s: 12.2 sn",
        "donanimlar": ["Apple CarPlay", "Hız Sabitleyici", "Start-Stop", "LED Farlar"],
    },
    {
        "ad": "Fiat Egea Cross",
        "alt_baslik": "veya benzeri",
        "kat": "CROSSOVER • EKONOMİK",
        "vites": "Manuel",
        "yakit": "Dizel",
        "fiyat": 1250,
        "km": "1500km",
        "resim": "https://raw.githubusercontent.com/raymond-design/car-images/main/egea.png",
        "motor": "1.3 MultiJet (95 HP)",
        "sanziman": "5 İleri Manuel",
        "tuketim": "4.4 Lt / 100km",
        "hizlanma": "0-100 km/s: 12.8 sn",
        "donanimlar": ["City Modu", "10 Tablet Ekran", "Tavan Çıtaları", "Yokuş Kalkış"],
    },
    {
        "ad": "Ford Focus",
        "alt_baslik": "veya benzeri",
        "kat": "COMPACT • KONFOR",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "fiyat": 1800,
        "km": "Sınırsız KM",
        "resim": "https://raw.githubusercontent.com/raymond-design/car-images/main/focus.png",
        "motor": "1.5 Ti-VCT (123 HP)",
        "sanziman": "6 İleri Otomatik",
        "tuketim": "6.2 Lt / 100km",
        "hizlanma": "0-100 km/s: 11.2 sn",
        "donanimlar": ["SYNC 4 Ekran", "Geri Görüş Kamerası", "Şerit Takip", "Kablosuz Şarj"],
    },
    {
        "ad": "Peugeot 508 GT",
        "alt_baslik": "veya benzeri",
        "kat": "SEDAN • PREMİUM",
        "vites": "Otomatik",
        "yakit": "Dizel",
        "fiyat": 2600,
        "km": "Sınırsız KM",
        "resim": "https://raw.githubusercontent.com/raymond-design/car-images/main/508.png",
        "motor": "1.5 BlueHDi (130 HP)",
        "sanziman": "8 İleri EAT8",
        "tuketim": "4.1 Lt / 100km",
        "hizlanma": "0-100 km/s: 9.9 sn",
        "donanimlar": ["Masajlı Koltuk", "Focal® Hi-Fi", "Gece Görüşü", "Kör Nokta"],
    },
    {
        "ad": "Volkswagen Tiguan",
        "alt_baslik": "veya benzeri",
        "kat": "SUV • PREMİUM",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "fiyat": 2800,
        "km": "Sınırsız KM",
        "resim": "https://raw.githubusercontent.com/raymond-design/car-images/main/tiguan.png",
        "motor": "1.5 TSI ACT (150 HP)",
        "sanziman": "7 İleri DSG",
        "tuketim": "5.7 Lt / 100km",
        "hizlanma": "0-100 km/s: 9.2 sn",
        "donanimlar": ["Cam Tavan", "Matrix LED Farlar", "Hayalet Ekran", "3 Bölge Klima"],
    },
]

# --- BEYAZ MOBİL UYGULAMA CSS TASARIMI ---
st.markdown(
    """
    <style>
    /* GENEL BEYAZ/AÇIK TEMA */
    .stApp {
        background-color: #F3F4F6 !important;
    }

    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    /* YAZI TİPLERİ VE RENKLERİ */
    html, body, [class*="css"], label, p, span, div {
        color: #1E293B !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* ÜST ARAMA VE BİLGİ KARTI */
    .app-header-card {
        background: #FFFFFF !important;
        padding: 16px 20px !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        margin-bottom: 16px !important;
        border: 1px solid #E2E8F0 !important;
    }

    /* BEYAZ MOBİL ARAÇ KARTI */
    .app-car-card {
        background: #FFFFFF !important;
        border-radius: 20px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
        border: 1px solid #E2E8F0 !important;
    }

    /* KART İÇİ TASARIM ELEMANLARI */
    .car-title-app {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .car-subtitle-app {
        font-size: 13px !important;
        color: #94A3B8 !important;
        font-weight: 500 !important;
        margin-bottom: 12px !important;
    }

    .spec-item-app {
        font-size: 13px !important;
        color: #475569 !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }

    .free-cancel-badge {
        color: #16A34A !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        margin-top: 10px !important;
        display: inline-block !important;
    }

    /* FİYAT ALANI */
    .price-main-app {
        font-size: 26px !important;
        font-weight: 900 !important;
        color: #0F172A !important;
    }
    .price-sub-app {
        font-size: 12px !important;
        color: #94A3B8 !important;
        font-weight: 600 !important;
    }

    /* CANLI TURUNCU HEPSİ KİRALA BUTONU */
    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #FF5722 0%, #F4511E 100%) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        height: 48px !important;
        width: 100% !important;
        box-shadow: 0 6px 16px rgba(244, 81, 30, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 20px rgba(244, 81, 30, 0.45) !important;
    }

    /* EXPANDER (DETAYLAR) STİLİ */
    div[data-testid="stExpander"] {
        background: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        margin-top: 8px !important;
    }

    /* INPUT STİLLERİ */
    input, div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- KAYIT SİSTEMİ FONKSİYONLARI ---
def kaydet(tip: str, mesaj: str):
    zaman = datetime.now().strftime("%d.%m.%Y %H:%M")
    with open(LOG_FILE, "a", encoding="utf-8-sig") as f:
        f.write(f"{zaman} | {tip} | {mesaj}\n")


def kayitlari_ayristir():
    if not os.path.exists(LOG_FILE):
        return "", ""
    girisler, kiralama = [], []
    with open(LOG_FILE, "r", encoding="utf-8-sig") as f:
        for satir in f:
            if "| GİRİŞ |" in satir:
                girisler.append(satir.strip())
            elif "| KİRALAMA |" in satir:
                kiralama.append(satir.strip())
    return "\n".join(girisler), "\n".join(kiralama)


# --- OTURUM YÖNETİMİ ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "user" not in st.session_state:
    st.session_state["user"] = {}
if "secili" not in st.session_state:
    st.session_state["secili"] = None

# --- GİRİŞ EKRANI ---
if not st.session_state["auth"]:
    st.markdown(
        """
        <div style="text-align: center; padding: 30px 0 20px 0;">
            <div style="background: #E0E7FF; color: #4338CA !important; padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: 800; display: inline-block; margin-bottom: 12px;">
                📍 Türkiye Geneli Teslimat
            </div>
            <h1 style="font-size: 38px; font-weight: 900; margin: 0; color: #0F172A !important;">DriveNow</h1>
            <p style="font-size: 15px; font-weight: 600; color: #64748B !important;">Hızlı & Kolay Araç Kiralama</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        st.markdown("<b>👋 Kullanıcı Bilgileriniz</b>", unsafe_allow_html=True)
        ad = st.text_input("Ad Soyad", placeholder="Örn: Cihan Demirci")
        tc = st.text_input(
            "T.C. Kimlik No", max_chars=11, placeholder="11 Haneli T.C. No"
        )
        tel = st.text_input(
            "Telefon No", max_chars=10, placeholder="5XXXXXXXXX"
        )

        submit = st.form_submit_button("ARAÇLARI LİSTELE ➔")

        if submit:
            tc_clean = tc.strip()
            tel_clean = tel.strip()
            if (
                ad.strip()
                and len(tc_clean) == 11
                and tc_clean.isdigit()
                and len(tel_clean) == 10
                and tel_clean.isdigit()
            ):
                st.session_state["auth"] = True
                st.session_state["user"] = {
                    "ad": ad.strip(),
                    "tc": tc_clean,
                    "tel": tel_clean,
                }
                kaydet(
                    "GİRİŞ",
                    f"Ad: {ad.strip()} - TC: {tc_clean} - Tel: {tel_clean}",
                )
                st.rerun()
            else:
                st.error(
                    "Lütfen bilgileri eksiksiz girin (TC: 11 rakam, Tel: 10 rakam)."
                )

else:
    # --- ANA UYGULAMA (TABS) ---
    t1, t2, t3 = st.tabs(["🏎️ Araçlar", "📜 Kayıtlarım", "🔑 Yönetici"])

    with t1:
        if st.session_state["secili"] is None:
            # 🔍 ÜST ARAMA VE BİLGİ PANELİ
            st.markdown('<div class="app-header-card">', unsafe_allow_html=True)
            c_loc, c_vites, c_gun = st.columns([2, 1.5, 1])
            with c_loc:
                konum = st.selectbox(
                    "📍 Teslim Noktası",
                    [
                        "Konya • Ereğli Merkez / KYK",
                        "Konya • Çumra İlçe Merkezi",
                        "Konya • Selçuklu / Otogar",
                        "Konya • Havalimanı (KYA)",
                        "İstanbul • Sabiha Gökçen HL",
                        "İstanbul • İstanbul Havalimanı",
                        "Ankara • Esenboğa HL",
                        "İzmir • Adnan Menderes HL",
                        "Antalya • Havalimanı",
                    ],
                )
            with c_vites:
                vites_filtre = st.selectbox(
                    "🔀 Vites Tipi", ["Tümü", "Otomatik", "Manuel"]
                )
            with c_gun:
                gun = st.number_input(
                    "⏱ Gün", min_value=1, max_value=30, value=1
                )
            st.markdown("</div>", unsafe_allow_html=True)

            # 🚗 MOBİL UYGULAMA BİREBİR ARAÇ LİSTESİ
            musait_sayisi = 0
            for a in ARACLAR:
                if vites_filtre != "Tümü" and a["vites"] != vites_filtre:
                    continue

                musait_sayisi += 1
                toplam_tutar = a["fiyat"] * gun

                #MOBİL UYGULAMA KART YAPISI (BEYAZ)
                with st.container():
                    st.markdown('<div class="app-car-card">', unsafe_allow_html=True)
                    
                    c_left, c_right = st.columns([1.3, 1])
                    
                    with c_left:
                        st.markdown(f'<div class="car-title-app">{a["ad"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="car-subtitle-app">{a["alt_baslik"]}</div>', unsafe_allow_html=True)
                        
                        st.markdown(f'<div class="spec-item-app">⛽ {a["yakit"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="spec-item-app">🔀 {a["vites"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="spec-item-app">🛣️ {a["km"]}</div>', unsafe_allow_html=True)
                        
                        st.markdown('<div class="free-cancel-badge">✔️ ÜCRETSİZ İPTAL</div>', unsafe_allow_html=True)

                    with c_right:
                        # Görsel Entegrasyonu
                        st.image(a["resim"], use_container_width=True)

                    # TIKLANABİLİR DETAYLAR
                    with st.expander("ℹ️ Detaylar ve Donanım"):
                        st.write(f"⚙️ **Motor:** {a['motor']}")
                        st.write(f"🕹️ **Şanzıman:** {a['sanziman']}")
                        st.write(f"⛽ **Tüketim:** {a['tuketim']}")
                        st.write(f"🚀 **Hızlanma:** {a['hizlanma']}")
                        st.write("**Özellikler:** " + ", ".join(a["donanimlar"]))

                    st.markdown("<br>", unsafe_allow_html=True)

                    # FİYAT VE "HEMEN KİRALA" TURUNCU BUTON
                    c_p, c_b = st.columns([1.2, 1])
                    with c_p:
                        st.markdown(f'<div class="price-main-app">{a["fiyat"]:,} ₺</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="price-sub-app">Toplam Tutar: {toplam_tutar:,} TL ({gun} Gün)</div>', unsafe_allow_html=True)
                    
                    with c_b:
                        if st.button("Hemen Kirala", key=f"btn_{a['ad']}"):
                            st.session_state["secili"] = {
                                "ad": a["ad"],
                                "kat": a["kat"],
                                "fiyat": a["fiyat"],
                                "toplam": toplam_tutar,
                                "gun": gun,
                                "konum": konum,
                            }
                            st.rerun()

                    st.markdown('</div>', unsafe_allow_html=True)

            if musait_sayisi == 0:
                st.warning("Seçilen filtreye uygun araç bulunamadı.")

        else:
            # 🔒 REZERVASYON VE EHLİYET ONAYI
            s = st.session_state["secili"]
            u = st.session_state["user"]

            st.subheader("🔒 Rezervasyon & Ehliyet Onayı")

            with st.container():
                st.markdown(
                    f"""
                    <div class="app-car-card" style="border-left: 5px solid #FF5722 !important;">
                        <b style="color:#FF5722;">SEÇİLEN ARAÇ ÖZETİ</b>
                        <h2 style="margin:4px 0;">{s['ad']}</h2>
                        <p style="color:#64748B; font-weight:600;">📍 {s['konum']} | ⏱ {s['gun']} Gün Kiralama</p>
                        <hr style="border:0.5px solid #E2E8F0; margin:10px 0;">
                        <span style="font-size:18px; font-weight:800;">Toplam Ödenecek: </span>
                        <span style="font-size:24px; font-weight:900; color:#FF5722;">{s['toplam']:,} ₺</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with st.form("kiralama_onay_formu"):
                st.write("📄 **Ehliyet Bilgilerinizi Girin**")
                st.info("💵 Ödeme araç teslimatında nakit veya kart ile alınacaktır.")

                c_e1, c_e2 = st.columns(2)
                with c_e1:
                    ehliyet_no = st.text_input("Ehliyet Seri No", placeholder="Örn: 123456")
                with c_e2:
                    ehliyet_sinif = st.selectbox("Ehliyet Sınıfı", ["B (Binek)", "B1", "A (Motosiklet)", "C", "D"])

                dosya = st.file_uploader("📷 Ehliyet Ön Yüzü Fotoğrafı (Zorunlu)", type=["jpg", "jpeg", "png"])

                onay = st.form_submit_button("REZERVASYONU ONAYLA ➔")

                if onay:
                    if ehliyet_no.strip() and dosya is not None:
                        safe_car_name = re.sub(r"[^\w\-]", "_", s["ad"])
                        ext = os.path.splitext(dosya.name)[1]
                        foto_ad = f"{u['tc']}_{safe_car_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
                        dosya_yolu = os.path.join(UPLOAD_DIR, foto_ad)

                        with open(dosya_yolu, "wb") as f:
                            f.write(dosya.getbuffer())

                        kaydet(
                            "KİRALAMA",
                            f"Müşteri: {u['ad']} (TC:{u['tc']}) | Araç: {s['ad']} | Konum: {s['konum']} | Gün: {s['gun']} | Ehliyet No: {ehliyet_no} | Tutar: {s['toplam']} ₺ | Foto: {foto_ad}",
                        )

                        st.balloons()
                        st.success(f"🎉 Tebrikler {u['ad']}! Rezervasyonunuz oluşturuldu.")
                        st.session_state["secili"] = None
                        st.rerun()
                    else:
                        st.error("Lütfen Ehliyet Belge Seri Numarasını girin ve Fotoğraf yükleyin.")

            if st.button("⬅️ Başka Araç Seç"):
                st.session_state["secili"] = None
                st.rerun()

    with t2:
        st.subheader("📜 Kiralama Kayıtlarınız")
        u_ad = st.session_state["user"]["ad"]
        u_tc = st.session_state["user"]["tc"]

        bulundu = False
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8-sig") as f:
                for satir in f:
                    if u_tc in satir or u_ad in satir:
                        bulundu = True
                        st.markdown(
                            f"""
                            <div class="app-car-card" style="border-left: 5px solid #16A34A !important;">
                                <b style="color:#16A34A;">✓ AKTİF REZERVASYON</b>
                                <p style="margin-top:6px; font-weight:600;">{satir.strip()}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        if not bulundu:
            st.info("Henüz kayıtlı bir kiralamanız bulunmuyor.")

    with t3:
        u = st.session_state["user"]
        st.subheader("🔑 Yönetici Paneli")

        st.markdown(
            f"""
            <div class="app-car-card">
                <b>👤 Sürücü Profili:</b> {u['ad']}<br>
                <b>🆔 TC:</b> {u['tc']} | 📞 <b>Tel:</b> +90 {u['tel']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        lock = st.checkbox("Yönetici Girişi")
        if lock:
            sifre = st.text_input("Admin Şifresi", type="password")
            if sifre == ADMIN_SIFRE:
                st.success("Yetkili Girişi Onaylandı.")

                g_logs, k_logs = kayitlari_ayristir()

                c1, c2 = st.columns(2)
                with c1:
                    st.download_button("📥 Giriş Raporu", g_logs, "girisler.txt", mime="text/plain")
                with c2:
                    st.download_button("📥 Kiralama Raporu", k_logs, "kiralamalar.txt", mime="text/plain")

                st.write("---")
                st.write("<b>📷 Yüklenen Ehliyet Fotoğrafları</b>", unsafe_allow_html=True)
                fotolar = os.listdir(UPLOAD_DIR)
                if fotolar:
                    for f in fotolar:
                        f_path = os.path.join(UPLOAD_DIR, f)
                        st.image(f_path, caption=f, width=200)
                else:
                    st.info("Yüklenen fotoğraf yok.")
            elif sifre != "":
                st.error("Hatalı Şifre!")

        if st.button("ÇIKIŞ YAP"):
            st.session_state["auth"] = False
            st.session_state["user"] = {}
            st.session_state["secili"] = None
            st.rerun()
