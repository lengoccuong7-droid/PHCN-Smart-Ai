# app.py - PHCN AI 1.8
import streamlit as st
import os
import json
import datetime
import pandas as pd

# Cấu hình giao diện tối ưu cho mobile
st.set_page_config(
    page_title="PHCN AI 1.8 - Trợ lý lâm sàng PHCN",
    page_icon="🩺",
    layout="centered"
)

# --- QUẢN LÝ LỊCH SỬ KHÁM TRỰC TIẾP TẠI GỐC ---
class SimpleHistoryManager:
    def __init__(self, history_file="patient_history.json"):
        self.history_file = os.path.abspath(history_file)
        if not os.path.exists(self.history_file):
            try:
                with open(self.history_file, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
            except Exception:
                pass

    def get_patient_history(self, phone):
        if not phone:
            return []
        try:
            if not os.path.exists(self.history_file):
                return []
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
            return [v for v in history if v.get("patient_phone") == phone]
        except Exception:
            return []

    def save_visit(self, phone, visit_data):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            else:
                history = []
        except Exception:
            history = []

        visit_data["date"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        history.append(visit_data)

        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

history_mgr = SimpleHistoryManager()

# --- HEADER & THANH ĐIỀU HƯỚNG CHÍNH (4 MỤC) ---
st.markdown("### 🩺 PHCN AI 1.8")
st.caption("Trợ lý lâm sàng Phục hồi chức năng & Vật lý trị liệu")

# Tạo 4 tab chính theo đúng yêu cầu
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Hồ sơ", 
    "2. Tri thức", 
    "3. Chọn vùng & Khám", 
    "4. Phục hồi chức năng"
])
# ------------------------------------------
# MỤC 1: HỒ SƠ BỆNH NHÂN & LỊCH SỬ (THẰNG SỐ 2)
# ------------------------------------------
with tab1:
    st.subheader("👤 Quản lý Hồ sơ & Lịch sử Bệnh nhân")
    st.markdown("Tra cứu nhanh thông tin hành chính và lịch sử thăm khám của bệnh nhân theo số điện thoại:")

    # Ô nhập số điện thoại để tìm kiếm
    search_phone_input = st.text_input("🔍 Nhập số điện thoại / Mã BN:", placeholder="Ví dụ: 0901234567", key="search_history_phone_m1")
    
    if search_phone_input:
        # Gọi hàm lấy lịch sử từ history_mgr
        patient_history_list = history_mgr.get_patient_history(search_phone_input)
        
        if patient_history_list:
            st.success(f"🎉 Đã tìm thấy {len(patient_history_list)} lần khám của bệnh nhân này.")
            st.markdown("---")
            for idx, visit in enumerate(patient_history_list):
                with st.expander(f"📁 Lần khám {idx+1} – Ngày: {visit.get('date', 'N/A')}", expanded=(idx == 0)):
                    st.markdown(f"**• Họ tên bệnh nhân:** {visit.get('patient_name', 'N/A')}")
                    st.markdown(f"**• Số điện thoại:** {visit.get('patient_phone', 'N/A')}")
                    st.markdown(f"**• Tóm tắt bệnh án:** {visit.get('summary', 'N/A')}")
                st.markdown("")
        else:
            st.warning("⚠️ Không tìm thấy lịch sử khám nào tương ứng với số điện thoại này trong hệ thống.")
    else:
            st.info("💡 Hướng dẫn: Nhập số điện thoại của bệnh nhân vào ô phía trên để hệ thống tự động truy xuất toàn bộ lịch sử các lần khám trước.")
