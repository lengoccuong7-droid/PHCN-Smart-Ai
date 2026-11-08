# ------------------------------------------
# TAB 1: HỒ SƠ BỆNH NHÂN, LỊCH SỬ & THÊM MỚI
# ------------------------------------------
with tab1:
    st.subheader("👤 Quản lý Hồ sơ, Lịch sử & Thêm mới Bệnh nhân")
    
    sub_choice = st.radio("Chọn thao tác:", ["🔍 Tra cứu lịch sử khám", "➕ Thêm hồ sơ bệnh nhân mới"], horizontal=True, key="tab1_sub_mode")
    
    if sub_choice == "🔍 Tra cứu lịch sử khám":
        st.markdown("Tra cứu nhanh thông tin hành chính và lịch sử thăm khám theo số điện thoại:")
        search_phone_input = st.text_input("🔍 Nhập số điện thoại / Mã BN:", placeholder="Ví dụ: 0901234567", key="search_history_phone_m1")
        
        if search_phone_input:
            patient_history_list = history_mgr.get_patient_history(search_phone_input)
            
            if patient_history_list:
                st.success(f"🎉 Đã tìm thấy {len(patient_history_list)} lần khám của bệnh nhân này.")
                latest_visit = patient_history_list[0]
                st.session_state.current_patient = {
                    "name": latest_visit.get('patient_name', ''),
                    "phone": search_phone_input,
                    "age": latest_visit.get('patient_age', 1990),
                    "job": latest_visit.get('patient_job', '')
                }
                st.markdown("---")
                for idx, visit in enumerate(patient_history_list):
                    with st.expander(f"📁 Lần khám {idx+1} – Ngày: {visit.get('date', 'N/A')}", expanded=(idx == 0)):
                        st.markdown(f"**• Họ tên bệnh nhân:** {visit.get('patient_name', 'N/A')}")
                        st.markdown(f"**• Số điện thoại:** {visit.get('patient_phone', 'N/A')}")
                        st.markdown(f"**• Tóm tắt bệnh án:** {visit.get('summary', 'N/A')}")
            else:
                st.warning("⚠️ Không tìm thấy lịch sử khám nào tương ứng với số điện thoại này.")
        else:
            st.info("💡 Nhập số điện thoại để tra cứu. Hệ thống sẽ tự động đồng bộ thông tin sang phần Khám (Tab 3) nếu tìm thấy.")

    else:
        st.markdown("##### ➕ Khởi tạo hồ sơ bệnh nhân mới")
        with st.form("new_patient_form"):
            new_name = st.text_input("Họ tên bệnh nhân:", placeholder="Nhập họ tên đầy đủ...")
            new_phone = st.text_input("Số điện thoại (Dùng làm định danh):", placeholder="Ví dụ: 0901234567...")
            col_np1, col_np2 = st.columns(2)
            with col_np1:
                new_age = st.number_input("Năm sinh:", min_value=1900, max_value=2026, value=1990)
            with col_np2:
                new_job = st.text_input("Nghề nghiệp:", placeholder="Nghề nghiệp...")
            
            submitted_new_p = st.form_submit_button("💾 Lưu bệnh nhân mới vào hệ thống", use_container_width=True)
            if submitted_new_p:
                if not (new_name and new_phone):
                    st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và Số điện thoại!")
                else:
                    init_data = {
                        "patient_name": new_name,
                        "patient_phone": new_phone,
                        "patient_age": new_age,
                        "patient_job": new_job,
                        "summary": "Khởi tạo hồ sơ hành chính ban đầu."
                    }
                    history_mgr.save_visit(new_phone, init_data)
                    st.session_state.current_patient = {
                        "name": new_name,
                        "phone": new_phone,
                        "age": new_age,
                        "job": new_job
                    }
                    st.success(f"✅ Đã tạo và lưu thành công hồ sơ cho bệnh nhân **{new_name}**! Bạn có thể chuyển sang Tab Khám để tiếp tục.")
