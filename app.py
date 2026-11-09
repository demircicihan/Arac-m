# DriveNow Premium - Tum Kodlar

Bu dosya projedeki tum kaynak kodlari tek yerde toplar.


## `app.py`

```python
"""DriveNow Premium — Streamlit uygulama girişi.

Çalıştırma:  streamlit run app.py
"""

from __future__ import annotations

from datetime import date

import streamlit as st

from drivenow import db
from drivenow.components import esc, initials
from drivenow.config import APP_NAME, APP_SUFFIX, DEMO_MODE
from drivenow.state import (
    current_user,
    init_state,
    is_guest,
    logout,
    session_expired,
    set_flash,
    show_flash,
    touch_session,
)
from drivenow.theme import inject_theme
from drivenow.views import account, admin, auth, booking, fleet

st.set_page_config(
    page_title=f"{APP_NAME} {APP_SUFFIX} • Araç Kiralama",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": f"{APP_NAME} {APP_SUFFIX} — premium araç kiralama deneyimi.",
    },
)


@st.cache_resource(show_spinner=False)
def _bootstrap() -> bool:
    db.init_db()
    return True


_bootstrap()
inject_theme()
init_state()

# --- Oturum süresi ----------------------------------------------------------
if (
    st.session_state.get("auth")
    and not is_guest()
    and session_expired()
):
    logout()
    set_flash("Oturum süreniz doldu. Güvenliğiniz için tekrar giriş yapın.", "warning")
    st.rerun()
touch_session()


def _topbar() -> None:
    user = current_user() or {}
    guest = is_guest()
    left, right = st.columns([3, 1.15], vertical_alignment="center")

    with left:
        st.markdown(
            '<div class="dn-topbar" style="padding-bottom:6px">'
            '<div class="dn-brand">'
            '<div class="dn-brand-mark">🚗</div>'
            "<div>"
            f'<div class="dn-brand-name">{esc(APP_NAME)} <span>{esc(APP_SUFFIX)}</span></div>'
            '<div class="dn-brand-sub">Premium Araç Kiralama</div>'
            "</div></div></div>",
            unsafe_allow_html=True,
        )

    with right:
        if st.session_state.get("auth") and not guest:
            chip, action = st.columns([2.1, 1], vertical_alignment="center")
            with chip:
                st.markdown(
                    '<div class="dn-user-chip">'
                    f'<div class="dn-avatar">{esc(initials(user.get("ad", "")))}</div>'
                    "<div>"
                    f'<b>{esc(user.get("ad", "Müşteri"))}</b>'
                    f'<small>{esc(user.get("email", "") or "Doğrulanmış üye")}</small>'
                    "</div></div>",
                    unsafe_allow_html=True,
                )
            with action:
                if st.button("Çıkış", width="stretch", key="topbar_logout"):
                    logout()
                    set_flash("Güvenli çıkış yapıldı. Tekrar bekleriz.", "info")
                    st.rerun()
        elif guest:
            chip, action = st.columns([2.1, 1], vertical_alignment="center")
            with chip:
                st.markdown(
                    '<div class="dn-user-chip">'
                    '<div class="dn-avatar">👤</div>'
                    "<div><b>Misafir</b><small>Keşif modu</small></div></div>",
                    unsafe_allow_html=True,
                )
            with action:
                if st.button("Giriş yap", width="stretch", key="topbar_login"):
                    st.session_state["auth"] = False
                    st.session_state["guest"] = False
                    st.session_state["user"] = None
                    st.rerun()


def _login_prompt(title: str, text: str) -> None:
    st.markdown(
        f'<div class="dn-empty"><div class="dn-empty__icon">🔐</div>'
        f"<b>{esc(title)}</b><span>{esc(text)}</span></div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("Giriş ekranına dön", type="primary", width="stretch"):
            st.session_state["auth"] = False
            st.session_state["guest"] = False
            st.session_state["user"] = None
            st.session_state["auth_notice"] = "Devam etmek için lütfen giriş yapın."
            st.rerun()


def _footer() -> None:
    demo = " • Demo modu" if DEMO_MODE else ""
    year = date.today().year
    st.markdown(
        '<div class="dn-footer">'
        f"<div><b>{esc(APP_NAME)} {esc(APP_SUFFIX)}</b> • Premium filo, kapınıza teslim{demo}</div>"
        "<div>destek@drivenow.com.tr • 0850 000 00 00 • Konya / Türkiye</div>"
        f"<div>© {year} DriveNow. Tüm hakları saklıdır.</div>"
        "</div>",
        unsafe_allow_html=True,
    )


# --- Giriş yapılmamış -------------------------------------------------------
if not st.session_state.get("auth"):
    auth.render()
    _footer()
    st.stop()

_topbar()
show_flash()

booking_active = bool(
    st.session_state.get("secili") or st.session_state.get("show_booking_success")
)

if booking_active:
    booking.render()
    _footer()
    st.stop()

NAV_ICONS = {
    "Filo": "🚗",
    "Rezervasyonlarım": "🧾",
    "Hesabım": "👤",
    "Yönetim": "🛠️",
}
nav = st.segmented_control(
    "Gezinme",
    list(NAV_ICONS.keys()),
    key="nav",
    format_func=lambda item: f"{NAV_ICONS[item]} {item}",
    label_visibility="collapsed",
    width="stretch",
    wrap=True,
)
nav = nav or "Filo"

if nav == "Filo":
    fleet.render()
elif nav == "Rezervasyonlarım":
    if is_guest():
        _login_prompt(
            "Rezervasyonlar için giriş gerekli",
            "Misafir modunda yalnızca filoyu keşfedebilirsiniz.",
        )
    else:
        account.render("reservations")
elif nav == "Hesabım":
    if is_guest():
        _login_prompt(
            "Hesabınıza erişmek için giriş yapın",
            "Profil, favoriler ve geçmiş kiralamalar üyelere özeldir.",
        )
    else:
        account.render()
elif nav == "Yönetim":
    admin.render()

_footer()
```


## `requirements.txt`

```text
streamlit>=1.66,<2
pandas>=2.2
plotly>=5.24
pydeck>=0.9
reportlab>=4.2
Pillow>=10.4
```


## `README.md`

```text
# DriveNow Premium 🚗

Konya merkezli, çok şehirli premium araç kiralama uygulaması. Streamlit üzerinde
çalışır; SQLite ile kalıcı veri saklar, PDF rezervasyon özeti üretir ve yönetim
paneli içerir.

> **ÖNEMLİ GÜVENLİK UYARISI**
> Eski sürümde kod içinde açık şekilde duran Gmail uygulama şifresi
> (`mjleglfzrcrxnmqb`) ve yönetici şifresi artık kullanılmıyor. Ancak eski şifre
> daha önce yayınlandığı için **derhal iptal edilip yenisi üretilmelidir**:
> Google Hesabı → Güvenlik → 2 Adımlı Doğrulama → Uygulama şifreleri.
> Yeni şifre yalnızca `.streamlit/secrets.toml` veya ortam değişkeni olarak
> tutulmalıdır. Yönetici şifresini de mutlaka değiştirin.

## Öne çıkanlar

**Tasarım**
- Koyu premium tema, turuncu/teal vurgular, Sora + Inter tipografi
- Cam efektli kartlar, animasyonlu geçişler, tamamen responsive düzen
- Özel hero, KPI kartları, durum etiketleri, adım göstergesi, boş durum ekranları

**İşlevsellik**
- 3 adımlı rezervasyon sihirbazı (ekstralar → sürücü → ödeme)
- Tarih/konum bazlı müsaitlik, çakışmasız atomik rezervasyon
- Uzun dönem, sadakat ve kupon indirimleri tek fiyat motorunda
- Ek hizmetler, tek yön ücreti, genç sürücü ücreti, depozito
- Favoriler, araç karşılaştırma, gelişmiş filtreler, harita
- Hesap alanı: rezervasyon iptal/uzatma, yorum, iletişim bilgileri
- Yönetim paneli: onay, teslim/iade, kupon, yorum, kullanıcı, rapor, yedek, sıfırlama
- PDF rezervasyon özeti (Türkçe font + QR) ve opsiyonel e-posta gönderimi
- SMS/OTP doğrulama akışı; demo modunda kod ekranda gösterilir

**Güvenlik**
- Kod içinde sır yok; tüm gizli değerler secrets/ortam değişkeninden okunur
- PBKDF2-SHA256 parola hash'i, sabit zamanlı karşılaştırma
- OTP süresi, deneme limiti ve istek hız limiti
- Tüm SQL sorguları parametreli; kullanıcı metinleri HTML kaçışlı
- Yüklenen görsellerde tür/boyut doğrulaması ve güvenli dosya adı
- Yönetici girişinde deneme limiti ve kilit
- Atomik rezervasyon (`BEGIN IMMEDIATE` + müsaitlik yeniden kontrolü)
- Oturum zaman aşımı ve denetim kaydı (audit log)

## Kurulum

```powershell
# 1) Bağımlılıklar
pip install -r requirements.txt

# 2) Gizli ayarlar
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
# secrets.toml içindeki ADMIN_PASSWORD ve SMTP değerlerini düzenleyin

# 3) Çalıştır
streamlit run app.py
```

Uygulama varsayılan olarak `data/drivenow.db` dosyasını oluşturur.
Farklı bir konum için:

```powershell
$env:DRIVENOW_DATA_DIR = "C:\veri\drivenow"
streamlit run app.py
```

## Streamlit Cloud'a dağıtım

1. Projeyi GitHub'a push edin (`.streamlit/secrets.toml` ve `data/` git'e girmez).
2. [share.streamlit.io](https://share.streamlit.io) üzerinden repoyu bağlayın.
3. **Advanced settings → Python version**: 3.12 seçin (3.15 henüz desteklenmiyor olabilir).
4. **Secrets** alanına `.streamlit/secrets.toml.example` içeriğini kopyalayıp
   gerçek değerlerle doldurun.
5. Uygulama ilk açılışta veritabanını ve filoyu otomatik kurar.

> Not: Streamlit Community Cloud'da dosya sistemi kalıcı değildir; uygulama
> yeniden başlatıldığında SQLite verisi sıfırlanabilir. Kalıcı veri için
> harici bir veritabanı (Postgres vb.) veya kalıcı disk desteği olan bir sunucu
> kullanın. Yönetim → Raporlar ekranından `.db` yedeği indirilebilir.

## Proje yapısı

```
app.py                     # Giriş noktası, yönlendirme, üst bar
drivenow/
  config.py                # Sabitler, secrets/ortam okuma, lokasyonlar
  db.py                    # SQLite şeması, CRUD, müsaitlik, analitik
  pricing.py               # Tek fiyat motoru (indirim, ekstra, kupon)
  fleet.py                 # 14 araçlık filo verisi
  invoice.py               # PDF rezervasyon özeti
  mailer.py                # SMTP e-posta gönderimi (opsiyonel)
  sms.py                   # SMS webhook (opsiyonel)
  security.py              # Parola hash, OTP, güvenli dosya adı
  validators.py            # TCKN, telefon, e-posta, Luhn, maskeleme
  uploads.py               # Görsel doğrulama ve kayıt
  components.py            # HTML bileşenleri (kaçışlı)
  theme.py                 # Uygulama CSS teması
  state.py                 # Oturum durumu ve yönlendirme
  views/
    auth.py                # Tanıtım, giriş, OTP
    fleet.py               # Filo, filtre, harita, karşılaştırma
    booking.py             # Rezervasyon sihirbazı
    account.py             # Hesap, rezervasyon, favori, yorum
    admin.py               # Yönetim paneli
```

## Demo hesaplar ve kuponlar

- Yönetici: `Yönetim` sekmesi → `ADMIN_PASSWORD` (secrets'ta tanımlı değilse
  demo modunda varsayılan `DriveNow!2026`, arayüzde uyarı gösterilir; canlı
  modda varsayılan şifreyle giriş kapalıdır).
- Müşteri: herhangi bir ad, geçerli biçimde TCKN, cep telefonu ve e-posta ile
  kayıt olun. Demo modunda SMS kodu ekranda görünür.
- Kuponlar: `HOSGELDIN10` (%10), `SUPRIZ10` (%10), `KONYA500` (500 ₺),
  `VIP15` (%15, min. 10.000 ₺).

## Test

```powershell
python -m compileall -q .
python -c "from drivenow import db; db.init_db(); print(len(db.get_vehicles()))"
streamlit run app.py
```

## Lisans / notlar

Araç görselleri Wikimedia Commons üzerinden hotlink edilir; ticari kullanımda
kendi filo fotoğraflarınızla değiştirin. Fiyatlar temsilîdir.
```


## `baslat.bat`

```bat
@echo off
chcp 65001 >nul
cd /d "%~dp0"
title DriveNow Premium

echo ============================================
echo   DriveNow Premium - Baslatici
echo ============================================
echo.

if not exist ".streamlit\secrets.toml" (
    copy ".streamlit\secrets.toml.example" ".streamlit\secrets.toml" >nul
    echo [i] .streamlit\secrets.toml olusturuldu.
)

python -c "import streamlit, pandas, plotly, pydeck, reportlab, PIL" 2>nul
if errorlevel 1 (
    echo [i] Gerekli paketler kuruluyor, lutfen bekleyin...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [HATA] Paketler kurulamadi. Python kurulu mu kontrol edin.
        pause
        exit /b 1
    )
)

echo.
echo [i] Uygulama baslatiliyor...
echo [i] Tarayici acilmazsa: http://localhost:8501
echo [i] Durdurmak icin bu pencerede Ctrl+C basin.
echo.

python -m streamlit run app.py

echo.
echo Uygulama kapandi.
pause
```


## `.gitignore`

```text
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
env/

# Streamlit gizli bilgiler
.streamlit/secrets.toml

# Uygulama verisi
data/
testdata/
*.db
*.db-wal
*.db-shm
data/uploads/

# Editör / işletim sistemi
.vscode/
.idea/
.DS_Store
Thumbs.db

# Test / geçici
.pytest_cache/
.coverage
htmlcov/
*.log
```


## `.streamlit/config.toml`

```toml
[theme]
base = "dark"
primaryColor = "#FF6B2C"
backgroundColor = "#070B12"
secondaryBackgroundColor = "#0F1726"
textColor = "#E9EEF7"
font = "sans serif"

[server]
headless = true
runOnSave = true
maxUploadSize = 8

[browser]
gatherUsageStats = false

[client]
toolbarMode = "minimal"
showErrorDetails = true
```


## `.streamlit/secrets.toml.example`

```text
# DriveNow Premium — örnek gizli ayarlar
# Bu dosyayı `.streamlit/secrets.toml` olarak kopyalayın ve değerleri doldurun.
# `.streamlit/secrets.toml` ASLA git'e eklenmemelidir.

# --- Yönetici ---------------------------------------------------------------
# Güçlü bir şifre belirleyin. Aşağıdaki satırı açıp doldurun.
# Boş bırakılırsa demo modunda varsayılan `DriveNow!2026` kullanılır ve
# arayüzde güvenlik uyarısı gösterilir.
# ADMIN_PASSWORD = "buraya-guclu-bir-sifre-yazin"

# Alternatif: PBKDF2 hash kullanmak isterseniz (önerilir).
# Üretmek için: python -c "from drivenow.security import hash_password; print(hash_password('sifreniz'))"
# ADMIN_PASSWORD_HASH = "pbkdf2_sha256$260000$..."

# --- Çalışma modu -----------------------------------------------------------
# true: SMS kodu ekranda gösterilir, TCKN yalnızca biçim kontrolünden geçer.
# false: gerçek SMS sağlayıcısı ve TCKN checksum doğrulaması gerekir.
DEMO_MODE = true

# --- E-posta (opsiyonel) ----------------------------------------------------
# Gönderim yapmak isterseniz aşağıdaki satırları açıp doldurun.
# Boş bırakılırsa e-posta gönderimi devre dışı kalır.
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
# SMTP_USER = "ornek@gmail.com"
# SMTP_PASSWORD = "gmail-uygulama-sifresi"
# SMTP_FROM = "ornek@gmail.com"
SMTP_FROM_NAME = "DriveNow Premium"

# --- SMS (opsiyonel) --------------------------------------------------------
# DEMO_MODE=false iken zorunludur. JSON gövde: {"phone": "...", "message": "..."}
SMS_WEBHOOK_URL = ""
SMS_WEBHOOK_TOKEN = ""
```


## `drivenow/__init__.py`

```python
"""DriveNow Premium — araç kiralama uygulaması."""

__all__ = ["__version__"]
__version__ = "2.0.0"
```


## `drivenow/components.py`

```python
"""Yeniden kullanılabilir HTML bileşenleri.

Kullanıcıdan gelen tüm metinler `esc()` ile kaçırılır; böylece ad, not,
yorum gibi alanlar HTML enjeksiyonuna yol açmaz.
"""

from __future__ import annotations

import html
from datetime import date

from .config import CURRENCY
from .pricing import Quote, duration_discount


def esc(value) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def tr_upper(value) -> str:
    """Türkçe kurallarına uygun büyük harf (i → İ)."""
    return str(value if value is not None else "").replace("i", "İ").upper()


def money(value: float, suffix: bool = True) -> str:
    formatted = f"{float(value or 0):,.0f}".replace(",", ".")
    return f"{formatted} {CURRENCY}" if suffix else formatted


def stars(rating: float) -> str:
    try:
        value = float(rating)
    except (TypeError, ValueError):
        value = 0
    full = int(round(value))
    return "★" * max(0, min(5, full)) + "☆" * max(0, 5 - full)


def initials(name: str) -> str:
    parts = [part for part in str(name or "").strip().split() if part]
    if not parts:
        return "DN"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def safe_url(url: str) -> str:
    value = str(url or "").strip()
    if value.startswith(("http://", "https://")):
        return html.escape(value, quote=True)
    return ""


def status_pill(status: str) -> str:
    mapping = {
        "Onay Bekliyor": "pending",
        "Aktif": "active",
        "Tamamlandı": "done",
        "İptal": "cancel",
    }
    css = mapping.get(status, "done")
    return f'<span class="dn-status dn-status--{css}">{esc(tr_upper(status))}</span>'


def section_header(kicker: str, title: str, subtitle: str = "") -> str:
    sub = f"<p>{esc(subtitle)}</p>" if subtitle else ""
    return (
        f'<div class="dn-section"><div>'
        f'<div class="dn-kicker">{esc(kicker)}</div>'
        f"<h2>{esc(title)}</h2>{sub}</div></div>"
    )


def kpi(label: str, value: str, hint: str = "", variant: str = "") -> str:
    extra = f" dn-kpi--{variant}" if variant else ""
    hint_html = f'<div class="dn-kpi__hint">{esc(hint)}</div>' if hint else ""
    return (
        f'<div class="dn-kpi{extra}">'
        f'<div class="dn-kpi__label">{esc(tr_upper(label))}</div>'
        f'<div class="dn-kpi__value">{value}</div>'
        f"{hint_html}</div>"
    )


def empty_state(icon: str, title: str, text: str) -> str:
    return (
        f'<div class="dn-empty"><div class="dn-empty__icon">{esc(icon)}</div>'
        f"<b>{esc(title)}</b><span>{esc(text)}</span></div>"
    )


def feature_grid(items: list[tuple[str, str, str]]) -> str:
    cards = "".join(
        f'<div class="dn-feature"><div class="dn-feature__icon">{esc(icon)}</div>'
        f"<b>{esc(title)}</b><span>{esc(text)}</span></div>"
        for icon, title, text in items
    )
    return f'<div class="dn-grid">{cards}</div>'


def car_card(
    car: dict,
    days: int,
    available: bool,
    favorite: bool = False,
    compare: bool = False,
) -> str:
    image = safe_url(car.get("gorsel", ""))
    image_html = (
        f'<img src="{image}" alt="{esc(car.get("ad"))}" loading="lazy" '
        f'referrerpolicy="no-referrer" onerror="this.remove()">'
        if image
        else ""
    )
    availability = (
        '<span class="dn-chip dn-chip--ok">● Müsait</span>'
        if available
        else '<span class="dn-chip dn-chip--bad">● Dolu</span>'
    )
    favorite_html = (
        '<span class="dn-badge">♥ Favori</span>' if favorite else ""
    )
    compare_html = (
        '<span class="dn-badge">⇄ Karşılaştırmada</span>' if compare else ""
    )
    daily = float(car.get("gunluk_fiyat") or 0)
    rental_days = max(1, int(days))
    rate, _label = duration_discount(rental_days)
    total = daily * rental_days * (1 - rate)
    discount_html = (
        f'<div class="dn-deposit">%{int(round(rate * 100))} uzun dönem indirimi uygulandı</div>'
        if rate > 0
        else ""
    )
    badge = car.get("badge") or ""
    badge_html = f'<span class="dn-badge">{esc(badge)}</span>' if badge else ""

    return (
        '<div class="dn-car">'
        f'<div class="dn-car__media"><span>🚗</span>{image_html}</div>'
        '<div class="dn-car__body">'
        '<div class="dn-car__top"><div>'
        f'<div class="dn-car__cat">{esc(tr_upper(car.get("kategori", "")))} • {esc(tr_upper(car.get("vites", "")))}</div>'
        f'<div class="dn-car__title">{esc(car.get("ad", ""))}</div>'
        "</div>"
        f'<div class="dn-rating">★ {float(car.get("puan") or 0):.1f}</div>'
        "</div>"
        f'<div class="dn-badges">{badge_html}{favorite_html}{compare_html}</div>'
        '<div class="dn-chips">'
        f'<span class="dn-chip">⚙️ {esc(car.get("vites", ""))}</span>'
        f'<span class="dn-chip">⛽ {esc(car.get("yakit", ""))}</span>'
        f'<span class="dn-chip">👥 {int(car.get("koltuk") or 0)} koltuk</span>'
        f'<span class="dn-chip">🧳 {int(car.get("bagaj") or 0)} Lt</span>'
        f"{availability}"
        "</div>"
        '<div class="dn-price-row">'
        '<div><div class="dn-price-label">Günlük</div>'
        f'<div class="dn-price">{money(daily)}</div></div>'
        '<div style="text-align:right"><div class="dn-price-label">'
        f"{rental_days} gün toplam</div>"
        f'<div class="dn-price dn-price--accent">{money(total)}</div>'
        f'<div class="dn-deposit">Depozito {money(car.get("depozito", 0))}</div>'
        f"{discount_html}"
        "</div></div></div></div>"
    )


def tech_details(car: dict) -> str:
    specs = [
        ("⚙️", "Motor", car.get("motor", "-")),
        ("🕹️", "Şanzıman", car.get("sanziman", "-")),
        ("⛽", "Tüketim", car.get("tuketim", "-")),
        ("🚀", "0-100 km/s", car.get("hizlanma", "-")),
        ("🏁", "Maks. hız", car.get("azami_hiz", "-")),
        ("🏎️", "Çekiş", car.get("cekis", "-")),
    ]
    grid = "".join(
        f'<div class="dn-feature" style="padding:12px">'
        f'<div style="font-size:11px;color:#93a3b8;margin-bottom:3px">{esc(icon)} {esc(label)}</div>'
        f'<div style="font-size:12.5px;color:#fff;font-weight:600">{esc(value)}</div></div>'
        for icon, label, value in specs
    )
    features = "".join(
        f'<span class="dn-chip">{esc(item)}</span>'
        for item in (car.get("donanimlar") or [])
    )
    return (
        f'<div class="dn-grid" style="grid-template-columns:repeat(auto-fit,minmax(160px,1fr))">{grid}</div>'
        f'<div class="dn-chips" style="margin-top:12px">{features}</div>'
    )


def price_breakdown(quote: Quote, show_deposit: bool = True) -> str:
    rows = []
    for line in quote.lines:
        negative = line.amount < 0
        css = " dn-row--discount" if negative else ""
        amount = money(abs(line.amount))
        prefix = "−" if negative else ""
        note = f"<small>{esc(line.note)}</small>" if line.note else ""
        rows.append(
            f'<div class="dn-row{css}"><span>{esc(line.label)}{note}</span>'
            f"<b>{prefix}{amount}</b></div>"
        )
    total_row = (
        '<div class="dn-row dn-row--total"><span>Genel toplam</span>'
        f"<b>{money(quote.total)}</b></div>"
    )
    deposit = ""
    if show_deposit and quote.deposit > 0:
        deposit = (
            f'<div class="dn-row"><span>Depozito<small>İade edilir, toplama dahil değil</small></span>'
            f"<b>{money(quote.deposit)}</b></div>"
        )
    return "".join(rows) + total_row + deposit


def quote_card(review: dict) -> str:
    return (
        '<div class="dn-quote">'
        f'<div class="dn-quote__stars">{stars(review.get("puan", 5))}</div>'
        f'<p>“{esc(review.get("yorum", ""))}”</p>'
        f'<b>{esc(review.get("ad", "Müşteri"))}</b>'
        f'<span>{esc(review.get("arac", ""))}</span>'
        "</div>"
    )


def profile_header(user: dict, tier: str, completed: int, total_spent: float) -> str:
    return (
        '<div class="dn-card"><div class="dn-profile">'
        f'<div class="dn-avatar">{esc(initials(user.get("ad")))}</div>'
        "<div>"
        f'<h3>{esc(user.get("ad", "Müşteri"))}</h3>'
        f'<p>{completed} tamamlanan kiralama • {money(total_spent)} harcama</p>'
        "</div>"
        f'<div class="dn-tier">💎 {esc(tier)} Üye</div>'
        "</div></div>"
    )


def date_tr(value: str | date) -> str:
    if isinstance(value, date):
        return value.strftime("%d.%m.%Y")
    try:
        return date.fromisoformat(str(value)[:10]).strftime("%d.%m.%Y")
    except ValueError:
        return str(value)
```


## `drivenow/config.py`

