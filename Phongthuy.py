import streamlit as st
import urllib.parse
import streamlit_authenticator as stauth

# --- BỘ NÃO LOGIC PHONG THỦY ---
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
    mapping = {1: "Khảm (Đông Tứ Mệnh)", 2: "Khôn (Tây Tứ Mệnh)", 3: "Chấn (Đông Tứ Mệnh)", 
               4: "Tốn (Đông Tứ Mệnh)", 6: "Càn (Tây Tứ Mệnh)", 7: "Đoài (Tây Tứ Mệnh)", 
               8: "Cấn (Tây Tứ Mệnh)", 9: "Ly (Đông Tứ Mệnh)"}
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
            return ket_qua + "🟡 **ĐÁNH GIÁ - CHƯA CHUẨN:** Mặt bếp nhìn về hướng tốt nhưng vị trí đặt bếp lại đè lên cung tốt (vô tinh thiêu đốt đi may mắn của cung đó). Nên dịch vị trí đặt cụm bếp sang góc khác."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Bếp đặt sai phong thủy, quay mặt về hướng xấu, dễ làm thất thoát tài lộc hoặc ảnh hưởng sức khỏe lửa ấm gia đình."
    elif vat_pham == "nha_ve_sing":
        if tinh_chat_vi_tri == "XẤU (HUNG)":
            return ket_qua + "🟢 **ĐÁNH GIÁ - RẤT TỐT:** Đúng chuẩn phong thủy **'Tọa Hung'**. Nhà vệ sinh đặt tại cung xấu giúp trấn áp, xả trôi các năng lượng tiêu cực và uế khí trong nhà."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Nhà vệ sinh đang đặt đè lên cung tốt của gia chủ, làm suy giảm nghiêm trọng vượng khí, may mắn và tài lộc."

# --- KHỞI TẠO CƠ SỞ DỮ LIỆU BÌNH LUẬN VÀ THÀNH VIÊN VÙNG NHỚ ---
if 'binh_luan_db' not in st.session_state:
    st.session_state['binh_luan_db'] = [
        {"user": "phongthuy_gia", "text": "Hệ thống tính toán quái số chuẩn phái Bát Trạch!"},
        {"user": "GiaChuMayMan", "text": "Đã đổi hướng đầu giường theo app và thấy ngủ ngon hơn hẳn."}
    ]

# CẬP NHẬT PHIÊN BẢN 0.4.x: Sử dụng mật khẩu dạng text thô, thư viện sẽ tự mã hóa tự động
if 'credentials' not in st.session_state:
    st.session_state['credentials'] = {
        'usernames': {
            'admin': {'name': 'Quản trị viên', 'password': 'admin123'},
            'user1': {'name': 'Gia chủ mẫu', 'password': 'user123'}
        }
    }

# --- CẤU HÌNH GIAO DIỆN VÀ STYLE ---
st.set_page_config(page_title="Phong Thủy Bát Trạch Cát Tường", page_icon="☯️", layout="wide")