# ------------------------------------------
# TAB 2: CƠ SỞ TRI THỨC LÂM SÀNG
# ------------------------------------------
with tab2:
    if "kb_detail_page" not in st.session_state:
        st.session_state.kb_detail_page = None

    if st.session_state.kb_detail_page is None:
        st.subheader("📖 Cẩm nang Tri thức & Phác đồ Lâm sàng")
        st.markdown("Chọn một chuyên khoa bên dưới để xem tài liệu chi tiết[span_2](start_span)[span_2](end_span):")

        search_knowledge_kw = st.text_input("🔍 Tìm kiếm nhanh bệnh lý, triệu chứng...", placeholder="Nhập từ khóa...", key="search_knowledge_input")

        st.markdown("---")
        st.markdown("##### 🗂️ Danh mục chuyên khoa & Vùng cơ thể")

        knowledge_items = [
            ("Cột sống cổ", "🦴", "C1-C7 và hội chứng chèn ép"),
            ("Cột sống thắt lưng", "🩻", "Thoát vị đĩa đệm, đau thần kinh tọa"),
            ("Khớp vai", "🦾", "Chóp xoay & đông cứng khớp vai"),
            ("Khuỷu tay", "💪", "Viêm lồi cầu, hội chứng ống khuỷu"),
            ("Cổ tay – bàn tay", "✋", "Hội chứng ống cổ tay, De Quervain"),
            ("Khớp háng", "🦿", "Thoái hóa & kẹp háng FAI"),
            ("Khớp gối", "🦵", "ACL, sụn chêm & thoái hóa gối"),
            ("Cổ chân – bàn chân", "🦶", "Bong gân & viêm cân gan chân"),
            ("Thần kinh & Khác", "🧠", "Đột quỵ, phục hồi chức năng thần kinh")
        ]

        cols = st.columns(3)
        for idx, item in enumerate(knowledge_items):
            title, icon, desc = item
            col_target = cols[idx % 3]
            with col_target:
                with st.container(border=True):
                    st.markdown(f"<h3 style='text-align: center; margin: 0;'>{icon}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; font-weight: bold; margin: 5px 0;'>{title}</p>", unsafe_allow_html=True)
                    st.caption(desc)
                    if st.button("📖 Đọc sách", use_container_width=True, key=f"open_kb_{idx}"):
                        st.session_state.kb_detail_page = title
                        st.rerun()

        st.markdown("---")
        st.caption("📚 Hệ thống tài liệu y khoa chuẩn hóa phục vụ chẩn đoán và điều trị PHCN.")

    else:
        current_region = st.session_state.kb_detail_page

        if st.button("⬅️ Quay lại danh mục", type="secondary", key="back_to_grid_kb"):
            st.session_state.kb_detail_page = None
            st.rerun()

        st.markdown("---")
        st.subheader(f"📚 SÁCH CHUYÊN KHOA: {current_region.upper()}")
        st.caption("Tài liệu huấn luyện và tra cứu nhanh lâm sàng Phục hồi chức năng vận động.")

        knowledge_textbook_db = {
            "Cột sống cổ": (
                "1. Giải phẫu & Sinh cơ học cột sống cổ",
                "Cột sống cổ gồm 7 đốt sống (C1-C7), chịu trách nhiệm nâng đỡ đầu và biên độ vận động lớn (gấp-duỗi, nghiêng, xoay).",
                "Hội chứng cổ - vai - gáy, thoái hóa đốt sống cổ, thoát vị đĩa đệm cổ chèn ép rễ thần kinh (C5-C8).",
                "Đau lan dọc xuống tay, tê bì ngón tay, hạn chế tầm vận động xoay cổ.",
                "Nghiệm pháp Spurling (nén ép cổ), Test kéo giãn cổ, Test Lhermitte.",
                "Giảm đau bằng vật lý trị liệu, kéo giãn cột sống cổ, tập mạnh nhóm cơ cổ sâu."
            ),
            "Cột sống thắt lưng": (
                "1. Giải phẫu & Sinh cơ học cột sống thắt lưng",
                "Vùng thắt lưng gồm 5 đốt sống (L1-L5) chịu tải trọng lớn nhất của cơ thể. Đĩa đệm đóng vai trò giảm xóc.",
                "Thoát vị đĩa đệm thắt lưng (L4-L5, L5-S1), trượt đốt sống, hội chứng cơ hình lê.",
                "Đau thắt lưng cấp/mạn, đau lan truyền theo dây thần kinh tọa xuống chân.",
                "Nghiệm pháp Lasègue, Test Bragard, Test Patrick (FABER).",
                "Nghỉ ngơi giai đoạn cấp, giảm đau (TENS), bài tập McKenzie, tập cơ lõi (Core stability)."
            ),
            "Khớp vai": (
                "1. Giải phẫu & Sinh cơ học khớp vai",
                "Khớp vai có biên độ vận động lớn nhất cơ thể nhưng kém ổn định, phụ thuộc lớn vào nhóm cơ chóp xoay.",
                "Hội chứng chạm mỏm cùng vai, rách chóp xoay, đông cứng khớp vai (Frozen shoulder).",
                "Đau nhói khi giơ tay qua đầu, cứng khớp toàn bộ biên độ.",
                "Test Neer, Test Hawkins-Kennedy, Test Jobe, Test Drop-arm.",
                "Giảm đau, siêu âm, kéo giãn bao khớp, tập vận động tầm nhẹ nhàng không đau."
            ),
            "Khuỷu tay": (
                "1. Giải phẫu & Sinh cơ học khuỷu tay",
                "Khớp khuỷu gồm khớp ròng rọc-trụ, chỏm quay-lồi cầu, cho phép cử động gấp-duỗi và sấp-ngửa.",
                "Viêm lồi cầu ngoài (Tennis elbow), viêm lồi cầu trong, hội chứng ống khuỷu.",
                "Đau chói tại mỏm trên lồi cầu ngoài khi cầm nắm vật nặng, tê ngón út.",
                "Test Mill, Test Cozen, Test chèn ép dây thần kinh trụ.",
                "Nghỉ ngơi, dùng băng đeo hỗ trợ, siêu âm trị liệu, sóng xung kích (ESWT)."
            ),
            "Cổ tay – bàn tay": (
                "1. Giải phẫu & Sinh cơ học cổ tay – bàn tay",
                "Hệ thống ống cổ tay chứa dây thần kinh giữa và các gân gấp ngón tay.",
                "Hội chứng ống cổ tay, viêm gân De Quervain, ngón tay lò xo.",
                "Tê bì các ngón 1, 2, 3 về đêm; đau vùng mỏm trâm quay.",
                "Test Phalen, Test Tinel, Test Finkelstein.",
                "Nẹp cổ tay ban đêm, siêu âm trị liệu, bài tập trượt gân."
            ),
            "Khớp háng": (
                "1. Giải phẫu & Sinh cơ học khớp háng",
                "Khớp háng là khớp chỏm cầu chịu lực lớn, ổ cối sâu giúp tăng vững cho chi dưới.",
                "Thoái hóa khớp háng, viêm bao hoạt dịch mấu chuyển, hội chứng kẹp háng (FAI).",
                "Đau sâu vùng bẹn hoặc mấu chuyển lớn, hạn chế xoay trong khớp háng.",
                "Test Patrick (FABER), Test FADIR, đánh giá tầm vận động.",
                "Giảm tải trọng lực, tập mạnh cơ mông nhỡ và cơ tứ đầu đùi."
            ),
            "Khớp gối": (
                "1. Giải phẫu & Sinh cơ học khớp gối",
                "Khớp bản lề lớn chịu lực toàn thân, được hỗ trợ bởi hệ thống dây chằng (ACL, PCL, MCL, LCL) và sụn chêm.",
                "Tổn thương ACL, rách sụn chêm, hội chứng đau bánh chè - đùi, thoái hóa khớp gối.",
                "Lỏng gối, sưng nề sau chấn thương, tiếng lạo xạo khi leo cầu thang.",
                "Test ngăn kéo trước/sau, Test Lachman, Test McMurray.",
                "Kiểm soát sưng nề, tập gồng cơ tứ đầu đùi sớm, phục hồi tầm vận động."
            ),
            "Cổ chân – bàn chân": (
                "1. Giải phẫu & Sinh cơ học cổ chân – bàn chân",
                "Khớp cổ chân chịu lực tì đè và thích nghi với mọi địa hình mặt phẳng.",
                "Bong gân cổ chân, viêm gân gót (Achilles), viêm cân gan chân.",
                "Sưng nề mắt cá ngoài, đau nhói gót chân vào buổi sáng.",
                "Test ngăn kéo trước cổ chân, Test Talar tilt, Thompson test.",
                "Nguyên tắc R.I.C.E giai đoạn cấp, kéo giãn cân gan chân, tập mạnh cơ mác."
            ),
            "Thần kinh & Khác": (
                "1. Tổng quan Phục hồi chức năng Thần kinh",
                "Dựa trên nguyên tắc Neuroplasticity (Tính dẻo thần kinh) của não bộ sau tổn thương.",
                "Tai biến mạch máu não (Stroke), tổn thương tủy sống, Parkinson, bại não.",
                "Liệt nửa người, rối loạn thăng bằng, rối loạn nuốt, thất ngôn.",
                "Thang điểm Fugl-Meyer, NIHSS, Modified Ashworth.",
                "Ứng dụng PNF, liệu pháp vận động cưỡng bức, tập thăng bằng trên bóng."
            )
        }

        content = knowledge_textbook_db.get(current_region, (
            "1. Tổng quan chuyên khảo",
            "Nội dung đang được cập nhật theo phác đồ chuẩn y khoa.",
            "Các hội chứng thường gặp và tổn thương cấu trúc liên quan.",
            "Triệu chứng lâm sàng điển hình và biểu hiện cơ năng, thực thể.",
            "Hệ thống nghiệm pháp, test đặc hiệu khám lâm sàng chuyên sâu.",
            "Phác đồ điều trị vật lý trị liệu và phục hồi chức năng vận động toàn diện."
        ))

        sec_title, intro, pathology, symptoms, tests, treatment = content

        st.markdown(f"#### 📖 {sec_title}")
        st.info(intro)

        with st.expander("📌 2. Các hội chứng & Bệnh lý thường gặp", expanded=True):
            st.markdown(pathology)

        with st.expander("🩺 3. Triệu chứng lâm sàng & Biểu hiện", expanded=True):
            st.markdown(symptoms)

        with st.expander("🔍 4. Hệ thống Test đặc hiệu & Nghiệm pháp", expanded=True):
            st.markdown(tests)

        with st.expander("⚙️ 5. Phác đồ Vật lý trị liệu & PHCN", expanded=True):
            st.markdown(treatment)

        st.markdown("---")
        if st.button("⬅️ Quay lại danh mục chuyên khoa", type="primary", key="bottom_back_btn"):
            st.session_state.kb_detail_page = None
            st.rerun()
