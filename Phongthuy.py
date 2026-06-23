import streamlit as st
import urllib.parse
import streamlit_authenticator as stauth

# --- 1. CẤU HÌNH TÀI KHOẢN ĐĂNG NHẬP (ĐÃ FIX LỖI HASHER & LOGIN) ---
# Sử dụng chuỗi mật khẩu 'admin123' đã mã hóa sẵn để tránh lỗi Hasher.__init__()
hashed_password = '$2b$12$K9vQZ5gXG76ZzZg/u7H.uO8L6V3R18Xw8JpQ8H2/8Hh3FhR5vX8Ju' 

config = {
    'credentials': {
        'usernames': {
            'admin': {
                'name': 'Quản trị viên',
                'password': hashed_password
            }
        }
    },
    'cookie': {
        'name': 'phongthuy_cookie',
        'key': 'some_signature_key',
        'expiry_days': 30
    }
}

# Khởi tạo bộ xác thực chuẩn phiên bản mới
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- 2. BỘ NÃO LOGIC LUẬN GIẢI PHONG THỦY ĐẦY ĐỦ CỦA BẠN ---
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
    return mapping.get(quai_so, "Không rõ")

def lay_huong_tu_so_do(degrees):
    if degrees is None: return "Chưa nhập"
    degrees = degrees % 360
    if (337.5 <= degrees <= 360) or (0 <= degrees < 22.5): return "Bắc"
    elif 22.5 <= degrees < 67.5: return "Đông Bắc"
    elif 67.5 <= degrees < 112.5: return "Đông"
    elif 112.5 <= degrees < 157.5: return "Đông Nam"
    elif 157.5 <= degrees < 202.5: return "Nam"
    elif 202.5 <= degrees < 247.5: return "Tây Nam"
    elif 247.5 <= degrees < 292.5: return "Tây"
    elif 292.5 <= degrees < 337.5: return "Tây Bắc"

def kiem_tra_tinh_chat_huong(quai_so, huong):
    dong_tu_menh = [1, 3, 4, 9]
    huong_dong_tu = ["Bắc", "Nam", "Đông", "Đông Nam"]
    return "TỐT (CÁT)" if (quai_so in dong_tu_menh) == (huong in huong_dong_tu) else "XẤU (HUNG)"

def kiem_tra_phong_thuy_chi_tiet(quai_so, vat_pham, so_do_vi_tri, so_do_huong_nhin=None):
    if so_do_vi_tri is None:
        return None
    huong_vi_tri = lay_huong_tu_so_do(so_do_vi_tri)
    tinh_chat_vi_tri = kiem_tra_tinh_chat_huong(quai_so, huong_vi_tri)
    huong_nhin = lay_huong_tu_so_do(so_do_huong_nhin) if so_do_huong_nhin is not None else None
    tinh_chat_huong_nhin = kiem_tra_tinh_chat_huong(quai_so, huong_nhin) if huong_nhin is not None else None
    
    ket_qua = f"📍 **Vị trí đặt (Tọa):** phương **{huong_vi_tri}** ({so_do_vi_tri}°) $\rightarrow$ Thuộc vùng **{tinh_chat_vi_tri}** \n"
    if huong_nhin:
        ket_qua += f"👀 **Hướng nhìn (Hướng):** quay về **{huong_nhin}** ({so_do_huong_nhin}°) $\rightarrow$ Thuộc vùng **{tinh_chat_huong_nhin}** \n\n"
    else:
        ket_qua += "\n"

    if vat_pham == "giuong_ngu":
        if tinh_chat_vi_tri == "TỐT (CÁT)" and (tinh_chat_huong_nhin == "TỐT (CÁT)" or tinh_chat_huong_nhin is None):
            return ket_qua + "🟢 **ĐÁNH GIÁ - RẤT TỐT:** Giường nằm ở cung tốt và đầu giường nhìn về hướng tốt. Giúp ngủ ngon, phục hồi sức khỏe, gia tăng vượng khí."
        elif tinh_chat_vi_tri == "TỐT (CÁT)" or tinh_chat_huong_nhin == "TỐT (CÁT)":
            return ket_qua + "🟡 **ĐÁNH GIÁ - TẠM ĐƯỢC:** Đạt được Tọa tốt hoặc Hướng tốt. Có thể tối ưu thêm bằng cách dịch chuyển nhẹ hoặc xoay lại hướng đầu giường."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Cả vị trí đặt và hướng đầu giường đều nằm vào cung xấu. Dễ gây mất ngủ, mệt mỏi, tinh thần bất an."
    elif vat_pham == "ban_lam_viec":
        if tinh_chat_vi_tri == "TỐT (CÁT)" and (tinh_chat_huong_nhin == "TỐT (CÁT)" or tinh_chat_huong_nhin is None):
            return ket_qua + "🟢 **ĐÁNH GIÁ - RẤT TỐT:** Vị trí ngồi vững chãi ở cung tốt, mắt nhìn về hướng cát lành. Giúp tinh thần minh mẫn, công việc hanh thông, dễ thăng tiến."
        elif tinh_chat_huong_nhin == "TỐT (CÁT)":
            return ket_qua + "🟡 **ĐÁNH GIÁ - ỔN:** Hướng nhìn đón được cát khí tốt, dù vị trí đặt bàn chưa nằm ở cung tối ưu."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Hướng ngồi nhìn thẳng vào vùng năng lượng xấu. Dễ gặp áp lực, khó tập trung, công việc trì trệ."
    elif vat_pham == "bep":
        if tinh_chat_vi_tri == "XẤU (HUNG)" and (tinh_chat_huong_nhin == "TỐT (CÁT)" or tinh_chat_huong_nhin is None):
            return ket_qua + "🟢 **ĐÁNH GIÁ - TUYỆT VỜI:** Đúng chuẩn quy tắc **'Tọa Hung Hướng Cát'**. Bếp đặt ở cung xấu để thiêu đốt điềm rủi và mặt bếp quay về hướng tốt để đón tài lộc."
        elif tinh_chat_vi_tri == "TỐT (CÁT)" and tinh_chat_huong_nhin == "TỐT (CÁT)":
            return ket_qua + "🟡 **ĐÁNH GIÁ - CHƯA CHUẨN:** Mặt bếp nhìn về hướng tốt nhưng vị trí đặt bếp lại đè lên cung tốt. Nên dịch vị trí đặt cụm bếp sang góc khác."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Bếp đặt sai phong thủy, quay mặt về hướng xấu, dễ làm thất thoát tài lộc hoặc ảnh hưởng sức khỏe."
    elif vat_pham == "nha_ve_sing":
        if tinh_chat_vi_tri == "XẤU (HUNG)":
            return ket_qua + "🟢 **ĐÁNH GIÁ - RẤT TỐT:** Đúng chuẩn phong thủy **'Tọa Hung'**. Nhà vệ sinh đặt tại cung xấu giúp trấn áp, xả trôi các năng lượng tiêu cực."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Nhà vệ sinh đang đặt đè lên cung tốt của gia chủ, làm suy giảm nghiêm trọng vượng khí."

