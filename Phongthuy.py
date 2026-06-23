import streamlit as st
import streamlit_authenticator as stauth

# --- 1. CẤU HÌNH HỆ THỐNG ---
# Mật khẩu đã được mã hóa (dùng cho tính năng đăng nhập)
hashed_password = '$2b$12$K9vQZ5gXG76ZzZg/u7H.uO8L6V3R18Xw8JpQ8H2/8Hh3FhR5vX8Ju' 
config = {
    'credentials': {'usernames': {'admin': {'name': 'Quản trị viên', 'password': hashed_password}}},
    'cookie': {'name': 'phongthuy_cookie', 'key': 'secret_key', 'expiry_days': 30}
}

authenticator = stauth.Authenticate(config['credentials'], config['cookie']['name'], config['cookie']['key'], config['cookie']['expiry_days'])

# --- 2. HÀM TÍNH TOÁN PHONG THỦY ---
def tinh_quai_so(nam, gioi_tinh):
    tong = sum(int(c) for c in str(nam))
    while tong > 9: tong = sum(int(c) for c in str(tong))
    quai_so = (11 - tong) if gioi_tinh == 'Nam' else (4 + tong)
    while quai_so > 9: quai_so -= 9
    return (2 if gioi_tinh == 'Nam' else 8) if quai_so == 5 else quai_so

# --- 3. GIAO DIỆN CHÍNH ---
st.set_page_config(page_title="Hệ Thống Phong Thủy", layout="wide")

# Sidebar đăng nhập
with st.sidebar:
    st.title("🔑 Đăng nhập hệ thống")
    authenticator.login(fields={'Form name': 'Đăng nhập'})
    if st.session_state.get("authentication_status"):
        st.success(f"Chào {st.session_state['name']}")
        authenticator.logout('Đăng xuất', 'main')

st.title("🔮 Tra Cứu Quái Số & Cung Mệnh Phong Thủy")

# Phần hướng dẫn từ image_1a7c98.png
st.info("""
🧭 **HƯỚNG DẪN SỬ DỤNG LA BÀN ĐỂ ĐO SỐ ĐỘ CHÍNH XÁC:**
1. **Đo Cung vị trí (Tọa độ đặt vật phẩm):** Bạn đứng ở chính giữa **Tâm nhà / Tâm phòng**, mở ứng dụng la bàn trên điện thoại, hướng đầu điện thoại thẳng về vị trí đang đặt (hoặc dự định đặt) Giường, Bếp, Bàn làm việc, WC để xem số độ hiển thị.
2. **Đo Hướng nhìn (Hướng đầu giường / Hướng nhìn):**
    * *Giường ngủ:* Nằm trên giường, hướng mắt nhìn về phía đuôi giường (hoặc đầu giường hướng đi đâu đo hướng đó).
    * *Bàn làm việc:* Ngồi vào ghế làm việc, hướng mắt nhìn thẳng ra phía trước bàn.
    * *Bếp nấu:* Đứng ở vị trí nấu, hướng mặt nhìn thẳng vào bếp nấu (hướng lưng người nấu quay về đâu chính là Hướng Bếp).
""")

# Khu vực nhập thông tin gia chủ
st.subheader("📅 Thông tin gia chủ")
c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
with c1:
    ngay = st.number_input("Ngày sinh:", 1, 31, 1)
with c2:
    thang = st.number_input("Tháng sinh:", 1, 12, 1)
with c3:
    nam = st.number_input("Năm sinh (Dương lịch):", 1900, 2026, 1995)
with c4:
    gioi_tinh = st.selectbox("Giới tính khai sinh:", ["Nam", "Nữ"])

# Tính toán
quai_so = tinh_quai_so(nam, gioi_tinh)

st.write("---")
st.markdown(f"### Mệnh quái của bạn: **{quai_so}**")

# Khu vực nhập thông số đo
st.subheader("📏 Nhập số đo phong thủy")
col_b1, col_b2 = st.columns(2)
with col_b1:
    t_do = st.number_input("Tọa độ vật phẩm (độ):", 0, 360, 0)
with col_b2:
    h_do = st.number_input("Hướng nhìn/Hướng bếp (độ):", 0, 360, 0)

if st.button("Xác nhận thông tin"):
    st.write(f"Đã cập nhật: Sinh ngày {ngay}/{thang}/{nam} - Giới tính: {gioi_tinh}")
    st.write("Hệ thống đã lưu số đo để luận giải.")

# Khu vực bình luận
st.subheader("💬 Bình luận cộng đồng")
if 'bl' not in st.session_state: st.session_state['bl'] = []
for item in st.session_state['bl']: st.write(f"- {item}")

text_bl = st.text_input("Nhập ý kiến của bạn:")
if st.button("Gửi bình luận"):
    if text_bl:
        st.session_state['bl'].append(text_bl)
        st.rerun()