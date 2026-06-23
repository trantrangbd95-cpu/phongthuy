import streamlit as st

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
    huong_vi_tri = lay_huong_tu_so_do(so_do_vi_tri)
    tinh_chat_vi_tri = kiem_tra_tinh_chat_huong(quai_so, huong_vi_tri)
    huong_nhin = lay_huong_tu_so_do(so_do_huong_nhin) if so_do_huong_nhin is not None else None
    tinh_chat_huong_nhin = kiem_tra_tinh_chat_huong(quai_so, huong_nhin) if huong_nhin else None
    
    ket_qua = f"📍 **Vị trí đặt (Tọa):** phương **{huong_vi_tri}** ({so_do_vi_tri}°) $\rightarrow$ Thuộc vùng **{tinh_chat_vi_tri}** \n"
    if huong_nhin:
        ket_qua += f"👀 **Hướng nhìn (Hướng):** quay về **{huong_nhin}** ({so_do_huong_nhin}°) $\rightarrow$ Thuộc vùng **{tinh_chat_huong_nhin}** \n\n"
    else:
        ket_qua += "\n"

    if vat_pham == "giuong_ngu":
        if tinh_chat_vi_tri == "TỐT (CÁT)" and tinh_chat_huong_nhin == "TỐT (CÁT)":
            return ket_qua + "🟢 **ĐÁNH GIÁ - RẤT TỐT:** Giường nằm ở cung tốt và đầu giường nhìn về hướng tốt. Giúp ngủ ngon, phục hồi sức khỏe, gia tăng vượng khí."
        elif tinh_chat_vi_tri == "TỐT (CÁT)" or tinh_chat_huong_nhin == "TỐT (CÁT)":
            return ket_qua + "🟡 **ĐÁNH GIÁ - TẠM ĐƯỢC:** Đạt được Tọa tốt hoặc Hướng tốt. Có thể tối ưu thêm bằng cách dịch chuyển nhẹ hoặc xoay lại hướng đầu giường."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Cả vị trí đặt và hướng đầu giường đều nằm vào cung xấu. Dễ gây mất ngủ, mệt mỏi, tinh thần bất an."

    elif vat_pham == "ban_lam_viec":
        if tinh_chat_vi_tri == "TỐT (CÁT)" and tinh_chat_huong_nhin == "TỐT (CÁT)":
            return ket_qua + "🟢 **ĐÁNH GIÁ - RẤT TỐT:** Vị trí ngồi vững chãi ở cung tốt, mắt nhìn về hướng cát lành. Giúp tinh thần minh mẫn, công việc hanh thông, dễ thăng tiến."
        elif tinh_chat_huong_nhin == "TỐT (CÁT)":
            return ket_qua + "🟡 **ĐÁNH GIÁ - ỔN:** Hướng nhìn đón được cát khí tốt, dù vị trí đặt bàn chưa nằm ở cung tối ưu."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Hướng ngồi nhìn thẳng vào vùng năng lượng xấu. Dễ gặp áp lực, khó tập trung, công việc trì trệ."

    elif vat_pham == "bep":
        if tinh_chat_vi_tri == "XẤU (HUNG)" and tinh_chat_huong_nhin == "TỐT (CÁT)":
            return ket_qua + "🟢 **ĐÁNH GIÁ - TUYỆT VỜI:** Đúng chuẩn quy tắc **'Tọa Hung Hướng Cát'**. Bếp đặt ở cung xấu để thiêu đốt điềm rủi và mặt bếp quay về hướng tốt để đón tài lộc."
        elif tinh_chat_vi_tri == "TỐT (CÁT)" and tinh_chat_huong_nhin == "TỐT (CÁT)":
            return ket_qua + "🟡 **ĐÁNH GIÁ - CHƯA CHUẨN:** Mặt bếp nhìn về hướng tốt nhưng vị trí đặt bếp lại đè lên cung tốt (vô tình thiêu đốt đi may mắn của cung đó). Nên dịch vị trí đặt cụm bếp sang góc khác."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Bếp đặt sai phong thủy, quay mặt về hướng xấu, dễ làm thất thoát tài lộc hoặc ảnh hưởng sức khỏe lửa ấm gia đình."

    elif vat_pham == "nha_ve_sinh":
        if tinh_chat_vi_tri == "XẤU (HUNG)":
            return ket_qua + "🟢 **ĐÁNH GIÁ - RẤT TỐT:** Đúng chuẩn phong thủy **'Tọa Hung'**. Nhà vệ sinh đặt tại cung xấu giúp trấn áp, xả trôi các năng lượng tiêu cực và uế khí trong nhà."
        else:
            return ket_qua + "🔴 **ĐÁNH GIÁ - XẤU:** Nhà vệ sinh đang đặt đè lên cung tốt của gia chủ, làm suy giảm nghiêm trọng vượng khí, may mắn và tài lộc."

