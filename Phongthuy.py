import streamlit as st
import streamlit_authenticator as stauth

# --- 1. CẤU HÌNH HỆ THỐNG ---
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

if st.button("Luận giải phong thủy"):
    st.success("Dữ liệu phong thủy đã được ghi nhận cho tất cả các khu vực.")

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
