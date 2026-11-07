# app.py
import streamlit as st
from Core.engine import SuperClinicalEngine
from Core.history_manager import HistoryManager
from Core.kb_builder import get_comprehensive_kb

# Cấu hình giao diện tối ưu cho mobile
st.set_page_config(
    page_title="Siêu App Lý Luận Lâm Sàng PHCN",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Siêu App Lý Luận Lâm Sàng PHCN & VLTL")

# Khởi tạo engine và quản lý lịch sử
engine = SuperClinicalEngine()
history_mgr = HistoryManager()
kb = get_comprehensive_kb()

# ==========================================
# 1. PHẦN HÀNH CHÍNH & KẾT NỐI LỊCH SỬ
# ==========================================
st.subheader("📋 1. Thông tin Hành chính & Bệnh nhân")

col1, col2 = st.columns(2)
with col1:
    patient_name = st.text_input("Họ và tên bệnh nhân:", key="input_name")
with col2:
    patient_phone = st.text_input("Số điện thoại / Mã BN:", key="input_phone")

patient_age = st.number_input("Tuổi:", min_value=1, max_value=120, value=30, key="input_age")

# Kiểm tra nếu đã nhập số điện thoại thì hiện lịch sử tái khám cũ
if patient_phone:
    past_visits = history_mgr.get_patient_history(patient_phone)
    if past_visits:
        st.info(f"📁 Tìm thấy {len(past_visits)} lần khám trước đây của bệnh nhân này.")
        with st.expander("📂 Xem lịch sử các lần khám và tái khám cũ"):
            for idx, visit in enumerate(past_visits):
                st.write(f"**Lần {idx+1} - Ngày:** {visit.get('date', 'N/A')}")
                st.write(f"• **Chẩn đoán:** {visit.get('pathology', 'N/A')}")
                st.write(f"• **Ghi chú:** {visit.get('summary', 'Không có dữ liệu')}")
                st.write("")

# ==========================================
# 2. PHẦN KHÁM LÂM SÀNG & BÀI TEST (HIỂN THỊ LIÊN TỤC)
# ==========================================
st.subheader("🔍 2. Đánh giá Lâm sàng & Bài Test")

# Chọn vùng cơ thể tổn thương
region = st.selectbox("Chọn vùng cơ thể / Khớp tổn thương:", list(kb.keys()), key="select_region")

selected_tests = []
pathology = ""
ly_do_vao_vien = ""

if region:
    specific_pathologies = list(kb[region].keys())
    pathology = st.selectbox("Chọn bệnh lý nghi ngờ:", specific_pathologies, key="select_pathology")
    
    if pathology:
        pathology_data = kb[region][pathology]
        
        st.markdown(f"**📌 Triệu chứng đặc trưng của {pathology}:**")
        for sym in pathology_data.get("symptoms", []):
            st.write(f"• {sym}")
            
        st.markdown(f"**🧪 Các bài Test lâm sàng đặc hiệu:**")
        for test in pathology_data.get("special_tests", []):
            if st.checkbox(f"Thực hiện: {test}", key=f"test_{test}"):
                selected_tests.append(test)

ly_do_vao_vien = st.text_area("✍️ Lý do vào viện / Ghi chú triệu chứng thực tế:", key="input_reason")

# ==========================================
# 3. LƯU HỒ SƠ & PHÂN TÍCH TÁI KHÁM
# ==========================================
st.markdown("")
if st.button("💾 Lưu ca khám & Phân tích chuyên sâu", type="primary"):
    if not patient_name or not patient_phone:
        st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và Số điện thoại/Mã bệnh nhân ở phần trên để lưu hồ sơ hành chính!")
    else:
        # Tổng hợp dữ liệu ca khám cho lần này
        exam_summary = f"Vùng: {region} | Bệnh lý: {pathology} | Test dương tính: {len(selected_tests)} bài"
        exam_data = {
            "patient_name": patient_name,
            "patient_age": patient_age,
            "patient_phone": patient_phone,
            "region": region,
            "pathology": pathology,
            "ly_do_vao_vien": ly_do_vao_vien,
            "selected_tests": selected_tests,
            "summary": exam_summary
        }
        
        # Lưu vào hệ thống lịch sử (hỗ trợ lưu vết tái khám)
        history_mgr.save_visit(patient_phone, exam_data)
        st.success(f"✅ Đã liên kết hành chính và lưu thành công hồ sơ khám cho bệnh nhân **{patient_name}**!")
        
        # Hiển thị định hướng phục hồi
        st.subheader("💡 Gợi ý Hướng xử trí & Phục hồi chức năng:")
        st.info("Dựa trên dữ liệu lâm sàng, tiến hành lên phác đồ tập vận động, giảm đau và lượng giá tầm vận động khớp định kỳ cho các lần tái khám tiếp theo.")