st.markdown("""
    <style>
    header[data-testid="stHeader"] {
        background-color: #0b0f19 !important;
    }
    header[data-testid="stHeader"] button, header[data-testid="stHeader"] a, header[data-testid="stHeader"] span {
        color: #f1f5f9 !important;
    }
    button[data-testid="embed-btn"], a[href*="github.com/edit"], button[title*="Deploy"], button[title*="Edit"] {
        display: none !important;
    }
    div[data-testid="stPopupMenuWindow"], div[role="menu"], ul[role="listbox"] {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #cbd5e1 !important;
    }
    div[data-testid="stPopupMenuWindow"] span, div[role="menu"] span, div[role="menu"] button {
        color: #111827 !important;
        background-color: #ffffff !important;
    }
    div[role="menuitem"]:hover, li[role="option"]:hover {
        background-color: #f1f5f9 !important;
    }
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%);
        color: #f1f5f9 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #334155;
    }
    label, p, span, .stCaption, div[data-testid="stWidgetLabel"] p {
        color: #f1f5f9 !important;
        font-weight: 500;
    }
    .stCaption, small {
        color: #94a3b8 !important;
    }
    h1, h2, h3 {
        color: #c084fc !important; 
        text-shadow: 0 0 10px rgba(192, 132, 252, 0.4);
    }
    .streamlit-expanderHeader {
        background-color: #1e1b4b !important;
        color: #f1f5f9 !important;
        border: 1px solid #4338ca !important;
        border-radius: 8px;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }
    .stAlert {
        background-color: #111827 !important;
        border: 1px solid #a855f7 !important;
        color: #f1f5f9 !important;
        border-radius: 10px;
    }
    .fb-share-btn {
        background-color: #1877f2;
        color: white !important;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- MENU CHUYỂN TRANG TẠI SIDEBAR ---
st.sidebar.markdown("## 🧭 ĐIỀU HƯỚNG HỆ THỐNG")
trang_hien_tai = st.sidebar.radio("Chọn trang hiển thị:", ["🔮 Kiểm tra Phong Thủy", "🔑 Đăng nhập / Đăng ký Tài khoản"])
st.sidebar.write("---")

# CẬP NHẬT PHIÊN BẢN 0.4.x: Khởi tạo Authenticator đúng cấu trúc hàm mới
authenticator = stauth.Authenticate(
    st.session_state['credentials'],
    'phong_thuy_cookie_secure',
    'auth_key_secure',
    cookie_expiry_days=30
)

# =======================================================
# PHÂN HỆ 1: TRANG ĐĂNG NHẬP / ĐĂNG KÝ
# =======================================================
if trang_hien_tai == "🔑 Đăng nhập / Đăng ký Tài khoản":
    st.title("🔑 Trung Tâm Tài Khoản Thành Viên")
    st.write("Đăng nhập để nhận quyền thảo luận và gửi bình luận phong thủy trên hệ thống.")
    
    tab_login, tab_register = st.tabs(["🔒 ĐĂNG NHẬP HỆ THỐNG", "📝 TẠO TÀI KHOẢN MỚI"])
    
    with tab_login:
        if st.session_state.get("authentication_status"):
            st.success(f"Bạn đang đăng nhập với tư cách: **{st.session_state['name']}**")
            authenticator.logout('Đăng xuất khỏi tài khoản', 'main')
        else:
            # CẬP NHẬT PHIÊN BẢN 0.4.x: Hàm login chỉ sử dụng tham số đặt vị trí location
            name, authentication_status, username = authenticator.login(location='main')
            if st.session_state.get("authentication_status") is False:
                st.error('Tài khoản hoặc mật khẩu không chính xác.')
            elif st.session_state.get("authentication_status") is None:
                st.info('Vui lòng điền thông tin để đăng nhập.')
                
    with tab_register:
        try:
            # CẬP NHẬT PHIÊN BẢN 0.4.x: Hàm đăng ký thành viên mới
            email_reg, username_reg, name_reg = authenticator.register_user(location='main')
            if username_reg:
                st.success('🎉 Đăng ký thành công! Bạn có thể chuyển sang tab Đăng nhập để sử dụng.')
        except Exception as e:
            st.error(f"Không thể đăng ký: {e}")

# =======================================================
# PHÂN HỆ 2: TRANG CHÍNH KIỂM TRA PHONG THỦY
# =======================================================
else:
    if st.session_state.get("authentication_status"):
        st.sidebar.markdown(f"🟢 Tài khoản: **{st.session_state['name']}**")
    else:
        st.sidebar.markdown("⚪ Trạng thái: **Khách ẩn danh**")

    # THANH BÊN: THÔNG TIN GIA CHỦ
    st.sidebar.header("🔮 CUNG MỆNH GIA CHỦ")
    col_d, col_m = st.sidebar.columns(2)
    with col_d:
        ngay_sinh = st.number_input("Ngày sinh (Dương lịch):", min_value=1, max_value=31, value=1, step=1)
    with col_m:
        thang_sinh = st.number_input("Tháng sinh (Dương lịch):", min_value=1, max_value=12, value=1, step=1)

    nam_sinh = st.sidebar.number_input("Năm sinh (Dương lịch):", min_value=1950, max_value=2026, value=1995, step=1)
    gioi_tinh = st.sidebar.selectbox("Giới tính Mệnh:", ["Nam", "Nữ"])

    q_so = tinh_quai_so(nam_sinh, gioi_tinh)
    quai_menh = lay_ten_quai_menh(q_so)
    st.sidebar.success(f"📅 **Sinh ngày:** {ngay_sinh}/{thang_sinh}/{nam_sinh}\n\n🌌 **Quái mệnh:** {quai_menh}")

    # GIAO DIỆN NHẬP SỐ ĐO
    st.header("📋 TỌA ĐỘ PHONG THỦY CÁC KHU VỰC")
    st.markdown("<span style='color: #a7f3d0;'>✨ **Mẹo linh hoạt:** Bạn chỉ cần nhập số liệu ở khu vực bạn muốn kiểm tra. Mục nào chưa đo hãy để trống, hệ thống tự động bỏ qua!</span>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. 🛏️ Khu vực Giường Ngủ")
        t_giuong = st.number_input("Tọa độ vị trí đặt giường (°):", min_value=0, max_value=360, value=None, step=1)
        st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(t_giuong)}**")
        h_giuong = st.number_input("Số độ hướng đầu giường (°):", min_value=0, max_value=360, value=None, step=1)
        st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(h_giuong)}**")

        st.write("---")
        st.subheader("2. 🍳 Khu vực Bếp Nấu")
        t_bep = st.number_input("Tọa độ vị trí đặt bếp (°):", min_value=0, max_value=360, value=None, step=1)
        st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(t_bep)}**")
        h_bep = st.number_input("Số độ Hướng Bếp (°):", min_value=0, max_value=360, value=None, step=1)
        st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(h_bep)}**")

    with col2:
        st.subheader("3. 💼 Khu vực Bàn Làm Việc")
        t_ban = st.number_input("Tọa độ vị trí đặt bàn làm việc (°):", min_value=0, max_value=360, value=None, step=1)
        st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(t_ban)}**")
        h_ban = st.number_input("Số độ hướng ngồi nhìn làm việc (°):", min_value=0, max_value=360, value=None, step=1)
        st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(h_ban)}**")

        st.write("---")
        st.subheader("4. 🚽 Khu vực Nhà Vệ Sinh")
        t_wc = st.number_input("Tọa độ vị trí đặt WC (°):", min_value=0, max_value=360, value=None, step=1)
        st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(t_wc)}**")

    st.write("---")

    if 'show_results' not in st.session_state:
        st.session_state['show_results'] = False

    if st.button("🔮 BẮT ĐẦU KIỂM TRA PHONG THỦY", use_container_width=True):
        if t_giuong is None and t_bep is None and t_ban is None and t_wc is None:
            st.warning("🪐 Vui lòng điền số độ của ít nhất một vị trí bạn muốn kiểm tra ở phía trên.")
            st.session_state['show_results'] = False
        else:
            st.session_state['show_results'] = True

    if st.session_state['show_results']:
        st.header("📋 KẾT QUẢ LUẬN GIẢI PHONG THỦY")
        
        danh_sach_tabs = []
        if t_giuong is not None: danh_sach_tabs.append("🛏️ GIƯỜNG NGỦ")
        if t_ban is not None: danh_sach_tabs.append("💼 BÀN LÀM VIỆC")
        if t_bep is not None: danh_sach_tabs.append("🍳 BẾP NẤU")
        if t_wc is not None: danh_sach_tabs.append("🚽 NHÀ VỆ SINH")
        danh_sach_tabs.append("💬 BÌNH LUẬN CỘNG ĐỒNG")
        
        tabs = st.tabs(danh_sach_tabs)
        tab_index = 0
        
        if t_giuong is not None:
            with tabs[tab_index]:
                st.markdown("### 🛏️ Phân Tích Cung Vị Giường Ngủ")
                st.info(kiem_tra_phong_thuy_chi_tiet(q_so, "giuong_ngu", t_giuong, h_giuong))
            tab_index += 1
        if t_ban is not None:
            with tabs[tab_index]:
                st.markdown("### 💼 Phân Tích Cung Vị Bàn Làm Việc")
                st.info(kiem_tra_phong_thuy_chi_tiet(q_so, "ban_lam_viec", t_ban, h_ban))
            tab_index += 1
        if t_bep is not None:
            with tabs[tab_index]:
                st.markdown("### 🍳 Phân Tích Cung Vị Bếp Nấu")
                st.info(kiem_tra_phong_thuy_chi_tiet(q_so, "bep", t_bep, h_bep))
            tab_index += 1
        if t_wc is not None:
            with tabs[tab_index]:
                st.markdown("### 🚽 Phân Tích Cung Vị Nhà Vệ Sinh")
                st.info(kiem_tra_phong_thuy_chi_tiet(q_so, "nha_ve_sing", t_wc))
            tab_index += 1

        # PHẦN KHU VỰC THẢO LUẬN & BÌNH LUẬN TẠI TAB CUỐI
        with tabs[tab_index]:
            st.markdown("### 💬 Ý Kiến & Bình Luận Từ Cộng Đồng")
            
            for bl in st.session_state['binh_luan_db']:
                st.markdown(f"👤 **{bl['user']}**: {bl['text']}")
            st.write("---")
            
            if st.session_state.get("authentication_status"):
                with st.form("gui_binh_luan_form", clear_on_submit=True):
                    text_input = st.text_area("Để lại bình luận của bạn:")
                    nut_gui = st.form_submit_button("Gửi Ý Kiến")
                    if nut_gui and text_input.strip() != "":
                        st.session_state['binh_luan_db'].append({
                            "user": st.session_state['username'],
                            "text": text_input
                        })
                        st.rerun()
            else:
                st.warning("🔒 Chức năng gửi bình luận chỉ dành cho thành viên. Bạn vui lòng chuyển qua mục '🔑 Đăng nhập / Đăng ký Tài khoản' tại thanh điều hướng bên trái để đăng nhập.")

        # Nút chia sẻ Facebook nằm cuối trang kết quả
        st.write("---")
        app_url = "https://kiemtraphongthuy.streamlit.app"
        encoded_url = urllib.parse.quote(app_url)
        fb_share_link = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"
        st.markdown(f'<a href="{fb_share_link}" target="_blank" class="fb-share-btn">🔵 CHIA SẺ KẾT QUẢ TRÊN FACEBOOK</a>', unsafe_allow_html=True)