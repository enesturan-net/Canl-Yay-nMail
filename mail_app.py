import streamlit as st
import base64
import json

# Sayfa yapılandırması
st.set_page_config(page_title="2026 İK Trendleri Mail Editörü", layout="wide")

# Görseldeki mavi renk kodu (Default)
DEFAULT_BLUE = "#00C5CD"

st.title("📧 LinkedIn Canlı Yayın Mail Editörü")
st.markdown("---")

# --- VERİ YÜKLEME (LOAD) ---
uploaded_config = st.sidebar.file_uploader("📂 Eski Ayarları Yükle (.json)", type=["json"])
if uploaded_config is not None:
    saved_data = json.load(uploaded_config)
else:
    saved_data = {}

# --- SIDEBAR - TASARIM AYARLARI ---
with st.sidebar:
    st.header("🎨 Tasarım Ayarları")
    header_color = st.color_picker("Header Arka Plan Rengi", saved_data.get("header_color", DEFAULT_BLUE))
    button_color = st.color_picker("Buton Rengi", saved_data.get("button_color", "#0077b5"))
    image_url = st.text_input("Görsel URL (Banner)", saved_data.get("image_url", "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&q=80&w=600"))
    
    st.header("📅 Yayın Detayları")
    live_date = st.text_input("Yayın Tarihi", saved_data.get("live_date", "25 Şubat 2026"))
    live_time = st.text_input("Yayın Saati", saved_data.get("live_time", "14:00"))
    live_link = st.text_input("LinkedIn Etkinlik Linki", saved_data.get("live_link", "https://linkedin.com/events/example"))

# --- ANA EKRAN DÜZENLEME ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 İçerik Düzenleme")
    main_title = st.text_input("Ana Başlık", saved_data.get("main_title", "2026 İK VİZYONU"))
    sub_title = st.text_input("Alt Başlık", saved_data.get("sub_title", "Verimlilik, Yapay Zeka ve Yeni İnsan Kaynakları Dönüşümü"))
    
    welcome_text = st.text_area("Karşılama Metni", saved_data.get("welcome_text", "Küresel ekonomide artık tek geçerli akçe 'verimlilik odaklı büyüme'[cite: 9]."), height=120)
    
    st.write("📌 **Trendleri Düzenle**")
    
    # Dinamik Trend Ekleme Sistemi
    if "trends" not in st.session_state:
        st.session_state.trends = saved_data.get("trends", [
            "Al-First Organizasyonlar: Hiyerarşinin otonom sistemlere evrilmesi[cite: 12].",
            "Beceri Temelli Seçme: Diplomanın yerini alan 'Skill-Based' model[cite: 13, 98].",
            "Akışkan İş Gücü: Modüler istihdam ve yetenek ekosistemi yönetimi[cite: 126, 136]."
        ])

    for i, trend in enumerate(st.session_state.trends):
        st.session_state.trends[i] = st.text_input(f"Trend {i+1}", trend, key=f"trend_input_{i}")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("➕ Trend Ekle"):
            st.session_state.trends.append("Yeni Trend Bilgisi")
            st.rerun()
    with col_btn2:
        if st.button("➖ Sonuncuyu Sil") and len(st.session_state.trends) > 0:
            st.session_state.trends.pop()
            st.rerun()

# --- HTML ŞABLON OLUŞTURMA ---
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
        <tr><td align="center"><img src="{image_url}" style="display: block; width: 100%; max-width: 600px; height: auto;"></td></tr>
        <tr>
            <td style="padding: 40px 30px; color: #333333;">
                <p style="line-height: 1.6; font-size: 15px;">{welcome_text}</p>
                <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 25px 0;">
                    <ul style="line-height: 2; font-size: 14px; margin: 0; padding-left: 20px;">{trends_html}</ul>
                </div>
                <p style="text-align: center; font-weight: bold;">📍 LinkedIn Live | 📅 {live_date} | ⏰ {live_time}</p>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{live_link}" style="background-color: {button_color}; color: white; padding: 15px 35px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Hemen Katıl</a>
                </div>
            </td>
        </tr>
    </table>
</body>
</html>
"""

with col2:
    st.subheader("👁️ Canlı Önizleme")
    st.components.v1.html(html_template, height=800, scrolling=True)

# --- KAYDET VE İNDİR BUTONLARI ---
st.markdown("---")
col_down1, col_down2 = st.columns(2)

# 1. Ayarları JSON olarak indir (Load/Save için)
config_data = {
    "header_color": header_color, "button_color": button_color, "image_url": image_url,
    "live_date": live_date, "live_time": live_time, "live_link": live_link,
    "main_title": main_title, "sub_title": sub_title, "welcome_text": welcome_text,
    "trends": st.session_state.trends
}
json_string = json.dumps(config_data)
st.download_button(
    label="💾 Mevcut Ayarları/Verileri Kaydet (JSON)",
    data=json_string,
    file_name="ik_mail_ayarlari.json",
    mime="application/json",
    use_container_width=True
)

# 2. HTML Olarak İndir (Mail için)
b64_html = base64.b64encode(html_template.encode('utf-8')).decode()
href_html = f'<a href="data:text/html;base64,{b64_html}" download="ik_trendleri_2026.html" style="text-decoration: none;"><button style="width: 100%; background-color: #28a745; color: white; padding: 15px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: bold;">📥 HTML Mail Dosyasını İndir</button></a>'
st.markdown(href_html, unsafe_allow_html=True)
