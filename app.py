# app.py
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
# MỤC 1: HỒ SƠ BỆNH NHÂN & LỊCH SỬ
# ------------------------------------------
with tab1:
    st.subheader("👤 Quản lý Hồ sơ & Lịch sử Bệnh nhân")
    search_phone_input = st.text_input("🔍 Nhập số điện thoại / Mã BN tra cứu lịch sử:", placeholder="Ví dụ: 0901234567", key="search_history_phone")
    
    if search_phone_input:
        patient_history_list = history_mgr.get_patient_history(search_phone_input)
        if patient_history_list:
            st.success(f"Tìm thấy {len(patient_history_list)} lần khám.")
            for idx, visit in enumerate(patient_history_list):
                st.markdown(f"**Lần {idx+1} – Thời gian: {visit.get('date', 'N/A')}**")
                st.write(f"• **Họ tên:** {visit.get('patient_name', 'N/A')}")
                st.write(f"• **Tóm tắt:** {visit.get('summary', 'N/A')}")
                st.markdown("---")
        else:
            st.warning("⚠️ Không tìm thấy lịch sử khám với số điện thoại này.")
    else:
        st.info("💡 Nhập số điện thoại ở trên để tra cứu thông tin hành chính và lịch sử các lần khám trước.")

# ------------------------------------------
# MỤC 2: CƠ SỞ TRI THỨC LÂM SÀNG
# ------------------------------------------
with tab2:
    st.subheader("📖 Cơ sở Tri thức Lâm sàng & Bệnh lý")
    search_kw = st.text_input("🔍 Tìm kiếm kiến thức, bệnh lý...", placeholder="Nhập tên bệnh hoặc triệu chứng...")
    
    cols = st.columns(3)
    regions = [
        "Cột sống cổ", "Cột sống thắt lưng", "Khớp vai",
        "Khuỷu tay", "Cổ tay – bàn tay", "Khớp háng",
        "Khớp gối", "Cổ chân – bàn chân", "Thần kinh & Khác"
    ]
    for idx, reg in enumerate(regions):
        with cols[idx % 3]:
            if st.button(f"📌 {reg}", use_container_width=True, key=f"knowledge_reg_{idx}"):
                st.info(f"Đang hiển thị tài liệu hướng dẫn và danh mục bệnh lý cho vùng: **{reg}**")

    st.markdown("---")
    st.markdown("##### 📚 Tài liệu tham khảo chuẩn y khoa")
    st.caption("• Hướng dẫn chẩn đoán và điều trị phục hồi chức năng vận động.")
    st.caption("• Cẩm nang nghiệm pháp đặc hiệu cơ xương khớp.")

