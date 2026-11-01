import os
import re
import io
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pywhatkit as kit

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="DriveNow Premium | Elite Fleet",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- SECRETS MANAGEMENT & AYARLAR ---
ADMIN_SIFRE = st.secrets.get("ADMIN_SIFRE", "cihan123")
GMAIL_ADRES = "sirket_epostaniz@gmail.com"  # E-posta gönderecek şirket hesabı
GMAIL_SIFRE = "uygulama_sifresi_buraya"       # Gmail Uygulama Şifresi (App Password)

# --- KLASÖR VE DOSYA KONTROLÜ ---
LOG_FILE = "kayitlar.txt"
UPLOAD_DIR = "yuklemeler"
DB_FILE = "drivenow.db"

os.makedirs(UPLOAD_DIR, exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8-sig") as f:
        f.write("")

# --- VERİTABANI (SQLite) BAŞLATMA ---
def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS kiralamalar 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, tc TEXT, ad TEXT, tel TEXT, email TEXT, 
                 arac TEXT, konum TEXT, bas_tarih DATE, bit_tarih DATE, gun INTEGER, 
                 toplam_tutar REAL, durum TEXT, olusturma_tarihi DATETIME)''')
    c.execute('''CREATE TABLE IF NOT EXISTS iadeler 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, kiralama_id INTEGER, 
                 km INTEGER, hasar_durumu TEXT, notlar TEXT, foto_yolu TEXT)''')
    conn.commit()
    return conn, c

conn, c = init_db()

# --- HARİTA KOORDİNATLARI ---
LOKASYONLAR = {
    "Konya • Ereğli Merkez / KYK Yurdu": [37.5133, 34.0525],
    "Konya • Ereğli Otogar & Tren Garı": [37.5250, 34.0450],
    "Konya • Çumra İlçe Merkezi": [37.5744, 32.7744],
    "Konya • Selçuklu / Otogar": [37.9535, 32.5100],
    "Konya • Zafer / Alaaddin Merkez": [37.8713, 32.4846],
    "Konya • Havalimanı (KYA)": [37.9790, 32.5619],
    "İstanbul • Sabiha Gökçen Havalimanı (SAW)": [40.8983, 29.3092],
    "İstanbul • İstanbul Havalimanı (IST)": [41.2753, 28.7519],
    "Ankara • Esenboğa Havalimanı (ESB)": [40.1281, 32.9951],
    "İzmir • Adnan Menderes Havalimanı (ADB)": [38.2924, 27.1570],
    "Antalya • Havalimanı (AYT) Dış/İç Hatlar": [36.9000, 30.7990],
}

# --- TÜRKÇE KARAKTER DÜZELTME FİLTRESİ ---
def tr_duzelt(metin):
    if not isinstance(metin, str):
        return str(metin)
    tr_harfler = "ıİğĞüÜşŞöÖçÇ"
    en_harfler = "iIgGuUsSoOcC"
    ceviri_tablosu = str.maketrans(tr_harfler, en_harfler)
    return metin.translate(ceviri_tablosu)

# --- GERÇEK ZAMANLI MÜSAİTLİK KONTROLÜ ---
def araba_musait_mi(arac_ad, bas_tarih, bit_tarih):
    c.execute('''SELECT id FROM kiralamalar 
                 WHERE arac = ? AND durum = 'Aktif' 
                 AND (? <= bit_tarih AND ? >= bas_tarih)''', 
              (arac_ad, bas_tarih.strftime("%Y-%m-%d"), bit_tarih.strftime("%Y-%m-%d")))
    return len(c.fetchall()) == 0

# --- PDF FATURA OLUŞTURMA FONKSİYONU ---
def pdf_fatura_olustur(musteri_ad, tc, tel, arac_ad, konum, bas_tarih, bit_tarih, gun, toplam_tutar, ekler):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, 750, tr_duzelt("DRIVENOW PREMIUM RENTALS - REZERVASYON OZETI"))
    p.line(50, 740, 550, 740)
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 710, tr_duzelt(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M')}"))
    p.drawString(50, 690, tr_duzelt(f"Musteri Ad Soyad: {musteri_ad}"))
    p.drawString(50, 670, tr_duzelt(f"TC Kimlik No: {tc}"))
    p.drawString(50, 650, tr_duzelt(f"Telefon: {tel}"))
    
    p.line(50, 635, 550, 635)
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 610, tr_duzelt("KIRALAMA VE ARAC BILGILERI"))
    p.setFont("Helvetica", 12)
    p.drawString(50, 585, tr_duzelt(f"Arac Modeli: {arac_ad}"))
    p.drawString(50, 565, tr_duzelt(f"Teslimat Noktasi: {konum}"))
    p.drawString(50, 545, tr_duzelt(f"Tarihler: {bas_tarih.strftime('%d.%m.%Y')} - {bit_tarih.strftime('%d.%m.%Y')} ({gun} Gun)"))
    
    if ekler:
        p.drawString(50, 525, tr_duzelt(f"Ekstra Hizmetler: {', '.join(ekler)}"))
    
    p.line(50, 505, 550, 505)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 475, tr_duzelt(f"TOPLAM TUTAR: {toplam_tutar:,.0f} TL"))
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 450, tr_duzelt("* Odeme arac teslimatinda nakit veya kredi karti ile yapilacaktir."))
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# --- E-POSTA GÖNDERİM FONKSİYONU ---
def eposta_gonder(alici_email, pdf_buffer, musteri_adi):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'DriveNow Premium - Rezervasyon Faturanız'
        msg['From'] = GMAIL_ADRES
        msg['To'] = alici_email
        msg.set_content(f"Merhaba {musteri_adi},\n\nRezervasyonunuz basariyla onaylanmistir. Fatura ve kiralama detaylariniz ekteki PDF dosyasinda yer almaktadir.\n\nIyi yolculuklar dileriz.")
        
        pdf_data = pdf_buffer.read()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='DriveNow_Fatura.pdf')
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_ADRES, GMAIL_SIFRE)
            smtp.send_message(msg)
        return True
    except Exception as e:
        return False

# --- ARAÇ FİLOSU ---
ARACLAR = [
    {
        "ad": "Fiat Egea Cross Lounge",
        "kat": "CROSSOVER • EKONOMİK",
        "vites": "Manuel",
        "yakit": "Dizel",
        "fiyat": 1250,
        "puan": "4.6",
        "koltuk": "5 Koltuk",
        "bagaj": "440 Lt",
        "badge": "🛣️ UYGUN & MUKAVEMETLİ",
        "motor": "1.3 MultiJet II (95 HP / 200 Nm)",
        "sanziman": "5 İleri Manuel",
        "tuketim": "4.4 Lt / 100km",
        "hizlanma": "0-100 km/s: 12.8 sn",
        "azami_hiz": "173 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": ["Yüksek Sürüş Pozisyonu", "City Direksiyon Modu", "10 Inc Tablet Ekran", "Tavan Çıtaları & LED Farlar", "Geri Görüş Kamerası"],
    },
    {
        "ad": "Renault Clio R.S. Line",
        "kat": "HATCHBACK • EKONOMİK",
        "vites": "Manuel",
        "yakit": "Benzin",
        "fiyat": 1350,
        "puan": "4.7",
        "koltuk": "5 Koltuk",
        "bagaj": "391 Lt",
        "badge": "💡 ŞEHİR DOSTU",
        "motor": "1.0 TCe Turbo (90 HP / 160 Nm)",
        "sanziman": "6 İleri Manuel",
        "tuketim": "5.0 Lt / 100km",
        "hizlanma": "0-100 km/s: 12.2 sn",
        "azami_hiz": "180 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": ["Apple CarPlay & Android Auto", "Ön & Arka Park Sensörü", "Start-Stop Sistemi", "EASYLINK 9.3 Inc Ekran", "Digital Gösterge Paneli"],
    },
    {
        "ad": "Ford Focus ST-Line",
        "kat": "COMPACT • KONFOR",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "fiyat": 1800,
        "puan": "4.8",
        "koltuk": "5 Koltuk",
        "bagaj": "392 Lt",
        "badge": "🌟 AİLE DOSTU",
        "motor": "1.5 Ti-VCT Ecoboost (123 HP / 153 Nm)",
        "sanziman": "6 İleri Tam Otomatik",
        "tuketim": "6.2 Lt / 100km",
        "hizlanma": "0-100 km/s: 11.2 sn",
        "azami_hiz": "195 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": ["SYNC 4 13.2 Inc Ekran", "Şerit Takip ve Destek", "180° Geri Görüş Kamerası", "Kablosuz Şarj", "ST-Line Gövde Kiti"],
    },
    {
        "ad": "Volkswagen Tiguan R-Line",
        "kat": "SUV • PREMİUM KONFOR",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "fiyat": 2800,
        "puan": "4.8",
        "koltuk": "5 Koltuk",
        "bagaj": "615 Lt",
        "badge": "🏕️ PREMİUM SUV",
        "motor": "1.5 TSI ACT (150 HP / 250 Nm)",
        "sanziman": "7 İleri DSG Otomatik",
        "tuketim": "5.7 Lt / 100km",
        "hizlanma": "0-100 km/s: 9.2 sn",
        "azami_hiz": "202 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": ["IQ.LIGHT Matrix LED Farlar", "Digital Cockpit Pro", "Panoramik Açılır Tavan", "3 Bölgeli Tam Otomatik Klima", "Bagaj Elektrikli Açılır"],
    },
    {
        "ad": "Peugeot 508 GT",
        "kat": "SEDAN • PREMİUM",
        "vites": "Otomatik",
        "yakit": "Dizel",
        "fiyat": 2600,
        "puan": "4.9",
        "koltuk": "5 Koltuk",
        "bagaj": "487 Lt",
        "badge": "🔥 EN ÇOK TERCİH EDİLEN",
        "motor": "1.5 BlueHDi (130 HP / 300 Nm Torque)",
        "sanziman": "8 İleri Tam Otomatik EAT8",
        "tuketim": "4.1 Lt / 100km",
        "hizlanma": "0-100 km/s: 9.9 sn",
        "azami_hiz": "208 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": ["Massage Seat", "Focal® Hi-Fi Ses Sistemi", "Night Vision Gece Görüşü", "Kör Nokta Uyarı", "Adaptif Hız Sabitleyici"],
    },
    {
        "ad": "Tesla Model 3 Performance",
        "kat": "LÜKS • %100 ELEKTRİK",
        "vites": "Otomatik",
        "yakit": "Elektrik",
        "fiyat": 3800,
        "puan": "5.0",
        "koltuk": "5 Koltuk",
        "bagaj": "561 Lt",
        "badge": "⚡ TEKNOLOJİ HARİKASI",
        "motor": "Dual Motor AWD (510 HP / 660 Nm Torque)",
        "sanziman": "Tek Vitesli Otomatik Direct Drive",
        "tuketim": "14.4 kWh / 100km (Menzil: 528 km)",
        "hizlanma": "0-100 km/s: 3.1 sn",
        "azami_hiz": "261 km/s",
        "cekis": "Dört Çeker (AWD)",
        "donanimlar": ["Full Self-Driving Autopilot", "Panoramik Cam Tavan", "15.4 Inc Touchscreen", "Koltuk & Direksiyon Isıtma", "Sentry Mode Güvenlik"],
    },
    {
        "ad": "BMW 420i Gran Coupé M Sport",
        "kat": "COUPE • PREMİUM SPOR",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "fiyat": 4200,
        "puan": "4.9",
        "koltuk": "5 Koltuk",
        "bagaj": "470 Lt",
        "badge": "💎 PREMİUM SPOR",
        "motor": "2.0 BMW TwinPower Turbo (170 HP / 250 Nm)",
        "sanziman": "8 İleri Steptronic Spor Otomatik",
        "tuketim": "6.6 Lt / 100km",
        "hizlanma": "0-100 km/s: 7.9 sn",
        "azami_hiz": "230 km/s",
        "cekis": "Arkadan İtiş (RWD)",
        "donanimlar": ["M Aerodinamik Paket", "Harman Kardon® Ses Sistemi", "BMW Curved Display", "Head-Up Display", "Lazer Far"],
    },
    {
        "ad": "Mercedes-Benz C200 4MATIC",
        "kat": "SEDAN • LÜKS KONFOR",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "fiyat": 4500,
        "puan": "4.9",
        "koltuk": "5 Koltuk",
        "bagaj": "455 Lt",
        "badge": "👑 KONFORUN SİMGESİ",
        "motor": "1.5 Mild-Hybrid Turbo (204 HP + 20 HP EQ)",
        "sanziman": "9G-TRONIC Otomatik",
        "tuketim": "6.4 Lt / 100km",
        "hizlanma": "0-100 km/s: 7.1 sn",
        "azami_hiz": "241 km/s",
        "cekis": "Dört Çeker (4MATIC)",
        "donanimlar": ["MBUX 11.9 Inc Dikey Ekran", "64 Renk Ambiyans Aydınlatma", "Burmester® 3D Ses", "Hafızalı Elektrikli Koltuklar", "Otonom Sürüş Destek"],
    },
    {
        "ad": "Audi A5 Cabriolet S-Line",
        "kat": "CABRIO • PREMİUM LÜKS",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "fiyat": 4900,
        "puan": "4.9",
        "koltuk": "4 Koltuk",
        "bagaj": "370 Lt",
        "badge": "☀️ ÜSTÜ AÇIK LÜKS",
        "motor": "2.0 40 TFSI Mild-Hybrid (204 HP / 320 Nm)",
        "sanziman": "7 İleri S tronic Otomatik",
        "tuketim": "6.3 Lt / 100km",
        "hizlanma": "0-100 km/s: 7.5 sn",
        "azami_hiz": "237 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": ["Otomatik Açılır Kumaş Tavan", "Virtual Cockpit Plus", "Bang & Olufsen 3D Sound", "Ense Isıtma Sistemi", "Matrix LED Farlar"],
    },
    {
        "ad": "Porsche Macan GTS",
        "kat": "SUV • LÜKS SPOR",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "fiyat": 7500,
        "puan": "5.0",
        "koltuk": "5 Koltuk",
        "bagaj": "488 Lt",
        "badge": "🏎️ ULTRA PERFORMANS",
        "motor": "2.9 V6 Twin-Turbo (440 HP / 550 Nm)",
        "sanziman": "7 İleri PDK Çift Kavrama",
        "tuketim": "9.9 Lt / 100km",
        "hizlanma": "0-100 km/s: 4.3 sn",
        "azami_hiz": "272 km/s",
        "cekis": "Dört Çeker (AWD)",
        "donanimlar": ["Spor Ekzoz Sistemi", "PASM Havalı Süspansiyon", "BOSE® Surround Sound", "GTS Spor Koltuklar", "Sport Chrono Paket"],
    },
]

# --- MODERN CSS TASARIMI ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 40%, #0F172A 100%) !important;
        background-attachment: fixed !important;
    }

    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    html, body, label, p, h1, h2, h3, h4, h5, h6, span, div, b, small, strong {
        color: #F8FAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", Roboto, sans-serif !important;
    }

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

    .car-card-detailed {
        background: rgba(30, 41, 59, 0.65) !important;
        backdrop-filter: blur(12px) !important;
        padding: 24px !important;
        border-radius: 26px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 12px !important;
        transition: transform 0.3s ease, border-color 0.3s ease !important;
    }
    .car-card-detailed:hover {
        border-color: rgba(99, 102, 241, 0.5) !important;
        transform: translateY(-2px);
    }

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

    .tech-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        background: rgba(15, 23, 42, 0.5);
        padding: 14px;
        border-radius: 14px;
        margin: 12px 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .tech-item {
        font-size: 12px;
        color: #CBD5E1 !important;
        font-weight: 600;
    }

    .feature-chip {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #E2E8F0 !important;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 8px;
        display: inline-block;
        margin-right: 6px;
        margin-top: 6px;
        border: 1px solid rgba(255, 255, 255, 0.1);
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

    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        margin-bottom: 15px !important;
    }

    div[data-testid="stExpander"] summary span[data-testid="stIconMaterial"] {
        display: none !important;
    }

    div[data-testid="stExpander"] summary svg {
        display: none !important;
    }

    div[data-testid="stExpander"] summary p {
        font-weight: 700 !important;
        font-size: 14px !important;
        color: #38BDF8 !important;
    }

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

    input, .stNumberInput div, div[data-baseweb="base-input"], div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #F8FAFC !important;
        border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
        -webkit-text-fill-color: #F8FAFC !important;
    }

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

# --- KAYIT SİSTEMİ FONKSİYONLARI (.TXT) ---
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
for k in ["auth", "user", "secili", "tamamlandi", "tarihler", "son_rezervasyon"]:
    if k not in st.session_state: 
        st.session_state[k] = None if k in ["secili", "tarihler", "son_rezervasyon"] else (False if k in ["auth", "tamamlandi"] else {})

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
        tc = st.text_input("T.C. Kimlik No", max_chars=11, placeholder="11 Haneli T.C. No")
        tel = st.text_input("Telefon No", max_chars=10, placeholder="5XXXXXXXXX (Başına 0 Koymadan)")
        email = st.text_input("E-Posta Adresi (Fatura otomatik gönderimi için)")

        submit = st.form_submit_button("LÜKS FİLOYU KEŞFET ➔")

        if submit:
            tc_clean = tc.strip()
            tel_clean = tel.strip()
            if ad.strip() and len(tc_clean) == 11 and tc_clean.isdigit() and len(tel_clean) == 10 and tel_clean.isdigit() and "@" in email:
                st.session_state["auth"] = True
                st.session_state["user"] = {"ad": ad.strip(), "tc": tc_clean, "tel": tel_clean, "email": email.strip()}
                kaydet("GİRİŞ", f"Ad: {ad.strip()} - TC: {tc_clean} - Tel: {tel_clean} - Email: {email.strip()}")
                st.rerun()
            else:
                st.error("Lütfen bilgileri eksiksiz ve doğru formatta girin (TC: 11 rakam, Tel: 10 rakam, Geçerli E-posta).")

else:
    # --- ANA UYGULAMA (TABS) ---
    t1, t2, t3 = st.tabs(["🏎️ Araç Filosu", "📜 Kiralama Kayıtlarım & Yorum Yap", "🔑 Yönetici"])

    with t1:
        if st.session_state["secili"] is None:
            # 🔍 ARAMA & TARİH SEÇİM PANELİ
            st.markdown('<div class="search-card">', unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:18px; font-weight:900;'>👋 Keyifli Sürüşler, <span style='color:#38BDF8;'>{st.session_state['user']['ad']}</span></div>", unsafe_allow_html=True)

            c_loc, c_vites = st.columns([2, 1.5])
            with c_loc:
                konum = st.selectbox("📍 Teslimat Noktası", list(LOKASYONLAR.keys()))
            with c_vites:
                vites_filtre = st.selectbox("🔀 Vites Tipi", ["Tümü", "Otomatik", "Manuel"])

            # Harita Entegrasyonu
            if konum in LOKASYONLAR:
                df_map = pd.DataFrame([{"lat": LOKASYONLAR[konum][0], "lon": LOKASYONLAR[konum][1]}])
                st.map(df_map, zoom=12, use_container_width=True)

            # 📅 TARİH ARALIĞI SEÇİMİ
            c_t1, c_t2 = st.columns(2)
            with c_t1:
                bas_tarih = st.date_input("📅 Alış Tarihi", datetime.now() + timedelta(days=1))
            with c_t2:
                bit_tarih = st.date_input("📅 İade Tarihi", datetime.now() + timedelta(days=2))

            gun = (bit_tarih - bas_tarih).days
            if gun <= 0:
                st.error("⚠️ İade tarihi alış tarihinden sonra olmalıdır!")
                gun = 1
            else:
                st.info(f"⏱️ Toplam Kiralama Süresi: **{gun} Gün**")

            st.markdown("</div>", unsafe_allow_html=True)

            # Dinamik İndirim Algoritması (7 gün ve üzeri kiralamalara %15 indirim)
            indirim_orani = 0.85 if gun >= 7 else 1.0
            if gun >= 7: 
                st.success(f"🎉 {gun} Günlük Uzun Dönem Kiralama: Otomatik %15 İndirim Uygulandı!")

            # 🚗 ARAÇ LİSTESİ VE GERÇEK ZAMANLI MÜSAİTLİK
            musait_sayisi = 0
            for a in ARACLAR:
                if vites_filtre != "Tümü" and a["vites"] != vites_filtre:
                    continue

                musait_sayisi += 1
                musait_mi = araba_musait_mi(a["ad"], bas_tarih, bit_tarih)
                gunluk_fiyat = a["fiyat"] * indirim_orani
                toplam_tutar = gunluk_fiyat * gun

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
                    f'<div style="margin-top:10px;">'
                    f'<span class="guarantee-badge">{"🟢 Seçilen Tarihlerde Müsait" if musait_mi else "🔴 Seçilen Tarihlerde Dolu"}</span>'
                    f'</div>'
                    f'<div class="price-row-box">'
                    f'<div>'
                    f'<div style="font-size:10px; font-weight:800; color:#94A3B8;">GÜNLÜK PİYASA DEĞERİ</div>'
                    f'<div style="font-size:20px; font-weight:900; color:#38BDF8;">{gunluk_fiyat:,.0f} ₺</div>'
                    f'</div>'
                    f'<div style="text-align:right;">'
                    f'<div style="font-size:10px; font-weight:800; color:#94A3B8;">{gun} GÜNLÜK TOPLAM</div>'
                    f'<div style="font-size:24px; font-weight:900; color:#FF6B00;">{toplam_tutar:,.0f} ₺</div>'
                    f'</div>'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

                with st.expander("🔻 Teknik Özellikler ve Donanımları Gör"):
                    st.markdown(
                        f"""
                        <div class="tech-grid">
                            <div class="tech-item">⚙️ <b>Motor & Güç:</b> {a['motor']}</div>
                            <div class="tech-item">🕹️ <b>Şanzıman:</b> {a['sanziman']}</div>
                            <div class="tech-item">⛽ <b>Ort. Tüketim:</b> {a['tuketim']}</div>
                            <div class="tech-item">🚀 <b>0-100 km/s:</b> {a['hizlanma']}</div>
                            <div class="tech-item">🏁 <b>Maks. Hız:</b> {a['azami_hiz']}</div>
                            <div class="tech-item">🏎️ <b>Çekiş Tipi:</b> {a['cekis']}</div>
                        </div>
                        <div style="margin-top:8px; margin-bottom:12px;">
                            <b style="font-size:12px; color:#93C5FD;">Öne Çıkan Lüks Donanımlar:</b><br>{chips_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                if musait_mi:
                    if st.button(f"⚡ Hemen Rezerve Et - {a['ad']}", key=f"btn_{a['ad']}"):
                        st.session_state["secili"] = {
                            "ad": a["ad"],
                            "kat": a["kat"],
                            "fiyat": gunluk_fiyat,
                            "toplam": toplam_tutar,
                            "gun": gun,
                            "konum": konum,
                            "bas_tarih": bas_tarih,
                            "bit_tarih": bit_tarih
                        }
                        st.session_state["tamamlandi"] = False
                        st.rerun()

                st.write("")

            if musait_sayisi == 0:
                st.warning("Seçilen vites tipine uygun araç bulunamadı.")

        else:
            # 🔒 REZERVE, KUPON VE EKSTRA HİZMETLER
            s = st.session_state["secili"]
            u = st.session_state["user"]

            st.markdown("<h3 style='font-size:22px; font-weight:900;'>🔒 Rezerve, Kupon ve Doğrulama</h3>", unsafe_allow_html=True)

            summary_html = (
                f'<div class="car-card-detailed" style="border-left: 6px solid #38BDF8 !important;">'
                f'<div style="font-size:12px; font-weight:900; color:#38BDF8;">SEÇTİĞİNİZ ARAÇ ÖZETİ</div>'
                f'<div style="font-size:26px; font-weight:900; margin:4px 0;">{s["ad"]}</div>'
                f'<div style="font-size:14px; color:#94A3B8; font-weight:700;">📍 {s["konum"]} | ⏱ {s["gun"]} Gün ({s["bas_tarih"].strftime("%d.%m.%Y")} - {s["bit_tarih"].strftime("%d.%m.%Y")})</div>'
                f'</div>'
            )
            st.markdown(summary_html, unsafe_allow_html=True)

            st.markdown("<b>🎟️ Promosyon / Kupon Kodu</b>", unsafe_allow_html=True)
            promo_kod = st.text_input("Kupon Kodu Giriniz (Örn: SUPRIZ10)", placeholder="İndirim kuponu...")

            st.markdown("<b>✨ Ekstra Hizmet Paketleri (İsteğe Bağlı)</b>", unsafe_allow_html=True)
            e_bebek = st.checkbox("👶 Bebek Koltuğu (+150 TL/Gün)")
            e_wifi = st.checkbox("🌐 Araç İçi Taşınabilir Wi-Fi Kit (+100 TL/Gün)")
            e_sigorta = st.checkbox("🛡️ Sınırsız Muafiyetsiz Kasko Güvencesi (+300 TL/Gün)")

            ek_tutar = 0
            secilen_ekler = []
            if e_bebek:
                ek_tutar += 150 * s["gun"]
                secilen_ekler.append("Bebek Koltuğu")
            if e_wifi:
                ek_tutar += 100 * s["gun"]
                secilen_ekler.append("Wi-Fi Kit")
            if e_sigorta:
                ek_tutar += 300 * s["gun"]
                secilen_ekler.append("Full Kasko")

            genel_toplam = s["toplam"] + ek_tutar
            if promo_kod.strip().upper() == "SUPRIZ10":
                genel_toplam *= 0.90
                st.success("🎉 SUPRIZ10 Kuponu Uygulandı: %10 Ek İndirim Kazandınız!")

            st.markdown(
                f'<div class="price-row-box">'
                f'<div style="font-size:14px; font-weight:800;">Nihai Toplam Tutar:</div>'
                f'<div style="font-size:24px; font-weight:900; color:#FF6B00;">{genel_toplam:,.0f} ₺</div>'
                f'</div><br>',
                unsafe_allow_html=True
            )

            # FORMU ÇALIŞTIRMA VE VERİ ALMA
            if not st.session_state["tamamlandi"]:
                with st.form("kiralama_onay_formu"):
                    c_e1, c_e2 = st.columns(2)
                    with c_e1:
                        ehliyet_no = st.text_input("Ehliyet Belge Seri No", placeholder="Örn: 123456")
                    with c_e2:
                        ehliyet_sinif = st.selectbox("Ehliyet Sınıfı", ["B (Binek)", "B1", "A (Motosiklet)", "C (Kamyon)", "D (Otobüs)"])

                    dosya = st.file_uploader("📷 Ehliyetinizin Ön Yüz Fotoğrafı (Zorunlu)", type=["jpg", "jpeg", "png"])
                    onay = st.form_submit_button("REZERVASYONU ONAYLA VE TAMAMLA ➔")

                    if onay:
                        if ehliyet_no.strip() and dosya is not None:
                            safe_car_name = re.sub(r"[^\w\-]", "_", s["ad"])
                            ext = os.path.splitext(dosya.name)[1]
                            foto_ad = f"{u['tc']}_{safe_car_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
                            dosya_yolu = os.path.join(UPLOAD_DIR, foto_ad)

                            with open(dosya_yolu, "wb") as f:
                                f.write(dosya.getbuffer())

                            # TXT Loglama
                            kaydet(
                                "KİRALAMA",
                                f"Müşteri: {u['ad']} (TC:{u['tc']}) | Araç: {s['ad']} | Konum: {s['konum']} | Gün: {s['gun']} | Tutar: {genel_toplam:,.0f} ₺ | Foto: {foto_ad}",
                            )

                            # SQLite Veritabanına Kaydet (Müsaitlik kilidi için kritik)
                            c.execute('''INSERT INTO kiralamalar 
                                         (tc, ad, tel, email, arac, konum, bas_tarih, bit_tarih, gun, toplam_tutar, durum, olusturma_tarihi) 
                                         VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                                      (u["tc"], u["ad"], u["tel"], u["email"], s["ad"], s["konum"], 
                                       s["bas_tarih"].strftime("%Y-%m-%d"), s["bit_tarih"].strftime("%Y-%m-%d"), 
                                       s["gun"], genel_toplam, "Aktif", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            conn.commit()

                            st.session_state["tamamlandi"] = True
                            st.session_state["son_rezervasyon"] = {
                                "toplam": genel_toplam,
                                "ekler": secilen_ekler
                            }
                            st.rerun()
                        else:
                            st.error("Lütfen Ehliyet Belge Numarasını girin ve Ehliyet Fotoğrafını yükleyin.")

            # REZERVASYON TAMAMLANDIKTAN SONRA İŞLEMLER (PDF VE E-POSTA)
            if st.session_state["tamamlandi"]:
                st.balloons()
                st.success(f"🎉 Tebrikler Sayın {u['ad']}! Rezervasyonunuz başarıyla oluşturuldu ve sisteme işlendi.")

                res_info = st.session_state["son_rezervasyon"]

                # 📄 PDF FATURA OLUŞTURMA
                pdf_file = pdf_fatura_olustur(u['ad'], u['tc'], u['tel'], s['ad'], s['konum'], s['bas_tarih'], s['bit_tarih'], s['gun'], res_info['toplam'], res_info['ekler'])

                # 📧 E-POSTA İLE FATURA GÖNDERİMİ
                if eposta_gonder(u['email'], pdf_file, u['ad']):
                    st.info(f"📧 Rezervasyon faturanız başarıyla {u['email']} adresine gönderildi.")
                else:
                    st.warning("⚠️ E-posta gönderilemedi. Lütfen kod içerisindeki Gmail ayarlarınızı kontrol edin.")

                st.download_button("📄 Rezervasyon Faturasını İndir (PDF)", pdf_file, file_name=f"fatura_{u['tc']}.pdf", mime="application/pdf")

            if st.button("⬅️ Başka Araç Seç"):
                st.session_state["secili"] = None
                st.session_state["tamamlandi"] = False
                st.rerun()

    with t2:
        st.markdown("<h3 style='font-size:20px; font-weight:900; margin-bottom:12px;'>Geçmiş Kiralama Kayıtlarınız</h3>", unsafe_allow_html=True)
        u_ad = st.session_state["user"]["ad"]
        u_tc = st.session_state["user"]["tc"]

        # SQLite üzerinden geçmiş kayıtları çekme
        df_gecmis = pd.read_sql_query(f"SELECT arac, konum, bas_tarih, bit_tarih, toplam_tutar, durum FROM kiralamalar WHERE tc = '{u_tc}'", conn)
        if not df_gecmis.empty:
            st.dataframe(df_gecmis, use_container_width=True)
        else:
            st.info("Henüz sistemde kiralama kaydınız bulunmuyor.")

        # ⭐️ YORUM VE PUANLAMA SEKTÖRÜ
        st.markdown("<br><b>⭐️ Deneyiminizi Değerlendirin & Yorum Yapın</b>", unsafe_allow_html=True)
        with st.form("yorum_formu"):
            sec_arac = st.selectbox("Değerlendirilecek Araç", [a["ad"] for a in ARACLAR])
            puan = st.slider("Puanınız", 1, 5, 5)
            yorum = st.text_area("Yorumunuz")
            y_submit = st.form_submit_button("Yorumu Gönder")

            if y_submit and yorum.strip():
                kaydet("YORUM", f"Müşteri: {u_ad} | Araç: {sec_arac} | Puan: {puan}★ | Yorum: {yorum.strip()}")
                st.success("Yorumunuz ve değerlendirmeniz başarıyla iletildi!")

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

        # 🔒 YÖNETİCİ PANELİ & GRAFİKLİ ANALİZ
        lock = st.checkbox("🔒 Yönetici Paneli Girişi")
        if lock:
            sifre = st.text_input("Admin Şifresi", type="password")
            if sifre == ADMIN_SIFRE:
                st.success("Yetkili Girişi Onaylandı.")

                # 📲 YÖNETİCİ KONTROLLÜ WHATSAPP ONAY MERKEZİ
                st.markdown("<b>📱 Admin WhatsApp Onay Merkezi</b>", unsafe_allow_html=True)
                bekleyen_rez = pd.read_sql_query("SELECT id, ad, tel, arac, bas_tarih, bit_tarih, toplam_tutar FROM kiralamalar WHERE durum='Aktif'", conn)
                
                if not bekleyen_rez.empty:
                    secilen_rez = st.selectbox(
                        "Onay Mesajı Gönderilecek Rezervasyon", 
                        bekleyen_rez.apply(lambda x: f"ID:{x['id']} - {x['ad']} ({x['arac']}) - {x['toplam_tutar']:,.0f} TL", axis=1).tolist()
                    )
                    
                    if secilen_rez:
                        r_id = secilen_rez.split(" - ")[0].replace("ID:", "")
                        secilen_kayit = bekleyen_rez[bekleyen_rez['id'] == int(r_id)].iloc[0]
                        
                        if st.button("💬 Bu Müşteriye WhatsApp Onayı Gönder (Admin)"):
                            try:
                                musteri_tel = f"+90{secilen_kayit['tel']}"
                                wa_mesaj = tr_duzelt(f"Sayin {secilen_kayit['ad']}, DriveNow uzerinden {secilen_kayit['arac']} araci icin yaptiginiz rezervasyon onaylanmistir. Tarihler: {secilen_kayit['bas_tarih']} / {secilen_kayit['bit_tarih']}. Tutar: {secilen_kayit['toplam_tutar']:,.0f} TL. Iyi yolculuklar dileriz!")
                                
                                simdi = datetime.now()
                                kit.sendwhatmsg(musteri_tel, wa_mesaj, simdi.hour, simdi.minute + 1, 15, True, 2)
                                st.success(f"Başarılı! {secilen_kayit['ad']} adlı müşterinin telefonuna WhatsApp onay mesajı kuyruğa eklendi.")
                            except Exception as e:
                                st.error("WhatsApp mesajı tetiklenirken hata oluştu. Bilgisayarınızda WhatsApp Web'in açık olduğundan emin olun.")
                else:
                    st.info("Onay bekleyen aktif kiralama bulunmuyor.")

                # 📊 GRAFİK VE CİRO ANALİZİ
                st.markdown("<b>📊 Ciro ve Performans Analizi</b>", unsafe_allow_html=True)
                df_analiz = pd.read_sql_query("SELECT * FROM kiralamalar", conn)
                if not df_analiz.empty:
                    toplam_ciro = df_analiz['toplam_tutar'].sum()
                    aktif_sayisi = len(df_analiz[df_analiz['durum'] == 'Aktif'])

                    c_m1, c_m2 = st.columns(2)
                    c_m1.metric("Toplam Tahsilat / Ciro", f"{toplam_ciro:,.0f} TL")
                    c_m2.metric("Aktif Kiralama Sayısı", aktif_sayisi)

                    fig = px.pie(df_analiz, names='arac', title="Araç Bazlı Kiralama Dağılımı", hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)

                # 🛠️ ARAÇ İADE (CHECK-OUT) VE HASAR KAYDI
                st.markdown("<b>🛠️ Araç İade & Hasar Yönetimi</b>", unsafe_allow_html=True)
                aktifler = pd.read_sql_query("SELECT id, tc, ad, arac FROM kiralamalar WHERE durum='Aktif'", conn)
                
                if not aktifler.empty:
                    secilen_iade_id = st.selectbox("İade Alınacak İşlem (ID - Müşteri - Araç)", aktifler.apply(lambda x: f"{x['id']} - {x['ad']} - {x['arac']}", axis=1).tolist(), key="iade_select")
                    k_id = secilen_iade_id.split(" - ")[0]
                    
                    with st.form("iade_formu"):
                        km = st.number_input("Dönüş Kilometresi", min_value=0, step=100)
                        hasar_durum = st.selectbox("Hasar Durumu", ["Sorunsuz", "Çizik/Gövde Hasarı", "Mekanik Arıza", "Kaza Tutanaklı"])
                        notlar = st.text_area("Yönetici Notları")
                        
                        if st.form_submit_button("İadeyi Tamamla ve Aracı Filoya Tekrar Müsait Yap"):
                            c.execute("UPDATE kiralamalar SET durum = 'Tamamlandı' WHERE id = ?", (k_id,))
                            c.execute("INSERT INTO iadeler (kiralama_id, km, hasar_durumu, notlar, foto_yolu) VALUES (?,?,?,?,?)", 
                                      (k_id, km, hasar_durum, notlar, "Yok"))
                            conn.commit()
                            st.success("Araç başarıyla iade alındı ve takvimi tekrar müsait duruma getirildi.")
                            st.rerun()
                else:
                    st.info("Sistemde iade bekleyen aktif kiralama bulunmuyor.")

                g_logs, k_logs = kayitlari_ayristir()
                st.markdown("<b>📄 Sistem Raporları (.txt)</b>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    st.download_button("📥 Giriş Yapanlar", g_logs, "giris_yapanlar.txt", mime="text/plain")
                with c2:
                    st.download_button("📥 Kiralama Yapanlar", k_logs, "kiralama_kayitlari.txt", mime="text/plain")

                st.markdown("<br><b>📷 Yüklenen Ehliyet Fotoğrafları</b>", unsafe_allow_html=True)
                fotolar = os.listdir(UPLOAD_DIR)
                if fotolar:
                    for f in fotolar:
                        f_path = os.path.join(UPLOAD_DIR, f)
                        st.image(f_path, caption=f, width=240)
                        with open(f_path, "rb") as file:
                            st.download_button(f"Fotoğrafı İndir: {f}", file, file_name=f, key=f"dl_{f}")
                else:
                    st.info("Henüz yüklenen fotoğraf yok.")

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🚨 Tüm Verileri ve Fotoğrafları Sıfırla"):
                    if os.path.exists(LOG_FILE):
                        os.remove(LOG_FILE)
                    if os.path.exists(DB_FILE):
                        os.remove(DB_FILE)
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
            st.session_state["tamamlandi"] = False
            st.rerun()
