import streamlit as st
import base64
import json

# Sayfa yapılandırması
st.set_page_config(page_title="2026 İK Trendleri Mail Editörü", layout="wide")

# İlettiğin görseldeki mavi renk tonu (Varsayılan)
DEFAULT_BLUE = "#00C5CD"

st.title("📧 LinkedIn Canlı Yayın Kayıt & İK Trendleri Editörü")
st.markdown("---")

# --- VERİ YÜKLEME (LOAD) ---
# Daha önce kaydedilen JSON dosyasını yükleyerek tüm alanları otomatik doldurur.
uploaded_config = st.sidebar.file_uploader("📂 Eski Ayarları Yükle (.json)", type=["json"])
if uploaded_config is not None:
    saved_data = json.load(uploaded_config)
else:
    saved_data = {}

# --- SIDEBAR - TASARIM VE FORM AYARLARI ---
with st.sidebar:
    st.header("🎨 Görsel Ayarlar")
    header_color = st.color_picker("Header Arka Plan Rengi", saved_data.get("header_color", DEFAULT_BLUE))
    button_color = st.color_picker("Buton Rengi", saved_data.get("button_color", "#0077b5"))
    image_url = st.text_input("Görsel URL (Banner)", saved_data.get("image_url", "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&q=80&w=600"))
    
    st.header("🔗 Kayıt Sistemi")
    # Oluşturduğun Google Form linkini buraya default olarak ekliyoruz.
    form_url = st.text_input("Google Form Linki", "https://docs.google.com/forms/d/e/1FAIpQLScsXefZT6vqhN8VoU59FY2zirhKp_Bhq8PcYi-2lF_ELCiIPQ/viewform")
    
    st.header("📅 Etkinlik Bilgisi")
    live_info = st.text_input("Yayın Tarihi & Saat", saved_data.get("live_info", "25 Şubat 2026 | 14:00"))

# --- ANA EKRAN DÜZENLEME ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 İçerik Yönetimi")
    main_title = st.text_input("Ana Başlık", saved_data.get("main_title", "2026 İK VİZYONU"))
    sub_title = st.text_input("Alt Başlık", saved_data.get("sub_title", "Verimlilik, Al-First ve İK Dönüşümü"))
    
    # Sunumdaki verimlilik vurgusunu içeren varsayılan metin
    default_msg = ("Küresel ekonomide artık tek geçerli akçe 'verimlilik odaklı büyüme'. "
                   "Geleceğin iş gücü stratejilerini ve 2030 vizyonunu konuşacağımız "
                   "canlı yayınımıza davetlisiniz.")
    welcome_text = st.text_area("Karşılama Mesajı", saved_data.get("welcome_text", default_msg), height=130)
    
    st.write("📌 **Dinamik Trend Listesi**")
    
    # Session State ile trend ekleme/çıkarma yönetimi
    if "trends" not in st.session_state:
        st.session_state.trends = saved_data.get("trends", [
            "Al-First Organizasyonlar: Hiyerarşinin otonom sistemlere evrilmesi",
            "Beceri Temelli Seçme: Diplomanın yerini alan 'Skill-Based' model",
            "Akışkan İş Gücü: Modüler istihdam ve otonomi"
        ])

    for i, trend in enumerate(st.session_state.trends):
        st.session_state.trends[i] = st.text_input(f"Trend {i+1}", trend, key=f"tr_idx_{i}")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("➕ Trend Ekle"):
            st.session_state.trends.append("Yeni Stratejik Trend")
            st.rerun()
    with col_btn2:
        if st.button("➖ Sonuncuyu Sil") and len(st.session_state.trends) > 0:
            st.session_state.trends.pop()
            st.rerun()

# --- HTML ŞABLON OLUŞTURMA ---
trends_html = "".join([f"<li style='margin-bottom:8px;'><strong>{t}</strong></li>" for t in st.session_state.trends])

html_template = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f7f6;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; margin-top: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-collapse: collapse;">
        <tr>
            <td align="center" style="background-color: {header_color}; padding: 45px 20px; border-radius: 8px 8px 0 0;">
                <h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: bold;">{main_title}</h1>
                <p style="color: #e0e0e0; margin-top: 12px; font-size: 16px;">{sub_title}</p>
            </td>
        </tr>
        <tr><td align="center"><img src="{image_url}" alt="İK Vizyonu" style="display: block; width: 100%; max-width: 600px; height: auto;"></td></tr>
        <tr>
            <td style="padding: 40px 35px; color: #333333;">
                <p style="line-height: 1.6; font-size: 15px; margin-bottom: 25px;">{welcome_text}</p>
                <div style="background-color: #f9f9f9; padding: 25px; border-radius: 8px; margin-bottom: 30px;">
                    <ul style="line-height: 2; font-size: 14px; margin: 0; padding-left: 20px; color: #444;">{trends_html}</ul>
                </div>
                <p style="text-align: center; font-weight: bold; font-size: 16px;">📅 {live_info}</p>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{form_url}" target="_blank" style="background-color: {button_color}; color: white; padding: 18px 45px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block; font-size: 18px;">Etkinliğe Kaydol & Katıl</a>
                </div>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 20px; background-color: #eeeeee; font-size: 11px; color: #888888;">
                © 2026 | Verimlilik Odaklı Büyüme & İK Dönüşümü <br>
                Bu e-posta kurumsal bilgilendirme amacıyla gönderilmiştir.
            </td>
        </tr>
    </table>
</body>
</html>
"""

with col2:
    st.subheader("👁️ Canlı Önizleme")
    st.components.v1.html(html_template, height=850, scrolling=True)

# --- KAYDET VE ÇIKTI AL ---
st.markdown("---")
col_res1, col_res2 = st.columns(2)

with col_res1:
    # Tüm ayarları bir JSON dosyası olarak kaydetme butonu
    config_to_save = {
        "header_color": header_color, "button_color": button_color, "image_url": image_url,
        "form_url": form_url, "live_info": live_info, "main_title": main_title,
        "sub_title": sub_title, "welcome_text": welcome_text, "trends": st.session_state.trends
    }
    st.download_button(
        label="💾 Mevcut Ayarları/Verileri Kaydet (JSON)",
        data=json.dumps(config_to_save),
        file_name="ik_trendleri_ayarlar.json",
        mime="application/json",
        use_container_width=True
    )

with col_res2:
    # Nihai HTML dosyasını indirme butonu
    b64_html = base64.b64encode(html_template.encode('utf-8')).decode()
    href_html = f'<a href="data:text/html;base64,{b64_html}" download="ik_davetiye_final.html" style="text-decoration: none;"><button style="width: 100%; background-color: #28a745; color: white; padding: 12px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: bold;">📥 HTML Mail Dosyasını İndir</button></a>'
    st.markdown(href_html, unsafe_allow_html=True)
