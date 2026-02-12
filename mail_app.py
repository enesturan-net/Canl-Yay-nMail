import streamlit as st
import base64

# Sayfa yapılandırması
st.set_page_config(page_title="2026 İK Trendleri Mail Oluşturucu", layout="wide")

st.title("📧 LinkedIn Canlı Yayın Mail Editörü")
st.info("Sunumdaki 2030 vizyonuna uygun içerikleri aşağıdan düzenleyebilirsin.")

# Yan panel - Düzenleme Alanları
with st.sidebar:
    st.header("🎨 Tasarım ve İçerik")
    header_color = st.color_picker("Header Arka Plan Rengi", "#004a99")
    button_color = st.color_picker("Buton Rengi", "#0077b5")
    image_url = st.text_input("Görsel URL (Banner)", "https://via.placeholder.com/600x200?text=2026+IK+Trendleri")
    
    st.header("📅 Yayın Bilgileri")
    live_date = st.text_input("Yayın Tarihi", "25 Şubat 2026")
    live_time = st.text_input("Yayın Saati", "14:00")
    live_link = st.text_input("LinkedIn Etkinlik Linki", "https://linkedin.com/events/...")

# Ana Ekran - İçerik Düzenleme
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Metin İçeriklerini Düzenle")
    main_title = st.text_input("Ana Başlık", "2026 İK VİZYONU")
    sub_title = st.text_input("Alt Başlık", "Verimlilik, Yapay Zeka ve Yeni İnsan Kaynakları Dönüşümü")
    welcome_text = st.text_area("Karşılama Metni", "Küresel ekonomide varlık fiyatlarına dayalı büyüme dönemi kapandı; artık tek geçerli akçe 'verimlilik'.")
    
    st.write("📌 **Trend Maddeleri**")
    t1 = st.text_input("Trend 1", "AI-First Organizasyonlar: Hiyerarşinin çöküşü.")
    t2 = st.text_input("Trend 2", "Beceri Temelli Model: Diplomanın sonu.")
    t3 = st.text_input("Trend 3", "Akışkan İş Gücü: Modüler istihdam.")
    t4 = st.text_input("Trend 4", "Yeşil Dönüşüm: ESG ve operasyonel verimlilik.")

# HTML Şablonu Oluşturma
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f7f6;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; margin-top: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        <tr>
            <td align="center" style="background-color: {header_color}; padding: 40px 20px;">
                <h1 style="color: #ffffff; margin: 0; font-size: 28px;">{main_title}</h1>
                <p style="color: #e0e0e0; margin-top: 10px;">{sub_title}</p>
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="{image_url}" alt="Banner" style="display: block; width: 100%; max-width: 600px;">
            </td>
        </tr>
        <tr>
            <td style="padding: 40px 30px; color: #333;">
                <p style="line-height: 1.6; font-size: 15px;">{welcome_text}</p>
                <ul style="line-height: 2; font-size: 15px;">
                    <li>{t1}</li>
                    <li>{t2}</li>
                    <li>{t3}</li>
                    <li>{t4}</li>
                </ul>
                <p style="text-align: center; font-weight: bold; margin-top: 30px;">
                    📍 LinkedIn Live | 📅 {live_date} | ⏰ {live_time}
                </p>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{live_link}" style="background-color: {button_color}; color: white; padding: 15px 30px; text-decoration: none; border-radius: 4px; font-weight: bold; display: inline-block;">Yayına Katıl</a>
                </div>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 20px; background-color: #eeeeee; font-size: 12px; color: #777;">
                © 2026 | 2030 Vizyonu İK Dönüşümü
            </td>
        </tr>
    </table>
</body>
</html>
"""

with col2:
    st.subheader("Önizleme")
    st.components.v1.html(html_template, height=700, scrolling=True)

# İndirme Butonu
st.divider()
b64 = base64.b64encode(html_template.encode()).decode()
href = f'<a href="data:text/html;base64,{b64}" download="ik_trendleri_2026_mail.html" style="text-decoration: none;"><button style="width: 100%; background-color: #28a745; color: white; padding: 15px; border: none; border-radius: 5px; cursor: pointer; font-size: 18px; font-weight: bold;">📥 HTML Olarak İndir ve Kaydet</button></a>'
st.markdown(href, unsafe_allow_広告=True)