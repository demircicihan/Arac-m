import os
import re
from datetime import datetime
import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="DriveNow Premium",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- SENSITIVE DATA / SECRETS MANAGEMENT ---
ADMIN_SIFRE = st.secrets.get("ADMIN_SIFRE", "cihan123")

# --- KLASÖR VE DOSYA KONTROLÜ ---
LOG_FILE = "kayitlar.txt"
UPLOAD_DIR = "yuklemeler"

os.makedirs(UPLOAD_DIR, exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8-sig") as f:
        f.write("")

# --- ZENGİN ARAÇ FİLOSU ---
ARACLAR = [
    {
        "ad": "Peugeot 508 GT",
        "kat": "SEDAN • PREMİUM",
        "vites": "Otomatik",
        "yakit": "Dizel",
        "fiyat": 1500,
        "puan": "4.9",
        "koltuk": "5 Koltuk",
        "bagaj": "2 Valiz",
    },
    {
        "ad": "Renault Clio",
        "kat": "HATCHBACK • EKONOMİK",
        "vites": "Manuel",
        "yakit": "Benzin",
        "fiyat": 900,
        "puan": "4.7",
        "koltuk": "5 Koltuk",
        "bagaj": "1 Valiz",
    },
    {
        "ad": "Ford Focus",
        "kat": "COMPACT • KONFOR",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "fiyat": 1200,
        "puan": "4.8",
        "koltuk": "5 Koltuk",
        "bagaj": "2 Valiz",
    },
    {
        "ad": "Fiat Egea Cross",
        "kat": "CROSSOVER • EKONOMİK",
        "vites": "Manuel",
        "yakit": "Dizel",
        "fiyat": 850,
        "puan": "4.6",
        "koltuk": "5 Koltuk",
        "bagaj": "2 Valiz",
    },
    {
        "ad": "Tesla Model 3",
        "kat": "LÜKS • %100 ELEKTRİK",
        "vites": "Otomatik",
        "yakit": "Elektrik",
        "fiyat": 2500,
        "puan": "5.0",
        "koltuk": "5 Koltuk",
        "bagaj": "3 Valiz",
    },
]

# --- TASARIM VE GÖRÜNÜRLÜK (CSS) ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(160deg, #F8FAFC 0%, #EEF2FF 50%, #F1F5F9 100%) !important;
        background-attachment: fixed !important;
    }

    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    /* TÜM YAZILAR KOYU LACİVERT */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small, strong {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", Roboto, sans-serif !important;
    }

    /* ARAMA KARTI */
    .search-card {
        background: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 22px !important;
        border: 1.5px solid #C7D2FE !important;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.08) !important;
        margin-bottom: 20px !important;
    }

    /* DETAYLI ARAÇ KARTI */
    .car-card-detailed {
        background: #FFFFFF !important;
        padding: 22px !important;
        border-radius: 24px !important;
        border: 1.5px solid #E2E8F0 !important;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06) !important;
        margin-bottom: 20px !important;
    }

    /* PASTEL ÖZELLİK ETİKETLERİ */
    .tag-vites { background: #EFF6FF !important; color: #1D4ED8 !important; font-size: 12px; font-weight: 800; padding: 5px 10px; border-radius: 8px; border: 1px solid #BFDBFE; display: inline-block; margin-right: 4px; }
    .tag-yakit { background: #FEF3C7 !important; color: #B45309 !important; font-size: 12px; font-weight: 800; padding: 5px 10px; border-radius: 8px; border: 1px solid #FDE68A; display: inline-block; margin-right: 4px; }
    .tag-koltuk { background: #F3E8FF !important; color: #6B21A8 !important; font-size: 12px; font-weight: 800; padding: 5px 10px; border-radius: 8px; border: 1px solid #E9D5FF; display: inline-block; margin-right: 4px; }
    .tag-bagaj { background: #ECFDF5 !important; color: #047857 !important; font-size: 12px; font-weight: 800; padding: 5px 10px; border-radius: 8px; border: 1px solid #A7F3D0; display: inline-block; }

    .guarantee-badge {
        background: #D1FAE5 !important;
        color: #047857 !important;
        font-weight: 800 !important;
        font-size: 12px !important;
        padding: 6px 12px !important;
        border-radius: 10px !important;
        display: inline-block !important;
        margin-top: 10px !important;
        border: 1px solid #A7F3D0 !important;
    }

    .price-row-box {
        background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 100%) !important;
        padding: 14px 18px !important;
        border-radius: 16px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-top: 14px !important;
        border: 1px solid #C7D2FE !important;
    }

    /* TURUNCU CTA BUTONLARI */
    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #FF6B00 0%, #FF5F00 100%) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        height: 52px !important;
        width: 100% !important;
        box-shadow: 0 8px 20px rgba(255, 95, 0, 0.3) !important;
        margin-top: 6px !important;
    }

    /* DOSYA YÜKLEYİCİ */
    [data-testid="stFileUploader"] section {
        background-color: #FFFFFF !important;
        border: 2px dashed #C7D2FE !important;
        border-radius: 14px !important;
        padding: 14px !important;
    }

    /* INPUT KUTULARI */
    input, .stNumberInput div, div[data-baseweb="base-input"], div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #C7D2FE !important;
        border-radius: 12px !important;
        -webkit-text-fill-color: #0F172A !important;
    }

    /* TAB DÜZENİ */
    div[data-baseweb="tab-list"] {
        background-color: rgba(199, 210, 254, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 18px !important;
        padding: 5px !important;
        border: 1px solid rgba(255,255,255,0.8) !important;
        margin-bottom: 15px !important;
    }
    div[aria-selected="true"] {
        background: #FFFFFF !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
    }

    /* VIP KART YAZI RENKLERİ OVERRIDE */
    .vip-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        padding: 24px !important;
        border-radius: 24px !important;
        box-shadow: 0 12px 30px rgba(0,0,0,0.22) !important;
        margin-bottom: 20px !important;
    }
    .vip-card * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    .vip-card .vip-tag {
        color: #93C5FD !important;
        -webkit-text-fill-color: #93C5FD !important;
    }
    .vip-card .vip-subtext {
        opacity: 0.7;
        color: #CBD5E1 !important;
        -webkit-text-fill-color: #CBD5E1 !important;
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
        <div style="text-align: center; padding: 20px 0 10px 0;">
            <div style="background: #1E293B; color: #FFF !important; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 800; display: inline-block; margin-bottom: 10px;">
                📍 Türkiye Geneli 7/24 Teslimat
            </div>
            <h1 style="font-size: 38px; font-weight: 900; margin: 0; color: #0F172A;">DriveNow</h1>
            <p style="font-size: 15px; font-weight: 600; color: #475569;">Premium Araç Kiralama Deneyimi</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        st.markdown(
            "<p style='font-size: 16px; font-weight: 800; margin-bottom: 8px;'>👋 Lütfen Bilgilerinizi Girin</p>",
            unsafe_allow_html=True,
        )
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
                    "Lütfen bilgileri eksiksiz ve doğru formatta girin (TC: 11 rakam, Tel: 10 rakam)."
                )

else:
    # --- ANA UYGULAMA (TABS) ---
    t1, t2, t3 = st.tabs(["🚗 Araç Seçimi", "📋 Kayıtlarım", "👤 Admin"])

    with t1:
        if st.session_state["secili"] is None:
            # 🔍 ARAMA & FİLTRELEME PANELİ
            st.markdown('<div class="search-card">', unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-size:16px; font-weight:900;'>👋 Merhaba, {st.session_state['user']['ad']}</div>",
                unsafe_allow_html=True,
            )

            c_loc, c_vites, c_gun = st.columns([2, 1.5, 1])
            with c_loc:
                konum = st.selectbox(
                    "📍 Teslimat Noktası",
                    [
                        "İstanbul • Sabiha Gökçen HL",
                        "İstanbul • İstanbul Havalimanı",
                        "Ankara • Esenboğa HL",
                        "İzmir • Adnan Menderes HL",
                        "Antalya • Havalimanı",
                        "Bursa • Şehir Merkezi",
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

            # 🚗 ARAÇ LİSTESİ
            musait_sayisi = 0
            for a in ARACLAR:
                if vites_filtre != "Tümü" and a["vites"] != vites_filtre:
                    continue

                musait_sayisi += 1
                toplam_tutar = a["fiyat"] * gun

                card_html = f"""
                <div class="car-card-detailed">
                    <div>
                        <span style="font-size:11px; font-weight:900; color:#2563EB; letter-spacing:0.5px;">{a['kat']}</span>
                        <span style="background:#FEF3C7; color:#B45309; font-size:12px; font-weight:900; padding:3px 8px; border-radius:8px; float:right;">★ {a['puan']}</span>
                    </div>
                    <div style="font-size:24px; font-weight:900; color:#0F172A; margin:4px 0 10px 0;">{a['ad']}</div>
                    <div style="margin-bottom:12px;">
                        <span class="tag-vites">🔀 {a['vites']}</span>
                        <span class="tag-yakit">⛽ {a['yakit']}</span>
                        <span class="tag-koltuk">👥 {a['koltuk']}</span>
                        <span class="tag-bagaj">🧳 {a['bagaj']}</span>
                    </div>
                    <div><span class="guarantee-badge">✓ Sınırsız KM • Full Kasko • Ücretsiz İptal</span></div>
                    <div class="price-row-box">
                        <div>
                            <div style="font-size:10px; font-weight:800; color:#64748B;">GÜNLÜK FİYAT</div>
                            <div style="font-size:18px; font-weight:900; color:#2563EB;">{a['fiyat']:,} ₺</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:10px; font-weight:800; color:#64748B;">{gun} GÜNLÜK TOPLAM</div>
                            <div style="font-size:22px; font-weight:900; color:#0F172A;">{toplam_tutar:,} ₺</div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

                if st.button(
                    f"Hemen Rezerve Et - {a['ad']}", key=f"btn_{a['ad']}"
                ):
                    st.session_state["secili"] = {
                        "ad": a["ad"],
                        "kat": a["kat"],
                        "fiyat": a["fiyat"],
                        "toplam": toplam_tutar,
                        "gun": gun,
                        "konum": konum,
                    }
                    st.rerun()

            if musait_sayisi == 0:
                st.warning("Seçilen vites tipine uygun araç bulunamadı.")

        else:
            # 🔒 DETAYLI KİRALAMA & KİMLİK EKRANI
            s = st.session_state["secili"]
            u = st.session_state["user"]

            st.markdown(
                "<h3 style='font-size:22px; font-weight:900;'>🔒 Kiralama ve Kimlik Doğrulama</h3>",
                unsafe_allow_html=True,
            )

            summary_html = f"""
            <div class="car-card-detailed" style="border-left: 6px solid #2563EB !important;">
                <div style="font-size:12px; font-weight:900; color:#2563EB;">SEÇİLEN ARAÇ VE DETAYLAR</div>
                <div style="font-size:24px; font-weight:900; margin:4px 0;">{s['ad']}</div>
                <div style="font-size:13px; color:#475569; font-weight:700;">📍 {s['konum']} | ⏱ {s['gun']} Günlük Kiralama</div>
                <div class="price-row-box" style="margin-top:10px;">
                    <div style="font-size:13px; font-weight:800;">Toplam Ödenecek Tutar:</div>
                    <div style="font-size:22px; font-weight:900; color:#FF6B00;">{s['toplam']:,} ₺</div>
                </div>
            </div>
            """
            st.markdown(summary_html, unsafe_allow_html=True)

            with st.form("kiralama_onay_formu"):
                st.markdown(
                    "<p style='font-size:15px; font-weight:800; margin-bottom:10px;'>📄 Ehliyet ve Doğrulama Bilgileri</p>",
                    unsafe_allow_html=True,
                )

                c_e1, c_e2 = st.columns(2)
                with c_e1:
                    ehliyet_no = st.text_input(
                        "Ehliyet Belge Seri No", placeholder="Örn: 123456"
                    )
                with c_e2:
                    ehliyet_sinif = st.selectbox(
                        "Ehliyet Sınıfı",
                        [
                            "B (Binek)",
                            "B1",
                            "A (Motosiklet)",
                            "C (Kamyon)",
                            "D (Otobüs)",
                        ],
                    )

                dosya = st.file_uploader(
                    "📷 Ehliyetinizin Ön Yüz Fotoğrafı (Zorunlu)",
                    type=["jpg", "jpeg", "png"],
                )

                onay = st.form_submit_button("KİRALAMAYI ONAYLA VE TAMAMLA ➔")

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
                            f"Müşteri: {u['ad']} (TC:{u['tc']}) | Araç: {s['ad']} | Konum: {s['konum']} | Gün: {s['gun']} | Ehliyet No: {ehliyet_no} | Sınıf: {ehliyet_sinif} | Tutar: {s['toplam']} ₺ | Foto: {foto_ad}",
                        )

                        st.balloons()
                        st.success(
                            f"🎉 Tebrikler Sayın {u['ad']}! {s['ad']} aracınız rezerve edildi."
                        )
                        st.session_state["secili"] = None
                        st.rerun()
                    else:
                        st.error(
                            "Lütfen Ehliyet Belge Numarasını girin ve Ehliyet Fotoğrafını yükleyin."
                        )

            if st.button("⬅️ Başka Araç Seç"):
                st.session_state["secili"] = None
                st.rerun()

    with t2:
        st.markdown(
            "<h3 style='font-size:20px; font-weight:900; margin-bottom:12px;'>Geçmiş Kiralama Kayıtlarınız</h3>",
            unsafe_allow_html=True,
        )
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
                            <div class="car-card-detailed" style="border-left: 6px solid #059669 !important; padding: 14px !important;">
                                <div style="font-size: 12px; color: #059669; font-weight: 900;">✓ KAYIT ONAYLANDI</div>
                                <div style="font-size: 14px; font-weight: 700; margin-top: 4px;">{satir.strip()}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        if not bulundu:
            st.info("Henüz sistemde kiralama kaydınız bulunmuyor.")

    with t3:
        u = st.session_state["user"]

        # YENİLENMİŞ VIP SÜRÜCÜ KARTI (Tüm metinler yüksek görünürlükte beyaz)
        driver_card_html = f"""
        <div class="vip-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                <span class="vip-tag" style="font-size:12px; font-weight:900; letter-spacing:2px;">DRIVENOW VIP CARD</span>
                <span style="font-size:20px;">💎</span>
            </div>
            <div class="vip-subtext" style="font-size:11px;">SÜRÜCÜ AD SOYAD</div>
            <div style="font-size:22px; font-weight:900; text-transform:uppercase; margin-bottom:14px;">{u['ad']}</div>
            <div style="display:flex; justify-content:space-between; background:rgba(255,255,255,0.1); padding:12px; border-radius:12px;">
                <div>
                    <div class="vip-subtext" style="font-size:10px;">TC NO</div>
                    <div style="font-size:14px; font-weight:800;">{u['tc']}</div>
                </div>
                <div>
                    <div class="vip-subtext" style="font-size:10px;">TELEFON</div>
                    <div style="font-size:14px; font-weight:800;">+90 {u['tel']}</div>
                </div>
            </div>
        </div>
        """
        st.markdown(driver_card_html, unsafe_allow_html=True)

        # 🔒 ŞİFRELİ YÖNETİCİ PANELİ
        lock = st.checkbox("🔒 Yönetici Paneli Girişi")
        if lock:
            sifre = st.text_input("Admin Şifresi", type="password")
            if sifre == ADMIN_SIFRE:
                st.success("Yetkili Girişi Onaylandı.")

                g_logs, k_logs = kayitlari_ayristir()

                st.markdown(
                    "<b>📄 Sistem Raporları (.txt)</b>", unsafe_allow_html=True
                )
                c1, c2 = st.columns(2)
                with c1:
                    st.download_button(
                        "📥 Giriş Yapanlar",
                        g_logs,
                        "giris_yapanlar.txt",
                        mime="text/plain",
                    )
                with c2:
                    st.download_button(
                        "📥 Kiralama Yapanlar",
                        k_logs,
                        "kiralama_kayitlari.txt",
                        mime="text/plain",
                    )

                st.markdown(
                    "<br><b>📷 Yüklenen Ehliyet Fotoğrafları</b>",
                    unsafe_allow_html=True,
                )
                fotolar = os.listdir(UPLOAD_DIR)
                if fotolar:
                    for f in fotolar:
                        f_path = os.path.join(UPLOAD_DIR, f)
                        st.image(f_path, caption=f, width=220)
                        with open(f_path, "rb") as file:
                            st.download_button(
                                f"Fotoğrafı İndir: {f}",
                                file,
                                file_name=f,
                                key=f"dl_{f}",
                            )
                else:
                    st.info("Henüz yüklenen fotoğraf yok.")

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🚨 Tüm Verileri ve Fotoğrafları Sıfırla"):
                    if os.path.exists(LOG_FILE):
                        os.remove(LOG_FILE)
                    for f in os.listdir(UPLOAD_DIR):
                        os.remove(os.path.join(UPLOAD_DIR, f))
                    st.success("Tüm veriler temizlendi!")
                    st.rerun()
            elif sifre != "":
                st.error("Hatalı Admin Şifresi!")

        if st.button("ÇIKIŞ YAP"):
            st.session_state["auth"] = False
            st.session_state["user"] = {}
            st.session_state["secili"] = None
            st.rerun()
