import os
import re
from datetime import datetime
import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="DriveNow Premium | Elite Fleet",
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

# --- DETAYLANDIRILMIŞ ULTRA ARAÇ FİLOSU (FOTOĞRAFSAN ARINDIRILMIŞ) ---
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
        "badge": "🔥 EN ÇOK TERCİH EDİLEN",
        "motor": "1.5 BlueHDi (130 HP)",
        "sanziman": "8 İleri EAT8",
        "tuketim": "4.1 Lt / 100km",
        "hizlanma": "0-100 km/s: 9.9 sn",
        "donanimlar": ["Massage Seat", "Focal® Hi-Fi", "Night Vision", "Kör Nokta"],
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
        "badge": "⚡ TEKNOLOJİ HARİKASI",
        "motor": "Dual Motor AWD (283 HP)",
        "sanziman": "Tek Vitesli Otomatik",
        "tuketim": "14.4 kWh / 100km",
        "hizlanma": "0-100 km/s: 6.1 sn",
        "donanimlar": ["Autopilot", "Cam Tavan", "15 Touchscreen", "Koltuk Isıtma"],
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
        "badge": "🌟 AİLE DOSTU",
        "motor": "1.5 Ti-VCT (123 HP)",
        "sanziman": "6 İleri Otomatik",
        "tuketim": "6.2 Lt / 100km",
        "hizlanma": "0-100 km/s: 11.2 sn",
        "donanimlar": ["SYNC 4 Ekran", "Şerit Takip", "Geri Görüş Kamerası", "Hız Sabitleyici"],
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
        "badge": "💡 ŞEHİR DOSTU",
        "motor": "1.0 TCe (90 HP)",
        "sanziman": "6 İleri Manuel",
        "tuketim": "5.0 Lt / 100km",
        "hizlanma": "0-100 km/s: 12.2 sn",
        "donanimlar": ["Apple CarPlay", "Park Sensörü", "Start-Stop", "EASYLINK"],
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
        "badge": "🛣️ UYGUN & MUKAVEMETLİ",
        "motor": "1.3 MultiJet (95 HP)",
        "sanziman": "5 İleri Manuel",
        "tuketim": "4.4 Lt / 100km",
        "hizlanma": "0-100 km/s: 12.8 sn",
        "donanimlar": ["Yüksek Sürüş Pozisyonu", "City Modu", "10 Tablet Ekran", "Tavan Çıtaları"],
    },
]

