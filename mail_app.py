import streamlit as st
import base64
import json
from datetime import datetime

# Sayfa yapılandırması
st.set_page_config(page_title="2026 İK Trendleri Mail Editörü", layout="wide")

# Görseldeki mavi renk kodu (Default)
DEFAULT_BLUE = "#00C5CD"

st.title("📧 LinkedIn Canlı Yayın & Takvim Entegrasyonlu Mail Editörü")
st.markdown("---")

# --- VERİ YÜKLEME (LOAD) ---
uploaded_config = st.sidebar.file_uploader("📂 Eski Ayarları Yükle (.json)", type=["json"])
if uploaded_config is not None:
    saved_data = json.load(uploaded_config)
else:
    saved_data = {}

# --- SIDEBAR - TASARIM VE ETKİNLİK AYARLARI ---
with st.sidebar:
    st.header("🎨 Tasarım Ayarları")
    header_color = st.color_picker("Header Arka Plan Rengi", saved_data.get("header_color", DEFAULT_BLUE))
    button_color = st.color_picker("Buton Rengi", saved_data.get("button_color", "#0077b5"))
    image_url = st.text_input("Görsel URL (Banner)", saved_data.get("image_url", "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&q=80&w=600"))
    
    st.header("📅 Takvim & Toplantı Detayları")
    event_name = st.text_input("Etkinlik Adı", saved_data.get("event_name", "2026 İK Trendleri Canlı Yayını"))
    live_date_raw = st.date_input("Yayın Tarihi", datetime(2026, 2, 25))
    live_time_raw = st.time_input("Yayın Saati", datetime.strptime("14:00", "%H:%M").time())
    teams_link = st.text_input("Teams Linki", "https://teams.live.com/meet/933864575548?p=HLDdg0GyoqEMK4OPTe")

# --- .ICS TAKVİM DOSYASI OLUŞTURMA ---
def create_ics(summary, date, time, url):
    dt_start = datetime.combine(date, time).strftime("%Y%m%dT%H%M%S")
    # Etkinlik süresini 1 saat olarak varsayalım
    dt_end = datetime.combine(date, time).replace(hour=(time.hour + 1) % 24).strftime("%Y%m%dT%H%M%S")
    
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//İK Trendleri//TR
BEGIN:VEVENT
SUMMARY:{summary}
DTSTART:{dt_start}
DTEND:{dt_end}
URL:{url}
DESCRIPTION:2026 İK Trendleri Canlı Yayınına katılımınız için teşekkürler. Toplantı linki: {url}
LOCATION:Online (Microsoft Teams)
END:VEVENT
END:VCALENDAR"""
    return base64.b64encode(ics_content.encode()).decode()

# --- ANA EKRAN DÜZENLEME ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 İçerik Düzenleme")
    main_title = st.text_input("Ana Başlık", saved_data.get("main_title", "2026 İK VİZYONU"))
    sub_title = st.text_input("Alt Başlık", saved_data.get("sub_title", "Verimlilik, Yapay Zeka ve İnsan Kaynakları"))
    welcome_text = st.text_area("Karşılama Metni", saved_data.get("welcome_text", "Verimlilik odaklı büyüme çağında İK'nın yeni yol haritasını birlikte keşfedelim."), height=100)
    
    # Dinamik Trend Yönetimi
    if "trends" not in st.session_state:
        st.session_state.trends = saved_data.get("trends", ["Al-First Organizasyonlar [cite: 58]", "Beceri Temelli Seçme [cite: 90]", "Akışkan İş Gücü [cite: 126]"])

    for i, trend in enumerate(st.session_state.trends):
        st.session_state.trends[i] = st.text_input(f"Trend {i+1}", trend, key=f"tr_{i}")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("➕ Trend Ekle"):
            st.session_state.trends.append("Yeni Trend")
            st.rerun()
    with col_btn2:
        if st.button("➖ Sonuncuyu Sil") and len(st.session_state.trends) > 0:
            st.session_state.trends.pop()
            st.rerun()

# --- HTML ŞABLON OLUŞTURMA ---
ics_b64 = create_ics(event_name, live_date_raw, live_time_raw, teams_link)
trends_html = "".join([f"<li><strong>{t}</strong></li>" for t in st.session_state.trends])

html_template = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f7f6;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; margin-top: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-collapse: collapse;">
        <tr>
            <td align="center" style="background-color: {header_color}; padding: 40px 20px;">
                <h1 style="color: #ffffff; margin: 0; font-size: 26px;">{main_title}</h1>
                <p style="color: #e0e0e0; margin-top: 10px; font-size: 16px;">{sub_title}</p>
            </td>
        </tr>
        <tr><td align="center"><img src="{image_url}" style="display: block; width: 100%; max-width: 600px;"></td></tr>
        <tr>
            <td style="padding: 40px 30px; color: #333333;">
                <p style="line-height: 1.6; font-size: 15px;">{welcome_text}</p>
                <ul style="line-height: 2; font-size: 14px;">{trends_html}</ul>
                <p style="text-align: center; font-weight: bold; margin-top: 20px;">
                    📅 {live_date_raw.strftime('%d %B %Y')} | ⏰ {live_time_raw.strftime('%H:%M')}
                </p>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="data:text/calendar;base64,{ics_b64}" download="etkinlik.ics" style="background-color: {button_color}; color: white; padding: 18px 40px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block; font-size: 18px;">Etkinliğe Kaydol</a>
                </div>
                <p style="text-align: center; font-size: 12px; color: #888; margin-top: 10px;">(Butona tıkladığınızda takvim kaydınız inecektir.)</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

with col2:
    st.subheader("👁️ Önizleme")
    st.components.v1.html(html_template, height=800, scrolling=True)

# --- İNDİRME ALANI ---
st.markdown("---")
config_data = {**saved_data, "trends": st.session_state.trends, "header_color": header_color}
st.download_button("💾 Ayarları Kaydet (JSON)", data=json.dumps(config_data), file_name="ik_ayarlar.json", use_container_width=True)

b64_html = base64.b64encode(html_template.encode('utf-8')).decode()
st.markdown(f'<a href="data:text/html;base64,{b64_html}" download="ik_trendleri_2026.html" style="text-decoration: none;"><button style="width: 100%; background-color: #28a745; color: white; padding: 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: bold;">📥 HTML Mail Dosyasını İndir</button></a>', unsafe_allow_html=True)