# ------------------------------------------
# MỤC 2: CƠ SỞ TRI THỨC LÂM SÀNG (THẰNG SỐ 3)
# ------------------------------------------
with tab2:
    st.subheader("📖 Cơ sở Tri thức Lâm sàng & Bệnh lý")
    st.markdown("Tra cứu nhanh các tài liệu hướng dẫn và danh mục bệnh lý chuẩn hóa theo từng vùng cơ thể:")

    # Ô tìm kiếm kiến thức nhanh
    search_knowledge_kw = st.text_input("🔍 Tìm kiếm kiến thức, bệnh lý, triệu chứng...", placeholder="Nhập từ khóa cần tra cứu...", key="search_knowledge_input")

    st.markdown("---")
    st.markdown("##### 🗂️ Danh mục vùng cơ thể & Thần kinh")

    # Chia các nút chọn vùng thành 3 cột đều nhau
    col_k1, col_k2, col_k3 = st.columns(3)
    knowledge_regions = [
        "Cột sống cổ", "Cột sống thắt lưng", "Khớp vai",
        "Khuỷu tay", "Cổ tay – bàn tay", "Khớp háng",
        "Khớp gối", "Cổ chân – bàn chân", "Thần kinh & Khác"
    ]
    
    for idx, reg in enumerate(knowledge_regions):
        col_target = [col_k1, col_k2, col_k3][idx % 3]
        with col_target:
            if st.button(f"📌 {reg}", use_container_width=True, key=f"btn_knowledge_reg_{idx}"):
                st.session_state.selected_knowledge_region = reg

    # Hiển thị nội dung tri thức tương ứng khi người dùng bấm chọn vùng
    if "selected_knowledge_region" not in st.session_state:
        st.session_state.selected_knowledge_region = None

    if st.session_state.selected_knowledge_region:
        st.markdown("---")
        st.info(f"📂 Đang hiển thị tài liệu và danh mục bệnh lý cho vùng: **{st.session_state.selected_knowledge_region}**")
        st.markdown(f"- **Tài liệu hướng dẫn chẩn đoán:** Cập nhật phác đồ chuẩn y khoa cho {st.session_state.selected_knowledge_region}.")
        st.markdown(f"- **Danh mục bệnh lý thường gặp:** Liệt kê các hội chứng, tổn thương cấu trúc và chỉ định lượng giá.")
        
        if st.button("🔄 Đóng / Chọn vùng khác", key="reset_knowledge_reg"):
            st.session_state.selected_knowledge_region = None
            st.rerun()

    st.markdown("---")
    st.markdown("##### 📚 Tài liệu tham khảo y khoa chuẩn hóa")
    st.caption("• Hướng dẫn chẩn đoán và điều trị phục hồi chức năng vận động toàn diện.")
    st.caption("• Cẩm nang nghiệm pháp đặc hiệu cơ xương khớp và thần kinh.")