# --- MODERN CSS & ANİMASYON TASARIMI ---
st.markdown(
    """
    <style>
    /* GENEL ARKA PLAN VE FONTLAR */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 40%, #0F172A 100%) !important;
        background-attachment: fixed !important;
    }

    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    /* YAZI RENKLERİ VE TİPOGRAFİ */
    html, body, [class*="css"], label, p, h1, h2, h3, h4, h5, h6, span, div, b, small, strong {
        color: #F8FAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", Roboto, sans-serif !important;
    }

    /* GLASSMORPHISM ARAMA KARTI */
    .search-card {
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        padding: 24px !important;
        border-radius: 28px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 25px !important;
    }

    /* MODERN ARAÇ KARTI */
    .car-card-detailed {
        background: rgba(30, 41, 59, 0.65) !important;
        backdrop-filter: blur(12px) !important;
        padding: 24px !important;
        border-radius: 26px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 22px !important;
        transition: transform 0.3s ease, border-color 0.3s ease !important;
    }
    .car-card-detailed:hover {
        border-color: rgba(99, 102, 241, 0.5) !important;
        transform: translateY(-2px);
    }

    /* CANLI BADGE VE ETİKETLER */
    .badge-highlight {
        background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%) !important;
        color: #FFFFFF !important;
        font-size: 11px !important;
        font-weight: 900 !important;
        padding: 4px 12px !important;
        border-radius: 20px !important;
        display: inline-block !important;
        margin-bottom: 10px !important;
        letter-spacing: 0.5px !important;
    }

    .tag-vites { background: rgba(59, 130, 246, 0.15) !important; color: #93C5FD !important; font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 10px; border: 1px solid rgba(147, 197, 253, 0.2); display: inline-block; margin-right: 6px; margin-bottom: 6px; }
    .tag-yakit { background: rgba(245, 158, 11, 0.15) !important; color: #FDE68A !important; font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 10px; border: 1px solid rgba(253, 230, 138, 0.2); display: inline-block; margin-right: 6px; margin-bottom: 6px; }
    .tag-koltuk { background: rgba(168, 85, 247, 0.15) !important; color: #E9D5FF !important; font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 10px; border: 1px solid rgba(233, 213, 255, 0.2); display: inline-block; margin-right: 6px; margin-bottom: 6px; }
    .tag-bagaj { background: rgba(16, 185, 129, 0.15) !important; color: #A7F3D0 !important; font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 10px; border: 1px solid rgba(167, 243, 208, 0.2); display: inline-block; margin-bottom: 6px; }

    /* TEKNİK ÖZELLİK ETİKETLERİ */
    .tech-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        background: rgba(15, 23, 42, 0.4);
        padding: 12px;
        border-radius: 14px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .tech-item {
        font-size: 12px;
        color: #CBD5E1 !important;
        font-weight: 600;
    }

    .feature-chip {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #E2E8F0 !important;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-right: 4px;
        margin-top: 4px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .guarantee-badge {
        background: rgba(16, 185, 129, 0.12) !important;
        color: #34D399 !important;
        font-weight: 800 !important;
        font-size: 12px !important;
        padding: 6px 14px !important;
        border-radius: 12px !important;
        display: inline-block !important;
        border: 1px solid rgba(52, 211, 153, 0.25) !important;
    }

    .payment-notice-badge {
        background: rgba(16, 185, 129, 0.15) !important;
        color: #34D399 !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        padding: 10px 16px !important;
        border-radius: 14px !important;
        display: block !important;
        margin-bottom: 16px !important;
        border: 1px solid rgba(52, 211, 153, 0.3) !important;
    }

    /* FİYAT KUTUSU */
    .price-row-box {
        background: rgba(15, 23, 42, 0.6) !important;
        padding: 16px 20px !important;
        border-radius: 18px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-top: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* CANLI BUTONLAR (GRADIENT) */
    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #FF6B00 0%, #FF3D00 100%) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        height: 54px !important;
        width: 100% !important;
        box-shadow: 0 10px 25px rgba(255, 107, 0, 0.35) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 30px rgba(255, 107, 0, 0.5) !important;
    }

    /* İNDİRME BUTONLARI */
    [data-testid="stDownloadButton"] > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #60A5FA !important;
        -webkit-text-fill-color: #60A5FA !important;
        border: 1.5px solid rgba(96, 165, 250, 0.4) !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        height: 48px !important;
        width: 100% !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: #2563EB !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* INPUT VE SELECTBOX STİLLERİ */
    input, .stNumberInput div, div[data-baseweb="base-input"], div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #F8FAFC !important;
        border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
        -webkit-text-fill-color: #F8FAFC !important;
    }

    /* SELECTBOX POPOVER (AÇILIR MENÜ) DÜZELTMESİ */
    div[data-baseweb="popover"], div[data-baseweb="popover"] * {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        -webkit-text-fill-color: #F8FAFC !important;
    }
    ul[data-baseweb="menu"] {
        background-color: #1E293B !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
    }
    li[data-baseweb="option"] {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
    }
    li[data-baseweb="option"]:hover, li[aria-selected="true"] {
        background-color: #334155 !important;
        color: #38BDF8 !important;
        -webkit-text-fill-color: #38BDF8 !important;
    }

    /* TAB DÜZENİ */
    div[data-baseweb="tab-list"] {
        background-color: rgba(30, 41, 59, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        padding: 6px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        margin-bottom: 20px !important;
    }
    div[aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
    }
    div[aria-selected="true"] span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* VIP SÜRÜCÜ KARTI */
    .vip-card {
        background: linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%) !important;
        padding: 26px !important;
        border-radius: 26px !important;
        border: 1px solid rgba(147, 197, 253, 0.2) !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4) !important;
        margin-bottom: 20px !important;
    }
    .vip-card * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    .vip-card .vip-tag {
        color: #38BDF8 !important;
        -webkit-text-fill-color: #38BDF8 !important;
    }
    .vip-card .vip-subtext {
        opacity: 0.65;
        color: #94A3B8 !important;
        -webkit-text-fill-color: #94A3B8 !important;
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
            <div style="background: rgba(99, 102, 241, 0.15); color: #818CF8 !important; padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: 800; display: inline-block; margin-bottom: 12px; border: 1px solid rgba(129, 140, 248, 0.3);">
                📍 Türkiye Geneli VIP Adrese Delivery
            </div>
            <h1 style="font-size: 42px; font-weight: 900; margin: 0; background: linear-gradient(90deg, #FFFFFF 0%, #38BDF8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">DriveNow</h1>
            <p style="font-size: 16px; font-weight: 600; color: #94A3B8;">Ayrıcalıklı Sürüş & Premium Filo Deneyimi</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        st.markdown(
            "<p style='font-size: 17px; font-weight: 800; margin-bottom: 12px;'>👋 Hoş Geldiniz, Bilgilerinizi Girin</p>",
            unsafe_allow_html=True,
        )
        ad = st.text_input("Ad Soyad", placeholder="Örn: Cihan Demirci")
        tc = st.text_input(
            "T.C. Kimlik No", max_chars=11, placeholder="11 Haneli T.C. No"
        )
        tel = st.text_input(
            "Telefon No", max_chars=10, placeholder="5XXXXXXXXX"
        )

        submit = st.form_submit_button("LÜKS FİLOYU KEŞFET ➔")

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
    t1, t2, t3 = st.tabs(["🏎️ Araç Filosu", "📜 Kiralama Kayıtlarım", "🔑 Yönetici"])

    with t1:
        if st.session_state["secili"] is None:
            # 🔍 ARAMA & FİLTRELEME PANELİ
            st.markdown('<div class="search-card">', unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-size:18px; font-weight:900;'>👋 Keyifli Sürüşler, <span style='color:#38BDF8;'>{st.session_state['user']['ad']}</span></div>",
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

            # 🚗 DETAYLI ARAÇ LİSTESİ (HTML GÖRSEL KARTLAR)
            musait_sayisi = 0
            for a in ARACLAR:
                if vites_filtre != "Tümü" and a["vites"] != vites_filtre:
                    continue

                musait_sayisi += 1
                toplam_tutar = a["fiyat"] * gun

                chips_list = [f'<span class="feature-chip">✨ {d}</span>' for d in a["donanimlar"]]
                chips_html = "".join(chips_list)

                card_html = (
                    f'<div class="car-card-detailed">'
                    f'<div>'
                    f'<span class="badge-highlight">{a["badge"]}</span>'
                    f'<span style="background:rgba(251, 191, 36, 0.2); color:#FBBF24; font-size:12px; font-weight:900; padding:4px 10px; border-radius:10px; float:right; border: 1px solid rgba(251, 191, 36, 0.3);">★ {a["puan"]}</span>'
                    f'</div>'
                    f'<div style="font-size:11px; font-weight:900; color:#818CF8; letter-spacing:1px; margin-top:2px;">{a["kat"]}</div>'
                    f'<div style="font-size:26px; font-weight:900; color:#FFFFFF; margin:4px 0 10px 0;">{a["ad"]}</div>'
                    f'<div>'
                    f'<span class="tag-vites">🔀 {a["vites"]}</span>'
                    f'<span class="tag-yakit">⛽ {a["yakit"]}</span>'
                    f'<span class="tag-koltuk">👥 {a["koltuk"]}</span>'
                    f'<span class="tag-bagaj">🧳 {a["bagaj"]}</span>'
                    f'</div>'
                    f'<div class="tech-grid">'
                    f'<div class="tech-item">⚙️ <b>Motor:</b> {a["motor"]}</div>'
                    f'<div class="tech-item">🕹️ <b>Şanzıman:</b> {a["sanziman"]}</div>'
                    f'<div class="tech-item">⛽ <b>Tüketim:</b> {a["tuketim"]}</div>'
                    f'<div class="tech-item">🚀 <b>Hızlanma:</b> {a["hizlanma"]}</div>'
                    f'</div>'
                    f'<div style="margin-top:8px;">{chips_html}</div>'
                    f'<div style="margin-top:10px;"><span class="guarantee-badge">🟢 Anında Teslim • Sınırsız KM • Full Kasko</span></div>'
                    f'<div class="price-row-box">'
                    f'<div>'
                    f'<div style="font-size:10px; font-weight:800; color:#94A3B8;">GÜNLÜK BİRİM</div>'
                    f'<div style="font-size:20px; font-weight:900; color:#38BDF8;">{a["fiyat"]:,} ₺</div>'
                    f'</div>'
                    f'<div style="text-align:right;">'
                    f'<div style="font-size:10px; font-weight:800; color:#94A3B8;">{gun} GÜNLÜK TOPLAM</div>'
                    f'<div style="font-size:24px; font-weight:900; color:#FF6B00;">{toplam_tutar:,} ₺</div>'
                    f'</div>'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

                if st.button(
                    f"⚡ Hemen Rezerve Et - {a['ad']}", key=f"btn_{a['ad']}"
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
            # 🔒 KİRALAMA VE DOĞRULAMA
            s = st.session_state["secili"]
            u = st.session_state["user"]

            st.markdown(
                "<h3 style='font-size:22px; font-weight:900;'>🔒 Rezerve ve Ehliyet Doğrulama</h3>",
                unsafe_allow_html=True,
            )

            summary_html = (
                f'<div class="car-card-detailed" style="border-left: 6px solid #38BDF8 !important;">'
                f'<div style="font-size:12px; font-weight:900; color:#38BDF8;">SEÇTİĞİNİZ ARAÇ ÖZETİ</div>'
                f'<div style="font-size:26px; font-weight:900; margin:4px 0;">{s["ad"]}</div>'
                f'<div style="font-size:14px; color:#94A3B8; font-weight:700;">📍 {s["konum"]} | ⏱ {s["gun"]} Gün Kiralama</div>'
                f'<div class="price-row-box" style="margin-top:14px;">'
                f'<div style="font-size:14px; font-weight:800;">Toplam Ödenecek Tutar:</div>'
                f'<div style="font-size:24px; font-weight:900; color:#FF6B00;">{s["toplam"]:,} ₺</div>'
                f'</div>'
                f'</div>'
            )
            st.markdown(summary_html, unsafe_allow_html=True)

            with st.form("kiralama_onay_formu"):
                st.markdown(
                    "<p style='font-size:16px; font-weight:800; margin-bottom:6px;'>📄 Ehliyet ve Onay Bilgileri</p>",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    '<span class="payment-notice-badge">💵 Ödeme İşlemi: Toplam tutar araç teslimatı sırasında nakit veya kredi kartı ile tahsil edilecektir.</span>',
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

                onay = st.form_submit_button("REZERVASYONU ONAYLA VE TAMAMLA ➔")

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
                            f"🎉 Tebrikler Sayın {u['ad']}! {s['ad']} aracınız başarıyla rezerve edildi."
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
                            f'<div class="car-card-detailed" style="border-left: 6px solid #10B981 !important; padding: 16px !important;">'
                            f'<div style="font-size: 12px; color: #34D399; font-weight: 900;">✓ KAYIT AKTİF</div>'
                            f'<div style="font-size: 14px; font-weight: 700; margin-top: 6px;">{satir.strip()}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

        if not bulundu:
            st.info("Henüz sistemde kiralama kaydınız bulunmuyor.")

    with t3:
        u = st.session_state["user"]

        # VIP SÜRÜCÜ KARTI
        driver_card_html = (
            f'<div class="vip-card">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">'
            f'<span class="vip-tag" style="font-size:12px; font-weight:900; letter-spacing:2px;">DRIVENOW VIP MEMBER</span>'
            f'<span style="font-size:20px;">💎</span>'
            f'</div>'
            f'<div class="vip-subtext" style="font-size:11px;">SÜRÜCÜ AD SOYAD</div>'
            f'<div style="font-size:24px; font-weight:900; text-transform:uppercase; margin-bottom:16px;">{u["ad"]}</div>'
            f'<div style="display:flex; justify-content:space-between; background:rgba(255,255,255,0.06); padding:14px; border-radius:14px; border:1px solid rgba(255,255,255,0.08);">'
            f'<div>'
            f'<div class="vip-subtext" style="font-size:10px;">TC NO</div>'
            f'<div style="font-size:14px; font-weight:800;">{u["tc"]}</div>'
            f'</div>'
            f'<div>'
            f'<div class="vip-subtext" style="font-size:10px;">TELEFON</div>'
            f'<div style="font-size:14px; font-weight:800;">+90 {u["tel"]}</div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(driver_card_html, unsafe_allow_html=True)

        # 🔒 YÖNETİCİ PANELİ
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
                        st.image(f_path, caption=f, width=240)
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
