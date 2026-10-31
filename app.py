card_html = f"""
<div class="car-card-detailed">
    <div>
        <span class="badge-highlight">{a['badge']}</span>
        <span style="background:rgba(251, 191, 36, 0.2); color:#FBBF24; font-size:12px; font-weight:900; padding:4px 10px; border-radius:10px; float:right; border: 1px solid rgba(251, 191, 36, 0.3);">★ {a['puan']}</span>
    </div>
    <div style="font-size:11px; font-weight:900; color:#818CF8; letter-spacing:1px; margin-top:2px;">{a['kat']}</div>
    <div style="font-size:26px; font-weight:900; color:#FFFFFF; margin:4px 0 10px 0;">{a['ad']}</div>
    
    <div>
        <span class="tag-vites">🔀 {a['vites']}</span>
        <span class="tag-yakit">⛽ {a['yakit']}</span>
        <span class="tag-koltuk">👥 {a['koltuk']}</span>
        <span class="tag-bagaj">🧳 {a['bagaj']}</span>
    </div>

    <div class="tech-grid">
        <div class="tech-item">⚙️ <b>Motor:</b> {a['motor']}</div>
        <div class="tech-item">🕹️ <b>Şanzıman:</b> {a['sanziman']}</div>
        <div class="tech-item">⛽ <b>Tüketim:</b> {a['tuketim']}</div>
        <div class="tech-item">🚀 <b>Hızlanma:</b> {a['hizlanma']}</div>
    </div>

    <div style="margin-top:6px;">
        {chips_html}
    </div>

    <div style="margin-top:8px;">
        <span class="guarantee-badge">🟢 Anında Teslim • Sınırsız KM • Full Kasko</span>
    </div>

    <div class="price-row-box">
        <div>
            <div style="font-size:10px; font-weight:800; color:#94A3B8;">GÜNLÜK BİRİM</div>
            <div style="font-size:20px; font-weight:900; color:#38BDF8;">{a['fiyat']:,} ₺</div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:10px; font-weight:800; color:#94A3B8;">{gun} GÜNLÜK TOPLAM</div>
            <div style="font-size:24px; font-weight:900; color:#FF6B00;">{toplam_tutar:,} ₺</div>
        </div>
    </div>
</div>
"""
