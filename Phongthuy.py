import streamlit as st
import urllib.parse

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
            return ket_qua + "🟡 **ĐÁNH GIÁ - CHƯA CHUẨN:** Mặt bếp nhìn về hướng tốt nhưng vị trí đặt bếp lại đè lên cung tốt (vô tình thiêu đốt đi may mắn của cung đó). Nên dịch vị trí đặt cụm bếp sang góc khác."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Bếp đặt sai phong thủy, quay mặt về hướng xấu, dễ làm thất thoát tài lộc hoặc ảnh hưởng sức khỏe lửa ấm gia đình."

    elif vat_pham == "nha_ve_sing":
        if tinh_chat_vi_tri == "XẤU (HUNG)":
            return ket_qua + "🟢 **ĐÁNH GIÁ - RẤT TỐT:** Đúng chuẩn phong thủy **'Tọa Hung'**. Nhà vệ sinh đặt tại cung xấu giúp trấn áp, xả trôi các năng lượng tiêu cực và uế khí trong nhà."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Nhà vệ sinh đang đặt đè lên cung tốt của gia chủ, làm suy giảm nghiêm trọng vượng khí, may mắn và tài lộc."

# --- THIẾT KẾ GIAO DIỆN WEBSITE & MÀU SẮC GALAXY TỬ VI ---
st.set_page_config(page_title="Phong Thủy Bát Trạch Cát Tường", page_icon="☯️", layout="wide")