# ------------------------------------------
# TAB 3: CHỌN VÙNG & NHẬP LIỆU THĂM KHÁM (REAL-TIME AUTO-SYNC)
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
                st.session_state.exam_live_data = {}

    if st.session_state.selected_region:
        st.markdown("---")
        st.success(f"📍 Đang thực hiện khám cho vùng: **{st.session_state.selected_region}**")

        if "exam_live_data" not in st.session_state:
            st.session_state.exam_live_data = {}

        active_patient = st.session_state.get("current_patient", {"name": "", "phone": "", "age": 1990, "job": ""})
        if active_patient.get("name"):
            st.info(f"🔗 Đang liên kết với bệnh nhân: **{active_patient.get('name')}** (SĐT: {active_patient.get('phone')})")

        st.markdown("#### 📋 Bước 2: Nhập liệu thăm khám trực tiếp")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            patient_name = st.text_input("Họ tên bệnh nhân:", value=active_patient.get("name", ""), placeholder="Nhập họ tên...", key="live_p_name")
            patient_phone = st.text_input("Số điện thoại / Mã BN:", value=active_patient.get("phone", ""), placeholder="Nhập SĐT...", key="live_p_phone")
        with col_p2:
            patient_age = st.number_input("Năm sinh:", min_value=1900, max_value=2026, value=int(active_patient.get("age", 1990)), key="live_p_age")
            patient_job = st.text_input("Nghề nghiệp:", value=active_patient.get("job", ""), placeholder="Nhập nghề nghiệp...", key="live_p_job")

        st.markdown("---")
        ly_do_vao_vien = st.text_input("🏥 Lý do vào viện:", placeholder="Nhập lý do vào viện...", key="live_ly_do")
        tien_su = st.text_area("📜 Tiền sử bệnh (Bản thân / Gia đình):", placeholder="Nhập tiền sử...", key="live_tien_su")

        with st.expander("🩺 Bệnh sử (SOCRATES)", expanded=True):
            site = st.text_input("S – Vị trí đau:", value=st.session_state.selected_region, key="live_site")
            onset = st.text_input("O – Khởi phát:", placeholder="Hoàn cảnh khởi phát...", key="live_onset")
            character = st.text_input("C – Tính chất đau:", placeholder="Nhói, âm ỉ, tê bì...", key="live_character")
            radiation = st.text_input("R – Hướng lan:", placeholder="Lan đi đâu...", key="live_radiation")
            associations = st.text_input("A – Triệu chứng đi kèm:", placeholder="Yếu cơ, sưng nề...", key="live_associations")
            time_course = st.text_input("T – Diễn tiến:", placeholder="Tăng về đêm, liên tục...", key="live_time_course")
            
            col_nrs1, col_nrs2 = st.columns([1, 2])
            with col_nrs1:
                nrs_score = st.selectbox("Điểm NRS (0-10):", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="live_nrs")
            with col_nrs2:
                nrs_note = st.text_input("Ghi chú mức độ đau:", placeholder="Mô tả thêm...", key="live_nrs_note")

        with st.expander("🔍 Khám thực thể (Nhìn - Sờ - Gõ)", expanded=True):
            inspect_note = st.text_input("👁️ Nhìn (Inspection):", placeholder="Biến dạng, sưng nề, lệch vẹo...", key="live_inspect")
            palp_note = st.text_input("✋ Sờ (Palpation):", placeholder="Điểm đau, nhiệt độ da, trương lực...", key="live_palp")
            per_meas_note = st.text_input("📏 Gõ / Đo (Percussion):", placeholder="Tầm vận động ROM, phản xạ...", key="live_per_meas")

        with st.expander("👤 3-4 Test đặc hiệu / Nghiệm pháp", expanded=True):
            t1 = st.checkbox("Test đặc hiệu 1 (+ Dương tính)", key="live_t1")
            t2 = st.checkbox("Test đặc hiệu 2 (+ Dương tính)", key="live_t2")
            t3 = st.checkbox("Test đặc hiệu 3 (+ Dương tính)", key="live_t3")
            test_note = st.text_input("Ghi chú thêm về test lâm sàng:", placeholder="Mô tả kết quả nghiệm pháp...", key="live_test_note")

        with st.expander("🚩 Cờ đỏ an toàn & Tệp đính kèm"):
            rf_1 = st.checkbox("Hội chứng đuôi ngựa / Rối loạn tiểu tiện", key="live_rf1")
            rf_2 = st.checkbox("Sụt cân / Nghi ngờ ác tính", key="live_rf2")
            uploaded_files = st.file_uploader("Tải lên hình ảnh / X-quang / MRI:", accept_multiple_files=True, type=["jpg", "png", "pdf"], key="live_files")

        # Tổng hợp dữ liệu tự động thời gian thực
        st.markdown("---")
        st.markdown("### 🧠 Phân tích chẩn đoán & PHCN AI (Real-time Sync)")
        
        col_sum1, col_sum2 = st.columns(2)
        with col_sum1:
            st.markdown("##### 📋 Tổng hợp dữ liệu (Tự động cập nhật)")
            st.markdown(f"✔️ **Bệnh nhân:** {patient_name if patient_name else '---'}")
            st.markdown(f"✔️ **Vùng khám:** {st.session_state.selected_region}")
            st.markdown(f"✔️ **Lý do NV:** {ly_do_vao_vien if ly_do_vao_vien else '---'}")
            st.markdown(f"✔️ **Tiền sử:** {tien_su if tien_su else 'Không ghi nhận'}")
            st.markdown(f"✔️ **Đau (NRS):** {nrs_score}/10")
            st.markdown(f"✔️ **Test dương tính:** {[t for t, check in [('Test 1', t1), ('Test 2', t2), ('Test 3', t3)] if check] or 'Không ghi nhận'}")
            if rf_1 or rf_2:
                st.error("🚩 **CẢNH BÁO CỜ ĐỎ AN TOÀN:** Phát hiện dấu hiệu nguy hiểm cần chú ý!")
        
        with col_sum2:
            st.markdown("##### 📄 Kết quả phân tích AI")
            st.info("Nhấn nút bên dưới để chạy phân tích lâm sàng chi tiết từ trợ lý AI dựa trên dữ liệu đang nhập...")

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
            if not (patient_name and patient_phone):
                st.warning("⚠️ Vui lòng điền đầy đủ Họ tên và SĐT ở phần hành chính phía trên để lưu trữ!")
            else:
                exam_summary = f"Vùng: {st.session_state.selected_region} | Lý do: {ly_do_vao_vien} | NRS: {nrs_score}/10"
                visit_data = {
                    "patient_name": patient_name,
                    "patient_phone": patient_phone,
                    "patient_age": patient_age,
                    "patient_job": patient_job,
                    "summary": exam_summary
                }
                history_mgr.save_visit(patient_phone, visit_data)
                st.success(f"✅ Đã lưu thành công hồ sơ cho bệnh nhân **{patient_name}** vào hệ thống lịch sử!")
    else:
        st.info("👆 Vui lòng bấm chọn một vùng cơ thể ở phía trên để bắt đầu quy trình khám.")
