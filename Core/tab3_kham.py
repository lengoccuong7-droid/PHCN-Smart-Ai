# =========================================================
# TAB 3: KHÁM LÂM SÀNG CHUYÊN SÂU (CHUẨN BỐ CỤC & CUỘN DỌC)
# =========================================================
import streamlit as st

def render(history_mgr):
    st.markdown("""
        <style>
        .grid-card-box {
            background: #ffffff;
            border-radius: 16px;
            padding: 14px 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #eaeaea;
            margin-bottom: 10px;
        }
        .icon-circle-btn {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin: 0 auto 8px auto;
            color: white;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        .scrollable-exam-feed {
            max-height: 750px;
            overflow-y: auto;
            padding-right: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    if "exam_active_region" not in st.session_state:
        st.session_state.exam_active_region = None

    regions = [
        ("Cột sống cổ", "🦴", "C1-C7 và hội chứng chèn ép", "linear-gradient(135deg, #ff6b6b, #ee5253)"),
        ("Cột sống thắt lưng", "🩻", "Thoát vị đĩa đệm, đau thần kinh tọa", "linear-gradient(135deg, #10ac84, #1dd1a1)"),
        ("Khớp vai", "🦾", "Chóp xoay & đông cứng khớp vai", "linear-gradient(135deg, #5f27cd, #341f97)"),
        ("Khuỷu tay", "💪", "Viêm lồi cầu, hội chứng ống khuỷu", "linear-gradient(135deg, #ff9f43, #ee5253)"),
        ("Cổ tay – bàn tay", "✋", "Hội chứng ống cổ tay, De Quervain", "linear-gradient(135deg, #48dbfb, #0abde3)"),
        ("Khớp háng", "🦿", "Thoái hóa & kẹp háng FAI", "linear-gradient(135deg, #f39c12, #e67e22)"),
        ("Khớp gối", "🦵", "ACL, sụn chêm & thoái hóa gối", "linear-gradient(135deg, #2e86de, #222f3e)"),
        ("Cổ chân – bàn chân", "🦶", "Bong gân & viêm cân gan chân", "linear-gradient(135deg, #ee5253, #ff6b6b)"),
        ("Thần kinh & Khác", "🧠", "Đột quỵ, phục hồi chức năng thần kinh", "linear-gradient(135deg, #0abde3, #2e86de)")
    ]

    # MÀN HÌNH 1: LƯỚI ICON CHỌN VÙNG KHÁM
    if st.session_state.exam_active_region is None:
        st.subheader("🎯 Chọn Vùng Thăm Khám Lâm Sàng")
        st.markdown("Chọn một vùng cơ thể bên dưới để mở phiếu thăm khám chuyên sâu độc lập:")

        cols_r = st.columns(3)
        for idx, item in enumerate(regions):
            title, icon, desc, color = item
            with cols_r[idx % 3]:
                st.markdown(f"""
                    <div class="grid-card-box">
                        <div class="icon-circle-btn" style="background: {color};">
                            {icon}
                        </div>
                        <div style="font-weight: 700; font-size: 12px; color: #1f2937; height: 30px; display: flex; align-items: center; justify-content: center;">{title}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("🩺 Bắt đầu khám", use_container_width=True, key=f"open_exam_{idx}"):
                    st.session_state.exam_active_region = title
                    st.rerun()
                        
    # MÀN HÌNH 2: TRANG CHI TIẾT KHÁM CÓ KHUNG CUỘN DỌC
    else:
        current_reg = st.session_state.exam_active_region

        c_top1, c_top2 = st.columns([1, 4])
        with c_top1:
            if st.button("⬅️ Quay lại", type="secondary", key="back_to_exam_grid"):
                st.session_state.exam_active_region = None
                st.rerun()
        with c_top2:
            st.subheader(f"📋 PHIẾU KHÁM LÂM SÀNG: {current_reg.upper()}")

        st.markdown("---")
        
        # Khung cuộn dọc cho toàn bộ nội dung khám
        st.markdown('<div class="scrollable-exam-feed">', unsafe_allow_html=True)

        active_patient = st.session_state.get("current_patient", {"name": "", "phone": "", "age": 1990, "job": ""})
        if active_patient.get("name"):
            st.info(f"🔗 Đang liên kết tự động từ Tab 1 – Bệnh nhân: **{active_patient.get('name')}** (SĐT: {active_patient.get('phone')})")

        # 1. HÀNH CHÍNH & HỎI BỆNH
        st.markdown("##### ✍️ 1. Hành chính & Lý do khám")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            p_name = st.text_input("Họ tên bệnh nhân:", value=active_patient.get("name", ""), key="rt_p_name")
            p_phone = st.text_input("Số điện thoại:", value=active_patient.get("phone", ""), key="rt_p_phone")
        with col_p2:
            p_age = st.number_input("Năm sinh:", min_value=1900, max_value=2026, value=int(active_patient.get("age", 1990)), key="rt_p_age")
            p_job = st.text_input("Nghề nghiệp:", value=active_patient.get("job", ""), key="rt_p_job")

        ly_do = st.text_input("🏥 Lý do vào viện / Than phiền chính:", key="rt_ly_do")
        tien_su = st.text_area("📜 Tiền sử bệnh:", key="rt_tien_su")

        with st.expander("🩺 2. Bệnh sử (Quy trình SOCRATES)", expanded=True):
            onset = st.text_input("O (Onset) – Khởi phát:", key="rt_onset")
            character = st.text_input("C (Character) – Tính chất đau:", key="rt_char")
            radiation = st.text_input("R (Radiation) – Hướng lan:", key="rt_rad")
            associations = st.text_input("A (Associations) – Triệu chứng kèm theo:", key="rt_assoc")
            
            col_nrs1, col_nrs2 = st.columns([1, 2])
            with col_nrs1:
                nrs = st.selectbox("Mức độ đau NRS (0-10):", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="rt_nrs")
            with col_nrs2:
                nrs_note = st.text_input("Ghi chú thêm mức độ đau:", key="rt_nrs_note")

        with st.expander("🔍 3. Khám thực thể (Nhìn – Sờ – Đo ROM)", expanded=True):
            inspect = st.text_area("👁️ NHÌN (Inspection):", key="rt_inspect")
            palp = st.text_area("✋ SỜ (Palpation):", key="rt_palp")
            rom_meas = st.text_area("📏 ĐO / GÕ (ROM & Phản xạ):", key="rt_rom")

        with st.expander("🖼️ 4. Hình ảnh Lâm sàng & Cận lâm sàng", expanded=True):
            uploaded_image = st.file_uploader("📤 Tải ảnh X-quang / MRI:", type=["png", "jpg", "jpeg"], key="rt_uploaded_img")
            camera_image = st.camera_input("📷 Chụp hình ảnh trực tiếp:", key="rt_camera_img")
            selected_img = uploaded_image if uploaded_image is not None else camera_image
            if selected_img is not None:
                st.image(selected_img, caption="🖼️ Hình ảnh lâm sàng", use_container_width=True)

        with st.expander(f"🧬 5. Nghiệm pháp / Test đặc hiệu ({current_reg})", expanded=True):
            st.caption("Đánh giá các test lâm sàng đặc hiệu:")
            test_results = {}
            for t_idx in range(2):
                t_name = f"Test đặc hiệu {t_idx+1}"
                res = st.radio(f"Nhập kết quả {t_name}:", ["Chưa làm / Âm tính (-)", "Dương tính (+)"], horizontal=True, key=f"ex_t_res_{t_idx}")
                test_results[t_name] = res

        with st.expander("🚩 6. Cờ đỏ an toàn lâm sàng (Red Flags)"):
            rf_1 = st.checkbox("Hội chứng đuôi ngựa / Rối loạn cơ tròn", key="rt_rf1")
            rf_2 = st.checkbox("Sụt cân nhanh / Tiền sử ung thư", key="rt_rf2")
            rf_3 = st.checkbox("Sốt cao, sưng nóng đỏ đau cấp tính", key="rt_rf3")

        st.markdown("---")
        st.markdown("### 🧠 TỜ GIẤY TRẮNG TỔNG HỢP & PHÂN TÍCH AI (Real-time)")

        has_pos_test = any([v == "Dương tính (+)" for v in test_results.values()])
        is_blank = not (p_name or ly_do or tien_su or onset or character or inspect or palp or rom_meas or has_pos_test or rf_1 or rf_2 or rf_3 or (nrs > 0) or (selected_img is not None))

        if is_blank:
            st.info("📄 *[Tờ giấy trắng]* — Chưa có dữ liệu. Thông tin sẽ tự động đồng bộ hiển thị tại đây theo thời gian thực.")
        else:
            col_sum1, col_sum2 = st.columns(2)
            with col_sum1:
                st.markdown("##### 📋 Tóm tắt ca bệnh")
                if p_name: st.markdown(f"• **Họ tên:** {p_name}")
                st.markdown(f"• **Vùng khám:** {current_reg}")
                if ly_do: st.markdown(f"• **Lý do khám:** {ly_do}")
                if character: st.markdown(f"• **Đau NRS:** {nrs}/10")
            with col_sum2:
                st.markdown("##### 🤖 Đề xuất chẩn đoán từ AI")
                st.success("Hệ thống đã ghi nhận dữ liệu lâm sàng.")

            if st.button("💾 Lưu hồ sơ bệnh án vào hệ thống lịch sử", type="primary", use_container_width=True):
                if not (p_name and p_phone):
                    st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và Số điện thoại!")
                else:
                    visit_data = {"patient_name": p_name, "patient_phone": p_phone, "summary": f"Vùng: {current_reg} | NRS: {nrs}/10"}
                    history_mgr.save_visit(p_phone, visit_data)
                    st.success(f"✅ Đã lưu hồ sơ cho bệnh nhân **{p_name}**!")

        st.markdown('</div>', unsafe_allow_html=True)