# Sửa triệt để lỗi màu chữ đen, dải trắng trên cùng header và định dạng lại toàn trang
st.markdown("""
    <style>
    /* Đổi màu dải header trên cùng từ trắng về cùng màu tối với trang bên dưới */
    header[data-testid="stHeader"] {
        background-color: #0b0f19 !important;
    }
    /* Bắt buộc nút Share và các biểu tượng góc phải có màu trắng sáng rõ */
    header[data-testid="stHeader"] button, header[data-testid="stHeader"] a, header[data-testid="stHeader"] span {
        color: #f1f5f9 !important;
    }
    /* Nền ứng dụng màu vũ trụ sâu thẳm */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%);
        color: #f1f5f9 !important;
    }
    /* Thanh bên trái */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #334155;
    }
    /* Bắt buộc toàn bộ text thường, label, caption phải có màu sáng */
    label, p, span, .stCaption, div[data-testid="stWidgetLabel"] p {
        color: #f1f5f9 !important;
        font-weight: 500;
    }
    /* Đổi màu chữ gợi ý xám nhạt bên dưới */
    .stCaption, small {
        color: #94a3b8 !important;
    }
    /* Các thẻ tiêu đề màu tím tinh vân lung linh */
    h1, h2, h3 {
        color: #c084fc !important; 
        text-shadow: 0 0 10px rgba(192, 132, 252, 0.4);
    }
    /* Khung Expander hướng dẫn */
    .streamlit-expanderHeader {
        background-color: #1e1b4b !important;
        color: #f1f5f9 !important;
        border: 1px solid #4338ca !important;
        border-radius: 8px;
    }
    /* Nút bấm lớn gradient neon */
    div.stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
    }
    /* Định dạng lại khung thông tin kết quả phong thủy */
    .stAlert {
        background-color: #111827 !important;
        border: 1px solid #a855f7 !important;
        color: #f1f5f9 !important;
        border-radius: 10px;
    }
    /* CSS cho nút chia sẻ Facebook */
    .fb-share-btn {
        background-color: #1877f2;
        color: white !important;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(24, 119, 242, 0.3);
    }
    .fb-share-btn:hover {
        background-color: #166fe5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("☯️ Hệ Thống Phong Thủy Bát Trạch")
st.write("---")

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
st.sidebar.success(f"📅 **Sinh ngày:** {ngay_sinh}/{thang_sinh}/{nam_sinh} (Dương lịch)\n\n🌌 **Quái mệnh:** {quai_menh}")

# GIAO DIỆN NHẬP SỐ ĐO LINH HOẠT
st.header("📋 TỌA ĐỘ PHONG THỦY CÁC KHU VỰC")
st.markdown("<span style='color: #a7f3d0;'>✨ **Mẹo linh hoạt:** Bạn chỉ cần nhập số liệu ở khu vực bạn muốn kiểm tra. Mục nào chưa muốn đo, vui lòng bỏ trống (hoặc xóa số), hệ thống sẽ tự bỏ qua danh mục đó!</span>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 🛏️ Khu vực Giường Ngủ")
    with st.expander("📖 Hướng dẫn đo Giường Ngủ"):
        st.info("• **Vị trí đặt (Tọa):** Đứng ở tâm nhà, mở la bàn điện thoại, nhìn về phía giường.\n• **Hướng đầu giường:** Nằm ngửa, đầu điện thoại hướng thẳng áp sát vào thành đầu giường.")
    t_giuong = st.number_input("Tọa độ vị trí đặt giường (°):", min_value=0, max_value=360, value=None, step=1, help="Để trống nếu không muốn kiểm tra mục này")
    st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(t_giuong)}**")
    h_giuong = st.number_input("Số độ hướng đầu giường (°):", min_value=0, max_value=360, value=None, step=1)
    st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(h_giuong)}**")

    st.write("---")
    st.subheader("2. 🍳 Khu vực Bếp Nấu")
    with st.expander("📖 Hướng dẫn đo Bếp Nấu"):
        st.info("• **Vị trí đặt (Tọa):** Đứng ở tâm nhà, mở la bàn xem bếp nằm góc nào.\n• **Hướng Bếp:** Đứng nhìn vào bếp, hướng màn hình điện thoại vào bụng (đuôi điện thoại chỉ vào tường bếp). Hướng la bàn chỉ ra ngoài là Hướng Bếp.")
    t_bep = st.number_input("Tọa độ vị trí đặt bếp (°):", min_value=0, max_value=360, value=None, step=1)
    st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(t_bep)}**")
    h_bep = st.number_input("Số độ Hướng Bếp (°):", min_value=0, max_value=360, value=None, step=1)
    st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(h_bep)}**")

with col2:
    st.subheader("3. 💼 Khu vực Bàn Làm Việc")
    with st.expander("📖 Hướng dẫn đo Bàn Làm Việc"):
        st.info("• **Vị trí đặt (Tọa):** Đứng ở tâm nhà/tâm phòng nhìn về góc đặt bàn.\n• **Hướng ngồi:** Ngồi vào bàn, mắt nhìn thẳng về trước, đầu điện thoại hướng theo mắt nhìn.")
    t_ban = st.number_input("Tọa độ vị trí đặt bàn làm việc (°):", min_value=0, max_value=360, value=None, step=1)
    st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(t_ban)}**")
    h_ban = st.number_input("Số độ hướng ngồi nhìn làm việc (°):", min_value=0, max_value=360, value=None, step=1)
    st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(h_ban)}**")

    st.write("---")
    st.subheader("4. 🚽 Khu vực Nhà Vệ Sinh")
    with st.expander("📖 Hướng dẫn đo Nhà Vệ Sinh"):
        st.info("• **Vị trí đặt (Tọa):** Đứng ở tâm nhà, đo xem cả phòng WC nằm ở góc phương vị nào. Chỉ cần tính vị trí đặt (Tọa), không cần đo hướng cửa.")
    t_wc = st.number_input("Tọa độ vị trí đặt WC (°):", min_value=0, max_value=360, value=None, step=1)
    st.caption(f"➡️ Hướng tương ứng: **{lay_huong_tu_so_do(t_wc)}**")

st.write("---")

# PHẦN HIỂN THỊ KẾT QUẢ THÔNG MINH
if st.button("🔮 BẮT ĐẦU KIỂM TRA PHONG THỦY", use_container_width=True):
    # Kiểm tra xem người dùng có điền ít nhất 1 mục hay không
    if t_giuong is None and t_bep is None and t_ban is None and t_wc is None:
        st.warning("🪐 Vui lòng điền số độ của ít nhất một vị trí bạn muốn kiểm tra ở phía trên.")
    else:
        st.header("📋 KẾT QUẢ LUẬN GIẢI PHONG THỦY")
        
        # Thiết lập danh sách các Tab dựa trên các mục thực tế có dữ liệu
        danh_sach_tabs = []
        if t_giuong is not None: danh_sach_tabs.append("🛏️ GIƯỜNG NGỦ")
        if t_ban is not None: danh_sach_tabs.append("💼 BÀN LÀM VIỆC")
        if t_bep is not None: danh_sach_tabs.append("🍳 BẾP NẤU")
        if t_wc is not None: danh_sach_tabs.append("🚽 NHÀ VỆ SINH")
        
        # Sinh các tab động trên giao diện
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

        # Thêm nút Chia sẻ kết quả lên Facebook ở cuối phần kết quả
        st.write("---")
        app_url = "https://kiemtraphongthuy.streamlit.app"
        encoded_url = urllib.parse.quote(app_url)
        fb_share_link = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"
        
        st.markdown(f'<a href="{fb_share_link}" target="_blank" class="fb-share-btn">🔵 CHIA SẺ KẾT QUẢ TRÊN FACEBOOK</a>', unsafe_allow_html=True)