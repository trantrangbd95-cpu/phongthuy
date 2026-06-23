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

Hướng dẫn chi tiết cho từng vị trí:

🛏️ Giường ngủ:

Cách đo: Đứng (hoặc nằm) ở giữa giường.

Thao tác: Hướng Đầu điện thoại về phía Đuôi giường (phía chân người nằm). Số độ đó chính là hướng giường của bạn.

🍳 Bếp nấu:

Cách đo: Đứng ở vị trí người nấu đứng thao tác hàng ngày.

Thao tác: Hướng Đầu điện thoại thẳng vào Mặt bếp/Nồi nấu (hướng mắt bạn đang nhìn). Lưng bạn đang quay về phía nào thì đó chính là phương vị "Tọa" của bếp.

💼 Bàn làm việc:

Cách đo: Ngồi vào ghế làm việc.

Thao tác: Hướng Đầu điện thoại thẳng ra phía Trước mặt bàn (hướng nhìn của bạn).

🚽 Nhà vệ sinh (WC):

Cách đo: Đứng ngay tại cửa phòng vệ sinh.

Thao tác: Nhìn thẳng vào trong phòng, hướng Đầu điện thoại vào phía trong phòng vệ sinh. Số độ đó là hướng cửa của nhà vệ sinh.

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



import streamlit as st

import streamlit_authenticator as stauth



# --- HÀM TÍNH QUÁI SỐ & ĐÁNH GIÁ ---

def tinh_quai_so(nam, gioi_tinh):

    tong = sum(int(c) for c in str(nam))

    while tong > 9: tong = sum(int(c) for c in str(tong))

    quai_so = (11 - tong) if gioi_tinh == 'Nam' else (4 + tong)

    while quai_so > 9: quai_so -= 9

    return (2 if gioi_tinh == 'Nam' else 8) if quai_so == 5 else quai_so



def lay_huong(deg):

    if 337.5 <= deg <= 360 or 0 <= deg < 22.5: return "Bắc"

    if 22.5 <= deg < 67.5: return "Đông Bắc"

    if 67.5 <= deg < 112.5: return "Đông"

    if 112.5 <= deg < 157.5: return "Đông Nam"

    if 157.5 <= deg < 202.5: return "Nam"

    if 202.5 <= deg < 247.5: return "Tây Nam"

    if 247.5 <= deg < 292.5: return "Tây"

    return "Tây Bắc"



def danh_gia_huong(quai_so, deg, ten_vat_pham):

    huong = lay_huong(deg)

    # Nhóm Đông Tứ Trạch: 1, 3, 4, 9 | Tây Tứ Trạch: 2, 6, 7, 8

    dong_tu = [1, 3, 4, 9]

    is_dong_tu = quai_so in dong_tu

    huong_tot_dong = ["Bắc", "Nam", "Đông", "Đông Nam"]

   

    huong_la_tot = (huong in huong_tot_dong) if is_dong_tu else (huong not in huong_tot_dong)

   

    if huong_la_tot:

        return f"✅ **{ten_vat_pham} hướng {huong}: TỐT.** Giúp gia chủ vượng tài lộc, sức khỏe dồi dào."

    else:

        return f"⚠️ **{ten_vat_pham} hướng {huong}: CHƯA TỐT.** Nên xoay lại hướng khác (gợi ý: { 'Bắc/Nam/Đông/Đông Nam' if is_dong_tu else 'Tây/Tây Bắc/Tây Nam/Đông Bắc'}) để tăng vượng khí."



if st.button("Luận giải phong thủy"):

    qs = tinh_quai_so(nam, gioi_tinh)

    st.write(f"### Kết quả cho Mệnh quái: {qs}")

   

    # Hiển thị đánh giá chi tiết

    st.write("---")

    st.write(danh_gia_huong(qs, h_giuong, "Giường ngủ"))

    st.write(danh_gia_huong(qs, h_ban, "Bàn làm việc"))

    st.write(danh_gia_huong(qs, h_bep, "Bếp nấu"))

    st.write(danh_gia_huong(qs, h_wc, "Nhà vệ sinh"))



st.subheader("💬 Bình luận cộng đồng")

if 'bl' not in st.session_state: st.session_state['bl'] = []

for item in st.session_state['bl']: st.write(f"- {item}")

text_bl = st.text_input("Ý kiến của bạn:")

if st.button("Gửi bình luận"):

    if text_bl:

        st.session_state['bl'].append(text_bl)

        st.rerun()