```python
"""Uygulama genelinde kullanılan sabitler ve yapılandırma.

Tüm gizli bilgiler (SMTP, admin şifresi, SMS webhook) ortam değişkenlerinden
veya Streamlit secrets dosyasından okunur. Kod içinde sır tutulmaz.
"""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

APP_NAME = "DriveNow"
APP_SUFFIX = "Premium"
APP_TAGLINE = "Premium filo, kapınıza teslim."
APP_DESCRIPTION = (
    "Konya, İstanbul, Ankara, İzmir ve Antalya'da yeni nesil araç kiralama. "
    "Şeffaf fiyat, ücretsiz iptal ve 7/24 yol yardımı."
)

BASE_DIR = Path(__file__).resolve().parent.parent


def _path_from_env(key: str, default: Path) -> Path:
    raw = os.environ.get(key)
    if not raw:
        return default
    return Path(raw).expanduser().resolve()


DATA_DIR = _path_from_env("DRIVENOW_DATA_DIR", BASE_DIR / "data")
UPLOAD_DIR = DATA_DIR / "uploads"
DB_PATH = _path_from_env("DRIVENOW_DB_PATH", DATA_DIR / "drivenow.db")
LEGACY_LOG_PATH = DATA_DIR / "kayitlar.txt"

for _folder in (DATA_DIR, UPLOAD_DIR):
    _folder.mkdir(parents=True, exist_ok=True)


def get_secret(key: str, default=None):
    """Secrets -> ortam değişkeni -> varsayılan sırasıyla değer okur."""
    value = None
    try:
        value = st.secrets[key]
    except Exception:
        value = None
    if value is None or value == "":
        value = os.environ.get(key, default)
    return value


def _as_bool(value, default: bool = False) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on", "evet"}


def _as_int(value, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# --- Çalışma modu -----------------------------------------------------------
# Demo modunda SMS kodu ekranda gösterilir ve TCKN yalnızca biçim olarak
# doğrulanır. Canlıya alırken DEMO_MODE = false yapın.
DEMO_MODE = _as_bool(get_secret("DEMO_MODE", os.environ.get("DRIVENOW_DEMO", "true")), True)

# --- Yönetici ---------------------------------------------------------------
ADMIN_PASSWORD = str(
    get_secret("ADMIN_PASSWORD", os.environ.get("DRIVENOW_ADMIN_PASSWORD", "DriveNow!2026"))
)
ADMIN_PASSWORD_HASH = str(get_secret("ADMIN_PASSWORD_HASH", "") or "")
ADMIN_USING_DEFAULT = not any(
    [
        get_secret("ADMIN_PASSWORD"),
        get_secret("ADMIN_PASSWORD_HASH"),
        os.environ.get("DRIVENOW_ADMIN_PASSWORD"),
    ]
)

# --- E-posta ----------------------------------------------------------------
SMTP_HOST = str(get_secret("SMTP_HOST", "smtp.gmail.com"))
SMTP_PORT = _as_int(get_secret("SMTP_PORT", 465), 465)
SMTP_USER = str(get_secret("SMTP_USER", "") or "")
SMTP_PASSWORD = str(get_secret("SMTP_PASSWORD", "") or "")
SMTP_FROM = str(get_secret("SMTP_FROM", SMTP_USER) or "")
SMTP_FROM_NAME = str(get_secret("SMTP_FROM_NAME", f"{APP_NAME} Premium") or "")

# --- SMS (opsiyonel) --------------------------------------------------------
SMS_WEBHOOK_URL = str(get_secret("SMS_WEBHOOK_URL", "") or "")
SMS_WEBHOOK_TOKEN = str(get_secret("SMS_WEBHOOK_TOKEN", "") or "")

# --- İş kuralları -----------------------------------------------------------
CURRENCY = "₺"
ONE_WAY_FEE = 750.0
YOUNG_DRIVER_AGE = 25
YOUNG_DRIVER_DAILY = 250.0
CANCELLATION_HOURS = 24
SESSION_TIMEOUT_MINUTES = 120
MAX_UPLOAD_MB = 8
OTP_TTL_SECONDS = 180
OTP_MAX_ATTEMPTS = 4
OTP_MAX_REQUESTS = 5
OTP_REQUEST_WINDOW_MIN = 10

# (gün eşiği, indirim oranı, etiket)
LONG_TERM_TIERS = (
    (30, 0.30, "30+ gün %30 indirim"),
    (21, 0.25, "21+ gün %25 indirim"),
    (14, 0.20, "14+ gün %20 indirim"),
    (7, 0.15, "7+ gün %15 indirim"),
)

# (tamamlanan kiralama eşiği, indirim oranı, seviye adı)
LOYALTY_TIERS = (
    (6, 0.10, "Gold"),
    (3, 0.05, "Silver"),
    (0, 0.00, "Standart"),
)

# --- Teslimat noktaları -----------------------------------------------------
LOKASYONLAR = {
    "Konya • Ereğli Merkez / KYK Yurdu": {
        "lat": 37.5133,
        "lon": 34.0525,
        "adres": "Ereğli Merkez, Konya",
        "saat": "08:00 – 22:00",
    },
    "Konya • Ereğli Otogar & Tren Garı": {
        "lat": 37.5250,
        "lon": 34.0450,
        "adres": "Ereğli Otogar, Konya",
        "saat": "07:00 – 23:00",
    },
    "Konya • Çumra İlçe Merkezi": {
        "lat": 37.5744,
        "lon": 32.7744,
        "adres": "Çumra, Konya",
        "saat": "09:00 – 20:00",
    },
    "Konya • Selçuklu / Otogar": {
        "lat": 37.9535,
        "lon": 32.5100,
        "adres": "Selçuklu, Konya",
        "saat": "07:00 – 23:00",
    },
    "Konya • Zafer / Alaaddin Merkez": {
        "lat": 37.8713,
        "lon": 32.4846,
        "adres": "Meram, Konya",
        "saat": "08:00 – 22:00",
    },
    "Konya • Havalimanı (KYA)": {
        "lat": 37.9790,
        "lon": 32.5619,
        "adres": "Konya Havalimanı",
        "saat": "7/24",
    },
    "İstanbul • Sabiha Gökçen Havalimanı (SAW)": {
        "lat": 40.8983,
        "lon": 29.3092,
        "adres": "Pendik, İstanbul",
        "saat": "7/24",
    },
    "İstanbul • İstanbul Havalimanı (IST)": {
        "lat": 41.2753,
        "lon": 28.7519,
        "adres": "Arnavutköy, İstanbul",
        "saat": "7/24",
    },
    "Ankara • Esenboğa Havalimanı (ESB)": {
        "lat": 40.1281,
        "lon": 32.9951,
        "adres": "Çubuk, Ankara",
        "saat": "7/24",
    },
    "İzmir • Adnan Menderes Havalimanı (ADB)": {
        "lat": 38.2924,
        "lon": 27.1570,
        "adres": "Gaziemir, İzmir",
        "saat": "7/24",
    },
    "Antalya • Havalimanı (AYT) Dış/İç Hatlar": {
        "lat": 36.9000,
        "lon": 30.7990,
        "adres": "Muratpaşa, Antalya",
        "saat": "7/24",
    },
}

KATEGORILER = ("Ekonomik", "Konfor", "SUV", "Premium", "Elektrik", "Van")
YAKITLAR = ("Benzin", "Dizel", "Elektrik", "Hibrit")
VITESLER = ("Otomatik", "Manuel")
```


## `drivenow/db.py`

```python
"""SQLite veri katmanı.

Her işlem kendi bağlantısını açar; WAL modu ve BEGIN IMMEDIATE ile eşzamanlı
rezervasyonlarda çakışma engellenir. Tüm sorgular parametrelidir.
"""

from __future__ import annotations

import json
import random
import sqlite3
import string
from contextlib import contextmanager
from datetime import date, datetime
from typing import Any, Iterable

import pandas as pd

from .config import DB_PATH, LOYALTY_TIERS
from .fleet import FLEET

STATUS_PENDING = "Onay Bekliyor"
STATUS_ACTIVE = "Aktif"
STATUS_DONE = "Tamamlandı"
STATUS_CANCELLED = "İptal"
ACTIVE_STATUSES = (STATUS_PENDING, STATUS_ACTIVE)


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    tc TEXT NOT NULL UNIQUE,
    tel TEXT NOT NULL,
    email TEXT NOT NULL,
    dogum_tarihi TEXT,
    ehliyet_no TEXT,
    ehliyet_sinif TEXT,
    rol TEXT NOT NULL DEFAULT 'musteri',
    pazarlama INTEGER NOT NULL DEFAULT 0,
    olusturma TEXT NOT NULL,
    son_giris TEXT
);

CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plaka TEXT NOT NULL UNIQUE,
    ad TEXT NOT NULL,
    kategori TEXT NOT NULL,
    vites TEXT NOT NULL,
    yakit TEXT NOT NULL,
    koltuk INTEGER NOT NULL,
    bagaj INTEGER NOT NULL,
    gunluk_fiyat REAL NOT NULL,
    puan REAL NOT NULL DEFAULT 4.5,
    depozito REAL NOT NULL DEFAULT 3000,
    badge TEXT,
    gorsel TEXT,
    motor TEXT,
    sanziman TEXT,
    tuketim TEXT,
    hizlanma TEXT,
    azami_hiz TEXT,
    cekis TEXT,
    donanimlar TEXT,
    aktif INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kod TEXT NOT NULL UNIQUE,
    user_id INTEGER REFERENCES users(id),
    vehicle_id INTEGER REFERENCES vehicles(id),
    arac TEXT NOT NULL,
    plaka TEXT,
    konum TEXT NOT NULL,
    iade_konum TEXT,
    bas_tarih TEXT NOT NULL,
    bit_tarih TEXT NOT NULL,
    gun INTEGER NOT NULL,
    gunluk_fiyat REAL NOT NULL,
    baz_tutar REAL NOT NULL,
    ekstra_tutar REAL NOT NULL DEFAULT 0,
    indirim_tutar REAL NOT NULL DEFAULT 0,
    tek_yon_ucret REAL NOT NULL DEFAULT 0,
    genc_sofor_ucret REAL NOT NULL DEFAULT 0,
    uzatma_tutar REAL NOT NULL DEFAULT 0,
    toplam_tutar REAL NOT NULL,
    depozito REAL NOT NULL DEFAULT 0,
    kupon TEXT,
    durum TEXT NOT NULL DEFAULT 'Onay Bekliyor',
    odeme_yontemi TEXT,
    odeme_durumu TEXT,
    kart_son4 TEXT,
    musteri_notu TEXT,
    iptal_nedeni TEXT,
    ehliyet_no TEXT,
    ehliyet_sinif TEXT,
    dogum_tarihi TEXT,
    ehliyet_foto TEXT,
    ikinci_sofor TEXT,
    olusturma TEXT NOT NULL,
    guncelleme TEXT
);

CREATE TABLE IF NOT EXISTS reservation_extras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_id INTEGER NOT NULL REFERENCES reservations(id) ON DELETE CASCADE,
    ad TEXT NOT NULL,
    gunluk_fiyat REAL NOT NULL,
    gun INTEGER NOT NULL,
    tutar REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS handovers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_id INTEGER NOT NULL REFERENCES reservations(id) ON DELETE CASCADE,
    tip TEXT NOT NULL,
    km INTEGER,
    yakit INTEGER,
    hasar TEXT,
    notlar TEXT,
    foto TEXT,
    tarih TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_id INTEGER UNIQUE REFERENCES reservations(id) ON DELETE CASCADE,
    user_id INTEGER,
    ad TEXT,
    arac TEXT NOT NULL,
    puan INTEGER NOT NULL,
    yorum TEXT,
    onayli INTEGER NOT NULL DEFAULT 0,
    tarih TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS coupons (
    kod TEXT COLLATE NOCASE PRIMARY KEY,
    tip TEXT NOT NULL,
    deger REAL NOT NULL,
    min_tutar REAL NOT NULL DEFAULT 0,
    max_kullanim INTEGER NOT NULL DEFAULT 0,
    kullanim INTEGER NOT NULL DEFAULT 0,
    baslangic TEXT,
    bitis TEXT,
    aktif INTEGER NOT NULL DEFAULT 1,
    aciklama TEXT
);

CREATE TABLE IF NOT EXISTS favorites (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vehicle_id INTEGER NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    tarih TEXT NOT NULL,
    PRIMARY KEY (user_id, vehicle_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici TEXT,
    islem TEXT NOT NULL,
    detay TEXT,
    tarih TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE INDEX IF NOT EXISTS idx_res_vehicle_dates
    ON reservations(vehicle_id, bas_tarih, bit_tarih);
CREATE INDEX IF NOT EXISTS idx_res_user ON reservations(user_id);
CREATE INDEX IF NOT EXISTS idx_res_status ON reservations(durum);
CREATE INDEX IF NOT EXISTS idx_reviews_vehicle ON reviews(arac, onayli);
CREATE INDEX IF NOT EXISTS idx_audit_date ON audit_log(tarih);
"""


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=30, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


@contextmanager
def transaction(immediate: bool = True):
    conn = connect()
    try:
        conn.execute("BEGIN IMMEDIATE" if immediate else "BEGIN")
        yield conn
        conn.execute("COMMIT")
    except Exception:
        try:
            conn.execute("ROLLBACK")
        except sqlite3.Error:
            pass
        raise
    finally:
        conn.close()


def fetch_all(sql: str, params: Iterable[Any] = ()) -> list[sqlite3.Row]:
    conn = connect()
    try:
        return conn.execute(sql, tuple(params)).fetchall()
    finally:
        conn.close()


def fetch_one(sql: str, params: Iterable[Any] = ()) -> sqlite3.Row | None:
    conn = connect()
    try:
        return conn.execute(sql, tuple(params)).fetchone()
    finally:
        conn.close()


def execute(sql: str, params: Iterable[Any] = ()) -> int:
    with transaction() as conn:
        cur = conn.execute(sql, tuple(params))
        return int(cur.lastrowid or 0)


def executemany(sql: str, rows: Iterable[Iterable[Any]]) -> None:
    with transaction() as conn:
        conn.executemany(sql, rows)


def query_df(sql: str, params: Iterable[Any] = ()) -> pd.DataFrame:
    conn = connect()
    try:
        return pd.read_sql_query(sql, conn, params=tuple(params))
    finally:
        conn.close()


# --- Ayarlar ---------------------------------------------------------------


def get_setting(key: str, default: str | None = None) -> str | None:
    row = fetch_one("SELECT value FROM settings WHERE key = ?", (key,))
    return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    with transaction() as conn:
        conn.execute(
            "INSERT INTO settings(key, value) VALUES(?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, str(value)),
        )


def _setting_conn(conn: sqlite3.Connection, key: str) -> str | None:
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else None


def _set_setting_conn(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO settings(key, value) VALUES(?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, str(value)),
    )


# --- Kurulum ---------------------------------------------------------------


def init_db() -> None:
    # executescript kendi COMMIT'ini yaptığı için ayrı bağlantıda çalıştırılır.
    conn = connect()
    try:
        conn.executescript(SCHEMA)
    finally:
        conn.close()
    with transaction() as conn:
        _ensure_columns(conn)
        _seed_vehicles(conn)
        _seed_coupons(conn)
        _migrate_legacy(conn)


def _ensure_columns(conn: sqlite3.Connection) -> None:
    """Eski v2 kurulumlarına yeni kolonları ekler (idempotent)."""
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(reservations)")}
    if "uzatma_tutar" not in existing:
        conn.execute(
            "ALTER TABLE reservations ADD COLUMN uzatma_tutar REAL NOT NULL DEFAULT 0"
        )


def _seed_vehicles(conn: sqlite3.Connection) -> None:
    for car in FLEET:
        conn.execute(
            """
            INSERT INTO vehicles (
                plaka, ad, kategori, vites, yakit, koltuk, bagaj, gunluk_fiyat,
                puan, depozito, badge, gorsel, motor, sanziman, tuketim,
                hizlanma, azami_hiz, cekis, donanimlar, aktif
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)
            ON CONFLICT(plaka) DO UPDATE SET
                ad = excluded.ad,
                kategori = excluded.kategori,
                vites = excluded.vites,
                yakit = excluded.yakit,
                koltuk = excluded.koltuk,
                bagaj = excluded.bagaj,
                gunluk_fiyat = excluded.gunluk_fiyat,
                puan = excluded.puan,
                depozito = excluded.depozito,
                badge = excluded.badge,
                gorsel = excluded.gorsel,
                motor = excluded.motor,
                sanziman = excluded.sanziman,
                tuketim = excluded.tuketim,
                hizlanma = excluded.hizlanma,
                azami_hiz = excluded.azami_hiz,
                cekis = excluded.cekis,
                donanimlar = excluded.donanimlar
            """,
            (
                car["plaka"],
                car["ad"],
                car["kategori"],
                car["vites"],
                car["yakit"],
                car["koltuk"],
                car["bagaj"],
                car["gunluk_fiyat"],
                car["puan"],
                car["depozito"],
                car["badge"],
                car["gorsel"],
                car["motor"],
                car["sanziman"],
                car["tuketim"],
                car["hizlanma"],
                car["azami_hiz"],
                car["cekis"],
                json.dumps(car["donanimlar"], ensure_ascii=False),
            ),
        )


def _seed_coupons(conn: sqlite3.Connection) -> None:
    coupons = [
        ("HOSGELDIN10", "yuzde", 10, 0, 0, "2027-12-31", "Yeni üye indirimi"),
        ("SUPRIZ10", "yuzde", 10, 0, 0, "2027-12-31", "Sürpriz indirim"),
        ("KONYA500", "sabit", 500, 5000, 200, "2027-12-31", "Konya'ya özel 500 TL"),
        ("VIP15", "yuzde", 15, 10000, 50, "2027-12-31", "VIP müşteri indirimi"),
    ]
    for kod, tip, deger, min_tutar, max_k, bitis, aciklama in coupons:
        conn.execute(
            """
            INSERT OR IGNORE INTO coupons
                (kod, tip, deger, min_tutar, max_kullanim, kullanim, baslangic, bitis, aktif, aciklama)
            VALUES (?,?,?,?,?,0,?,?,1,?)
            """,
            (kod, tip, deger, min_tutar, max_k, "2025-01-01", bitis, aciklama),
        )


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (name,)
    ).fetchone()
    return bool(row)


def _migrate_legacy(conn: sqlite3.Connection) -> None:
    """Eski tek dosyalık sürümün verisini yeni şemaya taşır."""
    if _setting_conn(conn, "legacy_migrated") == "1":
        return

    if _table_exists(conn, "kiralamalar"):
        rows = conn.execute("SELECT * FROM kiralamalar").fetchall()
        for row in rows:
            r = dict(row)
            tc = str(r.get("tc") or "").strip()
            if not tc:
                continue
            user = conn.execute("SELECT id FROM users WHERE tc = ?", (tc,)).fetchone()
            if user:
                user_id = int(user["id"])
            else:
                user_id = int(
                    conn.execute(
                        "INSERT INTO users (ad, tc, tel, email, olusturma, son_giris) "
                        "VALUES (?,?,?,?,?,?)",
                        (
                            r.get("ad") or "Eski Müşteri",
                            tc,
                            str(r.get("tel") or ""),
                            str(r.get("email") or ""),
                            r.get("olusturma_tarihi") or _now(),
                            _now(),
                        ),
                    ).lastrowid
                )
            vehicle = conn.execute(
                "SELECT id, plaka FROM vehicles WHERE ad = ?", (r.get("arac"),)
            ).fetchone()
            durum = STATUS_ACTIVE if r.get("durum") == "Aktif" else STATUS_DONE
            bas = str(r.get("bas_tarih") or date.today().isoformat())[:10]
            bit = str(r.get("bit_tarih") or bas)[:10]
            try:
                gun = max(1, (date.fromisoformat(bit) - date.fromisoformat(bas)).days)
            except ValueError:
                gun = int(r.get("gun") or 1)
            conn.execute(
                """
                INSERT OR IGNORE INTO reservations (
                    kod, user_id, vehicle_id, arac, plaka, konum, iade_konum,
                    bas_tarih, bit_tarih, gun, gunluk_fiyat, baz_tutar,
                    toplam_tutar, depozito, durum, olusturma, guncelleme
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    f"LEG-{int(r['id']):04d}",
                    user_id,
                    vehicle["id"] if vehicle else None,
                    r.get("arac") or "-",
                    vehicle["plaka"] if vehicle else None,
                    r.get("konum") or "-",
                    r.get("konum") or "-",
                    bas,
                    bit,
                    gun,
                    float(r.get("toplam_tutar") or 0) / gun,
                    float(r.get("toplam_tutar") or 0),
                    float(r.get("toplam_tutar") or 0),
                    0,
                    durum,
                    r.get("olusturma_tarihi") or _now(),
                    _now(),
                ),
            )
        conn.execute("ALTER TABLE kiralamalar RENAME TO legacy_kiralamalar")

    if _table_exists(conn, "yorumlar"):
        for row in conn.execute("SELECT * FROM yorumlar").fetchall():
            r = dict(row)
            conn.execute(
                """
                INSERT INTO reviews (reservation_id, user_id, ad, arac, puan, yorum, onayli, tarih)
                VALUES (NULL, NULL, ?, ?, ?, ?, 1, ?)
                """,
                (
                    r.get("ad") or "Müşteri",
                    r.get("arac") or "-",
                    int(r.get("puan") or 5),
                    r.get("yorum") or "",
                    r.get("tarih") or _now(),
                ),
            )
        conn.execute("ALTER TABLE yorumlar RENAME TO legacy_yorumlar")

    if _table_exists(conn, "iadeler"):
        conn.execute("ALTER TABLE iadeler RENAME TO legacy_iadeler")

    _set_setting_conn(conn, "legacy_migrated", "1")


# --- Kullanıcılar ----------------------------------------------------------


def upsert_user(
    ad: str,
    tc: str,
    tel: str,
    email: str,
    pazarlama: bool = False,
    dogum_tarihi: str | None = None,
) -> dict:
    now = _now()
    with transaction() as conn:
        row = conn.execute("SELECT * FROM users WHERE tc = ?", (tc,)).fetchone()
        if row:
            conn.execute(
                """
                UPDATE users
                   SET ad = ?, tel = ?, email = ?, son_giris = ?, pazarlama = ?
                 WHERE id = ?
                """,
                (
                    ad,
                    tel,
                    email,
                    now,
                    int(bool(pazarlama)),
                    row["id"],
                ),
            )
            user_id = int(row["id"])
        else:
            user_id = int(
                conn.execute(
                    """
                    INSERT INTO users
                        (ad, tc, tel, email, pazarlama, dogum_tarihi, olusturma, son_giris)
                    VALUES (?,?,?,?,?,?,?,?)
                    """,
                    (
                        ad,
                        tc,
                        tel,
                        email,
                        int(bool(pazarlama)),
                        dogum_tarihi,
                        now,
                        now,
                    ),
                ).lastrowid
            )
        fresh = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(fresh)


def get_user(user_id: int) -> dict | None:
    row = fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
    return dict(row) if row else None


def update_user_contact(user_id: int, email: str, pazarlama: bool) -> None:
    execute(
        "UPDATE users SET email = ?, pazarlama = ? WHERE id = ?",
        (email, int(bool(pazarlama)), user_id),
    )


# --- Araçlar ---------------------------------------------------------------


def _vehicle_row(row: sqlite3.Row) -> dict:
    car = dict(row)
    try:
        car["donanimlar"] = json.loads(car.get("donanimlar") or "[]")
    except (json.JSONDecodeError, TypeError):
        car["donanimlar"] = []
    return car


def get_vehicles(include_inactive: bool = False) -> list[dict]:
    sql = "SELECT * FROM vehicles"
    if not include_inactive:
        sql += " WHERE aktif = 1"
    sql += " ORDER BY gunluk_fiyat ASC"
    return [_vehicle_row(row) for row in fetch_all(sql)]


def get_vehicle(vehicle_id: int) -> dict | None:
    row = fetch_one("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
    return _vehicle_row(row) if row else None


def set_vehicle_active(vehicle_id: int, active: bool) -> None:
    execute("UPDATE vehicles SET aktif = ? WHERE id = ?", (int(bool(active)), vehicle_id))


def update_vehicle_pricing(vehicle_id: int, gunluk_fiyat: float, depozito: float) -> None:
    execute(
        "UPDATE vehicles SET gunluk_fiyat = ?, depozito = ? WHERE id = ?",
        (float(gunluk_fiyat), float(depozito), vehicle_id),
    )


def _busy_conn(
    conn: sqlite3.Connection,
    vehicle_id: int,
    bas: str,
    bit: str,
    exclude_id: int | None = None,
) -> bool:
    sql = """
        SELECT 1 FROM reservations
         WHERE vehicle_id = ?
           AND durum IN (?, ?)
           AND bas_tarih < ?
           AND bit_tarih > ?
    """
    params: list[Any] = [vehicle_id, STATUS_PENDING, STATUS_ACTIVE, bit, bas]
    if exclude_id:
        sql += " AND id <> ?"
        params.append(exclude_id)
    return conn.execute(sql, tuple(params)).fetchone() is not None


def vehicle_available(
    vehicle_id: int,
    bas: str,
    bit: str,
    exclude_id: int | None = None,
) -> bool:
    conn = connect()
    try:
        return not _busy_conn(conn, vehicle_id, bas, bit, exclude_id)
    finally:
        conn.close()


def available_vehicle_ids(bas: str, bit: str) -> set[int]:
    rows = fetch_all(
        """
        SELECT DISTINCT vehicle_id FROM reservations
         WHERE durum IN (?, ?)
           AND bas_tarih < ?
           AND bit_tarih > ?
        """,
        (STATUS_PENDING, STATUS_ACTIVE, bit, bas),
    )
    busy = {int(r["vehicle_id"]) for r in rows if r["vehicle_id"] is not None}
    return {int(car["id"]) for car in get_vehicles()} - busy


# --- Kuponlar --------------------------------------------------------------


def get_coupon(code: str) -> dict | None:
    if not code:
        return None
    row = fetch_one("SELECT * FROM coupons WHERE kod = ?", (code.strip(),))
    return dict(row) if row else None


def list_coupons() -> list[dict]:
    return [dict(r) for r in fetch_all("SELECT * FROM coupons ORDER BY kod")]


def create_coupon(
    kod: str,
    tip: str,
    deger: float,
    min_tutar: float,
    max_kullanim: int,
    bitis: str,
    aciklama: str,
) -> None:
    execute(
        """
        INSERT INTO coupons
            (kod, tip, deger, min_tutar, max_kullanim, kullanim, baslangic, bitis, aktif, aciklama)
        VALUES (?,?,?,?,?,0,?,?,1,?)
        """,
        (
            kod.strip().upper(),
            tip,
            float(deger),
            float(min_tutar),
            int(max_kullanim),
            date.today().isoformat(),
            bitis,
            aciklama.strip(),
        ),
    )


def set_coupon_active(kod: str, active: bool) -> None:
    execute("UPDATE coupons SET aktif = ? WHERE kod = ?", (int(bool(active)), kod))


def _increment_coupon_conn(conn: sqlite3.Connection, code: str) -> None:
    if not code:
        return
    conn.execute(
        "UPDATE coupons SET kullanim = kullanim + 1 WHERE kod = ?", (code.strip(),)
    )


# --- Rezervasyonlar --------------------------------------------------------


def _reservation_code(conn: sqlite3.Connection) -> str:
    alphabet = string.ascii_uppercase + string.digits
    for _ in range(25):
        code = f"DN-{datetime.now():%y%m}-{''.join(random.choices(alphabet, k=5))}"
        if not conn.execute("SELECT 1 FROM reservations WHERE kod = ?", (code,)).fetchone():
            return code
    raise RuntimeError("Rezervasyon kodu üretilemedi.")


def create_reservation(data: dict, extras: list[dict]) -> tuple[int, str]:
    """Rezervasyonu atomik olarak oluşturur; araç doluysa ValueError fırlatır."""
    bas = str(data["bas_tarih"])[:10]
    bit = str(data["bit_tarih"])[:10]
    with transaction() as conn:
        if _busy_conn(conn, int(data["vehicle_id"]), bas, bit):
            raise ValueError("Seçilen araç bu tarihlerde artık müsait değil.")
        code = _reservation_code(conn)
        now = _now()
        res_id = int(
            conn.execute(
                """
                INSERT INTO reservations (
                    kod, user_id, vehicle_id, arac, plaka, konum, iade_konum,
                    bas_tarih, bit_tarih, gun, gunluk_fiyat, baz_tutar,
                    ekstra_tutar, indirim_tutar, tek_yon_ucret, genc_sofor_ucret,
                    toplam_tutar, depozito, kupon, durum, odeme_yontemi,
                    odeme_durumu, kart_son4, musteri_notu, ehliyet_no,
                    ehliyet_sinif, dogum_tarihi, ehliyet_foto, ikinci_sofor,
                    olusturma, guncelleme
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    code,
                    data.get("user_id"),
                    int(data["vehicle_id"]),
                    data["arac"],
                    data.get("plaka"),
                    data["konum"],
                    data.get("iade_konum") or data["konum"],
                    bas,
                    bit,
                    int(data["gun"]),
                    float(data["gunluk_fiyat"]),
                    float(data["baz_tutar"]),
                    float(data.get("ekstra_tutar", 0)),
                    float(data.get("indirim_tutar", 0)),
                    float(data.get("tek_yon_ucret", 0)),
                    float(data.get("genc_sofor_ucret", 0)),
                    float(data["toplam_tutar"]),
                    float(data.get("depozito", 0)),
                    data.get("kupon"),
                    data.get("durum", STATUS_PENDING),
                    data.get("odeme_yontemi"),
                    data.get("odeme_durumu"),
                    data.get("kart_son4"),
                    data.get("musteri_notu"),
                    data.get("ehliyet_no"),
                    data.get("ehliyet_sinif"),
                    data.get("dogum_tarihi"),
                    data.get("ehliyet_foto"),
                    data.get("ikinci_sofor"),
                    now,
                    now,
                ),
            ).lastrowid
        )
        for extra in extras:
            conn.execute(
                """
                INSERT INTO reservation_extras (reservation_id, ad, gunluk_fiyat, gun, tutar)
                VALUES (?,?,?,?,?)
                """,
                (
                    res_id,
                    extra["ad"],
                    float(extra["gunluk_fiyat"]),
                    int(extra["gun"]),
                    float(extra["tutar"]),
                ),
            )
        _increment_coupon_conn(conn, data.get("kupon") or "")
        conn.execute(
            "INSERT INTO audit_log (kullanici, islem, detay, tarih) VALUES (?,?,?,?)",
            (
                data.get("musteri_ad") or "Müşteri",
                "REZERVASYON",
                f"{code} • {data['arac']} • {bas} / {bit} • {float(data['toplam_tutar']):,.0f} TL",
                now,
            ),
        )
        return res_id, code


def get_reservation(res_id: int) -> dict | None:
    row = fetch_one("SELECT * FROM reservations WHERE id = ?", (res_id,))
    return dict(row) if row else None


def get_reservation_by_code(code: str) -> dict | None:
    row = fetch_one("SELECT * FROM reservations WHERE kod = ?", (code,))
    return dict(row) if row else None


def get_reservation_extras(res_id: int) -> list[dict]:
    return [
        dict(r)
        for r in fetch_all(
            "SELECT ad, gunluk_fiyat, gun, tutar FROM reservation_extras WHERE reservation_id = ?",
            (res_id,),
        )
    ]


def user_reservations(user_id: int) -> list[dict]:
    return [
        dict(r)
        for r in fetch_all(
            "SELECT * FROM reservations WHERE user_id = ? ORDER BY id DESC", (user_id,)
        )
    ]


def cancel_reservation(res_id: int, reason: str, actor: str) -> None:
    now = _now()
    with transaction() as conn:
        conn.execute(
            """
            UPDATE reservations
               SET durum = ?, iptal_nedeni = ?, guncelleme = ?
             WHERE id = ?
            """,
            (STATUS_CANCELLED, reason.strip(), now, res_id),
        )
        conn.execute(
            "INSERT INTO audit_log (kullanici, islem, detay, tarih) VALUES (?,?,?,?)",
            (actor, "İPTAL", f"Rezervasyon #{res_id} • {reason.strip()}", now),
        )


def extend_reservation(
    res_id: int, new_bit: str, new_gun: int, new_total: float, ek_tutar: float
) -> None:
    execute(
        """
        UPDATE reservations
           SET bit_tarih = ?, gun = ?, toplam_tutar = ?,
               uzatma_tutar = uzatma_tutar + ?, guncelleme = ?
         WHERE id = ?
        """,
        (new_bit, int(new_gun), float(new_total), float(ek_tutar), _now(), res_id),
    )


def update_reservation_status(res_id: int, status: str, actor: str) -> None:
    execute(
        "UPDATE reservations SET durum = ?, guncelleme = ? WHERE id = ?",
        (status, _now(), res_id),
    )
    log_audit(actor, "DURUM", f"Rezervasyon #{res_id} → {status}")


def user_completed_count(user_id: int) -> int:
    row = fetch_one(
        "SELECT COUNT(*) AS n FROM reservations WHERE user_id = ? AND durum = ?",
        (user_id, STATUS_DONE),
    )
    return int(row["n"]) if row else 0


def loyalty_for(user_id: int | None) -> tuple[float, str]:
    if not user_id:
        return 0.0, "Standart"
    count = user_completed_count(int(user_id))
    for threshold, rate, name in LOYALTY_TIERS:
        if count >= threshold:
            return rate, name
    return 0.0, "Standart"


# --- Teslim / iade ---------------------------------------------------------


def add_handover(
    reservation_id: int,
    tip: str,
    km: int,
    yakit: int,
    hasar: str,
    notlar: str,
    foto: str,
    actor: str,
) -> None:
    now = _now()
    with transaction() as conn:
        conn.execute(
            """
            INSERT INTO handovers (reservation_id, tip, km, yakit, hasar, notlar, foto, tarih)
            VALUES (?,?,?,?,?,?,?,?)
            """,
            (reservation_id, tip, int(km), int(yakit), hasar, notlar, foto, now),
        )
        if tip == "iade":
            conn.execute(
                "UPDATE reservations SET durum = ?, guncelleme = ? WHERE id = ?",
                (STATUS_DONE, now, reservation_id),
            )
        conn.execute(
            "INSERT INTO audit_log (kullanici, islem, detay, tarih) VALUES (?,?,?,?)",
            (actor, tip.upper(), f"Rezervasyon #{reservation_id} • {km} km • {hasar}", now),
        )


def recent_handovers(limit: int = 50) -> list[dict]:
    return [
        dict(r)
        for r in fetch_all(
            """
            SELECT h.*, r.kod, r.arac, COALESCE(u.ad, 'Müşteri') AS musteri
              FROM handovers h
              JOIN reservations r ON r.id = h.reservation_id
              LEFT JOIN users u ON u.id = r.user_id
             ORDER BY h.id DESC
             LIMIT ?
            """,
            (limit,),
        )
    ]


# --- Yorumlar --------------------------------------------------------------


def add_review(
    reservation_id: int,
    user_id: int,
    ad: str,
    arac: str,
    puan: int,
    yorum: str,
) -> bool:
    try:
        execute(
            """
            INSERT INTO reviews (reservation_id, user_id, ad, arac, puan, yorum, onayli, tarih)
            VALUES (?,?,?,?,?,?,0,?)
            """,
            (reservation_id, user_id, ad, arac, int(puan), yorum.strip(), _now()),
        )
        return True
    except sqlite3.IntegrityError:
        return False


def approved_reviews(limit: int = 12) -> list[dict]:
    return [
        dict(r)
        for r in fetch_all(
            "SELECT ad, arac, puan, yorum, tarih FROM reviews "
            "WHERE onayli = 1 ORDER BY id DESC LIMIT ?",
            (limit,),
        )
    ]


def all_reviews() -> list[dict]:
    return [dict(r) for r in fetch_all("SELECT * FROM reviews ORDER BY id DESC")]


def user_reviews(user_id: int) -> list[dict]:
    return [
        dict(r)
        for r in fetch_all(
            "SELECT * FROM reviews WHERE user_id = ? ORDER BY id DESC", (user_id,)
        )
    ]


def set_review_approval(review_id: int, approved: bool) -> None:
    execute("UPDATE reviews SET onayli = ? WHERE id = ?", (int(bool(approved)), review_id))


def delete_review(review_id: int) -> None:
    execute("DELETE FROM reviews WHERE id = ?", (review_id,))


# --- Favoriler -------------------------------------------------------------


def favorite_ids(user_id: int | None) -> set[int]:
    if not user_id:
        return set()
    rows = fetch_all("SELECT vehicle_id FROM favorites WHERE user_id = ?", (user_id,))
    return {int(r["vehicle_id"]) for r in rows}


def toggle_favorite(user_id: int, vehicle_id: int) -> bool:
    with transaction() as conn:
        row = conn.execute(
            "SELECT 1 FROM favorites WHERE user_id = ? AND vehicle_id = ?",
            (user_id, vehicle_id),
        ).fetchone()
        if row:
            conn.execute(
                "DELETE FROM favorites WHERE user_id = ? AND vehicle_id = ?",
                (user_id, vehicle_id),
            )
            return False
        conn.execute(
            "INSERT INTO favorites (user_id, vehicle_id, tarih) VALUES (?,?,?)",
            (user_id, vehicle_id, _now()),
        )
        return True


def favorite_vehicles(user_id: int) -> list[dict]:
    rows = fetch_all(
        """
        SELECT v.* FROM favorites f
          JOIN vehicles v ON v.id = f.vehicle_id
         WHERE f.user_id = ?
         ORDER BY f.tarih DESC
        """,
        (user_id,),
    )
    return [_vehicle_row(row) for row in rows]


# --- Denetim ve raporlar ---------------------------------------------------


def log_audit(kullanici: str, islem: str, detay: str = "") -> None:
    execute(
        "INSERT INTO audit_log (kullanici, islem, detay, tarih) VALUES (?,?,?,?)",
        (kullanici, islem, detay, _now()),
    )


def audit_logs(limit: int = 300) -> list[dict]:
    return [
        dict(r)
        for r in fetch_all(
            "SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,)
        )
    ]


def stats() -> dict:
    def scalar(sql: str, params: Iterable[Any] = ()) -> float:
        row = fetch_one(sql, params)
        if not row:
            return 0.0
        return float(row[0] or 0)

    return {
        "ciro": scalar(
            "SELECT COALESCE(SUM(toplam_tutar),0) FROM reservations WHERE durum <> ?",
            (STATUS_CANCELLED,),
        ),
        "aktif": int(scalar("SELECT COUNT(*) FROM reservations WHERE durum = ?", (STATUS_ACTIVE,))),
        "bekleyen": int(
            scalar("SELECT COUNT(*) FROM reservations WHERE durum = ?", (STATUS_PENDING,))
        ),
        "tamamlanan": int(
            scalar("SELECT COUNT(*) FROM reservations WHERE durum = ?", (STATUS_DONE,))
        ),
        "iptal": int(
            scalar("SELECT COUNT(*) FROM reservations WHERE durum = ?", (STATUS_CANCELLED,))
        ),
        "kullanici": int(scalar("SELECT COUNT(*) FROM users")),
        "filo": int(scalar("SELECT COUNT(*) FROM vehicles WHERE aktif = 1")),
        "ortalama_puan": scalar("SELECT COALESCE(AVG(puan),0) FROM reviews WHERE onayli = 1"),
        "yorum": int(scalar("SELECT COUNT(*) FROM reviews WHERE onayli = 1")),
    }


def monthly_revenue() -> pd.DataFrame:
    return query_df(
        """
        SELECT substr(bas_tarih, 1, 7) AS ay,
               COUNT(*) AS adet,
               COALESCE(SUM(toplam_tutar), 0) AS ciro
          FROM reservations
         WHERE durum <> ?
         GROUP BY substr(bas_tarih, 1, 7)
         ORDER BY ay
        """,
        (STATUS_CANCELLED,),
    )


def vehicle_performance() -> pd.DataFrame:
    return query_df(
        """
        SELECT r.arac AS arac,
               COUNT(*) AS adet,
               COALESCE(SUM(r.toplam_tutar), 0) AS ciro,
               COALESCE(SUM(r.gun), 0) AS gun
          FROM reservations r
         WHERE r.durum <> ?
         GROUP BY r.arac
         ORDER BY ciro DESC
        """,
        (STATUS_CANCELLED,),
    )


def status_distribution() -> pd.DataFrame:
    return query_df(
        "SELECT durum, COUNT(*) AS adet FROM reservations GROUP BY durum ORDER BY adet DESC"
    )


def admin_reservations(status: str = "Tümü", search: str = "") -> pd.DataFrame:
    sql = """
        SELECT r.id, r.kod, COALESCE(u.ad, 'Müşteri') AS musteri,
               COALESCE(u.tel, '') AS tel, COALESCE(u.email, '') AS email,
               r.arac, r.plaka, r.konum, r.bas_tarih, r.bit_tarih, r.gun,
               r.toplam_tutar, r.durum, r.odeme_durumu, r.kupon, r.olusturma
          FROM reservations r
          LEFT JOIN users u ON u.id = r.user_id
         WHERE 1 = 1
    """
    params: list[Any] = []
    if status and status != "Tümü":
        sql += " AND r.durum = ?"
        params.append(status)
    if search.strip():
        like = f"%{search.strip()}%"
        sql += (
            " AND (r.kod LIKE ? OR u.ad LIKE ? OR u.tel LIKE ? "
            "OR r.arac LIKE ? OR r.plaka LIKE ?)"
        )
        params.extend([like, like, like, like, like])
    sql += " ORDER BY r.id DESC"
    return query_df(sql, params)


def users_df() -> pd.DataFrame:
    return query_df(
        """
        SELECT id, ad, tc, tel, email, olusturma, son_giris,
               (SELECT COUNT(*) FROM reservations r WHERE r.user_id = users.id) AS kiralama
          FROM users ORDER BY id DESC
        """
    )


def audit_df(limit: int = 300) -> pd.DataFrame:
    return query_df("SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,))


def legacy_log_text() -> str:
    from .config import LEGACY_LOG_PATH

    if not LEGACY_LOG_PATH.exists():
        return ""
    try:
        return LEGACY_LOG_PATH.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""


def backup_bytes() -> bytes:
    """WAL'i diske yazıp tutarlı bir DB kopyası döndürür."""
    conn = connect()
    try:
        conn.execute("PRAGMA wal_checkpoint(FULL)")
    finally:
        conn.close()
    return DB_PATH.read_bytes()


def reset_all() -> None:
    """Tüm operasyonel veriyi siler; filo ve kupon tanımları korunur."""
    with transaction() as conn:
        conn.execute("DELETE FROM reservation_extras")
        conn.execute("DELETE FROM handovers")
        conn.execute("DELETE FROM reviews")
        conn.execute("DELETE FROM favorites")
        conn.execute("DELETE FROM reservations")
        conn.execute("DELETE FROM users")
        conn.execute("DELETE FROM audit_log")
        conn.execute("UPDATE coupons SET kullanim = 0")
        conn.execute(
            "INSERT INTO audit_log (kullanici, islem, detay, tarih) VALUES (?,?,?,?)",
            ("Sistem", "SIFIRLAMA", "Tüm operasyonel veriler silindi.", _now()),
        )
```


