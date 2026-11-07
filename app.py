import streamlit as st
from Core.engine import SuperClinicalEngine
from app_helpers import apply_custom_css

st.set_page_config(page_title="Phục Hồi Chức Năng Và Vật Lý Trị Liệu AI", layout="wide")
apply_custom_css()

engine = SuperClinicalEngine()

# Khởi tạo trạng thái điều hướng màn hình
if 'nav_page' not in st.session_state:
    st.session_state['nav_page'] = 'home'
if 'selected_zone' not in st.session_state:
    st.session_state['selected_zone'] = 'Tổng quát'

# ==================== GIAO DIỆN 1: TRANG CHỦ ====================
if st.session_state['nav_page'] == 'home':
    st.title("🏥 PHỤC HỒI CHỨC NĂNG VÀ VẬT LÝ TRỊ LIỆU")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📁 HỒ SƠ BỆNH NHÂN", use_container_width=True):
            st.info("Quản lý hồ sơ bệnh nhân.")
    with col2:
        if st.button("📜 LỊCH SỬ KHÁM\n(Xem và theo dõi)", use_container_width=True):
            st.info("Tính năng lịch sử lưu trữ thủ công theo yêu cầu.")
    with col3:
        if st.button("⚙️ CÀI ĐẶT HỆ THỐNG", use_container_width=True):
            st.warning("Cấu hình hệ thống.")

    st.markdown("---")
    st.markdown("### 🚀 TRUY CẬP NHANH CHỨC NĂNG")
    
    if st.button("🩺 BẮT ĐẦU PHÍM CHỨC NĂNG KHÁM LÂM SÀNG", use_container_width=True, type="primary"):
        st.session_state['nav_page'] = 'exam_menu'
        st.rerun()

# ==================== GIAO DIỆN 2: CHỌN VÙNG KHÁM (GRID MENU) ====================
elif st.session_state['nav_page'] == 'exam_menu':
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("🏠 TRANG CHỦ"):
            st.session_state['nav_page'] = 'home'
            st.rerun()
    with col_title:
        st.title("🩺 VẬT LÝ TRỊ LIỆU AI - CHỌN VÙNG GIẢI PHẪU KHÁM")

    st.markdown("---")
    
    zones = [
        ("Cột sống cổ", "Cervical Spine"),
        ("Cột sống lưng", "Lumbar Spine"),
        ("Khớp vai", "Shoulder Joint"),
        ("Khớp khuỷu", "Elbow Joint"),
        ("Khớp cổ - bàn tay", "Wrist & Hand"),
        ("Khớp hông", "Hip Joint"),
        ("Khớp gối", "Knee Joint"),
        ("Khớp cổ - bàn chân", "Ankle & Foot")
    ]

    cols = st.columns(3)
    for i, (zone_name, zone_desc) in enumerate(zones):
        with cols[i % 3]:
            if st.button(f"📌 {zone_name.upper()}\n\n{zone_desc}", use_container_width=True):
                st.session_state['selected_zone'] = zone_name
                st.session_state['nav_page'] = 'exam_form'
                st.rerun()