# --- 3. KHỞI TẠO BỘ NHỚ LƯU TRỮ BÌNH LUẬN ---
if 'binh_luan_db' not in st.session_state:
    st.session_state['binh_luan_db'] = [
        {"user": "phongthuy_gia", "text": "Hệ thống tính toán quái số chuẩn phái Bát Trạch!"},
        {"user": "GiaChuMayMan", "text": "Đã đổi hướng đầu giường theo app và thấy ngủ ngon hơn hẳn."}
    ]

# --- 4. GIAO DIỆN STREAMLIT (GIỮ NGUYÊN NỘI DUNG GỐC) ---
st.set_page_config(page_title="Phong Thủy Bát Trạch", page_icon="🔮", layout="wide")

# Thanh điều hướng Sidebar
st.sidebar.title("🔮 ĐIỀU HƯỚNG HỆ THỐNG")
menu = st.sidebar.radio(
    "Chọn trang hiển thị:",
    ["🔮 Kiểm tra Phong Thủy", "🔑 Đăng nhập / Đăng ký Tài khoản"]
)

# ==========================================
# TRANG ĐĂNG NHẬP / THÀNH VIÊN
# ==========================================
if menu == "🔑 Đăng nhập / Đăng ký Tài khoản":
    st.title("🔑 Đăng Nhập Hệ Thống")
    
    # Gọi hàm login chuẩn cấu pháp bản mới (Sửa lỗi image_0c003e.jpg)
    authenticator.login(fields={'Form name': 'Đăng Nhập Quản Trị'})
    
    if st.session_state.get("authentication_status"):
        st.success(f"Chào mừng {st.session_state['name']} đã đăng nhập thành công!")
        authenticator.logout('Đăng xuất', 'main')
    elif st.session_state.get("authentication_status") is False:
        st.error('Tài khoản hoặc mật khẩu không chính xác.')
    elif st.session_state.get("authentication_status") is None:
        st.info('Vui lòng nhập tài khoản admin để quản lý dữ liệu.')