## `drivenow/fleet.py`

```python
"""Araç filosu verisi.

Fiyatlar günlük, KDV dahil ve temsilîdir. Görseller Wikimedia Commons
üzerinden hotlink edilir; ticari kullanımda kendi filo fotoğraflarınızla
değiştirin.
"""

from __future__ import annotations

FLEET: list[dict] = [
    {
        "plaka": "42 DN 101",
        "ad": "Fiat Egea Cross Lounge",
        "kategori": "Ekonomik",
        "vites": "Manuel",
        "yakit": "Dizel",
        "koltuk": 5,
        "bagaj": 440,
        "gunluk_fiyat": 1250.0,
        "puan": 4.6,
        "depozito": 2000.0,
        "badge": "🛣️ Uygun & Mukavemetli",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/10/Fiat_Tipo_Sedan_Facelift_Leonberg_2022_1X7A0412.jpg/960px-Fiat_Tipo_Sedan_Facelift_Leonberg_2022_1X7A0412.jpg",
        "motor": "1.3 MultiJet II (95 HP / 200 Nm)",
        "sanziman": "5 İleri Manuel",
        "tuketim": "4.4 Lt / 100 km",
        "hizlanma": "12.8 sn",
        "azami_hiz": "173 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": [
            "Yüksek Sürüş Pozisyonu",
            "City Direksiyon Modu",
            "10 inç Tablet Ekran",
            "LED Farlar & Tavan Çıtaları",
            "Geri Görüş Kamerası",
        ],
    },
    {
        "plaka": "42 DN 102",
        "ad": "Renault Clio R.S. Line",
        "kategori": "Ekonomik",
        "vites": "Manuel",
        "yakit": "Benzin",
        "koltuk": 5,
        "bagaj": 391,
        "gunluk_fiyat": 1350.0,
        "puan": 4.7,
        "depozito": 2000.0,
        "badge": "💡 Şehir Dostu",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3b/Renault_Clio_%28V%2C_Facelift%29_%E2%80%93_f_02092025.jpg/330px-Renault_Clio_%28V%2C_Facelift%29_%E2%80%93_f_02092025.jpg",
        "motor": "1.0 TCe Turbo (90 HP / 160 Nm)",
        "sanziman": "6 İleri Manuel",
        "tuketim": "5.0 Lt / 100 km",
        "hizlanma": "12.2 sn",
        "azami_hiz": "180 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": [
            "Apple CarPlay & Android Auto",
            "Ön & Arka Park Sensörü",
            "Start-Stop Sistemi",
            "EASYLINK 9.3 inç Ekran",
            "Dijital Gösterge Paneli",
        ],
    },
    {
        "plaka": "42 DN 103",
        "ad": "Ford Focus ST-Line",
        "kategori": "Konfor",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "koltuk": 5,
        "bagaj": 392,
        "gunluk_fiyat": 1800.0,
        "puan": 4.8,
        "depozito": 3000.0,
        "badge": "🌟 Aile Dostu",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/75/2018_Ford_Focus_ST-Line_X_1.0.jpg/330px-2018_Ford_Focus_ST-Line_X_1.0.jpg",
        "motor": "1.5 Ti-VCT EcoBoost (123 HP / 153 Nm)",
        "sanziman": "6 İleri Tam Otomatik",
        "tuketim": "6.2 Lt / 100 km",
        "hizlanma": "11.2 sn",
        "azami_hiz": "195 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": [
            "SYNC 4 13.2 inç Ekran",
            "Şerit Takip ve Destek",
            "180° Geri Görüş Kamerası",
            "Kablosuz Şarj",
            "ST-Line Gövde Kiti",
        ],
    },
    {
        "plaka": "42 DN 104",
        "ad": "Volkswagen Tiguan R-Line",
        "kategori": "SUV",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "koltuk": 5,
        "bagaj": 615,
        "gunluk_fiyat": 2800.0,
        "puan": 4.8,
        "depozito": 4000.0,
        "badge": "🏕️ Premium SUV",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/ef/Volkswagen_Tiguan_III_IMG_8823_%28cropped%29.jpg/330px-Volkswagen_Tiguan_III_IMG_8823_%28cropped%29.jpg",
        "motor": "1.5 TSI ACT (150 HP / 250 Nm)",
        "sanziman": "7 İleri DSG Otomatik",
        "tuketim": "5.7 Lt / 100 km",
        "hizlanma": "9.2 sn",
        "azami_hiz": "202 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": [
            "IQ.LIGHT Matrix LED Farlar",
            "Digital Cockpit Pro",
            "Panoramik Açılır Tavan",
            "3 Bölgeli Otomatik Klima",
            "Elektrikli Bagaj Kapağı",
        ],
    },
    {
        "plaka": "42 DN 105",
        "ad": "Peugeot 508 GT",
        "kategori": "Premium",
        "vites": "Otomatik",
        "yakit": "Dizel",
        "koltuk": 5,
        "bagaj": 487,
        "gunluk_fiyat": 2600.0,
        "puan": 4.9,
        "depozito": 4000.0,
        "badge": "🔥 En Çok Tercih Edilen",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/01/2019_Peugeot_508_GT-Line_BlueHDi_1.5_%28130_PS%29_Front.jpg/330px-2019_Peugeot_508_GT-Line_BlueHDi_1.5_%28130_PS%29_Front.jpg",
        "motor": "1.5 BlueHDi (130 HP / 300 Nm)",
        "sanziman": "8 İleri EAT8 Otomatik",
        "tuketim": "4.1 Lt / 100 km",
        "hizlanma": "9.9 sn",
        "azami_hiz": "208 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": [
            "Masajlı Koltuk",
            "Focal® Hi-Fi Ses Sistemi",
            "Night Vision Gece Görüşü",
            "Kör Nokta Uyarısı",
            "Adaptif Hız Sabitleyici",
        ],
    },
    {
        "plaka": "42 DN 106",
        "ad": "Tesla Model 3 Performance",
        "kategori": "Elektrik",
        "vites": "Otomatik",
        "yakit": "Elektrik",
        "koltuk": 5,
        "bagaj": 561,
        "gunluk_fiyat": 3800.0,
        "puan": 5.0,
        "depozito": 6000.0,
        "badge": "⚡ Teknoloji Harikası",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/a/ab/Tesla_Model_3_%282023%29_Autofr%C3%BChling_Ulm_IMG_9282.jpg/330px-Tesla_Model_3_%282023%29_Autofr%C3%BChling_Ulm_IMG_9282.jpg",
        "motor": "Dual Motor AWD (510 HP / 660 Nm)",
        "sanziman": "Tek Vitesli Direct Drive",
        "tuketim": "14.4 kWh / 100 km • 528 km menzil",
        "hizlanma": "3.1 sn",
        "azami_hiz": "261 km/s",
        "cekis": "Dört Çeker (AWD)",
        "donanimlar": [
            "Full Self-Driving Autopilot",
            "Panoramik Cam Tavan",
            "15.4 inç Dokunmatik Ekran",
            "Koltuk & Direksiyon Isıtma",
            "Sentry Mode Güvenlik",
        ],
    },
    {
        "plaka": "42 DN 107",
        "ad": "BMW 420i Gran Coupé M Sport",
        "kategori": "Premium",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "koltuk": 5,
        "bagaj": 470,
        "gunluk_fiyat": 4200.0,
        "puan": 4.9,
        "depozito": 6000.0,
        "badge": "💎 Premium Spor",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3c/2020_BMW_420i_Sport_Automatic_2.0.jpg/330px-2020_BMW_420i_Sport_Automatic_2.0.jpg",
        "motor": "2.0 TwinPower Turbo (170 HP / 250 Nm)",
        "sanziman": "8 İleri Steptronic Spor",
        "tuketim": "6.6 Lt / 100 km",
        "hizlanma": "7.9 sn",
        "azami_hiz": "230 km/s",
        "cekis": "Arkadan İtiş (RWD)",
        "donanimlar": [
            "M Aerodinamik Paket",
            "Harman Kardon® Ses",
            "BMW Curved Display",
            "Head-Up Display",
            "Lazer Far",
        ],
    },
    {
        "plaka": "42 DN 108",
        "ad": "Mercedes-Benz C200 4MATIC",
        "kategori": "Premium",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "koltuk": 5,
        "bagaj": 455,
        "gunluk_fiyat": 4500.0,
        "puan": 4.9,
        "depozito": 7000.0,
        "badge": "👑 Konforun Simgesi",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/24/Mercedes-Benz_W206_IMG_5796.jpg/330px-Mercedes-Benz_W206_IMG_5796.jpg",
        "motor": "1.5 Mild-Hybrid Turbo (204 HP + 20 HP EQ)",
        "sanziman": "9G-TRONIC Otomatik",
        "tuketim": "6.4 Lt / 100 km",
        "hizlanma": "7.1 sn",
        "azami_hiz": "241 km/s",
        "cekis": "Dört Çeker (4MATIC)",
        "donanimlar": [
            "MBUX 11.9 inç Dikey Ekran",
            "64 Renk Ambiyans Aydınlatma",
            "Burmester® 3D Ses",
            "Hafızalı Elektrikli Koltuklar",
            "Otonom Sürüş Desteği",
        ],
    },
    {
        "plaka": "42 DN 109",
        "ad": "Audi A5 Cabriolet S-Line",
        "kategori": "Premium",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "koltuk": 4,
        "bagaj": 370,
        "gunluk_fiyat": 4900.0,
        "puan": 4.9,
        "depozito": 7500.0,
        "badge": "☀️ Üstü Açık Lüks",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1d/Audi_A5_B10_DSC_7314.jpg/330px-Audi_A5_B10_DSC_7314.jpg",
        "motor": "2.0 40 TFSI Mild-Hybrid (204 HP / 320 Nm)",
        "sanziman": "7 İleri S tronic",
        "tuketim": "6.3 Lt / 100 km",
        "hizlanma": "7.5 sn",
        "azami_hiz": "237 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": [
            "Otomatik Açılır Kumaş Tavan",
            "Virtual Cockpit Plus",
            "Bang & Olufsen 3D Sound",
            "Ense Isıtma Sistemi",
            "Matrix LED Farlar",
        ],
    },
    {
        "plaka": "42 DN 110",
        "ad": "Porsche Macan GTS",
        "kategori": "SUV",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "koltuk": 5,
        "bagaj": 488,
        "gunluk_fiyat": 7500.0,
        "puan": 5.0,
        "depozito": 10000.0,
        "badge": "🏎️ Ultra Performans",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3a/Porsche_Macan_4_IMG_2153.jpg/330px-Porsche_Macan_4_IMG_2153.jpg",
        "motor": "2.9 V6 Twin-Turbo (440 HP / 550 Nm)",
        "sanziman": "7 İleri PDK Çift Kavrama",
        "tuketim": "9.9 Lt / 100 km",
        "hizlanma": "4.3 sn",
        "azami_hiz": "272 km/s",
        "cekis": "Dört Çeker (AWD)",
        "donanimlar": [
            "Spor Egzoz Sistemi",
            "PASM Havalı Süspansiyon",
            "BOSE® Surround Sound",
            "GTS Spor Koltuklar",
            "Sport Chrono Paket",
        ],
    },
    {
        "plaka": "42 DN 111",
        "ad": "Hyundai i20 Style",
        "kategori": "Ekonomik",
        "vites": "Manuel",
        "yakit": "Benzin",
        "koltuk": 5,
        "bagaj": 352,
        "gunluk_fiyat": 1150.0,
        "puan": 4.5,
        "depozito": 2000.0,
        "badge": "🧃 Genç Sürücü Dostu",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/82/Hyundai_i20_%28BC3%29_Facelift_Auto_Zuerich_2023_1X7A0968.jpg/960px-Hyundai_i20_%28BC3%29_Facelift_Auto_Zuerich_2023_1X7A0968.jpg",
        "motor": "1.4 MPI (100 HP / 133 Nm)",
        "sanziman": "6 İleri Manuel",
        "tuketim": "5.0 Lt / 100 km",
        "hizlanma": "12.8 sn",
        "azami_hiz": "180 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": [
            "10.25 inç Dokunmatik Ekran",
            "Kablosuz Apple CarPlay",
            "Geri Görüş Kamerası",
            "Şerit Takip Asistanı",
            "Otomatik Klima",
        ],
    },
    {
        "plaka": "42 DN 112",
        "ad": "Dacia Duster Journey",
        "kategori": "SUV",
        "vites": "Manuel",
        "yakit": "Dizel",
        "koltuk": 5,
        "bagaj": 445,
        "gunluk_fiyat": 1950.0,
        "puan": 4.6,
        "depozito": 3000.0,
        "badge": "⛰️ Yolun Her Yerinde",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9b/Dacia_Duster_III_IMG_8961.jpg/960px-Dacia_Duster_III_IMG_8961.jpg",
        "motor": "1.5 Blue dCi (115 HP / 260 Nm)",
        "sanziman": "6 İleri Manuel",
        "tuketim": "5.3 Lt / 100 km",
        "hizlanma": "10.6 sn",
        "azami_hiz": "180 km/s",
        "cekis": "Önden Çekiş (FWD)",
        "donanimlar": [
            "Modüler Tavan Barları",
            "8 inç Multimedya Ekranı",
            "Kör Nokta Uyarısı",
            "Arka Park Sensörü",
            "Yüksek Sürüş Pozisyonu",
        ],
    },
    {
        "plaka": "42 DN 113",
        "ad": "Mercedes-Benz Vito Tourer",
        "kategori": "Van",
        "vites": "Otomatik",
        "yakit": "Dizel",
        "koltuk": 8,
        "bagaj": 1410,
        "gunluk_fiyat": 5500.0,
        "puan": 4.8,
        "depozito": 8000.0,
        "badge": "👨‍👩‍👧‍👦 8 Kişilik VIP",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/25/Mercedes-Benz_Vito_Tourer_%28LRM_20230925_172513%29.jpg/960px-Mercedes-Benz_Vito_Tourer_%28LRM_20230925_172513%29.jpg",
        "motor": "2.0 CDI (190 HP / 440 Nm)",
        "sanziman": "9G-TRONIC Otomatik",
        "tuketim": "7.5 Lt / 100 km",
        "hizlanma": "9.5 sn",
        "azami_hiz": "200 km/s",
        "cekis": "Arkadan İtiş (RWD)",
        "donanimlar": [
            "8 Kişilik Konforlu Koltuk",
            "Çift Bölgeli Klima",
            "Elektrikli Sürgülü Kapı",
            "Geniş Bagaj Hacmi",
            "MBUX Multimedya",
        ],
    },
    {
        "plaka": "42 DN 114",
        "ad": "Volvo XC60 B5 AWD",
        "kategori": "SUV",
        "vites": "Otomatik",
        "yakit": "Benzin",
        "koltuk": 5,
        "bagaj": 613,
        "gunluk_fiyat": 5200.0,
        "puan": 4.9,
        "depozito": 8000.0,
        "badge": "🛡️ İsveç Güvenliği",
        "gorsel": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/4e/VOLVO_XC60_%28SPA%29_China_%2815%29.jpg/960px-VOLVO_XC60_%28SPA%29_China_%2815%29.jpg",
        "motor": "2.0 B5 Mild-Hybrid (250 HP / 350 Nm)",
        "sanziman": "8 İleri Otomatik",
        "tuketim": "7.2 Lt / 100 km",
        "hizlanma": "6.9 sn",
        "azami_hiz": "220 km/s",
        "cekis": "Dört Çeker (AWD)",
        "donanimlar": [
            "Pilot Assist",
            "Bowers & Wilkins Ses",
            "Panoramik Cam Tavan",
            "Isıtmalı Ön & Arka Koltuk",
            "360° Kamera",
        ],
    },
]
```


## `drivenow/invoice.py`

