import streamlit as st
import base64

# Sayfa yapılandırması
st.set_page_config(page_title="2026 İK Trendleri Mail Oluşturucu", layout="wide")

# Uygulama Başlığı
st.title("📧 LinkedIn Canlı Yayın Mail Editörü")
st.markdown("---")

# Yan Panel - Tasarım ve Yayın Bilgileri
with st.sidebar:
    st.header("🎨 Tasarım Ayarları")
    header_color = st.color_picker("Header Arka Plan Rengi", "#004a99")
    button_color = st.color_picker("Buton Rengi", "#0077b5")
    image_url = st.text_input("Görsel URL (Banner)", "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&q=80&w=600")
    
    st.header("📅 Yayın Detayları")
    live_date = st.text_input("Yayın Tarihi", "25 Şubat 2026")
    live_time = st.text_input("Yayın Saati", "14:00")
    live_link = st.text_input("LinkedIn Etkinlik Linki", "https://linkedin.com/events/example")

# Ana Ekran Kolonları
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 İçerik Düzenleme")
    main_title = st.text_input("Ana Başlık", "2026 İK VİZYONU")
    sub_title = st.text_input("Alt Başlık", "Verimlilik, Yapay Zeka ve Yeni İnsan Kaynakları Dönüşümü")
    
    # Sunumdaki temel mesajlara uygun karşılama metni
    default_welcome = ("Küresel ekonomide varlık fiyatlarına dayalı büyüme dönemi kapandı; "
                       "artık tek geçerli akçe 'verimlilik odaklı büyüme'. "
                       "McKinsey ve Gartner verileri ışığında hazırladığımız bu canlı yayında "
                       "geleceğin iş gücü stratejilerini konuşuyoruz.")
    welcome_text = st.text_area("Karşılama Metni", default_welcome, height=150)
    
    st.write("📌 **Öne Çıkan Trendler (Sunum Odaklı)**")
    t1 = st.text_input("Trend 1", "Al-First Organizasyonlar: Hiyerarşinin otonom sistemlere evrilmesi.")
    t2 = st.text_input("Trend 2", "Beceri Temelli Seçme: Diplomanın yerini alan 'Skill-Based' model.")
    t3 = st.text_input("Trend 3", "Akışkan İş Gücü: Modüler istihdam ve yetenek ekosistemi yönetimi.")
    t4 = st.text_input("Trend 4", "Yeşil Ekonomi: ESG süreçlerinin operasyonel verimliliğe katkısı.")

# HTML Şablonu (Mail formatına uygun)
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f7f6;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; margin-top: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-collapse: collapse;">
        <tr>
            <td align="center" style="background-color: {header_color}; padding: 40px 20px;">
                <h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: bold;">{main_title}</h1>
                <p style="color: #e0e0e0; margin-top: 10px; font-size: 16px;">{sub_title}</p>
            </td>
        </tr>
        <tr>
            <td align="center">
                <img src="{image_url}" alt="Trendler Görseli" style="display: block; width: 100%; max-width: 600px; height: auto;">
            </td>
        </tr>
        <tr>
            <td style="padding: 40px 30px; color: #333333;">
                <p style="line-height: 1.6; font-size: 15px;">{welcome_text}</p>
                <div style="background-color: #f9f9f9; padding: 20px; border-radius: 6px; margin: 25px 0;">
                    <ul style="line-height: 2; font-size: 14px; margin: 0; padding-left: 20px;">
                        <li><strong>{t1}</strong></li>
                        <li><strong>{t2}</strong></li>
                        <li><strong>{t3}</strong></li>
                        <li><strong>{t4}</strong></li>
                    </ul>
                </div>
                <p style="text-align: center; font-weight: bold; font-size: 16px; margin-top: 30px;">
                    📍 LinkedIn Live | 📅 {live_date} | ⏰ {live_time}
                </p>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{live_link}" style="background-color: {button_color}; color: white; padding: 15px 35px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Hemen Kaydol & Katıl</a>
                </div>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 20px; background-color: #eeeeee; font-size: 11px; color: #888888;">
                Bu e-posta 2026 İK Trendleri bilgilendirme kapsamında gönderilmiştir. <br>
                © 2026 Geleceğin İş Gücü Stratejileri
            </td>
        </tr>
    </table>
</body>
</html>
"""

with col2:
    st.subheader("👁️ Canlı Önizleme")
    st.components.v1.html(html_template, height=800, scrolling=True)

# Kaydet ve İndir Butonu
st.markdown("---")
st.subheader("💾 İşlemi Tamamla")

# Base64 dönüşümü ile indirme linki oluşturma
b64 = base64.b64encode(html_template.encode('utf-8')).decode()
href = f'<a href="data:text/html;base64,{b64}" download="ik_trendleri_2026_davet.html" style="text-decoration: none;"><button style="width: 100%; background-color: #28a745; color: white; padding: 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 20px; font-weight: bold;">📥 HTML Mail Dosyasını İndir</button></a>'

st.markdown(href, unsafe_allow_html=True)
st.success("Tüm düzenlemeler bittiyse yukarıdaki butona tıklayarak mail dosyasını indirebilirsin.")
