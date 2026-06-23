import streamlit as st
import streamlit_authenticator as stauth

# --- 1. CẤU HÌNH HỆ THỐNG ---
hashed_password = '$2b$12$K9vQZ5gXG76ZzZg/u7H.uO8L6V3R18Xw8JpQ8H2/8Hh3FhR5vX8Ju' 
config = {
    'credentials': {'usernames': {'admin': {'name': 'Quản trị viên', 'password': hashed_password}}},
    'cookie': {'name': 'phongthuy_cookie', 'key': 'secret_key', 'expiry_days': 30}
}
authenticator = stauth.Authenticate(config['credentials'], config['cookie']['name'], config['cookie']['key'], config['cookie']['expiry_days'])

# --- 2. HÀM TÍNH TOÁN ---
def tinh_quai_so(nam, gioi_tinh):
    tong = sum(int(c) for c in str(nam))
    while tong > 9: tong = sum(int(c) for c in str(tong))
    quai_so = (11 - tong) if gioi_tinh == 'Nam' else (4 + tong)
    while quai_so > 9: quai_so -= 9
    return (2 if gioi_tinh == 'Nam' else 8) if quai_so == 5 else quai_so

# --- 3. GIAO DIỆN ---
st.set_page_config(page_title="Hệ Thống Phong Thủy", layout="wide")

with st.sidebar:
    st.title("🔑 Đăng nhập hệ thống")
    authenticator.login(fields={'Form name': 'Đăng nhập'})

st.title("🔮 Tra Cứu Quái Số & Cung Mệnh Phong Thủy")

st.info("""
🧭 **HƯỚNG DẪN SỬ DỤNG LA BÀN ĐỂ ĐO SỐ ĐỘ CHÍNH XÁC:**
1. **Đo Cung vị trí:** Đứng ở **Tâm nhà**, hướng đầu điện thoại về vị trí đặt Giường, Bếp, Bàn làm việc, WC.
2. **Đo Hướng nhìn:** 
    * *Nhà vệ sinh (WC):* Đo "Tọa" (Vị trí đặt WC): Bạn nên đứng ở Tâm nhà (trung tâm của ngôi nhà), hướng đầu điện thoại về phía cửa nhà vệ sinh hoặc tâm của phòng vệ sinh để xác định nó nằm ở phương vị nào.
**-Đo "Hướng" (Hướng cửa WC): Nếu bạn muốn biết hướng khí của WC (thường tính theo hướng cửa hoặc hướng bồn cầu), hãy đứng ngay tại cửa nhà vệ sinh.
**-Hướng đầu điện thoại (loa nghe) thẳng về phía cửa WC hoặc bồn cầu. Số độ hiển thị trên màn hình chính là Hướng WC của bạn.
    * *Giường ngủ:* Cách đo bằng điện thoại:
**-Bạn đứng ở chính giữa giường, đặt điện thoại nằm phẳng trên mặt giường.**
**-Hướng Đầu điện thoại (loa nghe) về phía Đuôi giường (phía chân người nằm).**
Số độ hiển thị trên màn hình chính là Hướng giường của bạn.
    * *Bàn làm việc:* Mắt nhìn thẳng ra trước mặt bàn.Đầu điện thoại chỉ ra trước mặt bàn
    * *Bếp nấu:* Mắt nhìn vào mặt bếp (lưng người nấu quay về đâu chính là Hướng Bếp).
    **Cách đo bằng điện thoại:**
**-Bạn đứng đúng vị trí người nấu thường đứng.**
**-Để Đuôi điện thoại (cổng sạc) áp sát vào bụng (hoặc hướng về phía lưng bạn).**
**-Hướng Đầu điện thoại (loa nghe) thẳng về phía mặt bếp/nồi nấu (hướng mắt bạn đang nhìn).**
**-Số độ hiển thị chính là Hướng Bếp cần tra cứu.**
""")

st.subheader("📅 Thông tin gia chủ")
c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
with c1: ngay = st.number_input("Ngày sinh (Dương lịch):", 1, 31, 1)
with c2: thang = st.number_input("Tháng sinh (Dương lịch):", 1, 12, 1)
with c3: nam = st.number_input("Năm sinh (Dương lịch):", 1900, 2026, 1995)
with c4: gioi_tinh = st.selectbox("Giới tính khai sinh:", ["Nam", "Nữ"])

st.markdown(f"### Mệnh quái của bạn: **{tinh_quai_so(nam, gioi_tinh)}**")

st.subheader("📏 Nhập số đo phong thủy")
# Chia nhóm các khu vực để nhập số liệu
col1, col2 = st.columns(2)
with col1:
    st.write("#### 🛏️ Giường ngủ")
    t_giuong = st.number_input("Tọa giường (°):", 0, 360, 0, key="tg")
    h_giuong = st.number_input("Hướng giường (°):", 0, 360, 0, key="hg")
    
    st.write("#### 💼 Bàn làm việc")
    t_ban = st.number_input("Tọa bàn (°):", 0, 360, 0, key="tb")
    h_ban = st.number_input("Hướng bàn (°):", 0, 360, 0, key="hb")

with col2:
    st.write("#### 🍳 Bếp nấu")
    t_bep = st.number_input("Tọa bếp (°):", 0, 360, 0, key="tbep")
    h_bep = st.number_input("Hướng bếp (°):", 0, 360, 0, key="hbep")
    
    st.write("#### 🚽 Nhà vệ sinh (WC)")
    t_wc = st.number_input("Tọa WC (°):", 0, 360, 0, key="twc")
    h_wc = st.number_input("Hướng WC (°):", 0, 360, 0, key="hwc")

if st.button("Xác nhận thông tin"):
    st.success("Dữ liệu phong thủy đã được ghi nhận cho tất cả các khu vực.")

st.subheader("💬 Bình luận cộng đồng")
if 'bl' not in st.session_state: st.session_state['bl'] = []
for item in st.session_state['bl']: st.write(f"- {item}")
text_bl = st.text_input("Ý kiến của bạn:")
if st.button("Gửi bình luận"):
    if text_bl:
        st.session_state['bl'].append(text_bl)
        st.rerun()