```python
"""Rezervasyon özeti / fatura PDF üretimi.

Türkçe karakterler için sistemde bulunan bir TTF font kullanılır; font
bulunamazsa Helvetica + transliterasyon ile güvenli çıktı alınır.
"""

from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

NAVY = HexColor("#0B1220")
NAVY_SOFT = HexColor("#152238")
ORANGE = HexColor("#FF6B2C")
TEAL = HexColor("#17B8A6")
MUTED = HexColor("#6B7A90")
LIGHT = HexColor("#F2F5F9")
LINE = HexColor("#DCE3EC")
INK = HexColor("#16202E")

_FONT_REGULAR = "Helvetica"
_FONT_BOLD = "Helvetica-Bold"
_TURKISH_OK = False


def _register_fonts() -> None:
    global _FONT_REGULAR, _FONT_BOLD, _TURKISH_OK
    pairs = [
        ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf"),
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ),
        (
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ),
    ]
    for regular, bold in pairs:
        if not (Path(regular).exists() and Path(bold).exists()):
            continue
        try:
            pdfmetrics.registerFont(TTFont("DNFont", regular))
            pdfmetrics.registerFont(TTFont("DNFont-Bold", bold))
            _FONT_REGULAR = "DNFont"
            _FONT_BOLD = "DNFont-Bold"
            _TURKISH_OK = True
            return
        except Exception:
            continue


_register_fonts()


def _tr(text: str) -> str:
    if _TURKISH_OK:
        return str(text)
    table = str.maketrans("ıİğĞüÜşŞöÖçÇ₺", "iIgGuUsSoOcCTL")
    return str(text).translate(table)


def _money(value: float) -> str:
    formatted = f"{float(value or 0):,.0f}".replace(",", ".")
    return f"{formatted} TL"


def _date(value: str) -> str:
    try:
        return datetime.fromisoformat(str(value)[:10]).strftime("%d.%m.%Y")
    except ValueError:
        return str(value)


def _wrap(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    font: str,
    size: float,
    leading: float,
    color=INK,
    max_lines: int = 3,
) -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    lines = simpleSplit(_tr(text), font, size, width)[:max_lines]
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def build_invoice(
    reservation: dict,
    user: dict | None,
    extras: list[dict] | None = None,
) -> bytes:
    """Rezervasyon verisinden tek sayfalık PDF üretir."""
    extras = extras or []
    buffer = io.BytesIO()
    width, height = A4
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setTitle(_tr(f"DriveNow Fatura {reservation.get('kod', '')}"))
    c.setAuthor("DriveNow Premium")
    c.setSubject(_tr("Araç kiralama rezervasyon özeti"))

    margin = 18 * mm
    content_width = width - 2 * margin

    # --- Üst bant ---------------------------------------------------------
    band_h = 40 * mm
    c.setFillColor(NAVY)
    c.rect(0, height - band_h, width, band_h, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(0, height - band_h, width, 2.2 * mm, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont(_FONT_BOLD, 26)
    c.drawString(margin, height - 17 * mm, "DriveNow")
    c.setFont(_FONT_REGULAR, 9)
    c.setFillColor(HexColor("#9FB0C7"))
    c.drawString(margin, height - 23 * mm, _tr("PREMIUM ARAÇ KİRALAMA"))

    c.setFont(_FONT_BOLD, 12)
    c.setFillColor(white)
    c.drawRightString(width - margin, height - 15 * mm, _tr("REZERVASYON ÖZETİ"))
    c.setFont(_FONT_REGULAR, 9)
    c.setFillColor(HexColor("#C8D4E3"))
    c.drawRightString(
        width - margin,
        height - 21 * mm,
        _tr(f"Fatura No: FTR-{datetime.now():%Y}-{int(reservation.get('id') or 0):05d}"),
    )
    c.drawRightString(
        width - margin,
        height - 26 * mm,
        _tr(f"Düzenleme: {datetime.now():%d.%m.%Y %H:%M}"),
    )

    y = height - band_h - 12 * mm

    # --- Müşteri / kiralama kutuları -------------------------------------
    box_w = (content_width - 6 * mm) / 2
    box_h = 38 * mm

    c.setFillColor(LIGHT)
    c.roundRect(margin, y - box_h, box_w, box_h, 3 * mm, fill=1, stroke=0)
    c.roundRect(margin + box_w + 6 * mm, y - box_h, box_w, box_h, 3 * mm, fill=1, stroke=0)

    c.setFillColor(MUTED)
    c.setFont(_FONT_BOLD, 7.5)
    c.drawString(margin + 5 * mm, y - 7 * mm, _tr("MÜŞTERİ"))
    c.drawString(margin + box_w + 11 * mm, y - 7 * mm, _tr("KİRALAMA"))

    name = (user or {}).get("ad") or "Müşteri"
    c.setFillColor(INK)
    c.setFont(_FONT_BOLD, 11)
    c.drawString(margin + 5 * mm, y - 14 * mm, _tr(name)[:38])
    c.setFont(_FONT_REGULAR, 8.5)
    c.setFillColor(HexColor("#3C4A5C"))
    c.drawString(
        margin + 5 * mm, y - 20 * mm, _tr(f"TC: {(user or {}).get('tc', '-')}")
    )
    c.drawString(
        margin + 5 * mm, y - 25 * mm, _tr(f"Tel: 0{(user or {}).get('tel', '-')}")
    )
    c.drawString(
        margin + 5 * mm, y - 30 * mm, _tr(f"E-posta: {(user or {}).get('email', '-')}")[:52]
    )

    c.setFont(_FONT_BOLD, 11)
    c.setFillColor(INK)
    c.drawString(
        margin + box_w + 11 * mm,
        y - 14 * mm,
        _tr(str(reservation.get("arac", "-")))[:34],
    )
    c.setFont(_FONT_REGULAR, 8.5)
    c.setFillColor(HexColor("#3C4A5C"))
    c.drawString(
        margin + box_w + 11 * mm,
        y - 20 * mm,
        _tr(f"Rezervasyon: {reservation.get('kod', '-')}"),
    )
    c.drawString(
        margin + box_w + 11 * mm,
        y - 25 * mm,
        _tr(
            f"Tarih: {_date(reservation.get('bas_tarih', ''))} - "
            f"{_date(reservation.get('bit_tarih', ''))} ({reservation.get('gun', 1)} gün)"
        ),
    )
    c.drawString(
        margin + box_w + 11 * mm,
        y - 30 * mm,
        _tr(f"Teslim: {str(reservation.get('konum', '-'))[:40]}"),
    )

    y -= box_h + 12 * mm

    # --- Kalem tablosu ----------------------------------------------------
    c.setFillColor(NAVY_SOFT)
    c.roundRect(margin, y - 9 * mm, content_width, 9 * mm, 2 * mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(_FONT_BOLD, 8)
    c.drawString(margin + 4 * mm, y - 6 * mm, _tr("AÇIKLAMA"))
    c.drawRightString(width - margin - 4 * mm, y - 6 * mm, _tr("TUTAR"))
    y -= 14 * mm

    rows: list[tuple[str, float, bool]] = [
        (
            f"Araç kiralama • {reservation.get('gun', 1)} gün × "
            f"{_money(reservation.get('gunluk_fiyat', 0))}",
            float(reservation.get("baz_tutar") or 0),
            False,
        )
    ]
    for extra in extras:
        rows.append(
            (
                f"{extra.get('ad', 'Ek hizmet')} • {extra.get('gun', 1)} gün",
                float(extra.get("tutar") or 0),
                False,
            )
        )
    if float(reservation.get("indirim_tutar") or 0) > 0:
        rows.append(
            (
                "İndirimler (uzun dönem / sadakat / kupon)",
                -float(reservation.get("indirim_tutar") or 0),
                True,
            )
        )
    if float(reservation.get("tek_yon_ucret") or 0) > 0:
        rows.append(
            ("Farklı noktaya iade", float(reservation.get("tek_yon_ucret") or 0), False)
        )
    if float(reservation.get("genc_sofor_ucret") or 0) > 0:
        rows.append(
            ("Genç sürücü ücreti", float(reservation.get("genc_sofor_ucret") or 0), False)
        )
    if float(reservation.get("uzatma_tutar") or 0) > 0:
        rows.append(
            ("Kiralama uzatma", float(reservation.get("uzatma_tutar") or 0), False)
        )

    for index, (label, amount, is_discount) in enumerate(rows):
        if index % 2 == 1:
            c.setFillColor(HexColor("#F7F9FC"))
            c.rect(margin, y - 3 * mm, content_width, 8 * mm, fill=1, stroke=0)
        c.setFillColor(INK if not is_discount else TEAL)
        c.setFont(_FONT_REGULAR, 8.5)
        c.drawString(margin + 4 * mm, y, _tr(label)[:72])
        c.setFont(_FONT_BOLD, 8.5)
        c.drawRightString(
            width - margin - 4 * mm,
            y,
            _tr(("-" if amount < 0 else "") + _money(abs(amount))),
        )
        y -= 8 * mm

    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(margin, y + 3 * mm, width - margin, y + 3 * mm)

    # --- Toplam kutusu ----------------------------------------------------
    y -= 4 * mm
    total_w = 78 * mm
    total_x = width - margin - total_w
    c.setFillColor(NAVY)
    c.roundRect(total_x, y - 20 * mm, total_w, 20 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(HexColor("#9FB0C7"))
    c.setFont(_FONT_BOLD, 7.5)
    c.drawString(total_x + 5 * mm, y - 6 * mm, _tr("GENEL TOPLAM"))
    c.setFillColor(white)
    c.setFont(_FONT_BOLD, 17)
    c.drawRightString(total_x + total_w - 5 * mm, y - 14 * mm, _tr(_money(reservation.get("toplam_tutar", 0))))
    c.setFont(_FONT_REGULAR, 7)
    c.setFillColor(HexColor("#C8D4E3"))
    c.drawRightString(total_x + total_w - 5 * mm, y - 18 * mm, _tr("KDV dahil"))

    deposit = float(reservation.get("depozito") or 0)
    if deposit > 0:
        c.setFillColor(MUTED)
        c.setFont(_FONT_REGULAR, 7.5)
        c.drawString(
            margin,
            y - 8 * mm,
            _tr(
                f"Depozito: {_money(deposit)} (araç iadesinde, hasar yoksa geri ödenir)"
            ),
        )

    # --- QR + notlar ------------------------------------------------------
    y -= 30 * mm
    qr_payload = (
        f"DriveNow|{reservation.get('kod', '')}|{reservation.get('toplam_tutar', 0)}|"
        f"{reservation.get('bas_tarih', '')}|{reservation.get('bit_tarih', '')}"
    )
    qr = QrCodeWidget(qr_payload, barLevel="M")
    bounds = qr.getBounds()
    qr_width = bounds[2] - bounds[0]
    qr_height = bounds[3] - bounds[1]
    target = 26 * mm
    drawing = Drawing(
        target,
        target,
        transform=[target / qr_width, 0, 0, target / qr_height, 0, 0],
    )
    drawing.add(qr)
    renderPDF.draw(drawing, c, margin, y - 12 * mm)

    note_x = margin + 34 * mm
    c.setFillColor(MUTED)
    c.setFont(_FONT_BOLD, 7.5)
    c.drawString(note_x, y - 2 * mm, _tr("ÖNEMLİ NOTLAR"))
    notes = [
        "Rezervasyon, yönetici onayından sonra kesinleşir.",
        "Teslimde ehliyet ve kimlik ibrazı zorunludur.",
        "Ücretsiz iptal: kiralama başlangıcından 24 saat öncesine kadar.",
        "Yakıt seviyesi teslimdeki seviyede iade edilmelidir.",
    ]
    c.setFont(_FONT_REGULAR, 7.2)
    c.setFillColor(HexColor("#3C4A5C"))
    note_y = y - 7 * mm
    for note in notes:
        c.drawString(note_x, note_y, _tr(f"• {note}"))
        note_y -= 4.2 * mm

    # --- Alt bilgi --------------------------------------------------------
    c.setStrokeColor(LINE)
    c.line(margin, 22 * mm, width - margin, 22 * mm)
    c.setFillColor(MUTED)
    c.setFont(_FONT_REGULAR, 7)
    c.drawString(
        margin,
        17 * mm,
        _tr("DriveNow Premium • destek@drivenow.com.tr • 0850 000 00 00"),
    )
    c.drawRightString(
        width - margin,
        17 * mm,
        _tr("Bu belge rezervasyon özetidir; mali fatura yerine geçmez."),
    )
    c.drawString(margin, 13 * mm, _tr("drive-now.example • Konya / Türkiye"))

    c.showPage()
    c.save()
    return buffer.getvalue()
```


## `drivenow/mailer.py`

```python
"""E-posta gönderimi (opsiyonel).

SMTP bilgileri secrets/ortam değişkeninden gelir. Yapılandırılmamışsa
rezervasyon akışı bozulmaz; kullanıcıya yalnızca bilgilendirme gösterilir.
"""

from __future__ import annotations

import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from .config import (
    APP_NAME,
    SMTP_FROM,
    SMTP_FROM_NAME,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USER,
)


def email_configured() -> bool:
    return bool(SMTP_USER and SMTP_PASSWORD)


def _sender() -> str:
    address = SMTP_FROM or SMTP_USER
    if SMTP_FROM_NAME:
        return formataddr((SMTP_FROM_NAME, address))
    return address


def send_invoice(
    to_email: str,
    pdf_bytes: bytes,
    customer_name: str,
    reservation_code: str,
    total: float,
) -> tuple[bool, str]:
    if not email_configured():
        return (
            False,
            "E-posta servisi yapılandırılmadı. SMTP_USER ve SMTP_PASSWORD "
            "değerlerini secrets dosyasına ekleyin.",
        )
    if not to_email or "@" not in to_email:
        return False, "Geçerli bir alıcı e-postası yok."

    html = f"""
    <div style="font-family:Arial,Helvetica,sans-serif;background:#f4f6fa;padding:24px">
      <div style="max-width:560px;margin:auto;background:#ffffff;border-radius:16px;overflow:hidden;
                  border:1px solid #e3e8f0">
        <div style="background:#0b1220;padding:26px 28px">
          <div style="color:#ff6b2c;font-size:12px;letter-spacing:2px;font-weight:700">
            DRIVENOW PREMIUM
          </div>
          <div style="color:#ffffff;font-size:24px;font-weight:800;margin-top:6px">
            Rezervasyonunuz alındı
          </div>
        </div>
        <div style="padding:26px 28px;color:#1b2635;font-size:14px;line-height:1.65">
          <p>Merhaba <b>{customer_name}</b>,</p>
          <p>
            <b>{reservation_code}</b> numaralı rezervasyonunuz oluşturuldu.
            Yönetici onayından sonra kiralama kesinleşecek. Özet belgeniz ekte yer alıyor.
          </p>
          <table style="width:100%;border-collapse:collapse;margin:18px 0">
            <tr>
              <td style="padding:10px 0;color:#6b7a90">Toplam tutar</td>
              <td style="padding:10px 0;text-align:right;font-weight:800;color:#ff6b2c">
                {total:,.0f} TL
              </td>
            </tr>
            <tr>
              <td style="padding:10px 0;color:#6b7a90;border-top:1px solid #eef2f7">Rezervasyon kodu</td>
              <td style="padding:10px 0;text-align:right;font-weight:700;border-top:1px solid #eef2f7">
                {reservation_code}
              </td>
            </tr>
          </table>
          <p style="color:#6b7a90;font-size:12px">
            Sorularınız için destek@drivenow.com.tr adresine yazabilirsiniz.
          </p>
        </div>
        <div style="background:#f7f9fc;padding:16px 28px;color:#8a99ad;font-size:11px">
          {APP_NAME} Premium • Bu e-posta otomatik gönderilmiştir.
        </div>
      </div>
    </div>
    """

    message = EmailMessage()
    message["Subject"] = f"DriveNow • Rezervasyonunuz alındı ({reservation_code})"
    message["From"] = _sender()
    message["To"] = to_email
    message.set_content(
        f"Merhaba {customer_name},\n\n"
        f"{reservation_code} numaralı rezervasyonunuz oluşturuldu.\n"
        f"Toplam tutar: {total:,.0f} TL\n\n"
        "Detaylı özet ekteki PDF dosyasındadır.\n\nDriveNow Premium"
    )
    message.add_alternative(html, subtype="html")
    message.add_attachment(
        pdf_bytes,
        maintype="application",
        subtype="pdf",
        filename=f"DriveNow_{reservation_code}.pdf",
    )

    try:
        if int(SMTP_PORT) == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, int(SMTP_PORT), timeout=20) as smtp:
                smtp.login(SMTP_USER, SMTP_PASSWORD)
                smtp.send_message(message)
        else:
            with smtplib.SMTP(SMTP_HOST, int(SMTP_PORT), timeout=20) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(SMTP_USER, SMTP_PASSWORD)
                smtp.send_message(message)
        return True, ""
    except Exception as exc:  # noqa: BLE001 - kullanıcıya anlamlı mesaj dönüyoruz
        return False, f"{type(exc).__name__}: {exc}"
```


## `drivenow/pricing.py`

```python
"""Fiyatlandırma motoru.

Tek bir yerde hesaplanır; rezervasyon, fatura ve yönetim ekranı aynı
sonucu kullanır. Para birimi TL, fiyatlar KDV dahildir.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

from .config import (
    CANCELLATION_HOURS,
    LONG_TERM_TIERS,
    ONE_WAY_FEE,
    YOUNG_DRIVER_DAILY,
)
from .db import get_coupon


@dataclass(frozen=True)
class ExtraOption:
    key: str
    ad: str
    gunluk: float
    aciklama: str
    icon: str


EXTRAS: tuple[ExtraOption, ...] = (
    ExtraOption(
        "bebek",
        "Bebek Koltuğu",
        150.0,
        "0-3 yaş, ISOFIX uyumlu, temizlenmiş kılıf",
        "👶",
    ),
    ExtraOption(
        "wifi",
        "Araç İçi Wi-Fi",
        100.0,
        "Sınırsız internet, 5 cihaza kadar bağlantı",
        "📶",
    ),
    ExtraOption(
        "kasko",
        "Sınırsız Muafiyetsiz Kasko",
        300.0,
        "Hasar durumunda muafiyet ödemesi yok",
        "🛡️",
    ),
    ExtraOption(
        "sofor",
        "Ek Sürücü",
        120.0,
        "Aynı araç için ikinci yetkili sürücü",
        "🧑‍🤝‍🧑",
    ),
    ExtraOption(
        "gps",
        "Navigasyon & GPS",
        50.0,
        "Offline Türkiye haritası ve trafik",
        "🧭",
    ),
)

EXTRA_MAP = {extra.key: extra for extra in EXTRAS}


@dataclass
class QuoteLine:
    label: str
    amount: float
    note: str = ""


@dataclass
class Quote:
    days: int
    daily: float
    base: float
    extras_total: float
    duration_discount: float
    loyalty_discount: float
    coupon_discount: float
    one_way_fee: float
    young_driver_fee: float
    total: float
    deposit: float
    discount_total: float
    extras: list[dict] = field(default_factory=list)
    coupon_code: str | None = None
    coupon_error: str = ""
    duration_label: str = ""
    loyalty_label: str = ""
    lines: list[QuoteLine] = field(default_factory=list)


def days_between(start: date, end: date) -> int:
    return max(1, (end - start).days)


def duration_discount(days: int) -> tuple[float, str]:
    for threshold, rate, label in LONG_TERM_TIERS:
        if days >= threshold:
            return rate, label
    return 0.0, ""


def validate_coupon(code: str, base: float) -> tuple[dict | None, str]:
    code = (code or "").strip()
    if not code:
        return None, ""
    coupon = get_coupon(code)
    if not coupon:
        return None, "Kupon kodu bulunamadı."
    if not int(coupon.get("aktif") or 0):
        return None, "Bu kupon artık kullanılmıyor."
    today = date.today().isoformat()
    bitis = str(coupon.get("bitis") or "")
    baslangic = str(coupon.get("baslangic") or "")
    if bitis and today > bitis[:10]:
        return None, "Kuponun son kullanma tarihi geçmiş."
    if baslangic and today < baslangic[:10]:
        return None, "Kupon henüz başlamadı."
    max_k = int(coupon.get("max_kullanim") or 0)
    if max_k > 0 and int(coupon.get("kullanim") or 0) >= max_k:
        return None, "Kupon kullanım limiti dolmuş."
    if base < float(coupon.get("min_tutar") or 0):
        return (
            None,
            f"Bu kupon için minimum sepet {float(coupon['min_tutar']):,.0f} ₺.",
        )
    return coupon, ""


def coupon_amount(coupon: dict, amount: float) -> float:
    if not coupon:
        return 0.0
    if coupon.get("tip") == "sabit":
        return min(float(coupon.get("deger") or 0), amount)
    return amount * float(coupon.get("deger") or 0) / 100.0


def quote(
    vehicle: dict,
    days: int,
    selected_extras: set[str] | None = None,
    coupon_code: str = "",
    one_way: bool = False,
    young_driver: bool = False,
    loyalty_rate: float = 0.0,
    loyalty_label: str = "",
) -> Quote:
    days = max(1, int(days))
    selected_extras = selected_extras or set()
    daily = float(vehicle.get("gunluk_fiyat") or 0)
    base = daily * days

    extras: list[dict] = []
    extras_total = 0.0
    for option in EXTRAS:
        if option.key not in selected_extras:
            continue
        tutar = option.gunluk * days
        extras_total += tutar
        extras.append(
            {
                "ad": option.ad,
                "gunluk_fiyat": option.gunluk,
                "gun": days,
                "tutar": tutar,
            }
        )

    duration_rate, duration_label = duration_discount(days)
    duration_discount_amount = base * duration_rate
    loyalty_discount_amount = base * max(0.0, float(loyalty_rate))
    after_discounts = base - duration_discount_amount - loyalty_discount_amount

    coupon, coupon_error = validate_coupon(coupon_code, base)
    coupon_discount_amount = coupon_amount(coupon, max(0.0, after_discounts))

    one_way_fee = ONE_WAY_FEE if one_way else 0.0
    young_fee = YOUNG_DRIVER_DAILY * days if young_driver else 0.0

    total = (
        base
        - duration_discount_amount
        - loyalty_discount_amount
        - coupon_discount_amount
        + extras_total
        + one_way_fee
        + young_fee
    )
    total = max(0.0, round(total, 2))
    discount_total = round(
        duration_discount_amount + loyalty_discount_amount + coupon_discount_amount, 2
    )

    lines = [QuoteLine(f"{days} gün × {daily:,.0f} ₺", base)]
    if duration_discount_amount:
        lines.append(
            QuoteLine(duration_label, -round(duration_discount_amount, 2), "Uzun dönem")
        )
    if loyalty_discount_amount:
        lines.append(
            QuoteLine(
                f"{loyalty_label or 'Sadakat'} indirimi",
                -round(loyalty_discount_amount, 2),
                "Tamamlanan kiralamalar",
            )
        )
    if coupon_discount_amount:
        lines.append(
            QuoteLine(
                f"Kupon • {coupon['kod']}",
                -round(coupon_discount_amount, 2),
                coupon.get("aciklama") or "",
            )
        )
    for extra in extras:
        lines.append(
            QuoteLine(
                f"{extra['ad']} • {days} gün",
                round(extra["tutar"], 2),
                f"{extra['gunluk_fiyat']:,.0f} ₺/gün",
            )
        )
    if one_way_fee:
        lines.append(QuoteLine("Farklı noktaya iade", one_way_fee, "Tek yön ücreti"))
    if young_fee:
        lines.append(
            QuoteLine(
                "Genç sürücü ücreti",
                young_fee,
                f"{YOUNG_DRIVER_DAILY:,.0f} ₺/gün",
            )
        )

    return Quote(
        days=days,
        daily=daily,
        base=round(base, 2),
        extras_total=round(extras_total, 2),
        duration_discount=round(duration_discount_amount, 2),
        loyalty_discount=round(loyalty_discount_amount, 2),
        coupon_discount=round(coupon_discount_amount, 2),
        one_way_fee=one_way_fee,
        young_driver_fee=young_fee,
        total=total,
        deposit=float(vehicle.get("depozito") or 0),
        discount_total=discount_total,
        extras=extras,
        coupon_code=coupon["kod"] if coupon else None,
        coupon_error=coupon_error,
        duration_label=duration_label,
        loyalty_label=loyalty_label,
        lines=lines,
    )


def can_cancel_free(start_date: str | date, now: datetime | None = None) -> bool:
    """Kiralama başlangıcına 24 saatten fazla varsa ücretsiz iptal."""
    now = now or datetime.now()
    if isinstance(start_date, str):
        try:
            start = datetime.fromisoformat(start_date[:10])
        except ValueError:
            return False
    else:
        start = datetime.combine(start_date, datetime.min.time())
    return (start - now).total_seconds() >= CANCELLATION_HOURS * 3600
```


## `drivenow/security.py`

```python
"""Parola, OTP ve dosya adı güvenliği."""

from __future__ import annotations

import base64
import hashlib
import hmac
import re
import secrets
from pathlib import Path

PBKDF2_ITERATIONS = 260_000


def hash_password(password: str, iterations: int = PBKDF2_ITERATIONS) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return "pbkdf2_sha256${}${}${}".format(
        iterations,
        base64.b64encode(salt).decode(),
        base64.b64encode(digest).decode(),
    )


def verify_password(password: str, stored: str) -> bool:
    if not stored or not password:
        return False
    try:
        algorithm, iterations, salt_b64, digest_b64 = stored.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(digest_b64)
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, int(iterations)
        )
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


def generate_otp() -> str:
    return f"{secrets.randbelow(900_000) + 100_000}"


def constant_time_equal(left: str, right: str) -> bool:
    return hmac.compare_digest(str(left or ""), str(right or ""))


def safe_filename(name: str, fallback: str = "dosya") -> str:
    """Yol geçişi ve tehlikeli karakterleri temizler."""
    base = Path(str(name or "")).name
    base = base.replace("\x00", "")
    cleaned = re.sub(r"[^\w.\-]", "_", base, flags=re.UNICODE)
    cleaned = cleaned.strip("._")
    if not cleaned:
        cleaned = fallback
    return cleaned[:120]


def safe_folder_name(name: str, fallback: str = "kayit") -> str:
    cleaned = re.sub(r"[^\w\-]", "_", str(name or ""), flags=re.UNICODE).strip("_")
    return (cleaned or fallback)[:60]
```


## `drivenow/sms.py`

```python
"""SMS gönderimi.

Demo modunda gerçek SMS gönderilmez, kod arayüzde gösterilir. Canlıda
SMS_WEBHOOK_URL tanımlanarak herhangi bir SMS sağlayıcısına bağlanılabilir.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from .config import DEMO_MODE, SMS_WEBHOOK_TOKEN, SMS_WEBHOOK_URL


def sms_configured() -> bool:
    return bool(SMS_WEBHOOK_URL)


def send_sms(phone: str, message: str) -> tuple[bool, str]:
    if DEMO_MODE and not sms_configured():
        return True, "demo"
    if not sms_configured():
        return (
            False,
            "SMS sağlayıcısı tanımlı değil. SMS_WEBHOOK_URL ekleyin veya "
            "DEMO_MODE=true bırakın.",
        )
    payload = json.dumps({"phone": phone, "message": message}).encode("utf-8")
    request = urllib.request.Request(
        SMS_WEBHOOK_URL,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            **(
                {"Authorization": f"Bearer {SMS_WEBHOOK_TOKEN}"}
                if SMS_WEBHOOK_TOKEN
                else {}
            ),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            if 200 <= response.status < 300:
                return True, ""
            return False, f"SMS servisi HTTP {response.status} döndürdü."
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return False, f"SMS gönderilemedi: {exc}"
```


## `drivenow/state.py`