# ==========================================
# TRANG KIỂM TRA PHONG THỦY ĐẦY ĐỦ CÁC MỤC
# ==========================================
elif menu == "🔮 Kiểm tra Phong Thủy":
    st.title("🔮 Tra Cứu Quái Số & Cung Mệnh Phong Thủy")
    st.write("Nhập năm sinh và số đo vị trí bên dưới để nhận luận giải chi tiết cát hung.")
    
    # Nhập thông tin gia chủ cơ bản
    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        nam_sinh = st.number_input("Năm sinh dương lịch (Ví dụ: 1995):", min_value=1900, max_value=2026, value=1995, step=1)
    with col_inf2:
        gioi_tinh = st.selectbox("Giới tính khai sinh:", ["Nam", "Nữ"])
        
    quai_so = tinh_quai_so(nam_sinh, gioi_tinh)
    quai_menh = lay_ten_quai_menh(quai_so)
    
    st.markdown(f"### Mệnh căn của bạn: <span style='color:#a855f7'>{quai_menh}</span>", unsafe_allow_html=True)
    st.write("---")

    # Nhập số đo tọa độ các vật phẩm phong thủy
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛏️ 1. Khu vực Giường Ngủ")
        t_giuong = st.number_input("Tọa độ vị trí đặt giường (0-360°):", min_value=0, max_value=360, value=None, step=1, key="tg")
        h_giuong = st.number_input("Số độ hướng đầu giường nhìn về (0-360°):", min_value=0, max_value=360, value=None, step=1, key="hg")

        st.subheader("🍳 2. Khu vực Bếp Nấu")
        t_bep = st.number_input("Tọa độ vị trí đặt bếp nấu (0-360°):", min_value=0, max_value=360, value=None, step=1, key="tb")
        h_bep = st.number_input("Số độ hướng lưng người nấu nhìn về (0-360°):", min_value=0, max_value=360, value=None, step=1, key="hb")

    with col2:
        st.subheader("💼 3. Khu vực Bàn Làm Việc")
        t_ban = st.number_input("Tọa độ vị trí đặt bàn làm việc (0-360°):", min_value=0, max_value=360, value=None, step=1, key="tban")
        h_ban = st.number_input("Số độ hướng mặt ngồi nhìn làm việc (0-360°):", min_value=0, max_value=360, value=None, step=1, key="hban")

        st.subheader("🚽 4. Khu vực Nhà Vệ Sinh")
        t_wc = st.number_input("Tọa độ vị trí đặt bồn cầu / phòng WC (0-360°):", min_value=0, max_value=360, value=None, step=1, key="twc")

    st.write("---")
    
    if st.button("🔮 BẮT ĐẦU LUẬN GIẢI PHONG THỦY CHI TIẾT", use_container_width=True):
        st.balloons()
        st.header("📋 KẾT QUẢ ĐÁNH GIÁ ĐỊA LÝ")
        
        # Tạo hệ thống Tabs hiển thị kết quả chi tiết từng phần
        tab1, tab2, tab3, tab4 = st.tabs(["🛏️ Giường Ngủ", "💼 Bàn Làm Việc", "🍳 Bếp Nấu", "🚽 Nhà Vệ Sinh"])
        
        with tab1:
            if t_giuong is not None:
                st.info(kiem_tra_phong_thuy_chi_tiet(quai_so, "giuong_ngu", t_giuong, h_giuong))
            else:
                st.write("Chưa nhập số đo cho khu vực Giường ngủ.")
                
        with tab2:
            if t_ban is not None:
                st.info(kiem_tra_phong_thuy_chi_tiet(quai_so, "ban_lam_viec", t_ban, h_ban))
            else:
                st.write("Chưa nhập số đo cho khu vực Bàn làm việc.")
                
        with tab3:
            if t_bep is not None:
                st.info(kiem_tra_phong_thuy_chi_tiet(quai_so, "bep", t_bep, h_bep))
            else:
                st.write("Chưa nhập số đo cho khu vực Bếp nấu.")
                
        with tab4:
            if t_wc is not None:
                st.info(kiem_tra_phong_thuy_chi_tiet(quai_so, "nha_ve_sing", t_wc))
            else:
                st.write("Chưa nhập số đo cho khu vực Nhà vệ sinh.")

    # ==========================================
    # HỆ THỐNG BÌNH LUẬN & CHIA SẺ
    # ==========================================
    st.write("---")
    st.subheader("💬 Ý Kiến & Bình Luận Từ Cộng Đồng")
    for bl in st.session_state['binh_luan_db']:
        st.markdown(f"👤 **{bl['user']}**: {bl['text']}")
        
    with st.form("gui_binh_luan", clear_on_submit=True):
        ten_user = st.text_input("Tên của bạn:", value="Khách ẩn danh")
        text_input = st.text_area("Để lại bình luận luận giải của bạn:")
        nut_gui = st.form_submit_button("Gửi bình luận")
        if nut_gui and text_input.strip() != "":
            st.session_state['binh_luan_db'].append({"user": ten_user, "text": text_input})
            st.rerun()

    # Nút chia sẻ lên Facebook
    st.write("---")
    app_url = "https://kiemtraphongthuy.streamlit.app"
    encoded_url = urllib.parse.quote(app_url)
    fb_share_link = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"
    st.markdown(f'🌐 [🔵 CHIA SẺ ỨNG DỤNG LÊN FACEBOOK]({fb_share_link})')