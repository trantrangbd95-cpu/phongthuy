import streamlit as st
import streamlit_authenticator as stauth

# --- CẤU HÌNH GIAO DIỆN & CSS (CHỮ TO GẤP ĐÔI) ---
st.set_page_config(page_title="Hệ Thống Phong Thủy", layout="wide")
st.markdown("""
    <style>
    .big-font { font-size: 30px !important; font-weight: bold; color: #2E86C1; }
    </style>
    """, unsafe_allow_html=True)

# --- CÁC HÀM XỬ LÝ PHONG THỦY ---
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

def luan_giai_chi_tiet(qs, deg, ten_vat_pham):
    huong = lay_huong(deg)
    dong_tu = [1, 3, 4, 9]
    is_dong_tu = qs in dong_tu
    huong_tot = ["Bắc", "Nam", "Đông", "Đông Nam"] if is_dong_tu else ["Tây", "Tây Bắc", "Tây Nam", "Đông Bắc"]
    
    status = "TỐT" if huong in huong_tot else "XẤU"
    giai_thich = "đón được cát khí, tài lộc hanh thông" if status == "TỐT" else "bị phạm vào hướng sát khí, dễ gây hao tài hoặc ảnh hưởng sức khỏe"
    
    return f"""
    - **{ten_vat_pham}**: Đang quay về hướng **{huong}** $\rightarrow$ **{status}**.
    - *Vì sao?* Gia chủ thuộc {'Đông Tứ Mệnh' if is_dong_tu else 'Tây Tứ Mệnh'}, hướng {huong} {giai_thich}.
    - *Lời khuyên:* {'' if status == 'TỐT' else 'Nên điều chỉnh xoay về hướng: ' + ', '.join(huong_tot)}
    """

# --- GIAO DIỆN CHÍNH ---
st.title("🔮 Luận Giải Phong Thủy Bát Trạch Chuyên Sâu")

# Nhập thông tin
c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
with c1: ngay = st.number_input("Ngày sinh (Dương lịch):", 1, 31, 1)
with c2: thang = st.number_input("Tháng sinh (Dương lịch):", 1, 12, 1)
with c3: nam = st.number_input("Năm sinh (Dương lịch):", 1900, 2026, 1995)
with c4: gioi_tinh = st.selectbox("Giới tính:", ["Nam", "Nữ"])

qs = tinh_quai_so(nam, gioi_tinh)
st.write(f"### Gia chủ mệnh: **{qs}** - {'Đông Tứ Mệnh' if qs in [1,3,4,9] else 'Tây Tứ Mệnh'}")

# --- NHẬP SỐ ĐO & HIỆN HƯỚNG TỰ ĐỘNG ---
st.subheader("📏 Nhập số đo phong thủy")
col1, col2 = st.columns(2)
# Tạo các biến lưu số đo
inputs = {}
for vat_pham in ["Giường ngủ", "Bàn làm việc", "Bếp nấu", "Nhà vệ sinh"]:
    col = col1 if vat_pham in ["Giường ngủ", "Bàn làm việc"] else col2
    with col:
        deg = st.number_input(f"Hướng {vat_pham} (°):", 0, 360, 0, key=vat_pham)
        st.write(f"➡️ Hiện tại là hướng: **{lay_huong(deg)}**")
        inputs[vat_pham] = deg

# --- PHẦN LUẬN GIẢI CHỮ TO ---
if st.button("XEM KẾT QUẢ LUẬN GIẢI CHI TIẾT"):
    st.markdown('<p class="big-font">📋 KẾT QUẢ PHÂN TÍCH</p>', unsafe_allow_html=True)
    for vp, deg in inputs.items():
        st.write(luan_giai_chi_tiet(qs, deg, vp))