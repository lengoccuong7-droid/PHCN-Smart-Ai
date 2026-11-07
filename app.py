# app.py
import streamlit as st
from Core.engine import SuperClinicalEngine
from Core.history_manager import HistoryManager
from Core.kb_builder import get_comprehensive_kb

# Cấu hình giao diện tối ưu cho mobile
st.set_page_config(
    page_title="Siêu App Lý Luận Lâm Sàng & PHCN",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Siêu App Lý Luận Lâm Sàng & PHCN")

# Khởi tạo engine và quản lý lịch sử
engine = SuperClinicalEngine()
history_mgr = HistoryManager()
kb = get_comprehensive_kb()

# ==========================================
# THANH ĐIỀU HƯỚNG TÁCH BIỆT 2 CHỨC NĂNG RIÊNG
# ==========================================
app_mode = st.sidebar.radio(
    "📌 CHỌN MỤC CHỨC NĂNG:",
    [
        "1. Lý luận lâm sàng & Khám bệnh", 
        "2. Thư viện Bài tập Phục Hồi Chức Năng"
    ]
)

# ------------------------------------------
# MỤC 1: LÝ LUẬN LÂM SÀNG & KHÁM BỆNH (Bản chuẩn)
# ------------------------------------------
if app_mode == "1. Lý luận lâm sàng & Khám bệnh":
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

    st.markdown("")
    if st.button("💾 Lưu ca khám & Phân tích chuyên sâu", type="primary"):
        if not patient_name or not patient_phone:
            st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và Số điện thoại/Mã bệnh nhân ở phần trên để lưu hồ sơ hành chính!")
        else:
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
            
            history_mgr.save_visit(patient_phone, exam_data)
            st.success(f"✅ Đã liên kết hành chính và lưu thành công hồ sơ khám cho bệnh nhân **{patient_name}**!")
            
            st.subheader("💡 Gợi ý Hướng xử trí & Phục hồi chức năng:")
            st.info("Dựa trên dữ liệu lâm sàng, tiến hành lên phác đồ tập vận động, giảm đau và lượng giá tầm vận động khớp định kỳ cho các lần tái khám tiếp theo.")

# ------------------------------------------
# MỤC 2: THƯ VIỆN BÀI TẬP PHỤC HỒI CHỨC NĂNG (RIÊNG BIỆT)
# ------------------------------------------
else:
    st.subheader("🏋️‍♂️ Thư viện Bài tập Phục Hồi Chức Năng Chuyên Sâu")
    st.markdown("Chọn chương trình PHCN dưới đây để xem hệ thống các bài tập chuẩn y khoa kèm theo liều lượng cụ thể:")

    rehab_program = st.selectbox("🎯 Chọn chương trình Phục hồi chức năng:", [
        "1. PHCN sau tai biến mạch máu não (Liệt nửa người)",
        "2. PHCN hội chứng cong vẹo cột sống cổ / Cổ vai gáy",
        "3. PHCN cho trẻ bại não (Cerebral Palsy)",
        "4. PHCN sau mổ tái tạo dây chằng chéo trước (ACL)",
        "5. PHCN sau mổ kết hợp xương gãy thân xương đùi",
        "6. PHCN sau mổ gãy xương cổ tay / bàn tay",
        "7. PHCN sau phẫu thuật thay khớp háng toàn phần",
        "8. PHCN cho trẻ chậm nói / Rối loạn phát triển ngôn ngữ"
    ])

    st.markdown("---")

    if "1." in rehab_program:
        st.subheader("🧠 1. Chương trình PHCN sau tai biến mạch máu não")
        st.write("• **Mục tiêu:** Phòng ngừa co cứng, kích hoạt lại vận động bên liệt và phục hồi thăng bằng.")
        st.write("• **Các bài tập cốt lõi:**")
        st.write("  1. Vận động thụ động - chủ động hỗ trợ khớp vai và khuỷu tay bên liệt.")
        st.write("  2. Kỹ thuật ức chế trương lực cơ co cứng cơ gấp cổ tay và ngón tay.")
        st.write("  3. Tập nâng hông (Bridging) ở tư thế nằm ngửa.")
        st.write("  4. Tập thăng bằng ngồi trên ghế không tựa lưng.")
        st.write("  5. Bài tập đứng dồn lực lên chân liệt trước gương.")
        st.write("  6. Huấn luyện lại dáng đi với thanh song song / khung tập đi.")
        st.write("  7. Tập cầm nắm vật dụng sinh hoạt hàng ngày để tái giáo dục chi trên.")

    elif "2." in rehab_program:
        st.subheader("🦴 2. Chương trình PHCN cong vẹo cột sống cổ / Cổ vai gáy")
        st.write("• **Mục tiêu:** Thư giãn nhóm cơ co thắt, mạnh cơ cổ sâu, chỉnh sửa tư thế đầu.")
        st.write("• **Các bài tập cốt lõi:**")
        st.write("  1. Kéo giãn cơ thang trên (Upper Trapezius Stretch).")
        st.write("  2. Kéo giãn cơ nâng vai (Levator Scapulae Stretch).")
        st.write("  3. Kéo cằm ngược (Chin Tuck) mạnh cơ uốn cổ sâu.")
        st.write("  4. Xoay cổ chủ động biên độ nhẹ trong giới hạn không đau.")
        st.write("  5. Tập mạnh cơ duỗi cổ kháng lực đẳng cự nhẹ nhàng.")
        st.write("  6. Vận động khép xương bả vai ra sau (Scapular Retraction).")
        st.write("  7. Nhiệt trị liệu & Siêu âm giãn cơ điểm đau (Trigger points).")

    elif "3." in rehab_program:
        st.subheader("🧸 3. Chương trình PHCN cho trẻ bại não (Cerebral Palsy)")
        st.write("• **Mục tiêu:** Ức chế phản xạ nguyên bản bất thường, tăng cường kiểm soát đầu cổ.")
        st.write("• **Các bài tập cốt lõi:**")
        st.write("  1. Tạo thuận kiểm soát đầu cổ ở tư thế nằm sấp và ngửa.")
        st.write("  2. Tập tư thế nằm sấp chống khuỷu (Prone on elbows).")
        st.write("  3. Tập quỳ bốn điểm và nhún trọng lượng (Quadruped rocking).")
        st.write("  4. Tập phản ứng thăng bằng trên bóng trị liệu lớn (Bobath ball).")
        st.write("  5. Kéo giãn nhẹ nhàng nhóm cơ khép háng và gân kheo.")
        st.write("  6. Hướng dẫn tập đứng với bàn đứng hoặc nẹp trợ giúp AFO.")
        st.write("  7. Trị liệu vận động tinh qua trò chơi nhặt khối gỗ nhỏ.")

    elif "4." in rehab_program:
        st.subheader("🦵 4. Chương trình PHCN sau mổ tái tạo dây chằng chéo trước (ACL)")
        st.write("• **Mục tiêu:** Lấy lại biên độ duỗi thẳng hoàn toàn, phục hồi cơ tứ đầu đùi.")
        st.write("• **Các bài tập cốt lõi:**")
        st.write("  1. Duỗi gối thụ động tối đa (Passive Knee Extension).")
        st.write("  2. Gồng cơ tứ đầu đùi tĩnh (Isometric Quad Sets).")
        st.write("  3. Nâng chân thẳng ở tư thế nằm ngửa (Straight Leg Raise).")
        st.write("  4. Gập gối gót chạm mông chủ động trợ giúp.")
        st.write("  5. Đạp xe đạp tĩnh điện không kháng lực (Tuần 4-6).")
        st.write("  6. Ngồi xổm một phần (Mini Squats) biên độ 0-45 độ.")
        st.write("  7. Tập thăng bằng cảm giác bản thể trên đệm hơi.")

    elif "5." in rehab_program:
        st.subheader("🦴 5. Chương trình PHCN sau mổ kết hợp xương gãy thân xương đùi")
        st.write("• **Mục tiêu:** Ngăn ngừa teo cơ, chống huyết khối tĩnh mạch, hồi phục chức năng gối.")
        st.write("• **Các bài tập cốt lõi:**")
        st.write("  1. Bơm máu gập duỗi cổ chân liên tục phòng chống huyết khối.")
        st.write("  2. Gồng cơ mông và cơ đùi tĩnh (Glute & Quad Sets).")
        st.write("  3. Trượt gót chân trên giường (Heel Slides).")
        st.write("  4. Nâng chân thẳng có trợ giúp.")
        st.write("  5. Ngồi thõng chân mép giường đung đưa nhẹ nhàng.")
        st.write("  6. Tập đứng chịu lực một phần với khung tập đi.")
        st.write("  7. Tập bước đi lên xuống bậc thang thấp (Giai đoạn liền xương).")

    elif "6." in rehab_program:
        st.subheader("✋ 6. Chương trình PHCN sau mổ gãy xương cổ tay / bàn tay")
        st.write("• **Mục tiêu:** Chống phù nề, chống xơ hóa gân, lấy lại tầm vận động và lực nắm.")
        st.write("• **Các bài tập cốt lõi:**")
        st.write("  1. Kê cao tay kết hợp nắm - xòe các ngón tay giảm sưng.")
        st.write("  2. Vận động thụ động nhẹ nhàng khớp cổ tay gấp/duỗi.")
        st.write("  3. Vận động chủ động nghiêng quay / nghiêng trụ cổ tay.")
        st.write("  4. Tập mạnh cơ ngửa và sấp cẳng tay với kháng lực nhẹ.")
        st.write("  5. Bóp bóng cao su mềm tăng lực cơ bàn tay.")
        st.write("  6. Bài tập phối hợp đối chiếu ngón cái với các ngón.")
        st.write("  7. Siêu âm trị liệu chống dính sẹo mổ vùng cổ tay.")

    elif "7." in rehab_program:
        st.subheader("🦴 7. Chương trình PHCN sau phẫu thuật thay khớp háng toàn phần")
        st.write("• **Mục tiêu:** Bảo vệ khớp nhân tạo, phục hồi cơ mông, hướng dẫn sinh hoạt an toàn.")
        st.write("• **Các bài tập cốt lõi:**")
        st.write("  1. Bơm máu bàn chân phòng ngừa huyết khối tĩnh mạch.")
        st.write("  2. Ép mông tĩnh ở tư thế nằm ngửa (Gluteal Squeezes).")
        st.write("  3. Dạng chân trượt sang ngang trên mặt giường an toàn.")
        st.write("  4. Trượt gót chân gập háng nhẹ (Không vượt quá 90 độ).")
        st.write("  5. Nâng chân thẳng ở tư thế nằm ngửa.")
        st.write("  6. Tập đứng thẳng dồn lực đều hai chân với khung tập đi.")
        st.write("  7. Hướng dẫn tư thế an toàn (Không bắt chéo chân, không ngồi xổm).")

    elif "8." in rehab_program:
        st.subheader("🗣️ 8. Chương trình PHCN cho trẻ chậm nói / Rối loạn ngôn ngữ")
        st.write("• **Mục tiêu:** Kích thích cơ quan phát âm, mở rộng vốn từ vựng tiếp nhận.")
        st.write("• **Các bài tập cốt lõi:**")
        st.write("  1. Massage kích thích cơ vùng miệng - môi - má.")
        st.write("  2. Tập thổi hơi có mục đích (Thổi bóng bông, thổi còi, thổi nến).")
        st.write("  3. Giao tiếp mắt 1 kèm 1 với Flashcard hình ảnh sinh động.")
        st.write("  4. Bắt chước âm thanh động vật và tiếng kêu gần gũi.")
        st.write("  5. Đọc to rõ ràng các từ đơn tiết kèm đồ vật thực tế.")
        st.write("  6. Hát bài hát thiếu nhi có động tác minh họa.")
        st.write("  7. Hướng dẫn phụ huynh tương tác giao tiếp mở rộng tại nhà.")