```python
"""Oturum durumu yardımcıları."""

from __future__ import annotations

import time

import streamlit as st

from .config import SESSION_TIMEOUT_MINUTES

DEFAULTS: dict = {
    "auth": False,
    "user": None,
    "guest": False,
    "auth_stage": "form",
    "pending_user": None,
    "otp_code": None,
    "otp_expires": 0.0,
    "otp_attempts": 0,
    "otp_requests": [],
    "nav": "Filo",
    "secili": None,
    "booking_step": 1,
    "booking_coupon": None,
    "booking_extras": [],
    "booking_driver": {},
    "booking_success": None,
    "last_reservation": None,
    "email_result": None,
    "admin_ok": False,
    "admin_attempts": 0,
    "admin_lock_until": 0.0,
    "flash": None,
    "auth_notice": None,
    "compare": [],
    "last_activity": 0.0,
    "filters_reset": 0,
    "show_booking_success": False,
}


def init_state() -> None:
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if not st.session_state.get("last_activity"):
        touch_session()


def touch_session() -> None:
    st.session_state["last_activity"] = time.time()


def session_expired() -> bool:
    last = float(st.session_state.get("last_activity") or 0)
    return last > 0 and (time.time() - last) > SESSION_TIMEOUT_MINUTES * 60


def current_user() -> dict | None:
    user = st.session_state.get("user")
    return user if isinstance(user, dict) and user else None


def user_id() -> int | None:
    user = current_user()
    if not user:
        return None
    try:
        return int(user.get("id"))
    except (TypeError, ValueError):
        return None


def is_guest() -> bool:
    return bool(st.session_state.get("guest"))


def set_flash(message: str, kind: str = "success") -> None:
    st.session_state["flash"] = (kind, message)


def pop_flash() -> tuple[str, str] | None:
    flash = st.session_state.get("flash")
    st.session_state["flash"] = None
    return flash if isinstance(flash, tuple) else None


def show_flash() -> None:
    flash = pop_flash()
    if not flash:
        return
    kind, message = flash
    if kind == "success":
        st.success(message)
    elif kind == "error":
        st.error(message)
    elif kind == "warning":
        st.warning(message)
    else:
        st.info(message)


def logout() -> None:
    keep = {"nav"}
    for key in list(DEFAULTS.keys()):
        if key in keep:
            continue
        st.session_state[key] = DEFAULTS[key]
    st.session_state["nav"] = "Filo"
    st.session_state["last_activity"] = time.time()


def go(nav: str) -> None:
    st.session_state["nav"] = nav
    st.rerun()
```


## `drivenow/theme.py`

```python
"""Uygulamanın görsel teması (tek parça CSS)."""

from __future__ import annotations

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

:root {
    --dn-bg: #070b12;
    --dn-bg-soft: #0b1220;
    --dn-panel: rgba(17, 25, 40, 0.72);
    --dn-panel-solid: #111928;
    --dn-line: rgba(255, 255, 255, 0.08);
    --dn-line-strong: rgba(255, 255, 255, 0.14);
    --dn-text: #e9eef7;
    --dn-muted: #93a3b8;
    --dn-faint: #6b7c93;
    --dn-orange: #ff6b2c;
    --dn-orange-2: #ff3d57;
    --dn-teal: #1fc8b3;
    --dn-blue: #5b9dff;
    --dn-gold: #f5c451;
    --dn-red: #ff5c72;
    --dn-radius: 18px;
    --dn-shadow: 0 22px 55px rgba(0, 0, 0, 0.38);
}

html, body, [class*="css"] {
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.stApp {
    background:
        radial-gradient(1100px 520px at 12% -12%, rgba(255, 107, 44, 0.13), transparent 60%),
        radial-gradient(900px 480px at 92% -6%, rgba(31, 200, 179, 0.10), transparent 58%),
        linear-gradient(180deg, #070b12 0%, #0a101b 55%, #070b12 100%);
    background-attachment: fixed;
    color: var(--dn-text);
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(255, 255, 255, 0.022) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.022) 1px, transparent 1px);
    background-size: 64px 64px;
    mask-image: radial-gradient(circle at 50% 0%, black 0%, transparent 72%);
    z-index: 0;
}

.block-container {
    max-width: 1240px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

#MainMenu, footer { visibility: hidden; }

header[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3, h4, h5, h6 {
    font-family: "Sora", "Inter", sans-serif !important;
    color: var(--dn-text) !important;
    letter-spacing: -0.02em;
}

p, span, label, li, div {
    color: inherit;
}

a { color: var(--dn-blue); }

/* --- Üst bar ---------------------------------------------------------- */
.dn-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 6px 2px 18px 2px;
}
.dn-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}
.dn-brand-mark {
    width: 42px;
    height: 42px;
    border-radius: 13px;
    display: grid;
    place-items: center;
    font-size: 20px;
    background: linear-gradient(135deg, var(--dn-orange) 0%, var(--dn-orange-2) 100%);
    box-shadow: 0 10px 24px rgba(255, 107, 44, 0.32);
}
.dn-brand-name {
    font-family: "Sora", sans-serif;
    font-size: 20px;
    font-weight: 800;
    line-height: 1.05;
    color: #fff;
}
.dn-brand-name span { color: var(--dn-orange); }
.dn-brand-sub {
    font-size: 10px;
    letter-spacing: 2.2px;
    color: var(--dn-faint);
    text-transform: uppercase;
}
.dn-user-chip {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--dn-line);
    padding: 7px 12px 7px 8px;
    border-radius: 999px;
}
.dn-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    font-size: 12px;
    font-weight: 800;
    color: #fff;
    background: linear-gradient(135deg, #24344d, #101827);
    border: 1px solid var(--dn-line-strong);
}
.dn-user-chip b { font-size: 12.5px; color: var(--dn-text); }
.dn-user-chip small { display: block; font-size: 10px; color: var(--dn-faint); }

/* --- Navigasyon (segmented control) ----------------------------------- */
.stButtonGroup {
    background: rgba(13, 20, 33, 0.72);
    border: 1px solid var(--dn-line);
    padding: 6px;
    border-radius: 16px;
    gap: 4px;
    backdrop-filter: blur(14px);
}
.stButtonGroup [data-variant="segmented_control"] {
    border-radius: 11px !important;
    color: var(--dn-muted) !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    padding: 9px 16px !important;
    transition: all 0.18s ease !important;
}
.stButtonGroup [data-variant="segmented_control"]:hover {
    color: var(--dn-text) !important;
    background: rgba(255, 255, 255, 0.05) !important;
}
.stButtonGroup [data-selected] {
    background: linear-gradient(135deg, rgba(255, 107, 44, 0.18), rgba(255, 61, 87, 0.12)) !important;
    border-color: rgba(255, 107, 44, 0.38) !important;
    color: #fff !important;
    box-shadow: 0 6px 18px rgba(255, 107, 44, 0.18) !important;
}
.stButtonGroup [data-selected] * { color: #fff !important; }

/* --- Hero ------------------------------------------------------------- */
.dn-hero {
    position: relative;
    overflow: hidden;
    padding: 42px 38px;
    border-radius: 28px;
    border: 1px solid var(--dn-line);
    background:
        linear-gradient(135deg, rgba(23, 34, 54, 0.92) 0%, rgba(10, 16, 28, 0.92) 100%);
    box-shadow: var(--dn-shadow);
    margin-bottom: 26px;
}
.dn-hero::after {
    content: "";
    position: absolute;
    width: 420px;
    height: 420px;
    right: -120px;
    top: -160px;
    background: radial-gradient(circle, rgba(255, 107, 44, 0.22), transparent 68%);
    pointer-events: none;
}
.dn-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: var(--dn-teal);
    background: rgba(31, 200, 179, 0.10);
    border: 1px solid rgba(31, 200, 179, 0.24);
    padding: 7px 13px;
    border-radius: 999px;
    margin-bottom: 18px;
}
.dn-hero h1 {
    font-size: clamp(34px, 5vw, 58px) !important;
    line-height: 1.03 !important;
    margin: 0 0 16px 0 !important;
    font-weight: 800 !important;
    color: #fff !important;
}
.dn-hero h1 em {
    font-style: normal;
    background: linear-gradient(92deg, #ffb38a 0%, var(--dn-orange) 45%, #ff5f7a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.dn-hero p {
    color: var(--dn-muted) !important;
    font-size: 15.5px;
    line-height: 1.65;
    max-width: 640px;
    margin: 0 0 22px 0;
}
.dn-hero-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 28px;
    margin-top: 26px;
    padding-top: 22px;
    border-top: 1px solid var(--dn-line);
}
.dn-hero-stats div b {
    display: block;
    font-family: "Sora", sans-serif;
    font-size: 21px;
    color: #fff;
}
.dn-hero-stats div span {
    font-size: 11px;
    letter-spacing: 0.8px;
    color: var(--dn-faint);
}

/* --- Kartlar ---------------------------------------------------------- */
.dn-card {
    background: var(--dn-panel);
    border: 1px solid var(--dn-line);
    border-radius: var(--dn-radius);
    padding: 22px;
    backdrop-filter: blur(14px);
    box-shadow: 0 14px 38px rgba(0, 0, 0, 0.26);
}
.dn-card + .dn-card { margin-top: 14px; }

.dn-car {
    display: flex;
    gap: 20px;
    background: var(--dn-panel);
    border: 1px solid var(--dn-line);
    border-radius: 22px;
    padding: 20px;
    backdrop-filter: blur(14px);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.28);
    transition: transform 0.22s ease, border-color 0.22s ease;
    margin-bottom: 12px;
}
.dn-car:hover {
    transform: translateY(-3px);
    border-color: rgba(255, 107, 44, 0.34);
}
.dn-car__media {
    position: relative;
    flex: 0 0 218px;
    width: 218px;
    height: 148px;
    border-radius: 16px;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(31, 200, 179, 0.12), rgba(255, 107, 44, 0.10));
    border: 1px solid var(--dn-line);
    display: grid;
    place-items: center;
    font-size: 38px;
}
.dn-car__media img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}
.dn-car:hover .dn-car__media img { transform: scale(1.06); }
.dn-car__body { flex: 1 1 320px; min-width: 0; }
.dn-car__top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
}
.dn-car__cat {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.7px;
    color: var(--dn-teal);
    margin-bottom: 3px;
}
.dn-car__title {
    font-family: "Sora", sans-serif;
    font-size: 21px;
    font-weight: 700;
    color: #fff;
    line-height: 1.2;
    margin-bottom: 9px;
}
.dn-rating {
    flex: 0 0 auto;
    font-size: 11.5px;
    font-weight: 800;
    color: var(--dn-gold);
    background: rgba(245, 196, 81, 0.10);
    border: 1px solid rgba(245, 196, 81, 0.22);
    padding: 4px 9px;
    border-radius: 9px;
    white-space: nowrap;
}
.dn-badges { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
.dn-badge {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.2px;
    color: #ffd0b8;
    background: rgba(255, 107, 44, 0.10);
    border: 1px solid rgba(255, 107, 44, 0.22);
    padding: 3px 9px;
    border-radius: 999px;
}
.dn-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.dn-chip {
    font-size: 11px;
    font-weight: 600;
    color: #c5d2e3;
    background: rgba(255, 255, 255, 0.045);
    border: 1px solid var(--dn-line);
    padding: 5px 10px;
    border-radius: 9px;
    white-space: nowrap;
}
.dn-chip--ok {
    color: #7ff0dc;
    background: rgba(31, 200, 179, 0.10);
    border-color: rgba(31, 200, 179, 0.25);
}
.dn-chip--bad {
    color: #ffb3bf;
    background: rgba(255, 92, 114, 0.10);
    border-color: rgba(255, 92, 114, 0.25);
}
.dn-chip--warn {
    color: #ffd98a;
    background: rgba(245, 196, 81, 0.10);
    border-color: rgba(245, 196, 81, 0.24);
}
.dn-price-row {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 14px;
    margin-top: 14px;
    padding-top: 13px;
    border-top: 1px dashed var(--dn-line);
}
.dn-price-label {
    font-size: 9.5px;
    letter-spacing: 1.1px;
    text-transform: uppercase;
    color: var(--dn-faint);
    margin-bottom: 2px;
}
.dn-price {
    font-family: "Sora", sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    line-height: 1;
}
.dn-price--accent { color: var(--dn-orange); }
.dn-price small { font-size: 11px; color: var(--dn-faint); font-weight: 500; }
.dn-deposit { font-size: 10.5px; color: var(--dn-faint); margin-top: 5px; }

/* --- Bölüm başlıkları -------------------------------------------------- */
.dn-section {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 16px;
    margin: 30px 0 14px 0;
}
.dn-section h2 {
    font-size: 24px !important;
    margin: 0 !important;
    font-weight: 700 !important;
}
.dn-section p {
    margin: 5px 0 0 0 !important;
    color: var(--dn-muted) !important;
    font-size: 13px;
}
.dn-kicker {
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--dn-orange);
    margin-bottom: 6px;
}

/* --- Özellik / güven kartları ----------------------------------------- */
.dn-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 12px;
}
.dn-feature {
    background: rgba(255, 255, 255, 0.032);
    border: 1px solid var(--dn-line);
    border-radius: 16px;
    padding: 18px;
    transition: border-color 0.2s ease, transform 0.2s ease;
}
.dn-feature:hover {
    border-color: rgba(31, 200, 179, 0.32);
    transform: translateY(-2px);
}
.dn-feature__icon {
    width: 38px;
    height: 38px;
    border-radius: 11px;
    display: grid;
    place-items: center;
    font-size: 18px;
    background: rgba(31, 200, 179, 0.10);
    border: 1px solid rgba(31, 200, 179, 0.20);
    margin-bottom: 12px;
}
.dn-feature b {
    display: block;
    font-size: 13.5px;
    color: #fff;
    margin-bottom: 4px;
}
.dn-feature span { font-size: 12px; color: var(--dn-muted); line-height: 1.55; }

/* --- KPI -------------------------------------------------------------- */
.dn-kpi {
    background: linear-gradient(145deg, rgba(23, 34, 54, 0.85), rgba(12, 19, 32, 0.85));
    border: 1px solid var(--dn-line);
    border-radius: 16px;
    padding: 17px 18px;
    height: 100%;
}
.dn-kpi__label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    color: var(--dn-faint);
    margin-bottom: 8px;
}
.dn-kpi__value {
    font-family: "Sora", sans-serif;
    font-size: 25px;
    font-weight: 700;
    color: #fff;
    line-height: 1.1;
}
.dn-kpi__hint { font-size: 11px; color: var(--dn-muted); margin-top: 6px; }
.dn-kpi--accent { border-color: rgba(255, 107, 44, 0.28); }
.dn-kpi--teal { border-color: rgba(31, 200, 179, 0.24); }

/* --- Durum etiketleri -------------------------------------------------- */
.dn-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.4px;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid transparent;
    white-space: nowrap;
}
.dn-status::before {
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
}
.dn-status--pending { color: var(--dn-gold); background: rgba(245, 196, 81, 0.10); border-color: rgba(245, 196, 81, 0.25); }
.dn-status--active { color: var(--dn-teal); background: rgba(31, 200, 179, 0.10); border-color: rgba(31, 200, 179, 0.25); }
.dn-status--done { color: var(--dn-blue); background: rgba(91, 157, 255, 0.10); border-color: rgba(91, 157, 255, 0.25); }
.dn-status--cancel { color: var(--dn-red); background: rgba(255, 92, 114, 0.10); border-color: rgba(255, 92, 114, 0.25); }

/* --- Adım göstergesi --------------------------------------------------- */
.dn-steps {
    display: flex;
    gap: 8px;
    margin: 4px 0 18px 0;
}
.dn-step {
    flex: 1;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid var(--dn-line);
    background: rgba(255, 255, 255, 0.025);
    font-size: 11.5px;
    color: var(--dn-faint);
    font-weight: 600;
}
.dn-step b { display: block; font-size: 9px; letter-spacing: 1.4px; color: var(--dn-faint); margin-bottom: 3px; }
.dn-step--on {
    border-color: rgba(255, 107, 44, 0.42);
    background: rgba(255, 107, 44, 0.09);
    color: #fff;
}
.dn-step--on b { color: var(--dn-orange); }
.dn-step--done { border-color: rgba(31, 200, 179, 0.28); color: #bfeee7; }

/* --- Özet satırları ---------------------------------------------------- */
.dn-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    padding: 8px 0;
    border-bottom: 1px dashed rgba(255, 255, 255, 0.055);
    font-size: 12.5px;
}
.dn-row:last-child { border-bottom: none; }
.dn-row span { color: var(--dn-muted); }
.dn-row b { color: #fff; font-weight: 700; white-space: nowrap; }
.dn-row small { display: block; color: var(--dn-faint); font-size: 10.5px; margin-top: 2px; }
.dn-row--total {
    margin-top: 8px;
    padding-top: 14px;
    border-top: 1px solid var(--dn-line-strong);
    border-bottom: none;
    align-items: center;
}
.dn-row--total span { font-size: 13px; color: #fff; font-weight: 700; }
.dn-row--total b {
    font-family: "Sora", sans-serif;
    font-size: 24px;
    color: var(--dn-orange);
}
.dn-row--discount b { color: var(--dn-teal); }

/* --- Profil ------------------------------------------------------------ */
.dn-profile {
    display: flex;
    align-items: center;
    gap: 18px;
    flex-wrap: wrap;
}
.dn-profile .dn-avatar { width: 62px; height: 62px; font-size: 21px; }
.dn-profile h3 { margin: 0 !important; font-size: 22px !important; }
.dn-profile p { margin: 3px 0 0 0 !important; color: var(--dn-muted) !important; font-size: 12.5px; }
.dn-tier {
    margin-left: auto;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 7px 13px;
    border-radius: 999px;
    color: var(--dn-gold);
    background: rgba(245, 196, 81, 0.10);
    border: 1px solid rgba(245, 196, 81, 0.28);
}

/* --- Boş durum / not --------------------------------------------------- */
.dn-empty {
    text-align: center;
    padding: 42px 24px;
    border: 1px dashed var(--dn-line-strong);
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.018);
}
.dn-empty__icon { font-size: 34px; margin-bottom: 10px; }
.dn-empty b { display: block; color: #fff; font-size: 14px; margin-bottom: 5px; }
.dn-empty span { color: var(--dn-muted); font-size: 12.5px; }
.dn-note {
    font-size: 11.5px;
    color: var(--dn-muted);
    background: rgba(91, 157, 255, 0.06);
    border: 1px solid rgba(91, 157, 255, 0.16);
    border-radius: 11px;
    padding: 10px 13px;
    line-height: 1.5;
}
.dn-note--warn {
    background: rgba(245, 196, 81, 0.07);
    border-color: rgba(245, 196, 81, 0.20);
    color: #ffd98a;
}
.dn-note--ok {
    background: rgba(31, 200, 179, 0.07);
    border-color: rgba(31, 200, 179, 0.20);
    color: #9defe3;
}

/* --- OTP --------------------------------------------------------------- */
.dn-otp {
    text-align: center;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid rgba(255, 107, 44, 0.25);
    background: rgba(255, 107, 44, 0.06);
    margin-bottom: 16px;
}
.dn-otp__code {
    font-family: "Sora", monospace;
    font-size: 38px;
    letter-spacing: 12px;
    color: var(--dn-orange);
    font-weight: 800;
    margin: 6px 0 4px 0;
}
.dn-otp small { color: var(--dn-muted); font-size: 11px; }

/* --- Yorum ------------------------------------------------------------- */
.dn-quote {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--dn-line);
    border-radius: 16px;
    padding: 18px;
    height: 100%;
}
.dn-quote__stars { color: var(--dn-gold); font-size: 12px; letter-spacing: 1px; margin-bottom: 8px; }
.dn-quote p { font-size: 12.5px; color: #d6e0ee !important; line-height: 1.6; margin: 0 0 12px 0; }
.dn-quote b { font-size: 11.5px; color: #fff; }
.dn-quote span { display: block; font-size: 10.5px; color: var(--dn-faint); margin-top: 2px; }

/* --- Footer ------------------------------------------------------------ */
.dn-footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid var(--dn-line);
    display: flex;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
    color: var(--dn-faint);
    font-size: 11px;
}
.dn-footer b { color: var(--dn-muted); }

/* --- Streamlit widget'ları -------------------------------------------- */
div.stButton > button,
div.stFormSubmitButton > button,
div[data-testid="stDownloadButton"] > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 13.5px !important;
    border: 1px solid var(--dn-line-strong) !important;
    background: rgba(255, 255, 255, 0.05) !important;
    color: var(--dn-text) !important;
    min-height: 42px !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease !important;
}
div.stButton > button:hover,
div.stFormSubmitButton > button:hover,
div[data-testid="stDownloadButton"] > button:hover {
    transform: translateY(-1px);
    border-color: rgba(255, 107, 44, 0.42) !important;
    background: rgba(255, 107, 44, 0.10) !important;
}
div.stButton > button:focus-visible,
div.stFormSubmitButton > button:focus-visible,
div[data-testid="stDownloadButton"] > button:focus-visible {
    outline: 2px solid rgba(255, 107, 44, 0.65) !important;
    outline-offset: 2px !important;
}

div.stButton > button[kind="primary"],
div.stFormSubmitButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primaryFormSubmit"] {
    background: linear-gradient(135deg, #ff7a3d 0%, #ff3d57 100%) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 12px 26px rgba(255, 76, 60, 0.28) !important;
}
div.stButton > button[kind="primary"]:hover,
div.stFormSubmitButton > button[kind="primary"]:hover {
    box-shadow: 0 16px 34px rgba(255, 76, 60, 0.38) !important;
    filter: brightness(1.04);
}

button[data-testid="stBaseButton-secondary"],
button[data-testid="stBaseButton-secondaryFormSubmit"] {
    background: rgba(255, 255, 255, 0.05) !important;
    color: var(--dn-text) !important;
    border: 1px solid var(--dn-line-strong) !important;
}

div[data-testid="stDownloadButton"] > button {
    background: rgba(31, 200, 179, 0.08) !important;
    border-color: rgba(31, 200, 179, 0.28) !important;
    color: #9defe3 !important;
}

/* Girdiler */
div[data-baseweb="input"],
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"],
div[data-testid="stDateInput"] > div > div,
div[data-testid="stNumberInput"] > div > div {
    background: rgba(8, 13, 23, 0.82) !important;
    border: 1px solid var(--dn-line-strong) !important;
    border-radius: 12px !important;
    color: var(--dn-text) !important;
}
div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="textarea"]:focus-within,
div[data-testid="stDateInput"] > div > div:focus-within {
    border-color: rgba(255, 107, 44, 0.55) !important;
    box-shadow: 0 0 0 3px rgba(255, 107, 44, 0.10) !important;
}
input, textarea {
    color: var(--dn-text) !important;
    -webkit-text-fill-color: var(--dn-text) !important;
}
input::placeholder, textarea::placeholder {
    color: var(--dn-faint) !important;
    -webkit-text-fill-color: var(--dn-faint) !important;
}
div[data-baseweb="select"] svg { fill: var(--dn-muted) !important; }
div[data-baseweb="popover"] div[data-baseweb="menu"],
ul[data-baseweb="menu"] {
    background: #101827 !important;
    border: 1px solid var(--dn-line-strong) !important;
    border-radius: 12px !important;
}
li[data-baseweb="option"] {
    background: #101827 !important;
    color: var(--dn-text) !important;
}
li[data-baseweb="option"]:hover,
li[aria-selected="true"][data-baseweb="option"] {
    background: rgba(255, 107, 44, 0.12) !important;
}

label, div[data-testid="stWidgetLabel"] p {
    font-size: 12.5px !important;
    font-weight: 600 !important;
    color: var(--dn-muted) !important;
}

div[data-testid="stDateInput"] input,
div[data-testid="stDateInput"] span {
    color: var(--dn-text) !important;
    -webkit-text-fill-color: var(--dn-text) !important;
}
div[data-testid="stDateInput"] svg { fill: var(--dn-teal) !important; }

/* Sekmeler */
div[data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(13, 20, 33, 0.72) !important;
    border: 1px solid var(--dn-line);
    border-radius: 14px;
    padding: 5px;
    margin-bottom: 18px;
}
button[data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 9px 15px !important;
    color: var(--dn-muted) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: rgba(255, 107, 44, 0.12) !important;
    color: #fff !important;
}
div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display: none !important; }

/* Expander */
div[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.022) !important;
    border: 1px solid var(--dn-line) !important;
    border-radius: 14px !important;
    margin-bottom: 10px;
}
div[data-testid="stExpander"] summary {
    padding: 10px 14px !important;
    color: var(--dn-muted) !important;
    font-size: 12.5px !important;
    font-weight: 600 !important;
}
div[data-testid="stExpander"] summary:hover { color: #fff !important; }
div[data-testid="stExpander"] summary svg { color: var(--dn-teal) !important; }
div[data-testid="stExpander"] summary span[data-testid="stIconMaterial"] { display: none !important; }

/* Dosya yükleme */
section[data-testid="stFileUploaderDropzone"] {
    background: rgba(8, 13, 23, 0.65) !important;
    border: 1px dashed rgba(31, 200, 179, 0.35) !important;
    border-radius: 14px !important;
}
section[data-testid="stFileUploaderDropzone"] * { color: var(--dn-muted) !important; }
section[data-testid="stFileUploaderDropzone"] button {
    background: rgba(31, 200, 179, 0.10) !important;
    border: 1px solid rgba(31, 200, 179, 0.30) !important;
    color: #9defe3 !important;
    border-radius: 10px !important;
    height: auto !important;
    min-height: 0 !important;
    width: auto !important;
    padding: 7px 14px !important;
}
section[data-testid="stFileUploaderDropzone"] button * { color: #9defe3 !important; }

/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--dn-line) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    background: rgba(8, 13, 23, 0.55) !important;
}

/* Uyarı kutuları */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid var(--dn-line) !important;
    background: rgba(255, 255, 255, 0.035) !important;
}
div[data-testid="stAlert"] p { color: var(--dn-text) !important; }

/* Checkbox / radio */
label[data-baseweb="checkbox"] span,
div[role="radiogroup"] label span { color: var(--dn-text) !important; }
div[role="radiogroup"] { gap: 4px; }

/* Slider */
div[data-testid="stSlider"] div[role="slider"] { background: var(--dn-orange) !important; }

/* Metrik */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--dn-line);
    border-radius: 14px;
    padding: 14px 16px;
}
div[data-testid="stMetricValue"] { color: #fff !important; font-family: "Sora", sans-serif; }

/* Container (border) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px !important;
}

/* --- Responsive -------------------------------------------------------- */
@media (max-width: 820px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .dn-hero { padding: 28px 22px; border-radius: 22px; }
    .dn-hero h1 { font-size: 34px !important; }
    .dn-hero-stats { gap: 18px; }
    .dn-car { flex-direction: column; padding: 16px; }
    .dn-car__media { flex: 1 1 auto; width: 100%; height: 190px; }
    .dn-section { flex-direction: column; align-items: flex-start; gap: 6px; }
    .dn-profile .dn-tier { margin-left: 0; }
    .dn-steps { flex-direction: column; }
    .dn-topbar { flex-direction: column; align-items: flex-start; }
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { transition: none !important; animation: none !important; }
}
</style>
"""


def inject_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
```


## `drivenow/uploads.py`

```python
"""Dosya yükleme doğrulama ve güvenli kayıt."""

from __future__ import annotations

from datetime import datetime

from .config import MAX_UPLOAD_MB, UPLOAD_DIR
from .security import safe_filename, safe_folder_name

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None


def validate_image(uploaded) -> str:
    if uploaded is None:
        return ""
    if getattr(uploaded, "size", 0) > MAX_UPLOAD_MB * 1024 * 1024:
        return f"Dosya {MAX_UPLOAD_MB} MB sınırını aşıyor."
    if Image is not None:
        try:
            uploaded.seek(0)
            Image.open(uploaded).verify()
            uploaded.seek(0)
        except Exception:
            return "Yüklenen dosya geçerli bir görsel değil."
    return ""


def save_upload(uploaded, prefix: str) -> str:
    if uploaded is None:
        return ""
    filename = (
        f"{safe_folder_name(prefix, 'dosya')}_"
        f"{datetime.now():%Y%m%d_%H%M%S}_"
        f"{safe_filename(uploaded.name, 'goruntu.jpg')}"
    )
    path = UPLOAD_DIR / filename
    path.write_bytes(uploaded.getbuffer())
    return filename


def upload_path(filename: str):
    if not filename:
        return None
    path = (UPLOAD_DIR / safe_filename(filename, "")).resolve()
    try:
        path.relative_to(UPLOAD_DIR.resolve())
    except ValueError:
        return None
    return path if path.exists() else None


def delete_upload(filename: str) -> None:
    path = upload_path(filename)
    if path:
        try:
            path.unlink()
        except OSError:
            pass
```