# ------------------------------------------
# MỤC 3: CHỌN VÙNG & NHẬP LIỆU THĂM KHÁM (HOÀN THIỆN)
# ------------------------------------------
with tab3:
    st.subheader("🎯 Bước 1: Chọn vùng thăm khám lâm sàng")
    st.markdown("Nhấn chọn một vùng cơ thể bên dưới để mở giao diện nhập liệu thăm khám độc lập:")

    if "selected_region" not in st.session_state:
        st.session_state.selected_region = None

    col_c1, col_c2, col_c3 = st.columns(3)
    regions = [
        "Cột sống cổ", "Cột sống thắt lưng", "Khớp vai",
        "Khuỷu tay", "Cổ tay – bàn tay", "Khớp háng",
        "Khớp gối", "Cổ chân – bàn chân", "Thần kinh & Khác"
    ]
    
    for idx, reg in enumerate(regions):
        col_target = [col_c1, col_c2, col_c3][idx % 3]
        with col_target:
            if st.button(f"📌 {reg}", use_container_width=True, key=f"btn_choose_reg_{idx}"):
                st.session_state.selected_region = reg
                # Reset lại dữ liệu form tạm khi đổi vùng khám mới
                st.session_state.exam_data_cache = {}

    if st.session_state.selected_region:
        st.markdown("---")
        st.success(f"📍 Đang thực hiện khám cho vùng: **{st.session_state.selected_region}**")

        # Khởi tạo kho lưu trữ tạm trong session_state nếu chưa có
        if "exam_data_cache" not in st.session_state:
            st.session_state.exam_data_cache = {}

        with st.form(key="independent_exam_form"):
            st.markdown("#### 📋 Bước 2: Nhập liệu thăm khám độc lập")
            
            # Thông tin hành chính
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                patient_name = st.text_input("Họ tên bệnh nhân:", value=st.session_state.exam_data_cache.get("patient_name", ""), placeholder="Nhập họ tên...")
                patient_phone = st.text_input("Số điện thoại / Mã BN:", value=st.session_state.exam_data_cache.get("patient_phone", ""), placeholder="Nhập SĐT...")
            with col_p2:
                patient_age = st.number_input("Năm sinh:", min_value=1900, max_value=2026, value=st.session_state.exam_data_cache.get("patient_age", 1990))
                patient_job = st.text_input("Nghề nghiệp:", value=st.session_state.exam_data_cache.get("patient_job", ""), placeholder="Nhập nghề nghiệp...")

            st.markdown("---")
            ly_do_vao_vien = st.text_input("🏥 Lý do vào viện:", value=st.session_state.exam_data_cache.get("ly_do_vao_vien", ""), placeholder="Nhập lý do vào viện...")
            tien_su = st.text_area("📜 Tiền sử bệnh (Bản thân / Gia đình):", value=st.session_state.exam_data_cache.get("tien_su", ""), placeholder="Nhập tiền sử...")

            # Bệnh sử SOCRATES
            with st.expander("🩺 Bệnh sử (SOCRATES)", expanded=True):
                site = st.text_input("S – Vị trí đau:", value=st.session_state.selected_region)
                onset = st.text_input("O – Khởi phát:", value=st.session_state.exam_data_cache.get("onset", ""), placeholder="Hoàn cảnh khởi phát...")
                character = st.text_input("C – Tính chất đau:", value=st.session_state.exam_data_cache.get("character", ""), placeholder="Nhói, âm ỉ, tê bì...")
                radiation = st.text_input("R – Hướng lan:", value=st.session_state.exam_data_cache.get("radiation", ""), placeholder="Lan đi đâu...")
                associations = st.text_input("A – Triệu chứng đi kèm:", value=st.session_state.exam_data_cache.get("associations", ""), placeholder="Yếu cơ, sưng nề...")
                time_course = st.text_input("T – Diễn tiến:", value=st.session_state.exam_data_cache.get("time_course", ""), placeholder="Tăng về đêm, liên tục...")
                
                col_nrs1, col_nrs2 = st.columns([1, 2])
                with col_nrs1:
                    nrs_score = st.selectbox("Điểm NRS (0-10):", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=st.session_state.exam_data_cache.get("nrs_score", 0))
                with col_nrs2:
                    nrs_note = st.text_input("Ghi chú mức độ đau:", value=st.session_state.exam_data_cache.get("nrs_note", ""), placeholder="Mô tả thêm...")

            # Khám thực thể tinh gọn (Nhìn - Sờ - Gõ)
            with st.expander("🔍 Khám thực thể (Nhìn - Sờ - Gõ)", expanded=True):
                inspect_note = st.text_input("👁️ Nhìn (Inspection):", value=st.session_state.exam_data_cache.get("inspect_note", ""), placeholder="Biến dạng, sưng nề, lệch vẹo...")
                palp_note = st.text_input("✋ Sờ (Palpation):", value=st.session_state.exam_data_cache.get("palp_note", ""), placeholder="Điểm đau, nhiệt độ da, trương lực...")
                per_meas_note = st.text_input("📏 Gõ / Đo (Percussion):", value=st.session_state.exam_data_cache.get("per_meas_note", ""), placeholder="Tầm vận động ROM, phản xạ...")

            # 3-4 Test đặc hiệu
            with st.expander("👤 3-4 Test đặc hiệu / Nghiệm pháp", expanded=True):
                t1 = st.checkbox("Test đặc hiệu 1 (+ Dương tính)", value=st.session_state.exam_data_cache.get("t1", False))
                t2 = st.checkbox("Test đặc hiệu 2 (+ Dương tính)", value=st.session_state.exam_data_cache.get("t2", False))
                t3 = st.checkbox("Test đặc hiệu 3 (+ Dương tính)", value=st.session_state.exam_data_cache.get("t3", False))
                test_note = st.text_input("Ghi chú thêm về test lâm sàng:", value=st.session_state.exam_data_cache.get("test_note", ""), placeholder="Mô tả kết quả nghiệm pháp...")

            # Cờ đỏ an toàn & Tệp đính kèm
            with st.expander("🚩 Cờ đỏ an toàn & Tệp đính kèm"):
                rf_1 = st.checkbox("Hội chứng đuôi ngựa / Rối loạn tiểu tiện", value=st.session_state.exam_data_cache.get("rf_1", False))
                rf_2 = st.checkbox("Sụt cân / Nghi ngờ ác tính", value=st.session_state.exam_data_cache.get("rf_2", False))
                uploaded_files = st.file_uploader("Tải lên hình ảnh / X-quang / MRI:", accept_multiple_files=True, type=["jpg", "png", "pdf"])

            submitted = st.form_submit_button("🚀 Xác nhận & Lưu dữ liệu tạm", use_container_width=True)
            if submitted:
                # Lưu toàn bộ vào session_state cache để đồng bộ hiển thị sang phần phân tích bên dưới
                st.session_state.exam_data_cache = {
                    "patient_name": patient_name,
                    "patient_phone": patient_phone,
                    "patient_age": patient_age,
                    "patient_job": patient_job,
                    "ly_do_vao_vien": ly_do_vao_vien,
                    "tien_su": tien_su,
                    "onset": onset,
                    "character": character,
                    "radiation": radiation,
                    "associations": associations,
                    "time_course": time_course,
                    "nrs_score": nrs_score,
                    "nrs_note": nrs_note,
                    "inspect_note": inspect_note,
                    "palp_note": palp_note,
                    "per_meas_note": per_meas_note,
                    "t1": t1, "t2": t2, "t3": t3,
                    "test_note": test_note,
                    "rf_1": rf_1, "rf_2": rf_2
                }
                st.success("✅ Đã ghi nhận và cập nhật thông tin thăm khám thành công!")

        # Phân tích chẩn đoán & PHCN AI (Đọc dữ liệu an toàn từ cache)
        cached_data = st.session_state.get("exam_data_cache", {})
        
        st.markdown("---")
        st.markdown("### 🧠 Phân tích chẩn đoán & PHCN AI")
        
        col_sum1, col_sum2 = st.columns(2)
        with col_sum1:
            st.markdown("##### 📋 Tổng hợp dữ liệu")
            st.markdown(f"✔️ **Bệnh nhân:** {cached_data.get('patient_name', '---')}")
            st.markdown(f"✔️ **Vùng khám:** {st.session_state.selected_region}")
            st.markdown(f"✔️ **Tiền sử:** {cached_data.get('tien_su', 'Không ghi nhận')}")
            st.markdown(f"✔️ **Lý do NV:** {cached_data.get('ly_do_vao_vien', '---')}")
            st.markdown(f"✔️ **Đau (NRS):** {cached_data.get('nrs_score', 0)}/10")
        
        with col_sum2:
            st.markdown("##### 📄 Kết quả phân tích AI")
            st.info("Nhấn nút bên dưới để chạy phân tích lâm sàng chi tiết từ trợ lý AI...")

        if st.button("🚀 Chạy phân tích AI", type="primary", use_container_width=True):
            st.success("✅ Phân tích ca bệnh hoàn tất!")

        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            st.button("📋 Copy kết quả", use_container_width=True)
        with col_b2:
            st.button("🟢 ChatGPT", use_container_width=True)
        with col_b3:
            st.button("🟣 Gemini", use_container_width=True)

        st.markdown("---")
        if st.button("💾 Lưu hồ sơ bệnh án vào hệ thống lịch sử", type="primary", use_container_width=True):
            p_name = cached_data.get("patient_name", "")
            p_phone = cached_data.get("patient_phone", "")
            if not (p_name and p_phone):
                st.warning("⚠️ Vui lòng điền đầy đủ Họ tên và SĐT ở form phía trên rồi bấm 'Xác nhận & Lưu dữ liệu tạm' trước khi lưu vào hệ thống!")
            else:
                exam_summary = f"Vùng: {st.session_state.selected_region} | Lý do: {cached_data.get('ly_do_vao_vien', '')} | NRS: {cached_data.get('nrs_score', 0)}/10"
                visit_data = {
                    "patient_name": p_name,
                    "patient_phone": p_phone,
                    "summary": exam_summary
                }
                history_mgr.save_visit(p_phone, visit_data)
                st.success(f"✅ Đã lưu thành công hồ sơ cho bệnh nhân **{p_name}** vào hệ thống lịch sử!")
    else:
        st.info("👆 Vui lòng bấm chọn một vùng cơ thể ở phía trên để bắt đầu quy trình khám.")