# ==================== MÀN HÌNH NHẬP LIỆU KHÁM LÂM SÀNG CHI TIẾT ====================
elif st.session_state['nav_page'] == 'exam_form':
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("🔙 CHỌN VÙNG KHÁM"):
            st.session_state['nav_page'] = 'exam_menu'
            st.rerun()
    with col_title:
        st.title(f"🏥 KHÁM LÂM SÀNG & PHÂN TÍCH: {st.session_state['selected_zone'].upper()}")

    st.markdown("---")

    # Form nhập liệu cuộn gọn gàng
    with st.container(height=480):
        ly_do_vao_vien = st.text_input("1. Lý do vào viện", placeholder="Nhập lý do vào viện...")
        tien_su = st.text_area("2. Tiền sử bệnh", placeholder="Nhập tiền sử bệnh lý...")
        
        st.markdown("---")
        st.markdown("**3. Bệnh sử (Bộ câu hỏi SOCRATES)**")
        socrates_onset = st.text_input("- Khởi phát (Onset):", placeholder="Đột ngột hay từ từ...")
        socrates_site = st.text_input("- Vị trí (Site):", placeholder="Vị trí đau chính...")
        socrates_character = st.text_input("- Tính chất đau (Character):", placeholder="Nhói, âm ỉ, buốt, mỏi...")
        socrates_progression = st.text_input("- Diễn biến (Progression):", placeholder="Tăng dần, ổn định...")
        socrates_factors = st.text_input("- Yếu tố tăng/giảm (Factors):", placeholder="Tư thế làm tăng/giảm đau...")
        socrates_severity = st.text_input("- Ảnh hưởng sinh hoạt (Severity):", placeholder="Mức độ tác động sinh hoạt...")
        
        st.markdown("---")
        red_flags = st.multiselect(
            "4. Cờ đỏ (Red Flags)", 
            ["Sốt kèm đau khớp", "Yếu liệt chi", "Tê rát lan tỏa / Tê vùng yên ngựa", "Đau dữ dội không đáp ứng nghỉ ngơi", "Sụt cân không rõ nguyên nhân"]
        )
        
        st.markdown("---")
        st.markdown("**5. Khám lâm sàng thực thể**")
        lam_sang_nhin = st.text_input("- Nhìn:", placeholder="Đánh giá tư thế, biến dạng, sưng tấy...")
        lam_sang_so = st.text_input("- Sờ:", placeholder="Điểm đau chói, u cục, nhiệt độ da...")
        lam_sang_go = st.text_input("- Gõ:", placeholder="Phản xạ gân xương, gõ dồn dọc trục...")
        
        st.markdown("---")
        st.markdown("**6. Test đặc hiệu chính**")
        test_1 = st.text_input("- Test 1:", placeholder="Nhập kết quả Test 1...")
        st.caption("*(Lachman / Đánh giá độ vững dây chằng chéo trước)*")
        
        test_2 = st.text_input("- Test 2:", placeholder="Nhập kết quả Test 2...")
        st.caption("*(McMurray / Kiểm tra tổn thương sụn chêm)*")
        
        test_3 = st.text_input("- Test 3:", placeholder="Nhập kết quả Test 3...")
        st.caption("*(Apley / Phân biệt sụn chêm và dây chằng)*")
        
        st.markdown("---")
        image_notes = st.file_uploader("7. Lưu hình ảnh (X-Ray / MRI)", type=["jpg", "png", "jpeg"])

    # Gom dữ liệu form
    form_data = {
        "selected_zone": st.session_state['selected_zone'],
        "ly_do_vao_vien": ly_do_vao_vien,
        "tien_su": tien_su,
        "socrates_onset": socrates_onset,
        "socrates_site": socrates_site,
        "socrates_character": socrates_character,
        "socrates_progression": socrates_progression,
        "socrates_factors": socrates_factors,
        "socrates_severity": socrates_severity,
        "red_flags": ", ".join(red_flags),
        "lam_sang_nhin": lam_sang_nhin,
        "lam_sang_so": lam_sang_so,
        "lam_sang_go": lam_sang_go,
        "test_1": test_1,
        "test_2": test_2,
        "test_3": test_3,
        "image_notes": image_notes.name if image_notes else "Không có tệp"
    }

    # --- VÙNG CỐ ĐỊNH PHÍA DƯỚI (FIXED BOTTOM PANEL) ---
    st.markdown("---")
    st.header("📌 Bảng Điều khiển & Kết quả Phân tích AI")

    box_copy_text = engine.generate_box_copy(form_data)
    st.text_area("📋 Box Copy Tổng Hợp (Dữ liệu thô lâm sàng)", value=box_copy_text, height=120)

    if st.button("🚀 ĐƯA RA PHÂN TÍCH CHẨN ĐOÁN & PHCN", use_container_width=True):
        res = engine.parse_and_analyze(box_copy_text)
        st.session_state['analysis_res'] = res

    if 'analysis_res' in st.session_state:
        res = st.session_state['analysis_res']
        st.success(f"**Chẩn đoán ưu tiên:** {res['primary_diagnosis']} (Độ tin cậy: {res['confidence']})")
        st.text_area("📋 Ô kết quả AI chuẩn hóa:", value=res['ai_copy_output'], height=90)
        
        st.markdown("#### 🛠️ Thao Tác Nhanh (3 Nút Chức Năng):")
        col_n1, col_n2, col_n3 = st.columns(3)
        
        with col_n1:
            if st.button("📋 Nút Copy", use_container_width=True, help="Sao chép toàn bộ kết quả bệnh án"):
                st.toast("Đã sao chép nội dung vào bộ nhớ tạm!", icon="✅")
                
        with col_n2:
            if st.button("🤖 Nút ChatGPT", use_container_width=True, help="Chuyển định dạng sang ChatGPT để tối ưu câu lệnh"):
                st.markdown("[🔗 Mở ChatGPT để đối chiếu](https://chatgpt.com)", unsafe_allow_html=True)
                
        with col_n3:
            if st.button("✨ Nút Gemini", use_container_width=True, help="Đối chiếu chuyên sâu cùng Google Gemini"):
                st.markdown("[🔗 Mở Gemini Workspace](https://gemini.google.com)", unsafe_allow_html=True)