## `drivenow/validators.py`

```python
"""Girdi doğrulama yardımcıları."""

from __future__ import annotations

import re
from datetime import date, datetime

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
NAME_RE = re.compile(r"^[A-Za-zÇĞİÖŞÜçğıöşü\s.'\-]{3,60}$")


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def normalize_phone(value: str) -> str:
    """+90 532 123 45 67 / 0532... / 532... -> 5321234567."""
    digits = only_digits(value)
    if digits.startswith("90") and len(digits) == 12:
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) == 11:
        digits = digits[1:]
    return digits


def validate_phone(value: str) -> tuple[bool, str]:
    digits = normalize_phone(value)
    if len(digits) != 10:
        return False, "Telefon 10 haneli olmalı (örn. 5321234567)."
    if not digits.startswith("5"):
        return False, "Cep telefonu 5 ile başlamalı."
    return True, ""


def validate_tckn(value: str, strict: bool = True) -> tuple[bool, str]:
    """T.C. kimlik numarası biçim ve (isteğe bağlı) checksum doğrulaması."""
    digits = only_digits(value)
    if len(digits) != 11 or digits.startswith("0"):
        return False, "T.C. kimlik no 11 haneli olmalı ve 0 ile başlamamalı."
    if not strict:
        return True, ""
    nums = [int(c) for c in digits]
    odd_sum = sum(nums[0:9:2])
    even_sum = sum(nums[1:9:2])
    if (odd_sum * 7 - even_sum) % 10 != nums[9]:
        return False, "T.C. kimlik no doğrulanamadı. Lütfen kontrol edin."
    if sum(nums[:10]) % 10 != nums[10]:
        return False, "T.C. kimlik no doğrulanamadı. Lütfen kontrol edin."
    return True, ""


def validate_email(value: str) -> tuple[bool, str]:
    value = (value or "").strip()
    if not EMAIL_RE.match(value):
        return False, "Geçerli bir e-posta adresi girin."
    return True, ""


def validate_name(value: str) -> tuple[bool, str]:
    value = (value or "").strip()
    if not NAME_RE.match(value):
        return False, "Ad soyad en az 3 karakter olmalı ve rakam içermemeli."
    return True, ""


def luhn_check(card_number: str) -> bool:
    digits = only_digits(card_number)
    if not 13 <= len(digits) <= 19:
        return False
    total = 0
    for index, char in enumerate(reversed(digits)):
        digit = int(char)
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def parse_date(value) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def age_from(birth: date | None, today: date | None = None) -> int | None:
    if not birth:
        return None
    today = today or date.today()
    years = today.year - birth.year
    if (today.month, today.day) < (birth.month, birth.day):
        years -= 1
    return years


def mask_phone(value: str) -> str:
    digits = normalize_phone(value)
    if len(digits) != 10:
        return value
    return f"0{digits[:3]} *** ** {digits[-2:]}"


def mask_tckn(value: str) -> str:
    digits = only_digits(value)
    if len(digits) != 11:
        return value
    return f"{digits[:3]}*****{digits[-2:]}"


def mask_email(value: str) -> str:
    value = (value or "").strip()
    if "@" not in value:
        return value
    local, domain = value.split("@", 1)
    if len(local) <= 2:
        return f"{local[0]}***@{domain}"
    return f"{local[:2]}***@{domain}"
```


## `drivenow/views/__init__.py`

```python
"""Sayfa görünümleri."""

from . import account, admin, auth, booking, fleet

__all__ = ["auth", "fleet", "booking", "account", "admin"]
```


## `drivenow/views/account.py`

```python
"""Müşteri hesabı: rezervasyonlar, favoriler, yorumlar, ayarlar."""

from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from .. import db, invoice
from ..components import (
    car_card,
    date_tr,
    empty_state,
    esc,
    money,
    profile_header,
    section_header,
    status_pill,
)
from ..config import LOKASYONLAR
from ..pricing import can_cancel_free
from ..state import current_user, logout, set_flash, user_id
from ..validators import mask_phone, mask_tckn, validate_email


@st.cache_data(show_spinner=False, ttl=300)
def _invoice_bytes(
    res_id: int,
    kod: str,
    guncelleme: str,
    ad: str,
    tc: str,
    tel: str,
    email: str,
) -> bytes:
    reservation = db.get_reservation(res_id) or {}
    extras = db.get_reservation_extras(res_id)
    user = {"ad": ad, "tc": tc, "tel": tel, "email": email}
    return invoice.build_invoice(reservation, user, extras)


def _reservation_actions(res: dict, user: dict) -> None:
    res_id = int(res["id"])
    extras = db.get_reservation_extras(res_id)
    with st.expander(f"🧾 {res['kod']} • detaylar ve işlemler"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"**Araç:** {esc(res['arac'])}  \n"
                f"**Teslim:** {esc(res['konum'])}  \n"
                f"**İade:** {esc(res.get('iade_konum') or res['konum'])}  \n"
                f"**Tarih:** {date_tr(res['bas_tarih'])} → {date_tr(res['bit_tarih'])}"
            )
        with col2:
            st.markdown(
                f"**Ödeme:** {esc(res.get('odeme_yontemi') or '-')}  \n"
                f"**Ödeme durumu:** {esc(res.get('odeme_durumu') or '-')}  \n"
                f"**Kupon:** {esc(res.get('kupon') or '-')}  \n"
                f"**Depozito:** {money(res.get('depozito', 0))}"
            )
        if extras:
            st.markdown(
                "**Ek hizmetler:** "
                + ", ".join(esc(extra["ad"]) for extra in extras)
            )

        try:
            pdf = _invoice_bytes(
                res_id,
                res["kod"],
                str(res.get("guncelleme") or ""),
                user.get("ad", ""),
                user.get("tc", ""),
                user.get("tel", ""),
                user.get("email", ""),
            )
            st.download_button(
                "📄 Rezervasyon PDF'ini indir",
                pdf,
                file_name=f"DriveNow_{res['kod']}.pdf",
                mime="application/pdf",
                key=f"pdf_{res_id}",
                width="stretch",
            )
        except Exception as exc:  # noqa: BLE001
            st.warning(f"PDF oluşturulamadı: {exc}")

        status = res.get("durum")
        if status in (db.STATUS_PENDING, db.STATUS_ACTIVE):
            free = can_cancel_free(res["bas_tarih"])
            if status == db.STATUS_PENDING or free:
                onay = st.checkbox(
                    "İptal koşullarını okudum, rezervasyonu iptal etmek istiyorum.",
                    key=f"cancel_ok_{res_id}",
                )
                if st.button(
                    "Rezervasyonu iptal et",
                    key=f"cancel_{res_id}",
                    disabled=not onay,
                    width="stretch",
                ):
                    db.cancel_reservation(res_id, "Müşteri talebi", user.get("ad", ""))
                    set_flash(f"{res['kod']} rezervasyonu iptal edildi.", "success")
                    st.rerun()
            else:
                st.markdown(
                    '<div class="dn-note dn-note--warn">'
                    "Kiralama başlangıcına 24 saatten az kaldı. İptal için "
                    "destek ekibiyle iletişime geçin: 0850 000 00 00."
                    "</div>",
                    unsafe_allow_html=True,
                )

        if status == db.STATUS_ACTIVE:
            st.markdown("**Kiralamayı uzat**")
            current_end = date.fromisoformat(res["bit_tarih"])
            new_end = st.date_input(
                "Yeni iade tarihi",
                value=current_end + timedelta(days=1),
                min_value=current_end + timedelta(days=1),
                max_value=current_end + timedelta(days=30),
                key=f"ext_{res_id}",
            )
            if st.button("Uzatmayı onayla", key=f"extbtn_{res_id}", width="stretch"):
                try:
                    vehicle_id = int(res.get("vehicle_id") or 0)
                except (TypeError, ValueError):
                    vehicle_id = 0
                if not vehicle_id:
                    st.error("Rezervasyonun aracı bulunamadı. Lütfen destek ekibiyle iletişime geçin.")
                elif db.vehicle_available(
                    vehicle_id, res["bas_tarih"], new_end.isoformat(), res_id
                ):
                    new_days = max(1, (new_end - date.fromisoformat(res["bas_tarih"])).days)
                    extra_days = new_days - int(res["gun"])
                    extra_cost = float(res["gunluk_fiyat"]) * max(0, extra_days)
                    db.extend_reservation(
                        res_id,
                        new_end.isoformat(),
                        new_days,
                        float(res["toplam_tutar"]) + extra_cost,
                        extra_cost,
                    )
                    set_flash(
                        f"Kiralama {date_tr(new_end.isoformat())} tarihine kadar uzatıldı. "
                        f"Ek tutar: {money(extra_cost)}",
                        "success",
                    )
                    st.rerun()
                else:
                    st.error("Seçilen tarihte araç başka bir rezervasyonda. Farklı bir tarih deneyin.")

        if status == db.STATUS_DONE:
            existing = {
                int(review["reservation_id"])
                for review in db.user_reviews(int(user["id"]))
                if review.get("reservation_id")
            }
            if res_id not in existing:
                with st.form(f"review_{res_id}"):
                    puan = st.slider("Puanınız", 1, 5, 5, key=f"puan_{res_id}")
                    yorum = st.text_area("Yorumunuz", key=f"yorum_{res_id}")
                    if st.form_submit_button("Yorumu gönder", width="stretch"):
                        if not yorum.strip():
                            st.error("Lütfen bir yorum yazın.")
                        elif db.add_review(
                            res_id,
                            int(user["id"]),
                            user.get("ad", ""),
                            res["arac"],
                            puan,
                            yorum,
                        ):
                            set_flash(
                                "Yorumunuz alındı. Yönetici onayından sonra yayınlanacak.",
                                "success",
                            )
                            st.rerun()
                        else:
                            st.error("Bu rezervasyon için zaten yorum yapılmış.")
            else:
                st.info("Bu rezervasyon için yorumunuz alındı.")


def _reservations_tab(user: dict) -> None:
    reservations = db.user_reservations(int(user["id"]))
    if not reservations:
        st.markdown(
            empty_state(
                "🧾",
                "Henüz rezervasyonunuz yok",
                "Filo sekmesinden bir araç seçerek ilk rezervasyonunuzu oluşturun.",
            ),
            unsafe_allow_html=True,
        )
        return

    active = sum(1 for r in reservations if r["durum"] in db.ACTIVE_STATUSES)
    completed = sum(1 for r in reservations if r["durum"] == db.STATUS_DONE)
    st.markdown(
        f'<div class="dn-row" style="border:none;padding:2px 0 12px">'
        f"<span><b style='color:#fff'>{len(reservations)}</b> rezervasyon • "
        f"{active} aktif • {completed} tamamlanan</span></div>",
        unsafe_allow_html=True,
    )

    for res in reservations:
        extras = db.get_reservation_extras(int(res["id"]))
        extra_text = " • ".join(esc(e["ad"]) for e in extras) if extras else "Ek hizmet yok"
        st.markdown(
            f'<div class="dn-card" style="padding:18px;margin-bottom:10px">'
            f'<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap">'
            f"<div><div style='font-size:10px;letter-spacing:1.4px;color:#6b7c93;font-weight:800'>"
            f"{esc(res['kod'])}</div>"
            f"<div style='font-family:Sora,sans-serif;font-size:18px;font-weight:700;color:#fff;margin:3px 0'>"
            f"{esc(res['arac'])}</div>"
            f"<div style='font-size:11.5px;color:#93a3b8'>"
            f"📅 {date_tr(res['bas_tarih'])} → {date_tr(res['bit_tarih'])} • {res['gun']} gün<br>"
            f"📍 {esc(res['konum'])}<br>{extra_text}</div></div>"
            f"<div style='text-align:right'>"
            f"{status_pill(res['durum'])}"
            f"<div style='font-family:Sora,sans-serif;font-size:22px;color:#ff6b2c;font-weight:700;margin-top:8px'>"
            f"{money(res['toplam_tutar'])}</div>"
            f"<div style='font-size:10px;color:#6b7c93'>Toplam</div></div>"
            "</div></div>",
            unsafe_allow_html=True,
        )
        _reservation_actions(res, user)


def _favorites_tab(user: dict) -> None:
    favorites = db.favorite_vehicles(int(user["id"]))
    if not favorites:
        st.markdown(
            empty_state(
                "♡",
                "Favori listeniz boş",
                "Filo ekranındaki kalp simgesiyle araçları buraya ekleyebilirsiniz.",
            ),
            unsafe_allow_html=True,
        )
        return

    for car in favorites:
        st.markdown(car_card(car, 1, True, favorite=True), unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("Rezerve et", key=f"fav_res_{car['id']}", type="primary", width="stretch"):
                default_location = next(iter(LOKASYONLAR))
                st.session_state["secili"] = {
                    "vehicle_id": int(car["id"]),
                    "bas": (date.today() + timedelta(days=1)).isoformat(),
                    "bit": (date.today() + timedelta(days=2)).isoformat(),
                    "gun": 1,
                    "konum": default_location,
                    "iade_konum": default_location,
                }
                st.session_state["booking_step"] = 1
                st.rerun()
        with c2:
            if st.button("Favoriden çıkar", key=f"fav_del_{car['id']}", width="stretch"):
                db.toggle_favorite(int(user["id"]), int(car["id"]))
                set_flash("Favorilerden çıkarıldı.", "success")
                st.rerun()


def _reviews_tab(user: dict) -> None:
    reviews = db.user_reviews(int(user["id"]))
    if not reviews:
        st.markdown(
            empty_state(
                "⭐",
                "Henüz yorumunuz yok",
                "Tamamlanan bir kiralamanın ardından deneyiminizi paylaşabilirsiniz.",
            ),
            unsafe_allow_html=True,
        )
        return
    for review in reviews:
        approved = "Yayında" if int(review.get("onayli") or 0) else "Onay bekliyor"
        st.markdown(
            f'<div class="dn-card" style="padding:16px;margin-bottom:10px">'
            f'<div style="display:flex;justify-content:space-between;gap:10px">'
            f"<b style='color:#fff'>{esc(review['arac'])}</b>"
            f"<span class='dn-chip'>{esc(approved)}</span></div>"
            f"<div style='color:#f5c451;margin:6px 0'>{'★' * int(review['puan'])}</div>"
            f"<div style='font-size:12.5px;color:#c5d2e3'>{esc(review['yorum'])}</div>"
            f"<div style='font-size:10px;color:#6b7c93;margin-top:8px'>{esc(review['tarih'])}</div>"
            "</div>",
            unsafe_allow_html=True,
        )


def _settings_tab(user: dict) -> None:
    st.markdown("**İletişim bilgileri**")
    st.markdown(
        f"<div class='dn-note'>TC: {esc(mask_tckn(user.get('tc', '')))} • "
        f"Telefon: {esc(mask_phone(user.get('tel', '')))}</div>",
        unsafe_allow_html=True,
    )
    with st.form("settings_form"):
        email = st.text_input("E-posta", value=user.get("email", ""))
        pazarlama = st.checkbox(
            "Kampanya bildirimlerini al", value=bool(user.get("pazarlama"))
        )
        if st.form_submit_button("Bilgileri güncelle", type="primary", width="stretch"):
            ok, msg = validate_email(email)
            if not ok:
                st.error(msg)
            else:
                db.update_user_contact(int(user["id"]), email.strip().lower(), pazarlama)
                user["email"] = email.strip().lower()
                st.session_state["user"] = user
                set_flash("İletişim bilgileriniz güncellendi.", "success")
                st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    if st.button("Çıkış yap", width="stretch"):
        logout()
        st.rerun()


def render(section: str | None = None) -> None:
    user = current_user()
    if not user or not user_id():
        st.warning("Hesap sayfası için giriş yapmalısınız.")
        return

    reservations = db.user_reservations(int(user["id"]))
    spent = sum(
        float(r["toplam_tutar"])
        for r in reservations
        if r["durum"] != db.STATUS_CANCELLED
    )
    completed = sum(1 for r in reservations if r["durum"] == db.STATUS_DONE)
    _rate, tier = db.loyalty_for(int(user["id"]))

    title = "Rezervasyonlarım" if section == "reservations" else "Profil ve rezervasyonlar"
    subtitle = (
        "Aktif ve geçmiş tüm kiralamalarınız."
        if section == "reservations"
        else "Tüm kiralama geçmişiniz tek yerde."
    )
    st.markdown(
        section_header("HESABIM", title, subtitle),
        unsafe_allow_html=True,
    )
    st.markdown(
        profile_header(user, tier, completed, spent),
        unsafe_allow_html=True,
    )

    if section == "reservations":
        _reservations_tab(user)
        return

    t1, t2, t3, t4 = st.tabs(
        ["🧾 Rezervasyonlarım", "♡ Favorilerim", "⭐ Yorumlarım", "⚙️ Ayarlar"]
    )
    with t1:
        _reservations_tab(user)
    with t2:
        _favorites_tab(user)
    with t3:
        _reviews_tab(user)
    with t4:
        _settings_tab(user)
```


## `drivenow/views/admin.py`

```python
"""Yönetici paneli: onay, teslim/iade, kupon, yorum, raporlar."""

from __future__ import annotations

import sqlite3
import time
from datetime import date, timedelta
from urllib.parse import quote

import pandas as pd
import plotly.express as px
import streamlit as st

from .. import db, invoice
from ..components import (
    date_tr,
    empty_state,
    esc,
    kpi,
    money,
    section_header,
    status_pill,
)
from ..config import (
    ADMIN_PASSWORD,
    ADMIN_PASSWORD_HASH,
    ADMIN_USING_DEFAULT,
    DEMO_MODE,
    UPLOAD_DIR,
)
from ..security import constant_time_equal, verify_password
from ..state import set_flash
from ..uploads import save_upload, validate_image
from ..validators import normalize_phone


def _verify_admin(password: str) -> bool:
    if ADMIN_PASSWORD_HASH:
        return verify_password(password, ADMIN_PASSWORD_HASH)
    return constant_time_equal(password, ADMIN_PASSWORD)


def _login() -> None:
    st.markdown(
        section_header(
            "YÖNETİM",
            "Yönetici girişi",
            "Rezervasyon onayı, filo ve rapor yönetimi.",
        ),
        unsafe_allow_html=True,
    )
    if ADMIN_USING_DEFAULT and not DEMO_MODE:
        st.error(
            "Yönetici şifresi tanımlı değil. Canlı modda yönetim paneline erişmek "
            "için `.streamlit/secrets.toml` içine `ADMIN_PASSWORD` veya "
            "`ADMIN_PASSWORD_HASH` ekleyin."
        )
        return
    if ADMIN_USING_DEFAULT:
        st.warning(
            "Varsayılan yönetici şifresi kullanılıyor. Canlıya almadan önce "
            "`.streamlit/secrets.toml` içine güçlü bir `ADMIN_PASSWORD` ekleyin."
        )

    lock_until = float(st.session_state.get("admin_lock_until") or 0)
    if lock_until > time.time():
        st.error(
            f"Çok fazla hatalı deneme. {int(lock_until - time.time())} saniye sonra tekrar deneyin."
        )
        return

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.container(border=True):
            password = st.text_input("Yönetici şifresi", type="password")
            if st.button("Giriş yap", type="primary", width="stretch"):
                if _verify_admin(password):
                    st.session_state["admin_ok"] = True
                    st.session_state["admin_attempts"] = 0
                    db.log_audit("Yönetici", "GİRİŞ", "Yönetim paneli")
                    st.rerun()
                else:
                    attempts = int(st.session_state.get("admin_attempts") or 0) + 1
                    st.session_state["admin_attempts"] = attempts
                    if attempts >= 5:
                        st.session_state["admin_lock_until"] = time.time() + 120
                        st.error("5 hatalı deneme. 2 dakika kilitlendi.")
                    else:
                        st.error(f"Hatalı şifre. {5 - attempts} deneme hakkı kaldı.")


def _chart(fig, height: int = 320):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#93a3b8", size=11),
        margin=dict(l=10, r=10, t=42, b=10),
        height=height,
        legend=dict(orientation="h", y=-0.12),
    )
    return fig


def _dashboard(stats: dict) -> None:
    utilization = (stats["aktif"] / stats["filo"] * 100) if stats["filo"] else 0
    cols = st.columns(4)
    with cols[0]:
        st.markdown(
            kpi("Toplam ciro", money(stats["ciro"]), "İptaller hariç", "accent"),
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            kpi("Aktif kiralama", str(stats["aktif"]), f"{stats['bekleyen']} onay bekliyor"),
            unsafe_allow_html=True,
        )
    with cols[2]:
        st.markdown(
            kpi("Filo doluluk", f"%{utilization:.0f}", f"{stats['filo']} araç", "teal"),
            unsafe_allow_html=True,
        )
    with cols[3]:
        st.markdown(
            kpi(
                "Memnuniyet",
                f"{stats['ortalama_puan']:.1f} / 5",
                f"{stats['yorum']} onaylı yorum",
            ),
            unsafe_allow_html=True,
        )

    c1, c2 = st.columns([1.6, 1])
    with c1:
        monthly = db.monthly_revenue()
        if not monthly.empty:
            fig = px.bar(
                monthly,
                x="ay",
                y="ciro",
                text="adet",
                labels={"ay": "Ay", "ciro": "Ciro (TL)", "adet": "Adet"},
                color_discrete_sequence=["#ff6b2c"],
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(_chart(fig), width="stretch")
        else:
            st.info("Henüz ciro verisi yok.")
    with c2:
        dist = db.status_distribution()
        if not dist.empty:
            fig = px.pie(
                dist,
                names="durum",
                values="adet",
                hole=0.58,
                color="durum",
                color_discrete_map={
                    "Onay Bekliyor": "#f5c451",
                    "Aktif": "#1fc8b3",
                    "Tamamlandı": "#5b9dff",
                    "İptal": "#ff5c72",
                },
            )
            st.plotly_chart(_chart(fig), width="stretch")
        else:
            st.info("Rezervasyon dağılımı için veri yok.")

    perf = db.vehicle_performance().head(8)
    if not perf.empty:
        fig = px.bar(
            perf,
            x="ciro",
            y="arac",
            orientation="h",
            labels={"ciro": "Ciro (TL)", "arac": ""},
            color_discrete_sequence=["#1fc8b3"],
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(_chart(fig, 300), width="stretch")


def _reservations_tab() -> None:
    c1, c2 = st.columns([1, 2])
    with c1:
        status = st.selectbox(
            "Durum", ["Tümü", db.STATUS_PENDING, db.STATUS_ACTIVE, db.STATUS_DONE, db.STATUS_CANCELLED]
        )
    with c2:
        search = st.text_input("Ara (kod, müşteri, telefon, araç, plaka)")

    frame = db.admin_reservations(status, search)
    if frame.empty:
        st.info("Filtrelere uygun rezervasyon bulunamadı.")
        return

    st.dataframe(
        frame,
        width="stretch",
        hide_index=True,
        column_config={
            "toplam_tutar": st.column_config.NumberColumn("Tutar", format="%.0f ₺"),
            "id": st.column_config.NumberColumn("ID", width="small"),
        },
    )
    st.download_button(
        "📥 Rezervasyonları CSV indir",
        frame.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"rezervasyonlar_{date.today():%Y%m%d}.csv",
        mime="text/csv",
    )

    codes = frame["kod"].tolist()
    code = st.selectbox("İşlem yapılacak rezervasyon", codes)
    reservation = db.get_reservation_by_code(code)
    if not reservation:
        return
    user = db.get_user(int(reservation["user_id"])) if reservation.get("user_id") else None
    extras = db.get_reservation_extras(int(reservation["id"]))

    st.markdown(
        f'<div class="dn-card" style="padding:16px">'
        f'<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap">'
        f"<div><b style='color:#fff;font-size:16px'>{esc(reservation['arac'])}</b> "
        f"{status_pill(reservation['durum'])}<br>"
        f"<span style='font-size:11.5px;color:#93a3b8'>"
        f"{esc(code)} • {date_tr(reservation['bas_tarih'])} → {date_tr(reservation['bit_tarih'])} "
        f"• {reservation['gun']} gün<br>"
        f"👤 {esc((user or {}).get('ad', '-'))} • 📞 {esc((user or {}).get('tel', '-'))} "
        f"• ✉️ {esc((user or {}).get('email', '-'))}</span></div>"
        f"<div style='text-align:right'><div style='font-family:Sora,sans-serif;font-size:24px;"
        f"color:#ff6b2c;font-weight:700'>{money(reservation['toplam_tutar'])}</div>"
        f"<div style='font-size:10px;color:#6b7c93'>Toplam</div></div></div></div>",
        unsafe_allow_html=True,
    )

    a1, a2, a3 = st.columns(3)
    with a1:
        if reservation["durum"] == db.STATUS_PENDING:
            if st.button("✅ Onayla ve aktifleştir", type="primary", width="stretch"):
                db.update_reservation_status(
                    int(reservation["id"]), db.STATUS_ACTIVE, "Yönetici"
                )
                set_flash(f"{code} onaylandı.", "success")
                st.rerun()
    with a2:
        if reservation["durum"] == db.STATUS_PENDING:
            if st.button("✖️ Reddet", width="stretch"):
                db.cancel_reservation(
                    int(reservation["id"]), "Yönetici reddi", "Yönetici"
                )
                set_flash(f"{code} reddedildi.", "warning")
                st.rerun()
    with a3:
        try:
            pdf = invoice.build_invoice(reservation, user, extras)
            st.download_button(
                "📄 PDF indir",
                pdf,
                file_name=f"{code}.pdf",
                mime="application/pdf",
                width="stretch",
            )
        except Exception as exc:  # noqa: BLE001
            st.warning(f"PDF hatası: {exc}")

    tel = normalize_phone((user or {}).get("tel", ""))
    if tel:
        message = quote(
            f"Sayın {(user or {}).get('ad', 'müşterimiz')}, DriveNow rezervasyonunuz "
            f"({code}) onaylanmıştır. Tarih: {reservation['bas_tarih']} / "
            f"{reservation['bit_tarih']}. Tutar: {float(reservation['toplam_tutar']):,.0f} TL. "
            "İyi yolculuklar dileriz!"
        )
        st.markdown(
            f'<a href="https://wa.me/90{tel}?text={message}" target="_blank" '
            f'style="display:block;text-align:center;background:linear-gradient(135deg,#25D366,#128C7E);'
            f'color:#fff;padding:12px;border-radius:12px;font-weight:700;text-decoration:none;'
            f'margin-top:8px">💬 WhatsApp onay mesajını aç</a>',
            unsafe_allow_html=True,
        )


def _handover_tab() -> None:
    active = db.admin_reservations(db.STATUS_ACTIVE)
    if active.empty:
        st.info("Teslim/iade işlemi için aktif kiralama bulunmuyor.")
        return
    codes = active["kod"].tolist()
    code = st.selectbox("Rezervasyon", codes, key="handover_code")
    reservation = db.get_reservation_by_code(code)
    if not reservation:
        return
    user = db.get_user(int(reservation["user_id"])) if reservation.get("user_id") else None

    with st.form("handover_form"):
        tip = st.radio(
            "İşlem türü",
            ["Araç teslimi", "Araç iadesi"],
            horizontal=True,
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            km = st.number_input("Kilometre", min_value=0, step=100, value=0)
        with c2:
            yakit = st.slider("Yakıt / şarj seviyesi (%)", 0, 100, 100)
        with c3:
            hasar = st.selectbox(
                "Hasar durumu",
                ["Sorunsuz", "Çizik / gövde hasarı", "Mekanik arıza", "Kaza tutanaklı"],
            )
        notlar = st.text_area("Yönetici notu")
        foto = st.file_uploader("Fotoğraf (opsiyonel)", type=["jpg", "jpeg", "png", "webp"])
        submitted = st.form_submit_button(
            "İşlemi kaydet", type="primary", width="stretch"
        )

    if submitted:
        image_error = validate_image(foto)
        if image_error:
            st.error(image_error)
        else:
            foto_adi = save_upload(foto, f"handover_{code}")
            db.add_handover(
                int(reservation["id"]),
                "teslim" if tip == "Araç teslimi" else "iade",
                int(km),
                int(yakit),
                hasar,
                notlar.strip(),
                foto_adi,
                "Yönetici",
            )
            set_flash(
                f"{code} için {tip.lower()} kaydedildi."
                + (" Araç tekrar müsait." if tip == "Araç iadesi" else ""),
                "success",
            )
            st.rerun()

    st.markdown(
        f"<div class='dn-note'>Seçili müşteri: <b>{esc((user or {}).get('ad', '-'))}</b> • "
        f"{esc(reservation['arac'])} • {date_tr(reservation['bas_tarih'])} → "
        f"{date_tr(reservation['bit_tarih'])}</div>",
        unsafe_allow_html=True,
    )

    handovers = db.recent_handovers(30)
    if handovers:
        st.markdown("**Son teslim/iade kayıtları**")
        frame = pd.DataFrame(handovers)[
            ["tarih", "kod", "musteri", "arac", "tip", "km", "yakit", "hasar", "notlar"]
        ]
        st.dataframe(frame, width="stretch", hide_index=True)


def _coupons_tab() -> None:
    coupons = db.list_coupons()
    if coupons:
        frame = pd.DataFrame(coupons)
        st.dataframe(frame, width="stretch", hide_index=True)
    else:
        st.info("Tanımlı kupon yok.")

    with st.form("coupon_form"):
        st.markdown("**Yeni kupon oluştur**")
        c1, c2, c3 = st.columns(3)
        with c1:
            kod = st.text_input("Kod", placeholder="ORN100")
            tip = st.selectbox("Tip", ["yuzde", "sabit"])
        with c2:
            deger = st.number_input("Değer", min_value=1.0, value=10.0, step=1.0)
            min_tutar = st.number_input("Min. sepet", min_value=0.0, value=0.0, step=500.0)
        with c3:
            max_k = st.number_input("Maks. kullanım (0 = sınırsız)", min_value=0, value=0, step=10)
            bitis = st.date_input("Son kullanma", value=date.today() + timedelta(days=180))
        aciklama = st.text_input("Açıklama")
        if st.form_submit_button("Kuponu oluştur", type="primary", width="stretch"):
            if not kod.strip():
                st.error("Kupon kodu zorunlu.")
            elif tip == "yuzde" and not 1 <= deger <= 90:
                st.error("Yüzde indirimi 1-90 arasında olmalı.")
            else:
                try:
                    db.create_coupon(
                        kod, tip, deger, min_tutar, int(max_k), bitis.isoformat(), aciklama
                    )
                except sqlite3.IntegrityError:
                    st.error("Bu kupon kodu zaten var.")
                else:
                    set_flash(f"{kod.upper()} kuponu oluşturuldu.", "success")
                    st.rerun()

    if coupons:
        c1, c2 = st.columns([2, 1])
        with c1:
            secili = st.selectbox("Kupon seç", [c["kod"] for c in coupons], key="coupon_select")
        with c2:
            current = next(c for c in coupons if c["kod"] == secili)
            yeni = not int(current["aktif"])
            if st.button("Pasif yap" if int(current["aktif"]) else "Aktif yap", width="stretch"):
                db.set_coupon_active(secili, yeni)
                set_flash("Kupon durumu güncellendi.", "success")
                st.rerun()


def _reviews_tab() -> None:
    reviews = db.all_reviews()
    if not reviews:
        st.info("Henüz yorum yok.")
        return
    pending = sum(1 for r in reviews if not int(r["onayli"]))
    st.markdown(
        f"<div class='dn-note'>{len(reviews)} yorum • {pending} onay bekliyor</div>",
        unsafe_allow_html=True,
    )
    frame = pd.DataFrame(reviews)[["id", "ad", "arac", "puan", "yorum", "onayli", "tarih"]]
    st.dataframe(frame, width="stretch", hide_index=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        secili = st.selectbox("Yorum ID", [int(r["id"]) for r in reviews], key="review_select")
    with c2:
        if st.button("✅ Onayla", width="stretch"):
            db.set_review_approval(secili, True)
            set_flash("Yorum yayınlandı.", "success")
            st.rerun()
    with c3:
        if st.button("🚫 Yayından kaldır", width="stretch"):
            db.set_review_approval(secili, False)
            set_flash("Yorum yayından kaldırıldı.", "warning")
            st.rerun()
    with c4:
        if st.button("🗑️ Sil", width="stretch"):
            db.delete_review(secili)
            set_flash("Yorum silindi.", "warning")
            st.rerun()


def _users_tab() -> None:
    frame = db.users_df()
    if frame.empty:
        st.info("Kayıtlı kullanıcı yok.")
        return
    st.dataframe(frame, width="stretch", hide_index=True)
    st.download_button(
        "📥 Kullanıcıları CSV indir",
        frame.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"kullanicilar_{date.today():%Y%m%d}.csv",
        mime="text/csv",
    )


def _fleet_tab() -> None:
    cars = db.get_vehicles(include_inactive=True)
    if not cars:
        st.info("Filoda araç yok.")
        return

    frame = pd.DataFrame(
        [
            {
                "Plaka": car["plaka"],
                "Araç": car["ad"],
                "Kategori": car["kategori"],
                "Günlük fiyat": car["gunluk_fiyat"],
                "Depozito": car["depozito"],
                "Puan": car["puan"],
                "Aktif": bool(car["aktif"]),
            }
            for car in cars
        ]
    )
    st.dataframe(
        frame,
        width="stretch",
        hide_index=True,
        column_config={
            "Günlük fiyat": st.column_config.NumberColumn(format="%.0f ₺"),
            "Depozito": st.column_config.NumberColumn(format="%.0f ₺"),
        },
    )

    labels = {f"{car['plaka']} • {car['ad']}": car for car in cars}
    secili = st.selectbox("Düzenlenecek araç", list(labels.keys()), key="fleet_select")
    car = labels[secili]

    c1, c2, c3 = st.columns(3)
    with c1:
        fiyat = st.number_input(
            "Günlük fiyat (₺)",
            min_value=500.0,
            max_value=50000.0,
            value=float(car["gunluk_fiyat"]),
            step=50.0,
            key=f"fleet_price_{car['id']}",
        )
    with c2:
        depozito = st.number_input(
            "Depozito (₺)",
            min_value=0.0,
            max_value=50000.0,
            value=float(car["depozito"]),
            step=500.0,
            key=f"fleet_deposit_{car['id']}",
        )
    with c3:
        aktif = st.checkbox(
            "Filoda aktif",
            value=bool(car["aktif"]),
            key=f"fleet_active_{car['id']}",
        )

    if st.button("Değişiklikleri kaydet", type="primary", width="stretch"):
        db.update_vehicle_pricing(int(car["id"]), fiyat, depozito)
        db.set_vehicle_active(int(car["id"]), aktif)
        db.log_audit(
            "Yönetici",
            "FİLO",
            f"{car['plaka']} • {fiyat:,.0f} ₺/gün • "
            f"{'aktif' if aktif else 'pasif'}",
        )
        set_flash(f"{car['plaka']} güncellendi.", "success")
        st.rerun()


def _reports_tab(stats: dict) -> None:
    perf = db.vehicle_performance()
    if not perf.empty:
        st.markdown("**Araç performansı**")
        st.dataframe(perf, width="stretch", hide_index=True)
        st.download_button(
            "📥 Araç performansı CSV",
            perf.to_csv(index=False).encode("utf-8-sig"),
            file_name="arac_performansi.csv",
            mime="text/csv",
        )

    monthly = db.monthly_revenue()
    if not monthly.empty:
        st.markdown("**Aylık ciro**")
        st.dataframe(monthly, width="stretch", hide_index=True)
        st.download_button(
            "📥 Aylık ciro CSV",
            monthly.to_csv(index=False).encode("utf-8-sig"),
            file_name="aylik_ciro.csv",
            mime="text/csv",
        )

    st.markdown("**Denetim kayıtları**")
    logs = db.audit_df(300)
    if not logs.empty:
        st.dataframe(logs, width="stretch", hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        legacy = db.legacy_log_text()
        if legacy:
            st.download_button(
                "📥 Eski sistem logları",
                legacy.encode("utf-8-sig"),
                file_name="eski_kayitlar.txt",
                mime="text/plain",
                width="stretch",
            )
    with c2:
        try:
            st.download_button(
                "🗄️ Veritabanı yedeği (.db)",
                db.backup_bytes(),
                file_name=f"drivenow_{date.today():%Y%m%d}.db",
                mime="application/octet-stream",
                width="stretch",
            )
        except Exception as exc:  # noqa: BLE001
            st.warning(f"Yedek alınamadı: {exc}")

    st.markdown("---")
    st.markdown("### 🚨 Tehlikeli bölge")
    st.markdown(
        "<div class='dn-note dn-note--warn'>Bu işlem tüm rezervasyonları, "
        "kullanıcıları, yorumları ve yüklenen dosyaları siler. Filo ve kupon "
        "tanımları korunur.</div>",
        unsafe_allow_html=True,
    )
    onay = st.text_input("Onaylamak için SIFIRLA yazın")
    if st.button("Tüm verileri sıfırla", disabled=onay.strip().upper() != "SIFIRLA"):
        db.reset_all()
        for path in UPLOAD_DIR.glob("*"):
            if path.is_file():
                try:
                    path.unlink()
                except OSError:
                    pass
        st.session_state["admin_ok"] = False
        set_flash("Tüm operasyonel veriler sıfırlandı.", "warning")
        st.rerun()


def render() -> None:
    if not st.session_state.get("admin_ok"):
        _login()
        return

    stats = db.stats()
    head_left, head_right = st.columns([3, 1])
    with head_left:
        st.markdown(
            section_header(
                "YÖNETİM",
                "Operasyon merkezi",
                f"Son güncelleme: {date_tr(date.today())} • {stats['filo']} araç",
            ),
            unsafe_allow_html=True,
        )
    with head_right:
        if st.button("Yönetici oturumunu kapat", width="stretch"):
            st.session_state["admin_ok"] = False
            st.rerun()

    _dashboard(stats)

    t1, t2, t3, t4, t5, t6, t7 = st.tabs(
        [
            "📋 Rezervasyonlar",
            "🔑 Teslim & İade",
            "🎟️ Kuponlar",
            "⭐ Yorumlar",
            "👥 Kullanıcılar",
            "🚙 Filo",
            "📊 Raporlar",
        ]
    )
    with t1:
        _reservations_tab()
    with t2:
        _handover_tab()
    with t3:
        _coupons_tab()
    with t4:
        _reviews_tab()
    with t5:
        _users_tab()
    with t6:
        _fleet_tab()
    with t7:
        _reports_tab(stats)
```