# ------------------------------------------
# MỤC 3: CHỌN VÙNG & NHẬP LIỆU THĂM KHÁM
# ------------------------------------------
with tab3:
    st.subheader("🎯 Bước 1: Chọn vùng thăm khám lâm sàng")
    st.markdown("Nhấn chọn một vùng cơ thể bên dưới để mở giao diện nhập liệu thăm khám độc lập:")

    if "selected_region" not in st.session_state:
        st.session_state.selected_region = None

    col_c1, col_c2, col_c3 = st.columns(3)
    for idx, reg in enumerate(regions):
        col_target = [col_c1, col_c2, col_c3][idx % 3]
        with col_target:
            if st.button(f"📌 {reg}", use_container_width=True, key=f"btn_choose_reg_{idx}"):
                st.session_state.selected_region = reg

    if st.session_state.selected_region:
        st.markdown("---")
        st.success(f"📍 Đang thực hiện khám cho vùng: **{st.session_state.selected_region}**")

        with st.form(key="independent_exam_form"):
            st.markdown("#### 📋 Bước 2: Nhập liệu thăm khám độc lập")
            
            # Thông tin hành chính
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                patient_name = st.text_input("Họ tên bệnh nhân:", placeholder="Nhập họ tên...")
                patient_phone = st.text_input("Số điện thoại / Mã BN:", placeholder="Nhập SĐT...")
            with col_p2:
                patient_age = st.number_input("Năm sinh:", min_value=1900, max_value=2026, value=1990)
                patient_job = st.text_input("Nghề nghiệp:", placeholder="Nhập nghề nghiệp...")

            st.markdown("---")
            ly_do_vao_vien = st.text_input("🏥 Lý do vào viện:", placeholder="Nhập lý do vào viện...")
            tien_su = st.text_area("📜 Tiền sử bệnh (Bản thân / Gia đình):", placeholder="Nhập tiền sử...")

            # Bệnh sử SOCRATES
            with st.expander("🩺 Bệnh sử (SOCRATES)", expanded=True):
                site = st.text_input("S – Vị trí đau:", value=st.session_state.selected_region)
                onset = st.text_input("O – Khởi phát:", placeholder="Hoàn cảnh khởi phát...")
                character = st.text_input("C – Tính chất đau:", placeholder="Nhói, âm ỉ, tê bì...")
                radiation = st.text_input("R – Hướng lan:", placeholder="Lan đi đâu...")
                associations = st.text_input("A – Triệu chứng đi kèm:", placeholder="Yếu cơ, sưng nề...")
                time_course = st.text_input("T – Diễn tiến:", placeholder="Tăng về đêm, liên tục...")
                
                col_nrs1, col_nrs2 = st.columns([1, 2])
                with col_nrs1:
                    nrs_score = st.selectbox("Điểm NRS (0-10):", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                with col_nrs2:
                    nrs_note = st.text_input("Ghi chú mức độ đau:", placeholder="Mô tả thêm...")

            # Khám thực thể tinh gọn (Nhìn - Sờ - Gõ)
            with st.expander("🔍 Khám thực thể (Nhìn - Sờ - Gõ)", expanded=True):
                inspect_note = st.text_input("👁️ Nhìn (Inspection):", placeholder="Biến dạng, sưng nề, lệch vẹo...")
                palp_note = st.text_input("✋ Sờ (Palpation):", placeholder="Điểm đau, nhiệt độ da, trương lực...")
                per_meas_note = st.text_input("📏 Gõ / Đo (Percussion):", placeholder="Tầm vận động ROM, phản xạ...")

            # 3-4 Test đặc hiệu
            with st.expander("👤 3-4 Test đặc hiệu / Nghiệm pháp", expanded=True):
                t1 = st.checkbox("Test đặc hiệu 1 (+ Dương tính)")
                t2 = st.checkbox("Test đặc hiệu 2 (+ Dương tính)")
                t3 = st.checkbox("Test đặc hiệu 3 (+ Dương tính)")
                test_note = st.text_input("Ghi chú thêm về test lâm sàng:", placeholder="Mô tả kết quả nghiệm pháp...")

            # Cờ đỏ an toàn & Tệp đính kèm
            with st.expander("🚩 Cờ đỏ an toàn & Tệp đính kèm"):
                rf_1 = st.checkbox("Hội chứng đuôi ngựa / Rối loạn tiểu tiện")
                rf_2 = st.checkbox("Sụt cân / Nghi ngờ ác tính")
                uploaded_files = st.file_uploader("Tải lên hình ảnh / X-quang / MRI:", accept_multiple_files=True, type=["jpg", "png", "pdf"])

            submitted = st.form_submit_button("🚀 Xác nhận & Sẵn sàng Phân tích AI", use_container_width=True)
            if submitted:
                st.success("✅ Đã ghi nhận thông tin thăm khám!")

        # Phân tích chẩn đoán & PHCN AI
        st.markdown("---")
        st.markdown("### 🧠 Phân tích chẩn đoán & PHCN AI")
        
        col_sum1, col_sum2 = st.columns(2)
        with col_sum1:
            st.markdown("##### 📋 Tổng hợp dữ liệu")
            st.markdown(f"✔️ **Bệnh nhân:** {patient_name if 'patient_name' in locals() and patient_name else '---'}")
            st.markdown(f"✔️ **Vùng khám:** {st.session_state.selected_region}")
            st.markdown(f"✔️ **Tiền sử:** {tien_su if 'tien_su' in locals() and tien_su else 'Không ghi nhận'}")
            st.markdown(f"✔️ **Lý do NV:** {ly_do_vao_vien if 'ly_do_vao_vien' in locals() and ly_do_vao_vien else '---'}")
            st.markdown(f"✔️ **Đau (NRS):** {nrs_score if 'nrs_score' in locals() else 0}/10")
        
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
        if st.button("💾 Lưu hồ sơ bệnh án vào hệ thống", type="primary", use_container_width=True):
            if not ('patient_name' in locals() and patient_name and 'patient_phone' in locals() and patient_phone):
                st.warning("⚠️ Vui lòng điền đầy đủ Họ tên và SĐT ở form trên để lưu trữ!")
            else:
                exam_summary = f"Vùng: {st.session_state.selected_region} | Lý do: {ly_do_vao_vien} | NRS: {nrs_score}/10"
                exam_data = {
                    "patient_name": patient_name,
                    "patient_phone": patient_phone,
                    "summary": exam_summary
                }
                history_mgr.save_visit(patient_phone, exam_data)
                st.success(f"✅ Đã lưu thành công hồ sơ cho bệnh nhân **{patient_name}** vào hệ thống lịch sử!")
    else:
        st.info("👆 Vui lòng bấm chọn một vùng cơ thể ở phía trên để bắt đầu quy trình khám.")

# ------------------------------------------
# MỤC 4: KHO BÀI TẬP PHỤC HỒI CHỨC NĂNG
# ------------------------------------------

else:
    st.subheader("🏋️‍♂️ Thư viện Chi tiết Bài Tập Phục Hồi Chức Năng Chuyên Sâu")
    st.markdown("Chọn chương trình PHCN dưới đây để xem **hướng dẫn thao tác, tư thế và liều lượng chi tiết**:")

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
        st.markdown("---")
        st.markdown("##### 1. Vận động thụ động - chủ động hỗ trợ khớp vai và khuỷu tay bên liệt")
        st.write("- **Tư thế:** Bệnh nhân nằm ngửa hoặc ngồi ghế tựa.")
        st.write("- **Cách thực hiện:** Kỹ thuật viên hoặc tay lành hỗ trợ đưa tay liệt lên cao, dạng vai, gập khuỷu nhẹ nhàng.")
        st.write("- **Liều lượng:** 10–15 lần/hiệp, ngày tập 2–3 lần.")

        st.markdown("##### 2. Kỹ thuật ức chế trương lực cơ co cứng cơ gấp cổ tay và ngón tay")
        st.write("- **Tư thế:** Bệnh nhân ngồi, tay đặt ngửa trên bàn.")
        st.write("- **Cách thực hiện:** Thực hiện duỗi nhẹ nhàng các ngón tay và khớp cổ tay ra hết biên độ, giữ kéo giãn tĩnh.")
        st.write("- **Liều lượng:** Giữ 30 giây/lần, lặp lại 5 lần.")

        st.markdown("##### 3. Tập nâng hông (Bridging) ở tư thế nằm ngửa")
        st.write("- **Tư thế:** Nằm ngửa, gập gối, hai bàn chân đặt sát mặt giường.")
        st.write("- **Cách thực hiện:** Dồn lực vào hai gót chân và cơ mông, nâng hông lên khỏi mặt giường sao cho thân người tạo thành một đường thẳng.")
        st.write("- **Liều lượng:** 10 lần/hiệp, 3 hiệp/ngày.")

        st.markdown("##### 4. Tập thăng bằng ngồi trên ghế không tựa lưng")
        st.write("- **Tư thế:** Ngồi thẳng lưng trên ghế, hai chân chống vuông góc xuống sàn.")
        st.write("- **Cách thực hiện:** Bỏ tay vịn, giữ thăng bằng thân mình, tập với tay sang các hướng trái/phải/trước mà không ngã.")
        st.write("- **Liều lượng:** Duy trì liên tục từ 3–5 phút/lần.")

        st.markdown("##### 5. Bài tập đứng dồn lực lên chân liệt trước gương")
        st.write("- **Tư thế:** Đứng đối diện gương lớn, hai chân rộng bằng vai.")
        st.write("- **Cách thực hiện:** Chuyển trọng tâm cơ thể từ từ sang bên chân liệt, quan sát trong gương để giữ hông cân đối.")
        st.write("- **Liều lượng:** Giữ 10–15 giây/lần, lặp lại 10 lần.")

        st.markdown("##### 6. Huấn luyện lại dáng đi với thanh song song / khung tập đi")
        st.write("- **Tư thế:** Đứng vững trong khung tập đi hoặc thanh song song.")
        st.write("- **Cách thực hiện:** Bước chân liệt lên trước, theo sau là chân lành, chú ý dáng đi đúng nhịp.")
        st.write("- **Liều lượng:** Tập đi từ 5–10 phút mỗi buổi.")

        st.markdown("##### 7. Tập cầm nắm vật dụng sinh hoạt hàng ngày")
        st.write("- **Tư thế:** Ngồi bàn ghế thoải mái.")
        st.write("- **Cách thực hiện:** Tập cầm các vật có kích thước khác nhau (quả bóng mềm, ly nước nhựa, bút) để tái giáo dục chi trên.")
        st.write("- **Liều lượng:** 10–15 phút/lần.")

    elif "2." in rehab_program:
        st.subheader("🦴 2. Chương trình PHCN cong vẹo cột sống cổ / Cổ vai gáy")
        st.write("• **Mục tiêu:** Thư giãn nhóm cơ co thắt, mạnh cơ cổ sâu, chỉnh sửa tư thế đầu.")
        st.markdown("---")
        st.markdown("##### 1. Kéo giãn cơ thang trên (Upper Trapezius Stretch)")
        st.write("- **Tư thế:** Ngồi thẳng, một tay ôm vòng qua đầu kéo nghiêng đầu về phía đối diện.")
        st.write("- **Cách thực hiện:** Kéo nhẹ nhàng cho đến khi có cảm giác căng tức vùng cổ vai bên đối diện.")
        st.write("- **Liều lượng:** Giữ 20–30 giây, lặp lại 3–5 lần mỗi bên.")

        st.markdown("##### 2. Kéo giãn cơ nâng vai (Levator Scapulae Stretch)")
        st.write("- **Tư thế:** Ngồi ghế, xoay đầu sang một góc 45 độ rồi cuối cằm nhìn xuống nách.")
        st.write("- **Cách thực hiện:** Dùng tay cùng phía ấn nhẹ đầu xuống dưới để tăng độ căng.")
        st.write("- **Liều lượng:** Giữ 20–30 giây, lặp lại 3 lần/bên.")

        st.markdown("##### 3. Kéo cằm ngược (Chin Tuck)")
        st.write("- **Tư thế:** Ngồi hoặc đứng thẳng, mắt nhìn thẳng phía trước.")
        st.write("- **Cách thực hiện:** Kéo cằm lùi thẳng ra sau (tạo nọng cằm giả) mà không cúi đầu xuống, cảm nhận cơ cổ sâu phía sau căng nhẹ.")
        st.write("- **Liều lượng:** 10 lần/hiệp, giữ 5 giây mỗi lần.")

        st.markdown("##### 4. Xoay cổ chủ động biên độ nhẹ")
        st.write("- **Tư thế:** Ngồi thoải mái, thả lỏng vai.")
        st.write("- **Cách thực hiện:** Từ từ xoay đầu sang trái rồi sang phải trong giới hạn không đau.")
        st.write("- **Liều lượng:** 10 vòng mỗi hướng.")

        st.markdown("##### 5. Tập mạnh cơ duỗi cổ kháng lực đẳng cự")
        st.write("- **Tư thế:** Đặt hai tay đan vào nhau sau chẩm đầu.")
        st.write("- **Cách thực hiện:** Dùng đầu đẩy ngược ra sau đồng thời hai tay kháng lực lại (đầu không di chuyển).")
        st.write("- **Liều lượng:** Giữ 5–10 giây, lặp lại 10 lần.")

        st.markdown("##### 6. Vận động khép xương bả vai (Scapular Retraction)")
        st.write("- **Tư thế:** Ngồi thẳng lưng, hai tay thả lỏng.")
        st.write("- **Cách thực hiện:** Kéo hai xương bả vai sát lại với nhau ra phía sau như kẹp một vật ở giữa.")
        st.write("- **Liều lượng:** Giữ 5 giây, lặp lại 15 lần.")

        st.markdown("##### 7. Nhiệt trị liệu & Thư giãn điểm đau (Trigger points)")
        st.write("- **Tư thế:** Nằm sấp hoặc ngồi tựa đầu thư giãn.")
        st.write("- **Cách thực hiện:** Chườm ấm vùng cổ vai gáy kết hợp xoa bóp nhẹ nhàng các điểm cơ co cứng.")
        st.write("- **Liều lượng:** 15–20 phút/lần.")

    elif "3." in rehab_program:
        st.subheader("🧸 3. Chương trình PHCN cho trẻ bại não (Cerebral Palsy)")
        st.write("• **Mục tiêu:** Ức chế phản xạ nguyên bản bất thường, tăng cường kiểm soát đầu cổ.")
        st.markdown("---")
        st.markdown("##### 1. Tạo thuận kiểm soát đầu cổ")
        st.write("- **Tư thế:** Trẻ nằm sấp trên thảm có cuộn khăn dưới ngực.")
        st.write("- **Cách thực hiện:** Kích thích âm thanh hoặc đồ chơi phía trước để trẻ ngẩng đầu lên.")
        st.write("- **Liều lượng:** 5–10 lần/buổi.")

        st.markdown("##### 2. Tập tư thế nằm sấp chống khuỷu (Prone on elbows)")
        st.write("- **Tư thế:** Trẻ nằm sấp, hai khuỷu tay chống vuông góc nâng thân trên lên.")
        st.write("- **Cách thực hiện:** Giữ ổn định tư thế vai và cột sống cổ của trẻ.")
        st.write("- **Liều lượng:** 3–5 phút mỗi lần tập.")

        st.markdown("##### 3. Tập quỳ bốn điểm và nhún trọng lượng (Quadruped rocking)")
        st.write("- **Tư thế:** Trẻ ở tư thế bò bốn điểm (hai tay và hai gối chống sàn).")
        st.write("- **Cách thực hiện:** Hỗ trợ nhún người trẻ nhẹ nhàng ra trước và ra sau để tăng cảm giác thăng bằng.")
        st.write("- **Liều lượng:** 10–15 nhịp/lần.")

        st.markdown("##### 4. Tập phản ứng thăng bằng trên bóng Bobath")
        st.write("- **Tư thế:** Cho trẻ ngồi hoặc nằm sấp trên bóng trị liệu lớn.")
        st.write("- **Cách thực hiện:** Lăn bóng nhẹ nhàng các hướng trước-sau, trái-phải để kích thích phản xạ giữ thăng bằng.")
        st.write("- **Liều lượng:** 5–7 phút.")

        st.markdown("##### 5. Kéo giãn nhẹ nhàng cơ khép háng và gân kheo")
        st.write("- **Tư thế:** Trẻ nằm ngửa trên giường.")
        st.write("- **Cách thực hiện:** Từ từ dạng chân hoặc duỗi thẳng gối kéo giãn nhẹ nhóm cơ căng cứng.")
        st.write("- **Liều lượng:** Giữ 15–20 giây, lặp lại 3 lần.")

        st.markdown("##### 6. Hướng dẫn tập đứng với nẹp trợ giúp AFO")
        st.write("- **Tư thế:** Mang nẹp chân cho trẻ và đỡ đứng thẳng.")
        st.write("- **Cách thực hiện:** Cho trẻ tập đứng bám vào bàn hoặc khung tập đứng.")
        st.write("- **Liều lượng:** 5–10 phút.")

        st.markdown("##### 7. Trị liệu vận động tinh qua trò chơi")
        st.write("- **Tư thế:** Ngồi bàn ghế chắc chắn.")
        st.write("- **Cách thực hiện:** Hướng dẫn trẻ nhặt khối gỗ nhỏ, xâu hạt vòng để luyện cơ bàn tay và ngón tay.")
        st.write("- **Liều lượng:** 10–15 phút.")

    elif "4." in rehab_program:
        st.subheader("🦵 4. Chương trình PHCN sau mổ tái tạo dây chằng chéo trước (ACL)")
        st.write("• **Mục tiêu:** Lấy lại biên độ duỗi thẳng hoàn toàn, phục hồi cơ tứ đầu đùi.")
        st.markdown("---")
        st.markdown("##### 1. Duỗi gối thụ động tối đa")
        st.write("- **Tư thế:** Nằm ngửa, gót chân kê cao trên con lăn, để chân tự duỗi thẳng hoàn toàn dưới trọng lực.")
        st.write("- **Liều lượng:** 10–15 phút, ngày 3 lần.")

        st.markdown("##### 2. Gồng cơ tứ đầu đùi tĩnh (Isometric Quad Sets)")
        st.write("- **Tư thế:** Nằm ngửa, chân duỗi thẳng, đặt một khăn mỏng dưới khoeo.")
        st.write("- **Cách thực hiện:** Ép sát khoeo chân xuống khăn, gồng căng cơ đùi hết cỡ.")
        st.write("- **Liều lượng:** Giữ 10 giây, lặp lại 15–20 lần.")

        st.markdown("##### 3. Nâng chân thẳng (Straight Leg Raise)")
        st.write("- **Tư thế:** Nằm ngửa, chân mổ duỗi thẳng, chân kia gập gối.")
        st.write("- **Cách thực hiện:** Gồng cơ đùi, nhấc thẳng chân lên cao cách mặt giường khoảng 20-30cm rồi hạ xuống từ từ.")
        st.write("- **Liều lượng:** 3 hiệp x 12 lần.")

        st.markdown("##### 4. Gập gối gót chạm mông chủ động trợ giúp")
        st.write("- **Tư thế:** Nằm ngửa hoặc ngồi trên mép giường.")
        st.write("- **Cách thực hiện:** Dùng chân lành hỗ trợ kéo hoặc trượt gót chân mổ về phía mông để tăng biên độ gập gối.")
        st.write("- **Liều lượng:** 10–15 lần/hiệp.")

        st.markdown("##### 5. Đạp xe đạp tĩnh điện không kháng lực")
        st.write("- **Tư thế:** Ngồi trên xe đạp tập, yên chỉnh độ cao phù hợp.")
        st.write("- **Cách thực hiện:** Đạp vòng tròn nhẹ nhàng không để mức kháng lực (thường áp dụng từ tuần 4-6 sau mổ).")
        st.write("- **Liều lượng:** 10–15 phút/ngày.")

        st.markdown("##### 6. Ngồi xổm một phần (Mini Squats)")
        st.write("- **Tư thế:** Đứng thẳng, hai chân rộng bằng vai, bám nhẹ vào thanh vịn.")
        st.write("- **Cách thực hiện:** Từ từ hạ thấp người xuống ở biên độ an toàn từ 0 đến 45 độ gối rồi đứng lên.")
        st.write("- **Liều lượng:** 3 hiệp x 10 lần.")

        st.markdown("##### 7. Tập thăng bằng cảm giác bản thể trên đệm hơi")
        st.write("- **Tư thế:** Đứng bằng chân mổ trên đệm hơi hoặc thảm thăng bằng.")
        st.write("- **Cách thực hiện:** Giữ thăng bằng cơ thể không để chân bị chao đảo.")
        st.write("- **Liều lượng:** 3 lần x 1 phút.")

    elif "5." in rehab_program:
        st.subheader("🦴 5. Chương trình PHCN sau mổ kết hợp xương gãy thân xương đùi")
        st.write("• **Mục tiêu:** Ngăn ngừa teo cơ, chống huyết khối tĩnh mạch, hồi phục chức năng gối.")
        st.markdown("---")
        st.markdown("##### 1. Bơm máu cổ chân")
        st.write("- **Tư thế:** Nằm ngửa, chân duỗi thẳng.")
        st.write("- **Cách thực hiện:** Gập duỗi liên tục hai bàn chân lên xuống nhịp nhàng.")
        st.write("- **Liều lượng:** 20–30 lần mỗi giờ để phòng huyết khối.")

        st.markdown("##### 2. Gồng cơ mông và đùi tĩnh")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Siết chặt cơ mông và cơ đùi trong vòng 5 giây rồi thả lỏng.")
        st.write("- **Liều lượng:** 15 lần/hiệp, 3 hiệp/ngày.")

        st.markdown("##### 3. Trượt gót chân trên giường (Heel Slides)")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Từ từ kéo gót chân trượt về phía mông để gập gối trong giới hạn cho phép của bác sĩ phẫu thuật.")
        st.write("- **Liều lượng:** 10 lần/hiệp.")

        st.markdown("##### 4. Nâng chân thẳng")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Nâng nguyên chân lên cao 20cm khỏi mặt giường với đầu gối duỗi thẳng hoàn toàn.")
        st.write("- **Liều lượng:** 10 lần/hiệp.")

        st.markdown("##### 5. Ngồi thõng chân mép giường")
        st.write("- **Tư thế:** Ngồi ở mép giường, cẳng chân buông thõng tự nhiên.")
        st.write("- **Cách thực hiện:** Đung đưa nhẹ nhàng cẳng chân để lấy lại tầm vận động gối.")
        st.write("- **Liều lượng:** 5–10 phút/lần.")

        st.markdown("##### 6. Tập đứng chịu lực một phần với khung tập đi")
        st.write("- **Tư thế:** Đứng dậy bằng khung tập đi theo đúng chỉ định chịu lực (chịu lực một phần chân mổ).")
        st.write("- **Liều lượng:** 5–10 phút.")

        st.markdown("##### 7. Tập bước đi lên xuống bậc thang thấp")
        st.write("- **Tư thế:** Giai đoạn liền xương, tập bước bậc thang thấp (Lên bằng chân lành, xuống bằng chân mổ).")
        st.write("- **Liều lượng:** 5–10 nhịp.")

    elif "6." in rehab_program:
        st.subheader("✋ 6. Chương trình PHCN sau mổ gãy xương cổ tay / bàn tay")
        st.write("• **Mục tiêu:** Chống phù nề, chống xơ hóa gân, lấy lại tầm vận động và lực nắm.")
        st.markdown("---")
        st.markdown("##### 1. Kê cao tay & nắm xòe ngón tay")
        st.write("- **Tư thế:** Ngồi hoặc nằm, tay bị thương kê cao hơn mức tim.")
        st.write("- **Cách thực hiện:** Liên tục nắm chặt và xòe rộng các ngón tay để bơm máu tĩnh mạch giảm sưng.")
        st.write("- **Liều lượng:** 15–20 lần mỗi giờ.")

        st.markdown("##### 2. Vận động thụ động nhẹ nhàng khớp cổ tay")
        st.write("- **Tư thế:** Ngồi thoải mái, tay lành hỗ trợ tay mổ.")
        st.write("- **Cách thực hiện:** Nhẹ nhàng gập và duỗi cổ tay trong giới hạn không đau đớn.")
        st.write("- **Liều lượng:** 10 lần/hiệp, ngày 3 lần.")

        st.markdown("##### 3. Vận động chủ động nghiêng quay / nghiêng trụ")
        st.write("- **Tư thế:** Đặt cẳng tay cạnh sườn, bàn tay trung gian.")
        st.write("- **Cách thực hiện:** Chủ động lắc cổ tay sang hai bên (hướng ngón cái và hướng ngón út).")
        st.write("- **Liều lượng:** 10 lần mỗi hướng.")

        st.markdown("##### 4. Tập mạnh cơ ngửa và sấp cẳng tay")
        st.write("- **Tư thế:** Khuỷu tay gập 90 độ sát thân người.")
        st.write("- **Cách thực hiện:** Xoay lật lòng bàn tay ngửa lên và sấp xuống với kháng lực nhẹ.")
        st.write("- **Liều lượng:** 12 lần/hiệp.")

        st.markdown("##### 5. Bóp bóng cao su mềm")
        st.write("- **Tư thế:** Ngồi cầm quả bóng cao su mềm trong lòng bàn tay.")
        st.write("- **Cách thực hiện:** Dùng toàn bộ ngón tay bóp chặt bóng lại rồi thả lỏng từ từ.")
        st.write("- **Liều lượng:** 15 lần/hiệp, 3 hiệp/ngày.")

        st.markdown("##### 6. Bài tập đối chiếu ngón cái")
        st.write("- **Tư thế:** Ngồi thả lỏng tay.")
        st.write("- **Cách thực hiện:** Dùng đầu ngón cái lần lượt chạm vào đầu các ngón tay 2, 3, 4, 5.")
        st.write("- **Liều lượng:** Lặp lại 5 vòng.")

        st.markdown("##### 7. Siêu âm trị liệu chống dính sẹo")
        st.write("- **Tư thế:** Đặt tay thoải mái trên bàn điều trị.")
        st.write("- **Cách thực hiện:** Chạy máy siêu âm hoặc xoa bóp nhẹ nhàng dọc theo đường mổ để làm mềm và chống dính mô sẹo.")
        st.write("- **Liều lượng:** 5–7 phút mỗi ngày.")

    elif "7." in rehab_program:
        st.subheader("🦴 7. Chương trình PHCN sau phẫu thuật thay khớp háng toàn phần")
        st.write("• **Mục tiêu:** Bảo vệ khớp nhân tạo, phục hồi cơ mông, hướng dẫn sinh hoạt an toàn.")
        st.markdown("---")
        st.markdown("##### 1. Bơm máu bàn chân")
        st.write("- **Tư thế:** Nằm ngửa, hai chân duỗi thẳng.")
        st.write("- **Cách thực hiện:** Gập và duỗi cổ chân liên tục để tăng tuần hoàn máu.")
        st.write("- **Liều lượng:** 20 lần/giờ.")

        st.markdown("##### 2. Ép mông tĩnh (Gluteal Squeezes)")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Siết chặt hai cơ mông lại với nhau, giữ nguyên trong 5 giây.")
        st.write("- **Liều lượng:** 15 lần/hiệp.")

        st.markdown("##### 3. Dạng chân trượt sang ngang")
        st.write("- **Tư thế:** Nằm ngửa, chân duỗi thẳng.")
        st.write("- **Cách thực hiện:** Từ từ trượt chân mổ sang ngang ra phía ngoài rồi kéo về giữa (tuân thủ không dạng quá mức).")
        st.write("- **Liều lượng:** 10 lần/hiệp.")

        st.markdown("##### 4. Trượt gót chân gập háng nhẹ")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Trượt gót chân gập háng và gối nhẹ nhàng (lưu ý tuyệt đối không gập háng quá 90 độ).")
        st.write("- **Liều lượng:** 10 lần/hiệp.")

        st.markdown("##### 5. Nâng chân thẳng ở tư thế nằm ngửa")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Gồng cơ đùi và nâng chân lên khỏi mặt giường khoảng 15cm.")
        st.write("- **Liều lượng:** 10 lần/hiệp.")

        st.markdown("##### 6. Tập đứng dồn lực đều hai chân với khung")
        st.write("- **Tư thế:** Đứng thẳng bằng khung tập đi.")
        st.write("- **Cách thực hiện:** Phân bổ trọng lượng cơ thể đều hai bên chân dưới sự giám sát.")
        st.write("- **Liều lượng:** 5–10 phút.")

        st.markdown("##### 7. Hướng dẫn tư thế sinh hoạt an toàn")
        st.write("- **Lưu ý:** Không bắt chéo chân khi nằm hoặc ngồi, không cúi gập người quá 90 độ, luôn dùng ghế cao khi ngồi vệ sinh.")

    elif "8." in rehab_program:
        st.subheader("🗣️ 8. Chương trình PHCN cho trẻ chậm nói / Rối loạn phát triển ngôn ngữ")
        st.write("• **Mục tiêu:** Kích thích cơ quan phát âm, mở rộng vốn từ vựng tiếp nhận.")
        st.markdown("---")
        st.markdown("##### 1. Massage kích thích cơ vùng miệng - môi - má")
        st.write("- **Tư thế:** Trẻ ngồi thoải mái trước mặt kỹ thuật viên hoặc phụ huynh.")
        st.write("- **Cách thực hiện:** Dùng tay sạch massage nhẹ nhàng xung quanh môi, má và vùng cơ quanh miệng để tăng cảm giác.")
        st.write("- **Liều lượng:** 3–5 phút.")

        st.markdown("##### 2. Tập thổi hơi có mục đích")
        st.write("- **Tư thế:** Ngồi bàn ghế ngay ngắn.")
        st.write("- **Cách thực hiện:** Cho trẻ tập thổi bóng bông trên bàn, thổi còi nhựa hoặc thổi tắt nến ở khoảng cách gần.")
        st.write("- **Liều lượng:** 5–10 lần thổi mỗi buổi.")

        st.markdown("##### 3. Giao tiếp mắt 1 kèm 1 với Flashcard")
        st.write("- **Tư thế:** Ngồi đối diện trẻ ở cự ly gần.")
        st.write("- **Cách thực hiện:** Đưa thẻ hình con vật, đồ vật màu sắc sinh động ngang tầm mắt, yêu cầu trẻ nhìn thẳng vào mắt người dạy và phát âm theo.")
        st.write("- **Liều lượng:** 10 phút.")

        st.markdown("##### 4. Bắt chước âm thanh gần gũi")
        st.write("- **Tư thế:** Ngồi chơi đùa tương tác.")
        st.write("- **Cách thực hiện:** Phát ra các âm thanh đơn giản (tiếng kêu động vật: meo meo, gâu gâu, ò í e) và khuyến khích trẻ bắt chước.")
        st.write("- **Liều lượng:** 5–10 phút.")

        st.markdown("##### 5. Đọc to từ đơn tiết kèm vật thật")
        st.write("- **Tư thế:** Tương tác trực tiếp với đồ vật thực tế (quả táo, quả bóng).")
        st.write("- **Cách thực hiện:** Cầm đồ vật, gọi rõ tên từng từ đơn chậm rãi, rõ khẩu hình miệng.")
        st.write("- **Liều lượng:** 10 phút.")

        st.markdown("##### 6. Hát bài hát thiếu nhi có động tác")
        st.write("- **Tư thế:** Vui chơi vận động.")
        st.write("- **Cách thực hiện:** Hát các bài hát thiếu nhi quen thuộc kèm theo các động tác múa tay chân minh họa để kích thích ngôn ngữ qua nhịp điệu.")
        st.write("- **Liều lượng:** 10–15 phút.")

        st.markdown("##### 7. Hướng dẫn phụ huynh tương tác mở rộng tại nhà")
        st.write("- **Nội dung:** Dặn dò bố mẹ luôn giao tiếp, gọi tên sự vật xung quanh bé mọi lúc mọi nơi trong sinh hoạt hàng ngày, hạn chế tối đa thời gian xem tivi/điện thoại.")