# --- THIẾT KẾ GIAO DIỆN WEBSITE ---
st.set_page_config(page_title="Phong Thủy Bát Trạch Cát Tường", page_icon="☯️", layout="wide")

st.title("☯️ Hệ Thống Kiểm Tra Phong Thủy Nhà Ở Tự Động")
st.caption("Trường phái Bát Trạch Minh Cảnh - Tối ưu hóa 4 khu vực cốt lõi trong gia đình")
st.write("---")

# THANH BÊN: THÔNG TIN GIA CHỦ
st.sidebar.header("👤 THÔNG TIN GIA CHỦ")
col_d, col_m = st.sidebar.columns(2)
with col_d:
    ngay_sinh = st.number_input("Ngày sinh (Dương lịch):", min_value=1, max_value=31, value=1, step=1)
with col_m:
    thang_sinh = st.number_input("Tháng sinh (Dương lịch):", min_value=1, max_value=12, value=1, step=1)

nam_sinh = st.sidebar.number_input("Năm sinh (Dương lịch):", min_value=1950, max_value=2026, value=1995, step=1)
gioi_tinh = st.sidebar.selectbox("Giới tính Mệnh:", ["Nam", "Nữ"])

q_so = tinh_quai_so(nam_sinh, gioi_tinh)
quai_menh = lay_ten_quai_menh(q_so)
st.sidebar.success(f"📅 **Sinh ngày:** {ngay_sinh}/{thang_sinh}/{nam_sinh} (Dương lịch)\n\n🔹 **Cung mệnh:** {quai_menh}")

# GIAO DIỆN NHẬP SỐ ĐO
st.header("📋 NHẬP SỐ ĐO LA BÀN TẠI CÁC VỊ TRÍ")
st.markdown("> **Mẹo:** Khi bạn nhập số độ, hệ thống sẽ tự động hiển thị hướng chữ (Bắc, Đông, Tây, Nam...) ngay bên cạnh để bạn kiểm tra dễ dàng.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 🛏️ Khu vực Giường Ngủ")
    with st.expander("📖 Hướng dẫn đo Giường Ngủ (Bấm để xem)"):
        st.info("• **Vị trí đặt (Tọa):** Đứng ở vị trí tâm nhà, mở ứng dụng la bàn điện thoại lên, nhìn thẳng về hướng chiếc giường để lấy số độ.\n\n• **Hướng đầu giường:** Nằm ngửa trên giường, **đỉnh đầu quay về phía nào thì đó là hướng giường**. Hãy đặt điện thoại nằm ngửa, hướng đầu điện thoại chỉ thẳng vào thành đầu giường để đo số độ.")
    t_giuong = st.number_input(f"Tọa độ vị trí đặt giường (°) - Hiện tại: {lay_huong_tu_so_do(0)}", 0, 360, 0, key="tg")
    st.caption(f"➡️ Hướng la bàn tương ứng: **{lay_huong_tu_so_do(t_giuong)}**")
    h_giuong = st.number_input(f"Số độ hướng đầu giường (°) - Hiện tại: {lay_huong_tu_so_do(0)}", 0, 360, 0, key="hg")
    st.caption(f"➡️ Hướng la bàn tương ứng: **{lay_huong_tu_so_do(h_giuong)}**")

    st.write("---")
    st.subheader("2. 🍳 Khu vực Bếp Nấu")
    with st.expander("📖 Hướng dẫn đo Bếp Nấu (CHUẨN XÁC)"):
        st.info("• **Vị trí đặt (Tọa):** Đứng ở vị trí tâm nhà, mở ứng dụng la bàn lên xem cụm bếp đang nằm ở góc nào trong nhà.\n\n• **Hướng Bếp:** Chính là hướng **sau lưng của người nấu** khi đứng nấu ăn. \n\n*Cách đo dễ nhất:* Bạn đứng đối diện bếp (mặt nhìn vào tường). Bật la bàn điện thoại lên, **hướng màn hình điện thoại thẳng vào bụng bạn** (đuôi điện thoại hướng vào tường, đầu điện thoại hướng thẳng ra ngoài phòng khách). Số độ hiển thị lúc này chính là Hướng Bếp.")
    t_bep = st.number_input(f"Tọa độ vị trí đặt bếp (°) - Hiện tại: {lay_huong_tu_so_do(0)}", 0, 360, 0, key="tb")
    st.caption(f"➡️ Hướng la bàn tương ứng: **{lay_huong_tu_so_do(t_bep)}**")
    h_bep = st.number_input(f"Số độ Hướng Bếp (°) - Hiện tại: {lay_huong_tu_so_do(0)}", 0, 360, 0, key="hb")
    st.caption(f"➡️ Hướng la bàn tương ứng: **{lay_huong_tu_so_do(h_bep)}**")

