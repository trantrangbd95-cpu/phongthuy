import streamlit as st
import streamlit_authenticator as stauth
import urllib.parse

# --- 1. CẤU HÌNH ĐĂNG NHẬP ---
hashed_password = '$2b$12$K9vQZ5gXG76ZzZg/u7H.uO8L6V3R18Xw8JpQ8H2/8Hh3FhR5vX8Ju'
config = {'credentials': {'usernames': {'admin': {'name': 'Quản trị viên', 'password': hashed_password}}},
          'cookie': {'name': 'phongthuy_cookie', 'key': 'secret_key', 'expiry_days': 30}}
authenticator = stauth.Authenticate(config['credentials'], config['cookie']['name'], config['cookie']['key'], config['cookie']['expiry_days'])

# --- 2. HÀM XỬ LÝ PHONG THỦY ---
def tinh_quai_so(nam, gioi_tinh):
    tong = sum(int(c) for c in str(nam))
    while tong > 9: tong = sum(int(c) for c in str(tong))
    quai_so = (11 - tong) if gioi_tinh == 'Nam' else (4 + tong)
    while quai_so > 9: quai_so -= 9
    return (2 if gioi_tinh == 'Nam' else 8) if quai_so == 5 else quai_so

def lay_huong(deg):
    if deg is None: return "Chưa xác định"
    if 337.5 <= deg <= 360 or 0 <= deg < 22.5: return "Bắc"
    if 22.5 <= deg < 67.5: return "Đông Bắc"
    if 67.5 <= deg < 112.5: return "Đông"
    if 112.5 <= deg < 157.5: return "Đông Nam"
    if 157.5 <= deg < 202.5: return "Nam"
    if 202.5 <= deg < 247.5: return "Tây Nam"
    if 247.5 <= deg < 292.5: return "Tây"
    return "Tây Bắc"

def luan_giai(qs, t_deg, h_deg, ten):
    h_ten = lay_huong(h_deg)
    dong_tu = [1, 3, 4, 9]
    is_dong_tu = qs in dong_tu
    huong_tot = ["Bắc", "Nam", "Đông", "Đông Nam"] if is_dong_tu else ["Tây", "Tây Bắc", "Tây Nam", "Đông Bắc"]
    status = "TỐT" if h_ten in huong_tot else "XẤU"
    return f"**{ten}**: Tọa {lay_huong(t_deg)} | Hướng **{h_ten}** $\rightarrow$ **{status}**. {'Đón cát khí, gia chủ vượng tài lộc.' if status == 'TỐT' else 'Phạm sát khí, nên xoay về: ' + ', '.join(huong_tot)}"

# --- 3. GIAO DIỆN ---
st.set_page_config(page_title="Hệ Thống Phong Thủy", layout="wide")
st.markdown("<style>.big-font { font-size: 24px !important; font-weight: bold; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.title("🔑 Đăng nhập")
    authenticator.login(fields={'Form name': 'Quản trị'})

st.title("🔮 Tra Cứu Phong Thủy Bát Trạch")

st.info("""
🧭 **HƯỚNG DẪN ĐO LA BÀN:** * **Đo Tọa:** Đứng ở **Tâm nhà**, đầu điện thoại hướng về phía vật phẩm để biết nó nằm ở phương vị nào.
* **Đo Hướng:** Đứng tại vị trí vật phẩm, hướng đầu điện thoại về phía "Mắt nhìn" (Bếp: nhìn vào nồi; Giường: nhìn ra chân; Bàn: nhìn ra trước mặt; WC: nhìn vào phòng).
""")

# Nhập liệu
c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
with c1: ngay = st.number_input("Ngày:", 1, 31, 1)
with c2: thang = st.number_input("Tháng:", 1, 12, 1)
with c3: nam = st.number_input("Năm:", 1900, 2026, 1995)
with c4: gioi_tinh = st.selectbox("Giới tính:", ["Nam", "Nữ"])

qs = tinh_quai_so(nam, gioi_tinh)
st.write(f"### Mệnh quái: **{qs}** ({'Đông Tứ Mệnh' if qs in [1,3,4,9] else 'Tây Tứ Mệnh'})")

# Nhập Tọa & Hướng
data = {}
cols = st.columns(2)
vat_phams = ["Giường ngủ", "Bàn làm việc", "Bếp nấu", "Nhà vệ sinh"]
for i, vp in enumerate(vat_phams):
    c = cols[0] if i < 2 else cols[1]
    with c:
        st.write(f"#### {vp}")
        t = st.number_input(f"Tọa độ {vp} (°):", 0, 360, 0, key=f"t_{i}")
        h = st.number_input(f"Hướng nhìn {vp} (°):", 0, 360, 0, key=f"h_{i}")
        st.write(f"*(Tọa: {lay_huong(t)} - Hướng: {lay_huong(h)})*")
        data[vp] = (t, h)

if st.button("LUẬN GIẢI CHI TIẾT"):
    st.markdown('<p class="big-font">📋 KẾT QUẢ PHÂN TÍCH</p>', unsafe_allow_html=True)
    for vp, (t, h) in data.items():
        st.write(luan_giai(qs, t, h, vp))
    
    # Chia sẻ
    st.write("---")
    msg = urllib.parse.quote("Kết quả phong thủy của tôi: " + str(qs))
    st.markdown(f"[🔵 CHIA SẺ KẾT QUẢ LÊN FACEBOOK](https://www.facebook.com/sharer/sharer.php?u=https://your-app-url.com&quote={msg})")

# Bình luận
st.subheader("💬 Bình luận")
if 'bl' not in st.session_state: st.session_state['bl'] = []
for item in st.session_state['bl']: st.write(f"- {item}")
if text := st.text_input("Góp ý của bạn:"):
    if st.button("Gửi"):
        st.session_state['bl'].append(text)
        st.rerun()