## `drivenow/views/auth.py`

```python
"""Giriş / OTP ekranı ve tanıtım sayfası."""

from __future__ import annotations

import time

import streamlit as st

from .. import db
from ..components import car_card, esc, feature_grid, money, quote_card, section_header
from ..config import (
    APP_NAME,
    DEMO_MODE,
    OTP_MAX_ATTEMPTS,
    OTP_MAX_REQUESTS,
    OTP_REQUEST_WINDOW_MIN,
    OTP_TTL_SECONDS,
)
from ..security import constant_time_equal, generate_otp
from ..sms import send_sms
from ..state import set_flash, touch_session
from ..validators import (
    mask_phone,
    normalize_phone,
    only_digits,
    validate_email,
    validate_name,
    validate_tckn,
    validate_phone,
)

STATIC_REVIEWS = [
    {
        "ad": "Merve K.",
        "arac": "Peugeot 508 GT",
        "puan": 5,
        "yorum": "Araç tertemiz geldi, teslimat tam saatinde. Fatura ve WhatsApp onayı çok profesyoneldi.",
    },
    {
        "ad": "Ahmet Y.",
        "arac": "Volkswagen Tiguan R-Line",
        "puan": 5,
        "yorum": "Ailecek uzun yol yaptık. Bagaj hacmi ve konfor beklentimizin üzerindeydi.",
    },
    {
        "ad": "Elif S.",
        "arac": "Tesla Model 3 Performance",
        "puan": 4,
        "yorum": "Elektrikli araç deneyimi harikaydı. Şarj noktaları konusunda destek ekibi çok yardımcı oldu.",
    },
]


def _hero() -> None:
    st.markdown(
        """
        <div class="dn-hero">
            <div class="dn-eyebrow">📍 5 şehir • 14 araç • 7/24 destek</div>
            <h1>Yolculuğunuz<br><em>premium</em> başlasın.</h1>
            <p>
                Konya, İstanbul, Ankara, İzmir ve Antalya'da yeni nesil filo.
                Şeffaf fiyat, ücretsiz iptal ve kapınıza teslim avantajı.
            </p>
            <div class="dn-hero-stats">
                <div><b>14</b><span>PREMIUM ARAÇ</span></div>
                <div><b>4.9/5</b><span>MÜŞTERİ PUANI</span></div>
                <div><b>24 sa</b><span>ÜCRETSİZ İPTAL</span></div>
                <div><b>%30</b><span>UZUN DÖNEM İNDİRİMİ</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _login_card() -> None:
    with st.container(border=True):
        st.markdown(
            '<div class="dn-kicker">GİRİŞ / KAYIT</div>'
            '<div style="font-family:Sora,sans-serif;font-size:22px;font-weight:700;'
            'color:#fff;margin-bottom:4px">Rezervasyon için doğrulanın</div>'
            '<div style="font-size:12px;color:#93a3b8;margin-bottom:16px">'
            "Bilgileriniz yalnızca kiralama süreci için kullanılır.</div>",
            unsafe_allow_html=True,
        )

        if st.session_state.get("auth_notice"):
            st.info(st.session_state["auth_notice"])

        with st.form("auth_form", clear_on_submit=False):
            ad = st.text_input("Ad Soyad", placeholder="Örn. Cihan Demirci")
            tc = st.text_input("T.C. Kimlik No", max_chars=11, placeholder="11 haneli")
            tel = st.text_input(
                "Cep Telefonu", max_chars=14, placeholder="0532 123 45 67"
            )
            email = st.text_input("E-posta", placeholder="ornek@mail.com")
            kvkk = st.checkbox(
                "KVKK aydınlatma metnini okudum, kişisel verilerimin işlenmesini onaylıyorum."
            )
            pazarlama = st.checkbox("Kampanya ve fırsat bildirimlerini almak istiyorum.")
            submitted = st.form_submit_button(
                "SMS Doğrulama Kodu Gönder →", type="primary", width="stretch"
            )

        if submitted:
            errors = []
            ok, msg = validate_name(ad)
            if not ok:
                errors.append(msg)
            ok, msg = validate_tckn(tc, strict=not DEMO_MODE)
            if not ok:
                errors.append(msg)
            ok, msg = validate_phone(tel)
            if not ok:
                errors.append(msg)
            ok, msg = validate_email(email)
            if not ok:
                errors.append(msg)
            if not kvkk:
                errors.append("Devam etmek için KVKK onayı gerekli.")

            now = time.time()
            window = OTP_REQUEST_WINDOW_MIN * 60
            recent = [t for t in st.session_state.get("otp_requests", []) if now - t < window]
            st.session_state["otp_requests"] = recent
            if len(recent) >= OTP_MAX_REQUESTS:
                errors.append(
                    f"Çok fazla kod isteği. {OTP_REQUEST_WINDOW_MIN} dakika sonra tekrar deneyin."
                )

            if errors:
                for error in errors:
                    st.error(error)
                return

            code = generate_otp()
            phone = normalize_phone(tel)
            sent, send_msg = send_sms(
                phone, f"DriveNow doğrulama kodunuz: {code}"
            )
            if not sent:
                st.error(send_msg)
                return

            st.session_state["pending_user"] = {
                "ad": ad.strip(),
                "tc": only_digits(tc),
                "tel": phone,
                "email": email.strip().lower(),
                "pazarlama": bool(pazarlama),
            }
            st.session_state["otp_code"] = code
            st.session_state["otp_expires"] = now + OTP_TTL_SECONDS
            st.session_state["otp_attempts"] = 0
            st.session_state["otp_requests"] = recent + [now]
            st.session_state["auth_stage"] = "otp"
            st.rerun()

        st.markdown(
            '<div style="font-size:10.5px;color:#6b7c93;margin-top:10px;line-height:1.5">'
            + (
                "Demo modu aktif: doğrulama kodu ekranda gösterilir, TC checksum kontrolü kapalıdır."
                if DEMO_MODE
                else "Doğrulama kodu SMS ile gönderilir. TC kimlik no checksum kontrolünden geçer."
            )
            + "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='text-align:center;color:#6b7c93;font-size:11px;margin:14px 0 8px'>veya</div>",
            unsafe_allow_html=True,
        )
        if st.button("Misafir olarak filoyu keşfet →", width="stretch"):
            st.session_state["auth"] = True
            st.session_state["guest"] = True
            st.session_state["user"] = {
                "id": None,
                "ad": "Misafir",
                "tc": "",
                "tel": "",
                "email": "",
            }
            st.session_state["nav"] = "Filo"
            set_flash(
                "Misafir modundasınız. Rezervasyon oluşturmak için giriş yapmanız gerekir.",
                "info",
            )
            touch_session()
            st.rerun()


def _otp_card() -> None:
    pending = st.session_state.get("pending_user") or {}
    with st.container(border=True):
        st.markdown(
            '<div class="dn-kicker">SON ADIM</div>'
            '<div style="font-family:Sora,sans-serif;font-size:22px;font-weight:700;'
            'color:#fff;margin-bottom:4px">Telefonunuzu doğrulayın</div>'
            f'<div style="font-size:12px;color:#93a3b8;margin-bottom:16px">'
            f"{esc(mask_phone(pending.get('tel', '')))} numarasına 6 haneli kod gönderildi.</div>",
            unsafe_allow_html=True,
        )

        if DEMO_MODE:
            code = st.session_state.get("otp_code", "")
            st.markdown(
                f'<div class="dn-otp"><small>DEMO SMS • bu kod yalnızca test içindir</small>'
                f'<div class="dn-otp__code">{esc(code)}</div>'
                f"<small>Kod {OTP_TTL_SECONDS // 60} dakika geçerlidir.</small></div>",
                unsafe_allow_html=True,
            )
        else:
            st.info(
                f"Doğrulama kodu {mask_phone(pending.get('tel', ''))} numarasına gönderildi."
            )

        expired = time.time() > float(st.session_state.get("otp_expires") or 0)

        with st.form("otp_form"):
            entered = st.text_input(
                "6 Haneli Doğrulama Kodu", max_chars=6, placeholder="••••••"
            )
            verify = st.form_submit_button(
                "Kodu Onayla ve Giriş Yap →", type="primary", width="stretch"
            )
            col1, col2 = st.columns(2)
            with col1:
                resend = st.form_submit_button("Kodu yeniden gönder", width="stretch")
            with col2:
                back = st.form_submit_button("← Bilgileri düzenle", width="stretch")

        if back:
            st.session_state["auth_stage"] = "form"
            st.session_state["otp_code"] = None
            st.session_state["pending_user"] = None
            st.rerun()

        if resend:
            now = time.time()
            if now < float(st.session_state.get("otp_expires") or 0) - (
                OTP_TTL_SECONDS - 30
            ):
                st.warning("Yeni kod için 30 saniye bekleyin.")
            else:
                code = generate_otp()
                sent, message = send_sms(
                    pending.get("tel", ""), f"DriveNow doğrulama kodunuz: {code}"
                )
                if sent:
                    st.session_state["otp_code"] = code
                    st.session_state["otp_expires"] = now + OTP_TTL_SECONDS
                    st.session_state["otp_attempts"] = 0
                    set_flash("Yeni doğrulama kodu gönderildi.", "success")
                    st.rerun()
                else:
                    st.error(message)

        if verify:
            if expired:
                st.error("Kodun süresi doldu. Lütfen yeni kod isteyin.")
            elif not entered.strip():
                st.error("Lütfen doğrulama kodunu girin.")
            elif not constant_time_equal(only_digits(entered), st.session_state.get("otp_code", "")):
                attempts = int(st.session_state.get("otp_attempts") or 0) + 1
                st.session_state["otp_attempts"] = attempts
                remaining = OTP_MAX_ATTEMPTS - attempts
                if remaining <= 0:
                    st.session_state["otp_code"] = None
                    st.session_state["otp_expires"] = 0
                    st.error("Çok fazla hatalı deneme. Lütfen yeni kod isteyin.")
                else:
                    st.error(f"Hatalı kod. {remaining} deneme hakkınız kaldı.")
            else:
                try:
                    user = db.upsert_user(**pending)
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Kayıt oluşturulamadı: {exc}")
                else:
                    st.session_state["auth"] = True
                    st.session_state["guest"] = False
                    st.session_state["user"] = user
                    st.session_state["auth_stage"] = "form"
                    st.session_state["otp_code"] = None
                    st.session_state["pending_user"] = None
                    st.session_state["otp_attempts"] = 0
                    st.session_state["auth_notice"] = None
                    st.session_state["nav"] = "Filo"
                    db.log_audit(
                        user.get("ad", ""), "GİRİŞ", f"TC {user.get('tc', '')}"
                    )
                    set_flash(f"Hoş geldiniz {user.get('ad', '')}! Keyifli sürüşler.")
                    touch_session()
                    st.rerun()


def _social_proof() -> None:
    st.markdown(
        section_header(
            "MÜŞTERİ DENEYİMİ",
            "Yola çıkanlar ne diyor?",
            "Onaylanmış rezervasyonlardan gerçek değerlendirmeler.",
        ),
        unsafe_allow_html=True,
    )
    reviews = db.approved_reviews(3) or STATIC_REVIEWS
    cols = st.columns(3)
    for col, review in zip(cols, reviews):
        with col:
            st.markdown(quote_card(review), unsafe_allow_html=True)


def _fleet_preview() -> None:
    st.markdown(
        section_header(
            "FİLO",
            "Öne çıkan araçlar",
            "Ekonomikten performansa, her yolculuk için doğru araç.",
        ),
        unsafe_allow_html=True,
    )
    vehicles = db.get_vehicles()[:3]
    for car in vehicles:
        st.markdown(car_card(car, 1, True), unsafe_allow_html=True)


def _faq() -> None:
    st.markdown(
        section_header("SIK SORULANLAR", "Merak edilenler"),
        unsafe_allow_html=True,
    )
    with st.expander("Rezervasyon ne zaman kesinleşir?"):
        st.write(
            "Rezervasyon talebiniz oluşturulduktan sonra yönetici onayına düşer. "
            "Onaylandığında durum 'Aktif' olur ve WhatsApp/e-posta ile bilgilendirilirsiniz."
        )
    with st.expander("Ücretsiz iptal koşulları nedir?"):
        st.write(
            "Kiralama başlangıcına 24 saatten fazla varsa ücretsiz iptal edebilirsiniz. "
            "Daha kısa sürelerde lütfen destek ekibiyle iletişime geçin."
        )
    with st.expander("Depozito ne kadar ve ne zaman iade edilir?"):
        st.write(
            "Depozito araç segmentine göre 2.000–10.000 TL arasındadır. "
            "Araç hasarsız ve dolu yakıtla iade edildiğinde 3 iş günü içinde geri ödenir."
        )
    with st.expander("Ehliyet fotoğrafı zorunlu mu?"):
        st.write(
            "Rezervasyon sırasında yükleyebilir veya teslimat anında ibraz edebilirsiniz. "
            "Canlı kullanımda belge doğrulaması yapılmadan anahtar teslim edilmez."
        )
    with st.expander("Farklı şehirde iade mümkün mü?"):
        st.write(
            "Evet. Teslim ve iade noktaları farklıysa 750 TL tek yön ücreti uygulanır; "
            "tutar özet ekranında açıkça gösterilir."
        )


def render() -> None:
    _hero()

    if st.session_state.get("auth_stage") == "otp":
        _otp_card()
    else:
        col_left, col_right = st.columns([1.25, 1], gap="large")
        with col_left:
            st.markdown(
                feature_grid(
                    [
                        ("🚚", "Kapınıza teslim", "Seçtiğiniz noktaya araç teslimi ve iade."),
                        ("🛡️", "Şeffaf fiyat", "Gizli ücret yok; depozito ve ekstralar önceden belli."),
                        ("⚡", "Hızlı onay", "Rezervasyon sonrası WhatsApp ve e-posta bildirimi."),
                        ("🧾", "Dijital fatura", "PDF özet anında e-postanıza düşer."),
                    ]
                ),
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            st.markdown(
                '<div class="dn-note">'
                "💡 <b>İpucu:</b> 7 gün ve üzeri kiralamalarda otomatik %15, "
                "14 günde %20, 21 günde %25, 30 günde %30 indirim uygulanır."
                "</div>",
                unsafe_allow_html=True,
            )
        with col_right:
            _login_card()

    _fleet_preview()
    _social_proof()
    _faq()

    st.markdown(
        f"""
        <div class="dn-footer">
            <div><b>{esc(APP_NAME)} Premium</b> • Premium filo, kapınıza teslim.</div>
            <div>destek@drivenow.com.tr • 0850 000 00 00 • Konya / Türkiye</div>
            <div>© {time.strftime('%Y')} DriveNow. Tüm hakları saklıdır.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
```


## `drivenow/views/booking.py`

