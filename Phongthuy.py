import streamlit as st
import urllib.parse
import streamlit_authenticator as stauth

# --- 1. CẤU HÌNH TÀI KHOẢN ĐĂNG NHẬP (BẢN MỚI CHUẨN ĐÃ FIX HASHER) ---
# Trong bản 0.4.2, ta KHÔNG truyền tham số vào Hasher(), mà gọi trực tiếp .hash() hoặc .generate() đúng cách
# Hoặc đơn giản hơn, đây là chuỗi mật khẩu 'admin123' đã được mã hóa sẵn bằng bcrypt chuẩn:
hashed_password = '$2b$12$K9vQZ5gXG76ZzZg/u7H.uO8L6V3R18Xw8JpQ8H2/8Hh3FhR5vX8Ju' 

config = {
    'credentials': {
        'usernames': {
            'admin': {
                'name': 'Quản trị viên',
                'password': hashed_password  # Sử dụng mật khẩu đã mã hóa sẵn an toàn
            }
        }
    },
    'cookie': {
        'name': 'phongthuy_cookie',
        'key': 'some_signature_key',
        'expiry_days': 30
    }
}

# Khởi tạo bộ xác thực
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- 2. BỘ NÃO LOGIC PHONG THỦY ---
def tinh_quai_so(nam_sinh, gioi_tinh):
    tong = sum(int(chuso) for chuso in str(nam_sinh))
    while tong > 9:
        tong = sum(int(chuso) for chuso in str(tong))
    if gioi_tinh.lower() == 'nam':
        quai_so = 11 - tong
    else:
        quai_so = 4 + tong
    while quai_so > 9:
        quai_so -= 9
    if quai_so == 5:
        return 2 if gioi_tinh.lower() == 'nam' else 8
    return quai_so

def lay_ten_quai_menh(quai_so):
    mapping = {
        1: "Khảm (Đông Tứ Mệnh)", 2: "Khôn (Tây Tứ Mệnh)", 3: "Chấn (Đông Tứ Mệnh)",
        4: "Tốn (Đông Tứ Mệnh)", 6: "Càn (Tây Tứ Mệnh)", 7: "Đoài (Tây Tứ Mệnh)",
        8: "Cấn (Tây Tứ Mệnh)", 9: "Ly (Đông Tứ Mệnh)"
    }
    return mapping.get(quai_so, "Không xác định")

# --- 3. GIAO DIỆN ỨNG DỤNG (STREAMLIT) ---
st.set_page_config(page_title="Hệ Thống Phong Thủy", page_icon="🔮", layout="centered")

# Thanh điều hướng Sidebar
st.sidebar.title("🔮 ĐIỀU HƯỚNG HỆ THỐNG")
menu = st.sidebar.radio(
    "Chọn trang hiển thị:",
    ["🔮 Kiểm tra Phong Thủy", "🔑 Đăng nhập / Đăng ký Tài khoản"]
)

if menu == "🔑 Đăng nhập / Đăng ký Tài khoản":
    # Gọi hàm login theo cú pháp chuẩn của phiên bản mới
    authenticator.login(fields={'Form name': 'Đăng Nhập Hệ Thống'})
    
    if st.session_state["authentication_status"]:
        st.success(f"Chào mừng {st.session_state['name']} đã đăng nhập thành công!")
        authenticator.logout('Đăng xuất', 'main')
    elif st.session_state["authentication_status"] is False:
        st.error('Tài khoản hoặc mật khẩu không chính xác.')
    elif st.session_state["authentication_status"] is None:
        st.info('Vui lòng nhập tài khoản admin để cấu hình nâng cao.')

elif menu == "🔮 Kiểm tra Phong Thủy":
    st.title("🔮 Tra Cứu Quái Số & Cung Mệnh Phong Thủy")
    st.write("Nhập thông tin của bạn bên dưới để xem cung mệnh phát triển công danh, sự nghiệp.")
    
    # Form nhập liệu
    with st.form("phong_thuy_form"):
        nam_sinh = st.number_input("Năm sinh của bạn (Ví dụ: 1995):", min_value=1900, max_value=2026, value=1995, step=1)
        gioi_tinh = st.selectbox("Giới tính khai sinh:", ["Nam", "Nữ"])
        submit_button = st.form_submit_button(label="Tra cứu ngay")
        
    if submit_button:
        with st.spinner("Đang tính toán toán học phong thủy..."):
            quai_so = tinh_quai_so(nam_sinh, gioi_tinh)
            quai_menh = lay_ten_quai_menh(quai_so)
            
            st.balloons()
            st.success("### 🎉 Kết quả tra cứu của bạn:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Quái số của bạn", value=str(quai_so))
            with col2:
                st.metric(label="Cung mệnh / Hướng", value=quai_menh)
                
            st.info(f"💡 **Lời khuyên sơ lược:** Bạn thuộc nhóm **{quai_menh.split('(')[-1].replace(')', '')}**. Nên ưu tiên chọn các hướng làm việc, đặt giường ngủ theo đúng nhóm mệnh này để kích hoạt may mắn.")