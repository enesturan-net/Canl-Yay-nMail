import streamlit as st
import base64
import json
from urllib.parse import quote

# Sayfa yapılandırması
st.set_page_config(page_title="2026 İK Trendleri Mail Editörü", layout="wide")

# Görseldeki mavi renk kodu (Default)
DEFAULT_BLUE = "#00C5CD"

st.title("📧 LinkedIn Canlı Yayın Takvim Entegrasyonu")
st.info("Bu sürümde indirme zorunluluğu yoktur; buton doğrudan takvim kayıt sayfasına yönlendirir.")

# --- VERİ YÜKLEME ---
uploaded_config = st.sidebar.file_uploader("📂 Eski Ayarları Yükle (.json)", type=["json"])
saved_data = json.load(uploaded_config) if uploaded_config else {}

# --- SIDEBAR ---
with st.sidebar:
    st.header("🎨 Tasarım")
    header_color = st.color_picker("Header Rengi", saved_data.get("header_color", DEFAULT_BLUE))
    button_color = st.color_picker("Buton Rengi", saved_data.get("button_color", "#0077b5"))
    image_url = st.text_input("Görsel URL", saved_data.get("image_url", "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&q=80&w=600"))
    
    st.header("📅 Etkinlik Zamanı")
    event_date = st.date_input("Tarih", st.session_state.get('d', None) or saved_data.get("date", None) or __import__('datetime').date(2026, 2, 25))
    event_time = st.time_input("Saat", st.session_state.get('t', None) or saved_data.get("time", None) or __import__('datetime').time(14, 0))
    teams_link = st.text_input("Teams Linki", "https://teams.live.com/meet/933864575548?p=HLDdg0GyoqEMK4OPTe")

# --- TAKVİM LİNKİ OLUŞTURUCU (Google Calendar Format) ---
def generate_google_cal_link(title, date, time, link):
    start_dt = f"{date.replace('-','') }T{time.strftime('%H%M%S')}"
    # 1 saatlik etkinlik
    end_time = (time.hour + 1) % 24
    end_dt = f"{date.replace('-','') }T{end_time:02d}{time.strftime('%M%S')}"
    
    base_url = "https://www.google.com/calendar/render?action=TEMPLATE"
    text = f"&text={quote(title)}"
    dates = f"&dates={start_dt}/{end_dt}"
    details = f"&details={quote('Toplantı Linki: ' + link)}"
    location = f"&location={quote('Online / Microsoft Teams')}"
    return base_url + text + dates + details + location

# --- ANA EKRAN ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 İçerik")
    main_title = st.text_input("Ana Başlık", saved_data.get("main_title", "2026 İK VİZYONU"))
    sub_title = st.text_input("Alt Başlık", saved_data.get("sub_title", "Verimlilik ve Yapay Zeka Dönüşümü"))
    welcome_text = st.text_area("Mesaj", saved_data.get("welcome_text", "Geleceğin iş gücü stratejilerini birlikte konuşalım."), height=100)
    
    if "trends" not in st.session_state:
        st.session_state.trends = saved_data.get("trends", ["Al-First Organizasyonlar", "Beceri Temelli Seçme"])

    for i, trend in enumerate(st.session_state.trends):
        st.session_state.trends[i] = st.text_input(f"Trend {i+1}", trend, key=f"tr_in_{i}")

    if st.button("➕ Trend Ekle"):
        st.session_state.trends.append("Yeni Trend")
        st.rerun()

# --- HTML ŞABLON ---
cal_link = generate_google_cal_link(main_title, str(event_date), event_time, teams_link)
trends_html = "".join([f"<li><strong>{t}</strong></li>" for t in st.session_state.trends])

html_template = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f7f6;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; margin-top: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        <tr>
            <td align="center" style="background-color: {header_color}; padding: 40px 20px; border-radius: 8px 8px 0 0;">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">{main_title}</h1>
                <p style="color: #e0e0e0; margin-top: 10px;">{sub_title}</p>
            </td>
        </tr>
        <tr><td align="center"><img src="{image_url}" style="display: block; width: 100%; max-width: 600px;"></td></tr>
        <tr>
            <td style="padding: 30px; color: #333;">
                <p>{welcome_text}</p>
                <ul>{trends_html}</ul>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{cal_link}" target="_blank" style="background-color: {button_color}; color: white; padding: 18px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block; font-size: 18px;">Takvime Ekle & Kaydol</a>
                </div>
                <p style="text-align: center; font-size: 12px; color: #888; margin-top: 15px;">*Tıkladığınızda etkinlik otomatik olarak takviminize işlenir.</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

with col2:
    st.subheader("👁️ Önizleme")
    st.components.v1.html(html_template, height=750, scrolling=True)

# --- KAYDET VE İNDİR ---
st.markdown("---")
b64_html = base64.b64encode(html_template.encode('utf-8')).decode()
st.markdown(f'<a href="data:text/html;base64,{b64_html}" download="ik_davet.html" style="text-decoration: none;"><button style="width: 100%; background-color: #28a745; color: white; padding: 15px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: bold;">📥 Maili HTML Olarak Kaydet</button></a>', unsafe_allow_html=True)