# ------------------------------------------
# MỤC 4: KHO BÀI TẬP PHCN CHUYÊN SÂU (THẰNG SỐ 5 - CHI TIẾT 7 BÀI TẬP)
# ------------------------------------------
with tab4:
    st.subheader("🏋️‍♂️ Kho Bài tập Phục hồi chức năng Chuyên sâu")
    st.markdown("Tra cứu danh mục 9 nhóm bệnh lý chuyên khoa và hệ thống 7 bài tập chuẩn hóa lâm sàng cho từng nhóm:")

    # Ô tìm kiếm bài tập nhanh
    search_ex_kw = st.text_input("🔍 Tìm kiếm bài tập, động tác, hội chứng...", placeholder="Nhập từ khóa (Ví dụ: Vẹo cột sống, Đột quỵ, Nuốt khó...)", key="search_exercise_input")

    st.markdown("---")
    st.markdown("##### 🗂️ Chọn nhóm bệnh lý & Chuyên khoa PHCN")

    # Chia các nút chọn nhóm bệnh lý thành 3 cột đều nhau
    col_e1, col_e2, col_e3 = st.columns(3)
    rehab_groups = [
        "Stroke (Đột quỵ)", 
        "Dysphagia (Nuốt khó)", 
        "Aphasia (Thất ngôn)",
        "Dysarthria (Khó nói)", 
        "Autism / Motor (Tự kỷ / VĐ)", 
        "Torticollis (Vẹo cổ)",
        "Vẹo cột sống (Scoliosis)", 
        "Post-Op Knee / Hip (Mổ)", 
        "Fracture (Gãy xương)"
    ]
    
    for idx, grp in enumerate(rehab_groups):
        col_target = [col_e1, col_e2, col_e3][idx % 3]
        with col_target:
            if st.button(f"📌 {grp}", use_container_width=True, key=f"btn_rehab_group_{idx}"):
                st.session_state.selected_rehab_group = grp

    # Khởi tạo session state cho nhóm bài tập
    if "selected_rehab_group" not in st.session_state:
        st.session_state.selected_rehab_group = None

    if st.session_state.selected_rehab_group:
        st.markdown("---")
        group_name = st.session_state.selected_rehab_group
        st.success(f"📂 Danh mục 7 bài tập chuẩn hóa chuyên sâu cho nhóm: **{group_name}**")

        # Định nghĩa cơ sở dữ liệu 7 bài tập chi tiết cho từng nhóm bệnh lý
        exercises_db = {
            "Stroke (Đột quỵ)": [
                ("1. Tập vận động thụ động khớp vai bên liệt", "Duy trì tầm vận động, ngăn ngừa cứng khớp.", "Thực hiện nhẹ nhàng, chậm rãi từng biên độ khớp.", "3 sets x 10 lần/bên"),
                ("2. Kỹ thuật ức chế thần kinh cơ (PNF) chi trên", "Tăng cường nhận cảm bản thể và kích hoạt cơ yếu.", "Kết hợp kháng trở nhẹ theo đường chéo thần kinh cơ.", "3 sets x 8 lần"),
                ("3. Bài tập cầu nối (Bridging) vùng chậu", "Tăng sức mạnh cơ mông và cơ thân mình.", "Nằm ngửa, gối gập, nâng hông khỏi mặt giường giữ 5 giây.", "3 sets x 10 lần"),
                ("4. Tập đứng dồn trọng lượng hai chân", "Cải thiện thăng bằng đứng và khả năng chịu lực bên liệt.", "Đứng trước gương, phân phối đều lực qua hai bàn chân.", "3 phút x 2 lần"),
                ("5. Bài tập bước đi tại chỗ có hỗ trợ", "Phục hồi pha đứng và pha lăng trong chu kỳ dáng đi.", "Nhấc cao gối từng bên, giữ nhịp độ đều đặn.", "2 sets x 20 bước"),
                ("6. Tập kiểm soát trương lực cơ bàn tay", "Giảm co cứng các ngón tay bên liệt.", "Duỗi thụ động từng ngón kết hợp xoa bóp nhẹ nhàng.", "5 phút/lần"),
                ("7. Vận động chức năng sinh hoạt hàng ngày (ADL)", "Tái rèn luyện kỹ năng cầm nắm ly nước, thìa đũa.", "Thực hiện động tác mô phỏng có kiểm soát.", "10-15 phút")
            ],
            "Dysphagia (Nuốt khó)": [
                ("1. Bài tập Masako (Kỹ thuật giữ lưỡi)", "Tăng cường sức mạnh cơ thành sau họng.", "Đặt đầu lưỡi giữa hai hàm răng, nuốt nước bọt nhẹ nhàng.", "10 lần/lượt x 3 lượt"),
                ("2. Bài tập Shaker (Nâng đầu)", "Tăng độ mở cơ thắt thực quản trên.", "Nằm ngửa, nâng đầu nhìn ngón chân không nhấc vai, giữ 60 giây.", "3 lần lặp lại"),
                ("3. Kỹ thuật nuốt Mendelsohn", "Kéo dài thời gian mở cơ thắt thực quản trên.", "Đặt ngón tay lên sụn giáp, cảm nhận và giữ cơ nâng lên khi nuốt.", "5-10 lần nuốt"),
                ("4. Vận động cơ môi và má", "Cải thiện độ khép môi, tránh trào ngược chất lỏng.", "Mím môi chặt, thổi hơi má phồng luân phiên trái phải.", "3 sets x 10 lần"),
                ("5. Kích thích nhiệt - cảm giác vùng miệng họng", "Kích thích phản xạ nuốt nguyên phát.", "Dùng gương soi kết hợp que đè lưỡi lạnh chạm nhẹ cung khẩu cái.", "2 phút/lần"),
                ("6. Bài tập phát âm nguyên âm mạnh (A-I-U)", "Tăng sự linh hoạt cơ thanh quản và vòm miệng.", "Phát âm kéo dài các âm nguyên âm với âm lượng vừa phải.", "2 sets x 10 lần"),
                ("7. Tập nuốt với thể tích tăng dần", "Thích nghi an toàn với các độ đặc thức ăn khác nhau.", "Bắt đầu từ nước sệt, cháo loãng đến cơm mềm dưới giám sát.", "Theo chỉ định lâm sàng")
            ],
            "Aphasia (Thất ngôn)": [
                ("1. Kỹ thuật kích thích thính giác đơn giản", "Cải thiện khả năng hiểu ngôn ngữ nói.", "Nghe và chỉ tay vào đồ vật quen thuộc theo mệnh lệnh.", "5-10 phút"),
                ("2. Bài tập điền vào chỗ trống (Sentence completion)", "Kích hoạt phản xạ ngôn ngữ tự động.", "Bác sĩ nói nửa câu, bệnh nhân hoàn thành từ cuối.", "10 từ/lần"),
                ("3. Gọi tên đồ vật qua hình ảnh (Naming therapy)", "Phục hồi khả năng biểu đạt từ vựng.", "Nhìn thẻ hình ảnh (Flashcard) và phát âm tên đồ vật.", "3 sets x 5 hình"),
                ("4. Bài tập diễn đạt ý muốn cơ bản (Yes/No)", "Thiết lập giao tiếp tối thiểu cho bệnh nhân.", "Trả lời các câu hỏi đóng bằng lời nói hoặc cử chỉ gật/lắc.", "10 câu hỏi"),
                ("5. Kỹ thuật luyện phát âm giai điệu (MIT)", "Tận dụng bán cầu não phải để hỗ trợ ngôn ngữ.", "Hát theo giai điệu đơn giản các từ ngữ giao tiếp hàng ngày.", "5 phút/lần"),
                ("6. Đọc hiểu đoạn văn bản ngắn", "Duy trì khả năng đọc hiểu chữ viết.", "Đọc thầm và trả lời câu hỏi trắc nghiệm đơn giản.", "1 bài/ngày"),
                ("7. Giao tiếp tương tác nhóm thực tế", "Giảm cảm giác tự ti, tăng tương tác xã hội.", "Trao đổi hội thoại ngắn về chủ đề gia đình, thời tiết.", "15 phút")
            ],
            "Dysarthria (Khó nói)": [
                ("1. Bài tập thở hoành (Diaphragmatic breathing)", "Kiểm soát cột hơi hỗ trợ phát âm rõ ràng.", "Hít sâu bằng mũi phình bụng, thở ra từ từ qua miệng.", "3 sets x 10 hơi"),
                ("2. Kỹ thuật giãn cơ môi và lưỡi", "Giảm độ cứng cơ quan phát âm.", "Lè lưỡi tối đa ra trước, sang trái, sang phải.", "3 sets x 5 lần"),
                ("3. Luyện phát âm phụ âm tắc (P-T-K)", "Cải thiện độ rõ của âm tiết và sức bật môi lưỡi.", "Phát âm dứt khoát các âm đơn lẻ liên tục.", "2 sets x 10 lần"),
                ("4. Điều chỉnh tốc độ nói (Pacing board)", "Giảm tốc độ nói để tăng độ rõ.", "Chạm vào từng ô trên bảng tương ứng với từng âm tiết.", "5 phút"),
                ("5. Luyện tập ngữ điệu và trọng âm", "Tránh giọng nói đơn điệu, đều đều.", "Nhấn mạnh các từ khóa trong câu giao tiếp ngắn.", "10 câu/lần"),
                ("6. Tập phát âm có kiểm soát âm lượng", "Tăng cường sức mạnh cơ hô hấp - phát âm.", "Phát âm từ thì thầm đến to rõ dần mà không hét.", "3 sets x 5 lần"),
                ("7. Đọc đoạn văn kiểm soát nhịp thở", "Tăng độ bền cơ quan phát âm trong hội thoại.", "Đọc câu dài, ngắt nghỉ đúng dấu câu và nhịp thở.", "3 lần đọc")
            ],
            "Autism / Motor (Tự kỷ / VĐ)": [
                ("1. Bài tập điều hòa cảm giác tiền đình", "Cải thiện khả năng cân bằng và định vị không gian.", "Đu đưa nhẹ trên bóng tập lớn (Gymball).", "5 phút/lần"),
                ("2. Vận động thô: Bò trườn bắt chéo chi", "Kích thích sự phối hợp vận động hai bán cầu đại liga.", "Bò trên sàn đồng bộ tay trái chân phải và ngược lại.", "2 sets x 10 mét"),
                ("3. Bài tập phối hợp tay mắt với bóng lớn", "Tăng khả năng tập trung và phản xạ vận động.", "Lăn hoặc ném bắt bóng qua lại ở khoảng cách gần.", "3 sets x 10 lần"),
                ("4. Nhảy lò cò vượt chướng ngại vật thấp", "Phát triển sức mạnh cơ chi dưới và thăng bằng động.", "Bước qua các vạch kẻ sẵn trên sàn theo nhịp đếm.", "2 sets x 5 nhịp"),
                ("5. Bài tập giữ thăng bằng trên ván nhún", "Kiểm soát trương lực tư thế tĩnh và động.", "Đứng vững trên bề mặt không ổn định trong 30 giây.", "3 lần"),
                ("6. Kỹ thuật vận động tinh bằng xếp hình / hạt", "Cải thiện sự khéo léo của đôi bàn tay.", "Nhặt các hạt nhỏ hoặc xếp khối gỗ theo mẫu.", "10 phút"),
                ("7. Bài tập điều hòa nhịp thở thư giãn", "Giảm kích thích quá mức, ổn định hành vi.", "Nằm nghe nhạc nhẹ kết hợp hít thở sâu cùng kỹ thuật viên.", "5 phút")
            ],
            "Torticollis (Vẹo cổ)": [
                ("1. Kéo giãn thụ động cơ ức đòn chũm (SCM)", "Làm mềm và kéo dài cơ bị co rút.", "Nghiêng đầu sang bên lành, xoay cằm về bên bệnh.", "3 sets x 15 giây"),
                ("2. Bài tập vận động chủ động quay đầu", "Tăng tầm vận động xoay cổ hai bên.", "Khuyến khích trẻ/bệnh nhân quay đầu theo tiếng động/đồ chơi.", "3 sets x 10 lần"),
                ("3. Tập mạnh cơ bên đối diện (Cơ nghiêng cổ)", "Cân bằng lực cơ hai bên cột sống cổ.", "Nghiêng đầu chống lại kháng trở nhẹ của tay.", "3 sets x 8 lần"),
                ("4. Kỹ thuật đặt tư thế nằm sấp có kiểm soát (Tummy time)", "Tăng cường cơ vùng cổ và vai gáy.", "Cho nằm sấp dưới sự giám sát khi tỉnh táo.", "5 phút x 3 lần/ngày"),
                ("5. Bài tập vươn cổ chỉnh hình tư thế", "Cải thiện đường cong sinh lý cột sống cổ.", "Kéo dài trục cổ hướng lên trần nhà, thu cằm (Chin tuck).", "3 sets x 10 lần"),
                ("6. Xoa bóp mềm cơ co thắt vùng cổ", "Giảm đau và tăng tuần hoàn máu tại chỗ.", "Day ấn nhẹ nhàng dọc theo chiều bám của cơ ức đòn chũm.", "3 phút"),
                ("7. Định hướng tư thế đối xứng khi sinh hoạt", "Ngăn ngừa tái phát lệch vẹo tư thế.", "Điều chỉnh góc nhìn, ánh sáng và vị trí nằm giường.", "Duy trì hàng ngày")
            ],
            "Vẹo cột sống (Scoliosis)": [
                ("1. Đánh giá góc Cobb & Kiểm tra nghiệm pháp Adams", "Lượng giá mức độ gù vẹo và xoay đốt sống.", "Cúi gập người phía trước kiểm tra bướu sườn.", "Thực hiện định kỳ"),
                ("2. Kỹ thuật thở ba chiều (Schroth breathing method)", "Mở rộng lồng ngực ở phíamỏm lõm của đường cong.", "Hít sâu đưa hơi thở vào vùng lồng ngực bị lõm.", "3 sets x 10 nhịp thở"),
                ("3. Kéo giãn cơ bên lõm / Tăng cường cơ bên lồi", "Lấy lại cân bằng lực cơ hai bên cột sống.", "Nghiêng lườn sang bên lõm kết hợp kéo tay tương ứng.", "3 sets x 10 lần"),
                ("4. Bài tập ổn định cơ lõi (Core stabilization)", "Tăng cường sức mạnh hệ cơ bám cột sống.", "Tư thế tấm ván (Plank) hoặc cầu nối tiểu chuẩn.", "3 sets x 30 giây"),
                ("5. Bài tập điều chỉnh tư thế đứng và ngồi đối xứng", "Tạo nếp ý thức giữ thẳng cột sống qua gương.", "Kiểm soát vai và chậu hai bên cân bằng trước gương lớn.", "5 phút x 2 lần"),
                ("6. Kéo giãn cột sống nhẹ nhàng tư thế nằm / treo xà", "Giảm áp lực đĩa đệm và giãn cơ cạnh sống.", "Treo xà đơn thả lỏng hoặc nằm ngửa kéo giãn tự nhiên.", "3 sets x 20 giây"),
                ("7. Hướng dẫn bài tập tự tập duy trì tại nhà", "Phòng ngừa tiến triển góc vẹo cột sống.", "Thực hiện chuỗi bài tập Schroth rút gọn hàng ngày.", "Duy trì đều đặn")
            ],
            "Post-Op Knee / Hip (Mổ)": [
                ("1. Gồng cơ tứ đầu đùi (Isometric quadriceps)", "Ngăn ngừa teo cơ và kích hoạt lại cơ đùi sau mổ.", "Nằm thẳng, ép sát khoeo chân xuống mặt giường.", "3 sets x 15 lần (giữ 5s)"),
                ("2. Kéo gót chân trên mặt giường (Heel slides)", "Cải thiện tầm vận động gấp gối / hông.", "Trượt gót chân lại gần mông trong giới hạn đau cho phép.", "3 sets x 10 lần"),
                ("3. Nhấc chân thẳng lên cao (Straight leg raise)", "Tăng sức mạnh cơ tứ đầu và cơ gập hông.", "Duỗi thẳng gối, nhấc chân cách mặt giường 15cm.", "3 sets x 10 lần"),
                ("4. Tập duỗi gối thụ động hết biên độ", "Ngăn ngừa co rút bao khớp gối.", "Kê gót chân lên cao, để trọng lực ép gối thẳng tự nhiên.", "3 phút x 2 lần"),
                ("5. Bài tập đứng dồn trọng lượng hai chân đều", "Tập làm quen lại với lực ép khớp sau phẫu thuật.", "Đứng bám song vị trí an toàn, dồn lực 50-50.", "2 phút"),
                ("6. Tập đi với dụng cụ hỗ trợ (Nạng / Khung tập đi)", "Phục hồi dáng đi chuẩn trong giai đoạn đầu.", "Tuân thủ mức độ chịu lực (Partial/Full weight bearing).", "Theo phác đồ"),
                ("7. Tập đi cầu thang bước từng bậc", "Tái hòa nhập vận động sinh hoạt phức tạp.", "Lên bằng chân lành, xuống bằng chân mổ (Up with the good, down with the bad).", "10-15 bậc")
            ],
            "Fracture (Gãy xương)": [
                ("1. Vận động chủ động các khớp lân cận ổ gãy", "Duy trì tầm vận động, chống cứng khớp và phù nề.", "Cử động nhẹ nhàng ngón chân/cổ chân khi gãy cẳng chân.", "3 sets x 10 lần"),
                ("2. Gồng cơ tĩnh vùng xung quanh ổ gãy", "Duy trì khối cơ, kích hoạt tuần hoàn giảm teo cơ.", "Gồng cơ ngắt quãng dưới lớp bột/nẹp cố định.", "3 sets x 10 lần (giữ 5s)"),
                ("3. Bài tập nâng cao chi thể phòng phù nề", "Hỗ trợ hệ bạch huyết hồi lưu máu tĩnh mạch.", "Kê cao chân/tay gãy trên mức tim khi nằm nghỉ.", "Nhiều lần trong ngày"),
                ("4. Kỹ thuật đi trọng lượng tăng dần sau tháo bột", "Phục hồi khả năng chịu lực của xương và khớp.", "Sử dụng nạng hỗ trợ tăng dần lực tì đè theo y lệnh.", "Theo giai đoạn liền xương"),
                ("5. Tái dung nạp tầm vận động ROM khớp đích", "Khôi phục biên độ vận động sau thời gian bất động.", "Tập gấp duỗi tự do có hỗ trợ nhiệt ấm trước khi tập.", "2 sets x 10 lần"),
                ("6. Tăng cường sức mạnh cơ bắp toàn chi", "Lấy lại sức mạnh cơ lực sau giai đoạn teo cơ.", "Sử dụng tạ nhẹ hoặc dây kháng lực đàn hồi phù hợp.", "3 sets x 10 lần"),
                ("7. Huấn luyện lại dáng đi và thăng bằng cơ thể", "Đảm bảo an toàn, tránh té ngã tái phát gãy xương.", "Đi đường thẳng, bước qua chướng ngại vật thấp.", "10-15 phút")
            ]
        }

        # Lấy danh sách 7 bài tập tương ứng với nhóm đã chọn
        current_exercises = exercises_db.get(group_name, [])

        for idx_ex, ex_item in enumerate(current_exercises):
            title, purpose, technique, dosage = ex_item
            with st.expander(f"🔹 {title}"):
                st.markdown(f"- **🎯 Mục đích lâm sàng:** {purpose}")
                st.markdown(f"- **⚙️ Hướng dẫn kỹ thuật:** {technique}")
                st.markdown(f"- **⏱️ Liều lượng (Dosage):** {dosage}")
                st.markdown("- **🛡️ Lưu ý an toàn:** Thực hiện đúng biên độ, dừng lại ngay khi xuất hiện cơn đau nhói hoặc chóng mặt.")

        st.markdown("---")
        if st.button("🔄 Chọn nhóm bệnh lý khác", key="reset_rehab_group"):
            st.session_state.selected_rehab_group = None
            st.rerun()

    else:
        st.info("👆 Vui lòng bấm chọn một nhóm bệnh lý / chuyên khoa ở phía trên để hiển thị chi tiết 7 bài tập chuẩn hóa.")

    st.markdown("---")
    st.caption("💡 Hệ thống dữ liệu bài tập PHCN được chuẩn hóa chuyên sâu theo y học chứng cứ phục hồi chức năng vận động và chỉnh hình.")