with col2:
    st.subheader("3. 💼 Khu vực Bàn Làm Việc")
    with st.expander("📖 Hướng dẫn đo Bàn Làm Việc (Bấm để xem)"):
        st.info("• **Vị trí đặt (Tọa):** Đứng ở tâm phòng hoặc tâm nhà để xem góc đặt bàn làm việc.\n\n• **Hướng ngồi làm việc:** Khi bạn ngồi ngay ngắn vào ghế làm việc, **hướng mắt bạn nhìn thẳng về phía trước** chính là Hướng của bàn làm việc.")
    t_ban = st.number_input(f"Tọa độ vị trí đặt bàn (°) - Hiện tại: {lay_huong_tu_so_do(0)}", 0, 360, 0, key="tb_ban")
    st.caption(f"➡️ Hướng la bàn tương ứng: **{lay_huong_tu_so_do(t_ban)}**")
    h_ban = st.number_input(f"Số độ hướng ngồi nhìn (°) - Hiện tại: {lay_huong_tu_so_do(0)}", 0, 360, 0, key="hb_ban")
    st.caption(f"➡️ Hướng la bàn tương ứng: **{lay_huong_tu_so_do(h_ban)}**")

    st.write("---")
    st.subheader("4. 🚽 Khu vực Nhà Vệ Sinh")
    with st.expander("📖 Hướng dẫn đo Nhà Vệ Sinh (Bấm để xem)"):
        st.info("• **Vị trí đặt (Tọa):** Đứng ở vị trí tâm nhà, đo xem cả phòng WC đang nằm ở góc nào trong nhà.\n\n• **Lưu ý quan trọng:** Nhà vệ sinh là nơi xả uế khí nên phong thủy chỉ tính vị trí đặt đè lên cung nào để trấn uế. Do đó, **HOÀN TOÀN KHÔNG CẦN QUAY LA BÀN VỀ CỬA WC** (hướng cửa bước ra bước vào không có giá trị tính toán). Bạn chỉ cần nhập đúng tọa độ vị trí đặt phòng WC là đủ.")
    t_wc = st.number_input(f"Tọa độ vị trí đặt WC (°) - Hiện tại: {lay_huong_tu_so_do(0)}", 0, 360, 0, key="twc")
    st.caption(f"➡️ Hướng la bàn tương ứng: **{lay_huong_tu_so_do(t_wc)}**")

st.write("---")

# PHẦN HIỂN THỊ KẾT QUẢ ĐÃ ĐƯỢC PHÂN TÁCH RÕ RÀNG
if st.button("🔮 BẮT ĐẦU ĐÁNH GIÁ PHONG THỦY CHI TIẾT", use_container_width=True):
    st.header("📋 KẾT QUẢ PHÂN TÍCH PHONG THỦY")
    
    # Tạo 4 Tab riêng biệt để người dùng không bị rối mắt
    tab1, tab2, tab3, tab4 = st.tabs(["🛏️ GIƯỜNG NGỦ", "💼 BÀN LÀM VIỆC", "🍳 BẾP NẤU", "🚽 NHÀ VỆ SINH"])
    
    with tab1:
        st.markdown("### 🛏️ Kết quả Phong Thủy: Giường Ngủ")
        st.info(kiem_tra_phong_thuy_chi_tiet(q_so, "giuong_ngu", t_giuong, h_giuong))
        
    with tab2:
        st.markdown("### 💼 Kết quả Phong Thủy: Bàn Làm Việc")
        st.info(kiem_tra_phong_thuy_chi_tiet(q_so, "ban_lam_viec", t_ban, h_ban))
        
    with tab3:
        st.markdown("### 🍳 Kết quả Phong Thủy: Bếp Nấu")
        st.info(kiem_tra_phong_thuy_chi_tiet(q_so, "bep", t_bep, h_bep))
        
    with tab4:
        st.markdown("### 🚽 Kết quả Phong Thủy: Nhà Vệ Sinh")
        st.info(kiem_tra_phong_thuy_chi_tiet(q_so, "nha_ve_sinh", t_wc))