```python
"""Rezervasyon sihirbazı: ekstralar → sürücü → ödeme → onay."""

from __future__ import annotations

from datetime import date

import streamlit as st

from .. import db, invoice, mailer
from ..components import (
    date_tr,
    empty_state,
    esc,
    money,
    price_breakdown,
    safe_url,
    status_pill,
)
from ..config import (
    MAX_UPLOAD_MB,
    YOUNG_DRIVER_AGE,
    YOUNG_DRIVER_DAILY,
)
from ..pricing import (
    EXTRA_MAP,
    EXTRAS,
    Quote,
    days_between,
    quote as build_quote,
    validate_coupon,
)
from ..state import current_user, is_guest, set_flash, user_id
from ..uploads import save_upload, validate_image
from ..validators import age_from, luhn_check, only_digits


def _back_to_fleet() -> None:
    st.session_state["secili"] = None
    st.session_state["booking_step"] = 1
    st.session_state["booking_coupon"] = None
    st.session_state["booking_extras"] = []
    st.session_state["booking_driver"] = {}
    st.session_state["show_booking_success"] = False
    st.session_state["booking_success"] = None
    st.session_state["nav"] = "Filo"
    st.rerun()


def _steps(current: int) -> str:
    labels = [("1", "Ekstralar"), ("2", "Sürücü"), ("3", "Ödeme")]
    parts = []
    for index, (number, label) in enumerate(labels, start=1):
        css = "dn-step"
        if index == current:
            css += " dn-step--on"
        elif index < current:
            css += " dn-step--done"
        parts.append(
            f'<div class="{css}"><b>ADIM {number}</b>{esc(label)}</div>'
        )
    return f'<div class="dn-steps">{"".join(parts)}</div>'


def _summary(vehicle: dict, secili: dict, quote: Quote, days: int) -> None:
    image = safe_url(vehicle.get("gorsel", ""))
    image_html = (
        f'<img src="{image}" alt="{esc(vehicle["ad"])}" referrerpolicy="no-referrer" '
        f'onerror="this.remove()">'
        if image
        else ""
    )
    st.markdown(
        f'<div class="dn-card" style="padding:16px">'
        f'<div style="position:relative;height:140px;border-radius:14px;overflow:hidden;'
        f'background:linear-gradient(135deg,rgba(31,200,179,.12),rgba(255,107,44,.10));'
        f'display:grid;place-items:center;font-size:34px;margin-bottom:12px">'
        f"🚗{image_html}</div>"
        f'<div style="font-size:10px;letter-spacing:1.4px;color:#1fc8b3;font-weight:800">'
        f"{esc(vehicle['kategori'])}</div>"
        f'<div style="font-family:Sora,sans-serif;font-size:18px;font-weight:700;color:#fff;'
        f'margin:3px 0 8px">{esc(vehicle["ad"])}</div>'
        f'<div style="font-size:11.5px;color:#93a3b8;line-height:1.7">'
        f"📍 {esc(secili['konum'])}<br>"
        f"↩️ {esc(secili['iade_konum'])}<br>"
        f"📅 {date_tr(secili['bas'])} → {date_tr(secili['bit'])} • {days} gün</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="dn-card" style="padding:16px;margin-top:12px">'
        '<div class="dn-kicker">FİYAT ÖZETİ</div>'
        f"{price_breakdown(quote)}"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="dn-note" style="margin-top:10px">'
        "🔒 Ödeme bilgileri saklanmaz. Kart numarası yalnızca demo doğrulamasında kullanılır."
        "</div>",
        unsafe_allow_html=True,
    )


def _success_screen() -> None:
    data = st.session_state.get("booking_success") or {}
    reservation = data.get("reservation") or {}
    pdf = data.get("pdf")
    email_ok = data.get("email_ok")
    email_msg = data.get("email_msg", "")

    st.markdown(
        f"""
        <div class="dn-hero" style="text-align:center">
            <div style="font-size:54px;line-height:1">✅</div>
            <h1 style="font-size:34px;margin:10px 0 6px">Rezervasyonunuz alındı</h1>
            <p style="margin:0 auto 18px;max-width:520px">
                Sayın <b>{esc((current_user() or {}).get('ad', 'misafir'))}</b>,
                talebiniz yönetici onayına gönderildi. Onaylandığında bilgilendirileceksiniz.
            </p>
            <div style="display:inline-flex;gap:18px;flex-wrap:wrap;justify-content:center;
                        background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
                        border-radius:16px;padding:16px 22px">
                <div><div style="font-size:9px;letter-spacing:1.4px;color:#6b7c93">REZERVASYON KODU</div>
                    <div style="font-family:Sora,monospace;font-size:22px;color:#ff6b2c;font-weight:800">
                        {esc(reservation.get('kod', '-'))}</div></div>
                <div><div style="font-size:9px;letter-spacing:1.4px;color:#6b7c93">TOPLAM</div>
                    <div style="font-family:Sora,sans-serif;font-size:22px;color:#fff;font-weight:800">
                        {money(reservation.get('toplam_tutar', 0))}</div></div>
                <div><div style="font-size:9px;letter-spacing:1.4px;color:#6b7c93">DURUM</div>
                    <div style="margin-top:4px">{status_pill(reservation.get('durum', 'Onay Bekliyor'))}</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if email_ok:
        st.info(f"📧 Rezervasyon özeti {(current_user() or {}).get('email', '')} adresine gönderildi.")
    else:
        st.warning(f"📧 E-posta gönderilemedi: {email_msg}")

    col1, col2 = st.columns(2)
    with col1:
        if pdf:
            st.download_button(
                "📄 Rezervasyon PDF'ini indir",
                pdf,
                file_name=f"DriveNow_{reservation.get('kod', 'rezervasyon')}.pdf",
                mime="application/pdf",
                width="stretch",
            )
    with col2:
        if st.button("📋 Rezervasyonlarıma git", type="primary", width="stretch"):
            st.session_state["show_booking_success"] = False
            st.session_state["booking_success"] = None
            st.session_state["nav"] = "Rezervasyonlarım"
            st.rerun()

    if st.button("← Filoya dön", width="stretch"):
        _back_to_fleet()


def render() -> None:
    if st.session_state.get("show_booking_success"):
        _success_screen()
        return

    secili = st.session_state.get("secili")
    if not secili:
        st.markdown(
            empty_state(
                "🚗",
                "Henüz araç seçilmedi",
                "Filo sekmesinden bir araç seçerek rezervasyona başlayın.",
            ),
            unsafe_allow_html=True,
        )
        if st.button("← Filoya dön", width="stretch"):
            _back_to_fleet()
        return

    user = current_user()
    if not user or is_guest() or not user_id():
        st.warning("Rezervasyon için giriş yapmanız gerekir.")
        if st.button("Giriş ekranına dön", type="primary"):
            st.session_state["auth"] = False
            st.session_state["guest"] = False
            st.session_state["user"] = None
            st.rerun()
        return

    vehicle = db.get_vehicle(int(secili["vehicle_id"]))
    if not vehicle:
        st.error("Seçilen araç artık filoda değil.")
        if st.button("← Filoya dön"):
            _back_to_fleet()
        return

    bas = date.fromisoformat(secili["bas"])
    bit = date.fromisoformat(secili["bit"])
    days = days_between(bas, bit)

    top_left, top_right = st.columns([1, 3])
    with top_left:
        if st.button("← Filoya dön", width="stretch"):
            _back_to_fleet()
    with top_right:
        st.markdown(
            '<div style="text-align:right;color:#6b7c93;font-size:11px;padding-top:10px">'
            "Güvenli rezervasyon • 24 saat ücretsiz iptal</div>",
            unsafe_allow_html=True,
        )

    step = int(st.session_state.get("booking_step") or 1)
    st.markdown(_steps(step), unsafe_allow_html=True)

    # --- Fiyat girdileri ---------------------------------------------------
    selected_extras = set(st.session_state.get("booking_extras") or [])
    if step == 1:
        selected_extras = {
            key for key in EXTRA_MAP if st.session_state.get(f"x_{key}")
        }

    birth = st.session_state.get("b_dogum")
    age = age_from(birth) if isinstance(birth, date) else None
    young_driver = bool(age is not None and 18 <= age < YOUNG_DRIVER_AGE)

    loyalty_rate, loyalty_label = db.loyalty_for(user_id())
    coupon_code = st.session_state.get("booking_coupon") or ""
    one_way = secili["konum"] != secili["iade_konum"]

    quote = build_quote(
        vehicle,
        days,
        selected_extras,
        coupon_code=coupon_code,
        one_way=one_way,
        young_driver=young_driver,
        loyalty_rate=loyalty_rate,
        loyalty_label=loyalty_label,
    )

    left, right = st.columns([1.55, 1], gap="large")

    with left:
        if step == 1:
            st.markdown(
                '<div class="dn-kicker">EK HİZMETLER</div>'
                '<div style="font-family:Sora,sans-serif;font-size:20px;font-weight:700;'
                'color:#fff;margin-bottom:12px">Yolculuğunuzu kişiselleştirin</div>',
                unsafe_allow_html=True,
            )
            for option in EXTRAS:
                st.checkbox(
                    f"{option.icon}  {option.ad}  •  +{money(option.gunluk)}/gün",
                    value=option.key in selected_extras,
                    key=f"x_{option.key}",
                    help=option.aciklama,
                )

            st.markdown(
                '<div class="dn-kicker" style="margin-top:18px">KUPON</div>',
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns([2.2, 1])
            with c1:
                coupon_input = st.text_input(
                    "Kupon kodu",
                    value=coupon_code,
                    placeholder="Örn. HOSGELDIN10",
                    key="coupon_input",
                    label_visibility="collapsed",
                )
            with c2:
                apply_coupon = st.button("Uygula", width="stretch")

            if apply_coupon:
                coupon, error = validate_coupon(
                    coupon_input, float(vehicle["gunluk_fiyat"]) * days
                )
                if error:
                    st.session_state["booking_coupon"] = None
                    st.error(error)
                else:
                    st.session_state["booking_coupon"] = coupon["kod"]
                    set_flash(f"{coupon['kod']} kuponu uygulandı.", "success")
                    st.rerun()

            if coupon_code:
                st.markdown(
                    f'<div class="dn-note dn-note--ok">🎟️ <b>{esc(coupon_code)}</b> uygulandı. '
                    f"İndirim: {money(quote.coupon_discount)}</div>",
                    unsafe_allow_html=True,
                )
                if st.button("Kuponu kaldır", key="remove_coupon"):
                    st.session_state["booking_coupon"] = None
                    st.rerun()

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            if st.button("Devam et → Sürücü bilgileri", type="primary", width="stretch"):
                st.session_state["booking_extras"] = [
                    key for key in EXTRA_MAP if st.session_state.get(f"x_{key}")
                ]
                st.session_state["booking_step"] = 2
                st.rerun()

        elif step == 2:
            st.markdown(
                '<div class="dn-kicker">SÜRÜCÜ BİLGİLERİ</div>'
                '<div style="font-family:Sora,sans-serif;font-size:20px;font-weight:700;'
                'color:#fff;margin-bottom:12px">Kiralama sözleşmesi için bilgiler</div>',
                unsafe_allow_html=True,
            )
            driver = st.session_state.get("booking_driver") or {}
            with st.form("driver_form"):
                c1, c2 = st.columns(2)
                with c1:
                    ehliyet_no = st.text_input(
                        "Ehliyet belge no *",
                        value=driver.get("ehliyet_no", ""),
                        placeholder="Örn. 123456",
                    )
                with c2:
                    siniflar = ["B (Binek)", "B1", "A (Motosiklet)", "C (Kamyon)", "D (Otobüs)"]
                    default_class = driver.get("ehliyet_sinif", siniflar[0])
                    ehliyet_sinif = st.selectbox(
                        "Ehliyet sınıfı",
                        siniflar,
                        index=siniflar.index(default_class) if default_class in siniflar else 0,
                    )

                c3, c4 = st.columns(2)
                with c3:
                    birth_value = (
                        date.fromisoformat(driver["dogum"])
                        if driver.get("dogum")
                        else date(1995, 1, 1)
                    )
                    birth = st.date_input(
                        "Doğum tarihi *",
                        value=birth_value,
                        min_value=date(1940, 1, 1),
                        max_value=date.today(),
                        key="b_dogum",
                    )
                with c4:
                    st.markdown(
                        f'<div class="dn-note" style="margin-top:28px">'
                        f"25 yaş altı sürücülerde günlük {money(YOUNG_DRIVER_DAILY)} genç sürücü ücreti uygulanır."
                        "</div>",
                        unsafe_allow_html=True,
                    )

                uploaded = st.file_uploader(
                    f"Ehliyet ön yüz fotoğrafı (opsiyonel, maks. {MAX_UPLOAD_MB} MB)",
                    type=["jpg", "jpeg", "png", "webp"],
                )
                ikinci = st.checkbox("İkinci sürücü ekle")
                ikinci_ad = ""
                if ikinci:
                    ikinci_ad = st.text_input(
                        "İkinci sürücü ad soyad",
                        value=driver.get("ikinci_sofor", ""),
                        placeholder="Ad Soyad",
                    )
                terms = st.checkbox(
                    "Kiralama koşullarını, yakıt ve iade politikasını okudum ve kabul ediyorum. *"
                )

                nav1, nav2 = st.columns(2)
                with nav1:
                    back = st.form_submit_button("← Ekstralar", width="stretch")
                with nav2:
                    forward = st.form_submit_button(
                        "Devam et → Ödeme", type="primary", width="stretch"
                    )

            if back:
                st.session_state["booking_step"] = 1
                st.rerun()

            if forward:
                errors = []
                if not ehliyet_no.strip():
                    errors.append("Ehliyet belge numarası zorunlu.")
                if not terms:
                    errors.append("Kiralama koşullarını kabul etmelisiniz.")
                if age_from(birth) is not None and age_from(birth) < 18:
                    errors.append("18 yaşından küçük sürücülere araç verilemez.")
                image_error = validate_image(uploaded)
                if image_error:
                    errors.append(image_error)
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    st.session_state["booking_driver"] = {
                        "ehliyet_no": ehliyet_no.strip(),
                        "ehliyet_sinif": ehliyet_sinif,
                        "dogum": birth.isoformat(),
                        "ikinci_sofor": ikinci_ad.strip(),
                        "dosya": uploaded,
                    }
                    st.session_state["booking_step"] = 3
                    st.rerun()

        else:
            st.markdown(
                '<div class="dn-kicker">ÖDEME</div>'
                '<div style="font-family:Sora,sans-serif;font-size:20px;font-weight:700;'
                'color:#fff;margin-bottom:12px">Son adım</div>',
                unsafe_allow_html=True,
            )
            driver = st.session_state.get("booking_driver") or {}
            st.markdown(
                f'<div class="dn-note dn-note--ok">'
                f"👤 {esc(user['ad'])} • Ehliyet {esc(driver.get('ehliyet_no', '-'))} • "
                f"Doğum {date_tr(driver.get('dogum', ''))}</div>",
                unsafe_allow_html=True,
            )

            odeme = st.radio(
                "Ödeme yöntemi",
                ["Araç tesliminde öde", "Kredi kartı ile şimdi öde (demo)"],
                horizontal=True,
            )
            kart_son4 = ""
            if odeme.startswith("Kredi kartı"):
                with st.container(border=True):
                    st.markdown(
                        '<div class="dn-note dn-note--warn">'
                        "Demo ödeme: kart bilgileri doğrulanır ancak kaydedilmez, "
                        "yalnızca son 4 hane saklanır.</div>",
                        unsafe_allow_html=True,
                    )
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        kart_no = st.text_input(
                            "Kart numarası", placeholder="4242 4242 4242 4242", max_chars=23
                        )
                    with c2:
                        cvv = st.text_input("CVV", max_chars=4, type="password")
                    c3, c4 = st.columns(2)
                    with c3:
                        kart_ad = st.text_input("Kart üzerindeki isim")
                    with c4:
                        skt = st.text_input("Son kullanma (AA/YY)", placeholder="12/28")

            notu = st.text_area(
                "Eklemek istediğiniz not (opsiyonel)",
                placeholder="Örn. Teslimat saatini 18:00 olarak planlayabilir misiniz?",
            )

            if st.button("🔒 Rezervasyonu tamamla", type="primary", width="stretch"):
                errors = []
                if odeme.startswith("Kredi kartı"):
                    digits = only_digits(kart_no)
                    if not luhn_check(digits):
                        errors.append("Kart numarası geçersiz.")
                    if len(only_digits(cvv)) not in (3, 4):
                        errors.append("CVV 3 veya 4 haneli olmalı.")
                    if not kart_ad.strip():
                        errors.append("Kart üzerindeki isim zorunlu.")
                    try:
                        ay, yil = [part.strip() for part in skt.split("/")]
                        ay_i = int(ay)
                        yil_i = 2000 + int(yil) if len(yil) == 2 else int(yil)
                        if not 1 <= ay_i <= 12:
                            raise ValueError
                        if (yil_i, ay_i) < (date.today().year, date.today().month):
                            raise ValueError
                    except (ValueError, AttributeError):
                        errors.append("Son kullanma tarihi AA/YY biçiminde ve gelecekte olmalı.")
                    if not errors:
                        kart_son4 = only_digits(kart_no)[-4:]

                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    foto = save_upload(driver.get("dosya"), str(user.get("tc", "")))
                    payload = {
                        "user_id": user_id(),
                        "vehicle_id": int(vehicle["id"]),
                        "arac": vehicle["ad"],
                        "plaka": vehicle["plaka"],
                        "konum": secili["konum"],
                        "iade_konum": secili["iade_konum"],
                        "bas_tarih": secili["bas"],
                        "bit_tarih": secili["bit"],
                        "gun": days,
                        "gunluk_fiyat": float(vehicle["gunluk_fiyat"]),
                        "baz_tutar": quote.base,
                        "ekstra_tutar": quote.extras_total,
                        "indirim_tutar": quote.discount_total,
                        "tek_yon_ucret": quote.one_way_fee,
                        "genc_sofor_ucret": quote.young_driver_fee,
                        "toplam_tutar": quote.total,
                        "depozito": quote.deposit,
                        "kupon": quote.coupon_code,
                        "durum": db.STATUS_PENDING,
                        "odeme_yontemi": "Kredi kartı (demo)"
                        if odeme.startswith("Kredi kartı")
                        else "Teslimde ödeme",
                        "odeme_durumu": "Ödendi (demo)"
                        if odeme.startswith("Kredi kartı")
                        else "Teslimde ödenecek",
                        "kart_son4": kart_son4,
                        "musteri_notu": notu.strip(),
                        "ehliyet_no": driver.get("ehliyet_no", ""),
                        "ehliyet_sinif": driver.get("ehliyet_sinif", ""),
                        "dogum_tarihi": driver.get("dogum", ""),
                        "ehliyet_foto": foto,
                        "ikinci_sofor": driver.get("ikinci_sofor", ""),
                        "musteri_ad": user.get("ad", ""),
                    }
                    try:
                        res_id, _code = db.create_reservation(payload, quote.extras)
                    except ValueError as exc:
                        st.error(str(exc))
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"Rezervasyon oluşturulamadı: {exc}")
                    else:
                        reservation = db.get_reservation(res_id) or {}
                        pdf_bytes = None
                        email_ok = False
                        email_msg = "E-posta servisi yapılandırılmadı."
                        try:
                            pdf_bytes = invoice.build_invoice(
                                reservation, user, quote.extras
                            )
                        except Exception as exc:  # noqa: BLE001
                            email_msg = f"PDF oluşturulamadı: {exc}"
                        if pdf_bytes:
                            email_ok, email_msg = mailer.send_invoice(
                                user.get("email", ""),
                                pdf_bytes,
                                user.get("ad", ""),
                                reservation.get("kod", ""),
                                float(reservation.get("toplam_tutar") or 0),
                            )
                        st.session_state["booking_success"] = {
                            "reservation": reservation,
                            "pdf": pdf_bytes,
                            "email_ok": email_ok,
                            "email_msg": email_msg,
                        }
                        st.session_state["show_booking_success"] = True
                        st.session_state["secili"] = None
                        st.session_state["booking_step"] = 1
                        st.session_state["booking_coupon"] = None
                        st.session_state["booking_extras"] = []
                        st.session_state["booking_driver"] = {}
                        st.balloons()
                        st.rerun()

            if st.button("← Sürücü bilgileri", width="stretch"):
                st.session_state["booking_step"] = 2
                st.rerun()

    with right:
        _summary(vehicle, secili, quote, days)
        if quote.coupon_error:
            st.warning(quote.coupon_error)
        st.markdown(
            '<div class="dn-note" style="margin-top:10px">'
            "🛡️ <b>Güvenli ödeme</b> • 24 saat ücretsiz iptal • 7/24 yol yardımı"
            "</div>",
            unsafe_allow_html=True,
        )
```


## `drivenow/views/fleet.py`

```python
"""Araç filosu, arama, filtreler, harita ve karşılaştırma."""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import pydeck as pdk
import streamlit as st

from .. import db
from ..components import (
    car_card,
    empty_state,
    esc,
    money,
    section_header,
    tech_details,
)
from ..config import KATEGORILER, LOKASYONLAR, ONE_WAY_FEE, YAKITLAR, VITESLER
from ..pricing import days_between, duration_discount
from ..state import current_user, is_guest, set_flash, user_id


def _map(location: str, return_location: str) -> None:
    rows = []
    for name, info in LOKASYONLAR.items():
        rows.append(
            {
                "name": name,
                "lat": info["lat"],
                "lon": info["lon"],
                "secili": name in {location, return_location},
            }
        )
    df = pd.DataFrame(rows)
    selected = df[df["secili"]]
    others = df[~df["secili"]]

    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=others,
            get_position="[lon, lat]",
            get_radius=900,
            get_fill_color=[31, 200, 179, 150],
            get_line_color=[255, 255, 255, 60],
            line_width_min_pixels=1,
            pickable=True,
            stroked=True,
        )
    ]
    if not selected.empty:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=selected,
                get_position="[lon, lat]",
                get_radius=2200,
                get_fill_color=[255, 107, 44, 235],
                get_line_color=[255, 255, 255],
                line_width_min_pixels=2,
                pickable=True,
                stroked=True,
            )
        )

    deck = pdk.Deck(
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        initial_view_state=pdk.ViewState(
            latitude=float(selected["lat"].mean()) if not selected.empty else 38.9,
            longitude=float(selected["lon"].mean()) if not selected.empty else 33.5,
            zoom=5.2 if len(selected) > 1 else 9.5,
            pitch=0,
        ),
        layers=layers,
        tooltip={"text": "{name}"},
    )
    st.pydeck_chart(deck, width="stretch")


def _comparison(cars: list[dict], days: int) -> None:
    if len(cars) < 2:
        return
    rate, _label = duration_discount(days)
    rows = {
        "Günlük fiyat": [money(c["gunluk_fiyat"]) for c in cars],
        f"{days} gün toplam": [
            money(float(c["gunluk_fiyat"]) * days * (1 - rate)) for c in cars
        ],
        "Kategori": [c["kategori"] for c in cars],
        "Vites": [c["vites"] for c in cars],
        "Yakıt": [c["yakit"] for c in cars],
        "Koltuk": [str(c["koltuk"]) for c in cars],
        "Bagaj": [f"{c['bagaj']} Lt" for c in cars],
        "Puan": [f"{float(c['puan']):.1f} ★" for c in cars],
        "Depozito": [money(c["depozito"]) for c in cars],
        "Motor": [c.get("motor", "-") for c in cars],
        "Tüketim": [c.get("tuketim", "-") for c in cars],
    }
    frame = pd.DataFrame(rows, index=[c["ad"] for c in cars]).T
    st.markdown(
        '<div class="dn-kicker" style="margin-top:6px">KARŞILAŞTIRMA</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(frame, width="stretch")
    if st.button("Karşılaştırmayı temizle", key="clear_compare"):
        st.session_state["compare"] = []
        for car in cars:
            st.session_state.pop(f"cmp_{car['id']}", None)
        st.rerun()


def render() -> None:
    user = current_user() or {}
    guest = is_guest()

    st.markdown(
        section_header(
            "FİLO",
            f"Hoş geldiniz, {user.get('ad', 'misafir')}",
            "Tarih ve konum seçin; uygun araçları anında görün.",
        ),
        unsafe_allow_html=True,
    )

    today = date.today()
    with st.container(border=True, key="search_panel"):
        col1, col2 = st.columns(2)
        with col1:
            konum = st.selectbox(
                "📍 Teslim noktası",
                list(LOKASYONLAR.keys()),
                key="f_konum",
            )
        with col2:
            ayni_nokta = st.checkbox("Aynı noktaya iade", value=True, key="f_ayni")
            if ayni_nokta:
                iade_konum = konum
            else:
                iade_konum = st.selectbox(
                    "↩️ İade noktası",
                    list(LOKASYONLAR.keys()),
                    index=list(LOKASYONLAR).index(konum),
                    key="f_iade",
                )

        c1, c2 = st.columns(2)
        with c1:
            bas = st.date_input(
                "📅 Alış tarihi", value=today + timedelta(days=1), min_value=today, key="f_bas"
            )
        with c2:
            bit = st.date_input(
                "📅 İade tarihi", value=today + timedelta(days=2), min_value=today, key="f_bit"
            )

        valid_range = bit > bas
        days = days_between(bas, bit) if valid_range else 1
        if not valid_range:
            st.error("İade tarihi alış tarihinden sonra olmalı.")
        else:
            rate, label = duration_discount(days)
            extra = f" • {label}" if rate else ""
            st.markdown(
                f'<div class="dn-note dn-note--ok">⏱️ <b>{days} gün</b> kiralama{esc(extra)}</div>',
                unsafe_allow_html=True,
            )

        if iade_konum != konum:
            st.markdown(
                f'<div class="dn-note dn-note--warn">↩️ Farklı noktaya iade: '
                f"{money(ONE_WAY_FEE)} tek yön ücreti eklenir.</div>",
                unsafe_allow_html=True,
            )

        with st.expander("🎛️ Gelişmiş filtreler"):
            f1, f2, f3 = st.columns(3)
            with f1:
                kategoriler = st.multiselect(
                    "Kategori", list(KATEGORILER), default=list(KATEGORILER), key="f_kat"
                )
            with f2:
                vites = st.selectbox("Vites", ["Tümü", *VITESLER], key="f_vites")
            with f3:
                yakit = st.selectbox("Yakıt", ["Tümü", *YAKITLAR], key="f_yakit")

            f4, f5, f6 = st.columns(3)
            with f4:
                max_fiyat = st.slider(
                    "Maks. günlük fiyat", 1000, 8000, 8000, step=100, key="f_fiyat"
                )
            with f5:
                min_koltuk = st.selectbox("Min. koltuk", [2, 4, 5, 7], index=0, key="f_koltuk")
            with f6:
                sort = st.selectbox(
                    "Sıralama",
                    ["Önerilen", "Fiyat (artan)", "Fiyat (azalan)", "Puan", "Bagaj"],
                    key="f_sort",
                )

            if st.button("Filtreleri sıfırla", key="f_reset"):
                for key in ["f_kat", "f_vites", "f_yakit", "f_fiyat", "f_koltuk", "f_sort"]:
                    st.session_state.pop(key, None)
                st.rerun()

    with st.expander("🗺️ Teslimat noktalarını haritada gör"):
        _map(konum, iade_konum)

    bas_iso = bas.isoformat()
    bit_iso = bit.isoformat()
    available = db.available_vehicle_ids(bas_iso, bit_iso) if valid_range else set()
    favorites = db.favorite_ids(user_id())
    all_cars = db.get_vehicles()

    cars = []
    for car in all_cars:
        if kategoriler and car["kategori"] not in kategoriler:
            continue
        if vites != "Tümü" and car["vites"] != vites:
            continue
        if yakit != "Tümü" and car["yakit"] != yakit:
            continue
        if float(car["gunluk_fiyat"]) > max_fiyat:
            continue
        if int(car["koltuk"]) < int(min_koltuk):
            continue
        cars.append(car)

    if sort == "Fiyat (artan)":
        cars.sort(key=lambda c: c["gunluk_fiyat"])
    elif sort == "Fiyat (azalan)":
        cars.sort(key=lambda c: c["gunluk_fiyat"], reverse=True)
    elif sort == "Puan":
        cars.sort(key=lambda c: c["puan"], reverse=True)
    elif sort == "Bagaj":
        cars.sort(key=lambda c: c["bagaj"], reverse=True)

    musait = sum(1 for car in cars if int(car["id"]) in available)
    st.markdown(
        f'<div class="dn-row" style="border:none;padding:6px 2px">'
        f"<span><b style='color:#fff'>{len(cars)}</b> araç listeleniyor</span>"
        f'<b style="color:#1fc8b3">{musait} müsait</b></div>',
        unsafe_allow_html=True,
    )

    if not cars:
        st.markdown(
            empty_state(
                "🔎",
                "Filtrelere uygun araç yok",
                "Fiyat aralığını veya kategori filtrelerini genişletmeyi deneyin.",
            ),
            unsafe_allow_html=True,
        )
        return

    compare_ids = []
    for car in cars:
        car_id = int(car["id"])
        if st.session_state.get(f"cmp_{car_id}"):
            compare_ids.append(car_id)
    st.session_state["compare"] = compare_ids
    compare_cars = [car for car in all_cars if int(car["id"]) in compare_ids]
    _comparison(compare_cars, days)

    for car in cars:
        car_id = int(car["id"])
        is_available = car_id in available
        is_favorite = car_id in favorites
        st.markdown(
            car_card(
                car,
                days,
                is_available,
                favorite=is_favorite,
                compare=car_id in compare_ids,
            ),
            unsafe_allow_html=True,
        )

        with st.expander("🔧 Teknik özellikler ve donanımlar"):
            st.markdown(tech_details(car), unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns([1, 1, 1.6])
        with col_a:
            label = "♥ Favoriden çıkar" if is_favorite else "♡ Favorilere ekle"
            if st.button(label, key=f"fav_{car_id}", width="stretch"):
                if guest or not user_id():
                    st.warning("Favoriler için giriş yapmalısınız.")
                else:
                    state = db.toggle_favorite(int(user_id()), car_id)
                    set_flash(
                        "Favorilere eklendi." if state else "Favorilerden çıkarıldı.",
                        "success",
                    )
                    st.rerun()
        with col_b:
            st.checkbox("⇄ Karşılaştır", key=f"cmp_{car_id}")
        with col_c:
            if st.button(
                "⚡ Hemen rezerve et",
                key=f"res_{car_id}",
                type="primary",
                width="stretch",
                disabled=not (is_available and valid_range),
            ):
                if guest or not user_id():
                    st.session_state["auth"] = False
                    st.session_state["guest"] = False
                    st.session_state["user"] = None
                    st.session_state["auth_notice"] = (
                        "Rezervasyon oluşturmak için lütfen giriş yapın."
                    )
                    st.rerun()
                st.session_state["secili"] = {
                    "vehicle_id": car_id,
                    "bas": bas_iso,
                    "bit": bit_iso,
                    "gun": days,
                    "konum": konum,
                    "iade_konum": iade_konum,
                }
                st.session_state["booking_step"] = 1
                st.session_state["booking_coupon"] = None
                st.session_state["booking_extras"] = []
                st.session_state["booking_driver"] = {}
                st.rerun()

        st.markdown(
            "<div style='height:1px;background:rgba(255,255,255,.06);margin:8px 0 18px'></div>",
            unsafe_allow_html=True,
        )
```