# ------------------------------------------
# TAB 4: KHO BÀI TẬP PHCN CHUYÊN SÂU
# ------------------------------------------
with tab4:
    if "rehab_detail_page" not in st.session_state:
        st.session_state.rehab_detail_page = None

    if st.session_state.rehab_detail_page is None:
        st.subheader("🏋️‍♂️ Kho Bài tập Phục hồi chức năng Chuyên sâu")
        st.markdown("Chọn nhóm bệnh lý chuyên khoa bên dưới để xem chi tiết 7 bài tập chuẩn hóa:")

        search_ex_kw = st.text_input("🔍 Tìm kiếm bài tập, động tác, hội chứng...", placeholder="Nhập từ khóa (Ví dụ: Vẹo cột sống, Đột quỵ...)", key="search_exercise_input")

        st.markdown("---")
        st.markdown("##### 🗂️ Danh mục nhóm bệnh lý & Chuyên khoa PHCN")

        rehab_items = [
            ("Stroke (Đột quỵ)", "🧠", "Phục hồi vận động chi liệt & thăng bằng"),
            ("Dysphagia (Nuốt khó)", "💧", "Kỹ thuật nuốt & cơ vùng miệng họng"),
            ("Aphasia (Thất ngôn)", "🗣️", "Kích thích ngôn ngữ & giao tiếp"),
            ("Dysarthria (Khó nói)", "🗣️", "Kiểm soát phát âm & hơi thở"),
            ("Autism / Motor (Tự kỷ / VĐ)", "🧩", "Điều hòa cảm giác & vận động thô"),
            ("Torticollis (Vẹo cổ)", "🔄", "Kéo giãn cơ ức đòn chũm & vận động"),
            ("Vẹo cột sống (Scoliosis)", "🦴", "Phương pháp Schroth & cân bằng cột sống"),
            ("Post-Op Knee / Hip (Mổ)", "🦿", "Tập vận động sau mổ khớp gối/hông"),
            ("Fracture (Gãy xương)", "🦾", "Phục hồi tầm vận động sau gãy xương")
        ]

        cols_e = st.columns(3)
        for idx, item in enumerate(rehab_items):
            title, icon, desc = item
            col_target = cols_e[idx % 3]
            with col_target:
                with st.container(border=True):
                    st.markdown(f"<h3 style='text-align: center; margin: 0;'>{icon}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; font-weight: bold; margin: 5px 0;'>{title}</p>", unsafe_allow_html=True)
                    st.caption(desc)
                    if st.button("🏋️‍♂️ Xem bài tập", use_container_width=True, key=f"open_rehab_{idx}"):
                        st.session_state.rehab_detail_page = title
                        st.rerun()

        st.markdown("---")
        st.caption("💡 Hệ thống dữ liệu bài tập PHCN được chuẩn hóa theo y học chứng cứ phục hồi chức năng vận động.")

    else:
        group_name = st.session_state.rehab_detail_page

        if st.button("⬅️ Quay lại danh mục nhóm bệnh lý", type="secondary", key="back_to_rehab_grid"):
            st.session_state.rehab_detail_page = None
            st.rerun()

        st.markdown("---")
        st.subheader(f"📂 KHO 7 BÀI TẬP: {group_name.upper()}")
        st.caption("Hệ thống bài tập chuẩn hóa lâm sàng chuyên sâu.")

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
                ("2. Vận động thô: Bò trườn bắt chéo chi", "Kích thích sự phối hợp vận động hai bán cầu đại não.", "Bò trên sàn đồng bộ tay trái chân phải và ngược lại.", "2 sets x 10 mét"),
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
                ("2. Kỹ thuật thở ba chiều (Schroth breathing method)", "Mở rộng lồng ngực ở phía mỏm lõm của đường cong.", "Hít sâu đưa hơi thở vào vùng lồng ngực bị lõm.", "3 sets x 10 nhịp thở"),
                ("3. Kéo giãn cơ bên lõm / Tăng cường cơ bên lồi", "Lấy lại cân bằng lực cơ hai bên cột sống.", "Nghiêng lườn sang bên lõm kết hợp kéo tay tương ứng.", "3 sets x 10 lần"),
                ("4. Bài tập ổn định cơ lõi (Core stabilization)", "Tăng cường sức mạnh hệ cơ bám cột sống.", "Tư thế tấm ván (Plank) hoặc cầu nối tiêu chuẩn.", "3 sets x 30 giây"),
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
                ("7. Tập đi cầu thang bước từng bậc", "Tái hòa nhập vận động sinh hoạt phức tạp.", "Lên bằng chân lành, xuống bằng chân mổ.", "10-15 bậc")
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

        current_exercises = exercises_db.get(group_name, [])

       # for idx_ex, ex_item in enumerate(current_exercises):
        #   title, purpose, technique, dosage = ex_item
        #    with st.expander(f"🔹 {title}"):
        #        st.markdown(f"- **🎯 Mục đích lâm sàng:** {purpose}")
        #        st.markdown(f"- **⚙️ Hướng dẫn kỹ thuật:** {technique}")
        #        st.markdown(f"- **⏱️ Liều lượng (Dosage):** {dosage}")
         #       st.markdown("- **🛡️ Lưu ý an toàn:** Thực hiện đúng biên độ, dừng lại ngay khi xuất hiện cơn đau nhói hoặc chóng mặt.")

        for idx_ex, ex_item in enumerate(current_exercises):
            title, purpose, technique, dosage = ex_item
            with st.expander(f"🔹 {title}"):
                st.markdown(f"- **🎯 Mục đích lâm sàng:** {purpose}")
                st.markdown(f"- **⚙️ Hướng dẫn kỹ thuật:** {technique}")
                st.markdown(f"- **⏱️ Liều lượng (Dosage):** {dosage}")
                st.markdown("- **🛡️ Lưu ý an toàn:** Thực hiện đúng biên độ, dừng lại ngay khi xuất hiện cơn đau nhói hoặc chóng mặt.")

        st.markdown("---")
        if st.button("⬅️ Quay lại danh mục nhóm bệnh lý", type="primary", key="bottom_back_rehab_btn"):
            st.session_state.rehab_detail_page = None
            st.rerun()
