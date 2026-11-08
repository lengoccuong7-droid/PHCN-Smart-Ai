# =========================================================
# TAB 3: KHÁM LÂM SÀNG CHUYÊN SÂU (TÍCH HỢP ẢNH LÂM SÀNG & TỜ GIẤY TRẮNG REAL-TIME)
# =========================================================
import streamlit as st

def render(history_mgr):
    if "exam_active_region" not in st.session_state:
        st.session_state.exam_active_region = None

    # MÀN HÌNH 1: LƯỚI NÚT BẤM CHỌN VÙNG KHÁM
    if st.session_state.exam_active_region is None:
        st.subheader("🎯 Chọn Vùng Thăm Khám Lâm Sàng")
        st.markdown("Chọn một vùng cơ thể bên dưới để mở phiếu thăm khám chuyên sâu độc lập:")

        regions = [
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

        cols_r = st.columns(3)
        for idx, item in enumerate(regions):
            title, icon, desc = item
            col_target = cols_r[idx % 3]
            with col_target:
                with st.container(border=True):
                    st.markdown(f"<h3 style='text-align: center; margin: 0;'>{icon}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; font-weight: bold; margin: 5px 0;'>{title}</p>", unsafe_allow_html=True)
                    st.caption(desc)
                    if st.button("🩺 Bắt đầu khám", use_container_width=True, key=f"open_exam_{idx}"):
                        st.session_state.exam_active_region = title
                        st.rerun()
                        
    # MÀN HÌNH 2: TRANG CHI TIẾT KHÁM & TỜ GIẤY TRẮNG ĐỒNG BỘ THỜI GIAN THỰC
    else:
        current_reg = st.session_state.exam_active_region

        if st.button("⬅️ Quay lại chọn vùng khám", type="secondary", key="back_to_exam_grid"):
            st.session_state.exam_active_region = None
            st.rerun()

        st.markdown("---")
        st.subheader(f"📋 PHIẾU KHÁM LÂM SÀNG: {current_reg.upper()}")
        
        # Lấy dữ liệu hành chính tự động đồng bộ từ Tab 1
        active_patient = st.session_state.get("current_patient", {"name": "", "phone": "", "age": 1990, "job": ""})
        if active_patient.get("name"):
            st.info(f"🔗 Đang liên kết tự động từ Tab 1 – Bệnh nhân: **{active_patient.get('name')}** (SĐT: {active_patient.get('phone')})")

        # 1. HÀNH CHÍNH & HỎI BỆNH
        st.markdown("##### ✍️ 1. Hành chính & Lý do khám")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            p_name = st.text_input("Họ tên bệnh nhân:", value=active_patient.get("name", ""), placeholder="Nhập họ tên...", key="rt_p_name")
            p_phone = st.text_input("Số điện thoại:", value=active_patient.get("phone", ""), placeholder="Nhập SĐT...", key="rt_p_phone")
        with col_p2:
            p_age = st.number_input("Năm sinh:", min_value=1900, max_value=2026, value=int(active_patient.get("age", 1990)), key="rt_p_age")
            p_job = st.text_input("Nghề nghiệp:", value=active_patient.get("job", ""), placeholder="Nhập nghề nghiệp...", key="rt_p_job")

        ly_do = st.text_input("🏥 Lý do vào viện / Than phiền chính:", placeholder="Ví dụ: Đau vai lan xuống tay, hạn chế xoay cổ...", key="rt_ly_do")
        tien_su = st.text_area("📜 Tiền sử bệnh (Bản thân / Gia đình / Chấn thương):", placeholder="Nhập tiền sử...", key="rt_tien_su")

        with st.expander("🩺 2. Bệnh sử (Quy trình SOCRATES)", expanded=True):
            onset = st.text_input("O (Onset) – Khởi phát:", placeholder="Hoàn cảnh xuất hiện...", key="rt_onset")
            character = st.text_input("C (Character) – Tính chất đau:", placeholder="Nhói, âm ỉ, tê bì...", key="rt_char")
            radiation = st.text_input("R (Radiation) – Hướng lan:", placeholder="Lan dọc cánh tay...", key="rt_rad")
            associations = st.text_input("A (Associations) – Triệu chứng kèm theo:", placeholder="Teo cơ, yếu sức...", key="rt_assoc")
            
            col_nrs1, col_nrs2 = st.columns([1, 2])
            with col_nrs1:
                nrs = st.selectbox("Mức độ đau NRS (0-10):", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="rt_nrs")
            with col_nrs2:
                nrs_note = st.text_input("Ghi chú thêm mức độ đau:", placeholder="Đau tăng về đêm...", key="rt_nrs_note")

        # 2. KHÁM THỰC THỂ: NHÌN - SỜ - ĐO (ROM)
        with st.expander("🔍 3. Khám thực thể (Nhìn – Sờ – Đo ROM)", expanded=True):
            inspect = st.text_area("👁️ NHÌN (Inspection):", placeholder="Quan sát biến dạng, lệch vẹo tư thế, sưng nề, teo cơ...", key="rt_inspect")
            palp = st.text_area("✋ SỜ (Palpation):", placeholder="Xác định điểm đau chói, trương lực cơ...", key="rt_palp")
            rom_meas = st.text_area("📏 ĐO / GÕ (ROM & Phản xạ):", placeholder="Tầm vận động khớp, lực cơ MMT, phản xạ gân xương...", key="rt_rom")

        # 3. MỤC TẢI LÊN / CHỤP HÌNH ẢNH LÂM SÀNG (X-QUANG, TƯ THẾ, TỔN THƯƠNG)
        with st.expander("🖼️ 4. Hình ảnh Lâm sàng & Cận lâm sàng (X-quang, MRI, Dáng đi, Tư thế)", expanded=True):
            st.caption("Tải tệp ảnh có sẵn hoặc chụp hình trực tiếp từ máy tính/điện thoại:")
            
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                uploaded_image = st.file_uploader("📤 Tải ảnh X-quang / MRI / Tổn thương:", type=["png", "jpg", "jpeg"], key="rt_uploaded_img")
            with col_img2:
                camera_image = st.camera_input("📷 Chụp hình ảnh lâm sàng trực tiếp:", key="rt_camera_img")
            
            selected_img = uploaded_image if uploaded_image is not None else camera_image
            if selected_img is not None:
                st.image(selected_img, caption="🖼️ Hình ảnh lâm sàng được ghi nhận", use_container_width=True)

        # 4. TEST ĐẶC HIỆU TỰ ĐỘNG THEO VÙNG (CÓ CÔNG DỤNG, KỸ THUẬT & NHẬP KẾT QUẢ)
        with st.expander(f"🧬 5. Nghiệm pháp / Test đặc hiệu chuyên khoa ({current_reg})", expanded=True):
            st.caption("Đánh giá các test lâm sàng đặc hiệu có sẵn cho vùng cơ thể này:")

            specific_tests_db = {
                "Cột sống cổ": [
                    ("Spurling Test", "Kiểm tra chèn ép rễ thần kinh cổ", "Bệnh nhân ngồi, nghiêng đầu sang bên đau. Bác sĩ ấn nhẹ từ đỉnh đầu xuống."),
                    ("Distraction Test (Test kéo giãn cổ)", "Đánh giá giảm chèn ép rễ khi giải phóng áp lực", "Bệnh nhân nằm/ngồi, bác sĩ nâng cằm và chẩm kéo nhẹ lên trên."),
                    ("Lhermitte Sign", "Đánh giá tổn thương tủy cổ / xơ cứng rải rác", "Bệnh nhân gập cổ tối đa chủ động. Xem có cảm giác như điện giật dọc sống lưng.")
                ],
                "Cột sống thắt lưng": [
                    ("Lasègue Test (SLR - Nâng chân thẳng)", "Đánh giá kích thích rễ thần kinh tọa (L4-S1)", "Nằm ngửa, nâng thẳng chân bệnh nhân lên. Dương tính khi đau nhói <70 độ."),
                    ("Bragard Test", "Xác định rõ tổn thương gốc rễ thần kinh", "Nâng chân tới góc đau trong Lasègue, hạ nhẹ 5 độ rồi gập lưng cổ chân đột ngột."),
                    ("Patrick / FABER Test", "Phân biệt tổn thương khớp háng hay khớp cùng chậu", "Nằm ngửa, chân gập gối đặt cổ chân lên gối bên kia, ấn gối xuống mặt giường.")
                ],
                "Khớp vai": [
                    ("Neer Test", "Đánh giá hội chứng chạm mỏm cùng vai", "Cố định xương bả vai, đưa tay bệnh nhân xoay trong và gập tối đa lên trên."),
                    ("Hawkins-Kennedy Test", "Đánh giá chèn ép gân cơ trên gai dưới mỏm cùng", "Gập vai 90 độ, gập khuỷu 90 độ, bác sĩ thực hiện xoay trong cẳng tay đột ngột."),
                    ("Jobe Test (Empty Can)", "Đánh giá rách/viêm gân cơ trên gai (Supraspinatus)", "Dang vai 90 độ, xoay trong ngón cái hướng xuống đất, ấn tay xuống chống lại lực giữ.")
                ],
                "Khuỷu tay": [
                    ("Cozen Test", "Đánh giá viêm lồi cầu ngoài (Tennis Elbow)", "Cố định khuỷu, bệnh nhân nắm tay, duỗi cổ tay có kháng trở từ bác sĩ."),
                    ("Mill Test", "Đánh giá co kéo gân duỗi tại lồi cầu ngoài", "Bác sĩ sấp cẳng tay, gập cổ tay và duỗi thẳng khuỷu tay bệnh nhân."),
                    ("Tinel Sign tại ống khuỷu", "Kiểm tra chèn ép dây thần kinh trụ tại mỏm trên lồi cầu trong", "Dùng ngón tay/búa phản xạ gõ nhẹ vào rãnh thần kinh trụ ở khuỷu tay.")
                ],
                "Cổ tay – bàn tay": [
                    ("Phalen Test", "Đánh giá hội chứng ống cổ tay (Chèn ép dây TK giữa)", "Ấn lưng hai bàn tay vào nhau, gập cổ tay tối đa 90 độ trong 60 giây."),
                    ("Tinel Sign cổ tay", "Kiểm tra chèn ép dây thần kinh giữa tại ống cổ tay", "Gõ nhẹ vào vùng dây nẹp chằng vòng cổ tay mặt trước."),
                    ("Finkelstein Test", "Đánh giá viêm gân De Quervain (Gân duỗi/dạng ngắn ngón cái)", "Bệnh nhân gấp ngón cái vào lòng bàn tay, nắm các ngón còn lại rồi nghiêng trụ cổ tay.")
                ],
                "Khớp háng": [
                    ("FADIR Test", "Đánh giá kẹp háng (FAI) hoặc rách sụn bọc ổ cối", "Gập háng 90 độ, khép háng và xoay trong khớp háng."),
                    ("Thomas Test", "Đánh giá co rút cơ thắt lưng chậu (Iliopsoas)", "Nằm ngửa, co tối đa một bên gối áp sát ngục. Xem chân còn lại có bị hổng khỏi mặt giường."),
                    ("Trendelenburg Test", "Đánh giá yếu cơ mông nhỡ (Gluteus medius)", "Bệnh nhân đứng một chân. Quan sát xem khung chậu bên đối diện có bị xệ xuống.")
                ],
                "Khớp gối": [
                    ("Lachman Test", "Đánh giá đứt dây chằng chéo trước (ACL) - Độ chính xác cao nhất", "Gập gối 20-30 độ, một tay giữ đùi, một tay kéo mâm chày ra trước."),
                    ("Anterior Drawer Test (Ngăn kéo trước)", "Kiểm tra độ vững dây chằng chéo trước (ACL)", "Gập gối 90 độ, ngồi lên bàn chân bệnh nhân, kéo mạnh mâm chày ra trước."),
                    ("McMurray Test", "Đánh giá tổn thương rách sụn chêm gối", "Gập gối tối đa, vừa xoay cẳng tay ra ngoài/vào trong vừa duỗi gối dần ra.")
                ],
                "Cổ chân – bàn chân": [
                    ("Anterior Drawer Cổ chân", "Đánh giá đứt dây chằng sên-mác trước", "Một tay giữ cẳng chân, một tay kéo gót chân ra trước ở tư thế gấp nhẹ mặt lòng."),
                    ("Thompson Test", "Kiểm tra đứt gân gót (Achilles tendon)", "Nằm sấp, bóp mạnh vào cơ bắp chân. Nếu bàn chân không gấp mặt lòng -> Dương tính (+)."),
                    ("Talar Tilt Test", "Đánh giá dây chằng mác-gót", "Lật trong bàn chân ở tư thế cổ chân trung tính để kiểm tra độ lỏng khớp.")
                ],
                "Thần kinh & Khác": [
                    ("Thang điểm Fugl-Meyer", "Đánh giá mức độ phục hồi vận động sau đột quỵ", "Lượng giá chi trên/chi dưới theo các chuỗi vận động tách biệt."),
                    ("Modified Ashworth Scale (MAS)", "Đánh giá mức độ co cứng trương lực cơ (Độ 0 đến 4)", "Gập duỗi thụ động chi thể nhanh để kiểm tra sức kháng trương lực cơ."),
                    ("Babinski Sign", "Đánh giá tổn thương bó tháp (Thần kinh trung ương)", "Vạch nhẹ bờ ngoài lòng bàn chân từ gót lên ngón út rồi vòng sang ngón cái.")
                ]
            }

            active_tests = specific_tests_db.get(current_reg, [
                ("Test đặc hiệu 1", "Đánh giá tổn thương cấu trúc vùng", "Thực hiện kỹ thuật khám chuẩn."),
                ("Test đặc hiệu 2", "Kiểm tra độ vững khớp/dây chằng", "Thực hiện theo quy trình lâm sàng.")
            ])

            test_results = {}
            for t_idx, (t_name, t_use, t_tech) in enumerate(active_tests):
                st.markdown(f"**🔹 {t_idx+1}. {t_name}**")
                st.caption(f"• **Công dụng:** {t_use}  \n• **Kỹ thuật:** {t_tech}")
                
                res = st.radio(f"Nhập kết quả {t_name}:", ["Chưa làm / Âm tính (-)", "Dương tính (+)"], horizontal=True, key=f"ex_t_res_{t_idx}")
                test_results[t_name] = res
                st.markdown("---")

        with st.expander("🚩 6. Cờ đỏ an toàn lâm sàng (Red Flags)"):
            rf_1 = st.checkbox("Hội chứng đuôi ngựa / Rối loạn cơ tròn", key="rt_rf1")
            rf_2 = st.checkbox("Sụt cân nhanh không rõ nguyên nhân / Tiền sử ung thư", key="rt_rf2")
            rf_3 = st.checkbox("Sốt cao, sưng nóng đỏ đau cấp tính", key="rt_rf3")

        # 5. TỜ GIẤY TRẮNG TỔNG HỢP & PHÂN TÍCH AI (REAL-TIME AUTO-SYNC)
        st.markdown("---")
        st.markdown("### 🧠 TỜ GIẤY TRẮNG TỔNG HỢP & PHÂN TÍCH AI (Real-time)")

        has_pos_test = any([v == "Dương tính (+)" for v in test_results.values()])
        is_blank = not (p_name or ly_do or tien_su or onset or character or inspect or palp or rom_meas or has_pos_test or rf_1 or rf_2 or rf_3 or (nrs > 0) or (selected_img is not None))

        if is_blank:
            st.info("📄 *[Tờ giấy trắng]* — Chưa có dữ liệu. Mọi thông tin hành chính từ Tab 1 và dữ liệu thăm khám/hình ảnh nhập phía trên sẽ tự động đồng bộ hiển thị tại đây theo thời gian thực.")
        else:
            col_sum1, col_sum2 = st.columns(2)
            with col_sum1:
                st.markdown("##### 📋 Tóm tắt ca bệnh (Đồng bộ thời gian thực)")
                if p_name: 
                    st.markdown(f"• **Họ tên bệnh nhân:** {p_name}")
                st.markdown(f"• **Năm sinh:** {p_age} | **Nghề nghiệp:** {p_job if p_job else 'Chưa cập nhật'}")
                st.markdown(f"• **Vùng khám chuyên khoa:** {current_reg}")
                if ly_do: st.markdown(f"• **Lý do khám:** {ly_do}")
                if tien_su: st.markdown(f"• **Tiền sử:** {tien_su}")
                if character: st.markdown(f"• **Bệnh sử (SOCRATES):** {character} (Mức đau NRS: {nrs}/10)")
                if inspect: st.markdown(f"• **Nhìn (Inspection):** {inspect}")
                if palp: st.markdown(f"• **Sờ (Palpation):** {palp}")
                if rom_meas: st.markdown(f"• **Đo (ROM/Phản xạ):** {rom_meas}")
                
                if selected_img is not None:
                    st.markdown("• **Hình ảnh lâm sàng:** Đã đính kèm 1 hình ảnh (X-quang/Tư thế).")
                    st.image(selected_img, width=150)
                
                pos_tests_list = [t for t, res in test_results.items() if res == "Dương tính (+)"]
                if pos_tests_list:
                    st.markdown(f"• **Test đặc hiệu dương tính (+):** {', '.join(pos_tests_list)}")
                
                if rf_1 or rf_2 or rf_3:
                    st.error("🚩 **CẢNH BÁO CỜ ĐỎ:** Phát hiện dấu hiệu nguy cơ cao lâm sàng!")

            with col_sum2:
                st.markdown("##### 🤖 Đề xuất chẩn đoán & PHCN từ AI")
                st.success("Hệ thống đã nhận diện dữ liệu lâm sàng và hình ảnh thời gian thực.")
                if st.button("🚀 Chạy phân tích AI chuyên sâu", type="primary", use_container_width=True):
                    st.info("Đang xử lý phân tích chẩn đoán hình ảnh và đề xuất phác đồ PHCN...")

            st.markdown("---")
            if st.button("💾 Lưu hồ sơ bệnh án vào hệ thống lịch sử", type="primary", use_container_width=True):
                if not (p_name and p_phone):
                    st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và Số điện thoại ở phần hành chính phía trên!")
                else:
                    exam_summary = f"Vùng: {current_reg} | Lý do: {ly_do} | NRS: {nrs}/10 | Ảnh: {'Có' if selected_img else 'Không'} | Test(+): {', '.join(pos_tests_list) if pos_tests_list else 'Không'}"
                    visit_data = {
                        "patient_name": p_name,
                        "patient_phone": p_phone,
                        "patient_age": p_age,
                        "patient_job": p_job,
                        "summary": exam_summary
                    }
                    history_mgr.save_visit(p_phone, visit_data)
                    st.success(f"✅ Đã lưu thành công hồ sơ cho bệnh nhân **{p_name}** vào hệ thống lịch sử!")
