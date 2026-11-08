# =========================================================
# TAB 3: KHÁM LÂM SÀNG CHUYÊN SÂU (TỐI ƯU MOBILE)
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
        /* Đảm bảo responsive trên mobile */
        @media (max-width: 768px) {
            .row-container { display: flex; flex-direction: column; }
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

    if st.session_state.exam_active_region is None:
        st.subheader("🎯 Chọn Vùng Thăm Khám Lâm Sàng")
        st.markdown("Chọn một vùng cơ thể bên dưới để mở phiếu thăm khám:")

        cols_r = st.columns(2) # 2 cột trên mobile cho các ô vùng khám rộng rãi hơn
        for idx, item in enumerate(regions):
            title, icon, desc, color = item
            with cols_r[idx % 2]:
                st.markdown(f"""
                    <div class="grid-card-box">
                        <div class="icon-circle-btn" style="background: {color};">
                            {icon}
                        </div>
                        <div style="font-weight: 700; font-size: 13px; color: #1f2937; min-height: 40px; display: flex; align-items: center; justify-content: center;">{title}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("🩺 Bắt đầu khám", use_container_width=True, key=f"open_exam_{idx}"):
                    st.session_state.exam_active_region = title
                    st.rerun()
    else:
        current_reg = st.session_state.exam_active_region

        if st.button("⬅️ Quay lại chọn vùng khám", type="secondary"):
            st.session_state.exam_active_region = None
            st.rerun()

        st.markdown(f"### 📋 PHIẾU KHÁM: {current_reg.upper()}")
        st.markdown("---")

        active_patient = st.session_state.get("current_patient", {"name": "", "phone": "", "age": 1990, "job": ""})
        if active_patient.get("name"):
            st.info(f"🔗 Bệnh nhân: **{active_patient.get('name')}** (SĐT: {active_patient.get('phone')})")

        # Form nhập liệu theo dạng xếp dọc 1 cột tối ưu cho mobile
        st.markdown("##### ✍️ 1. Hành chính & Lý do khám")
        p_name = st.text_input("Họ tên bệnh nhân:", value=active_patient.get("name", ""), key="rt_p_name")
        p_phone = st.text_input("Số điện thoại:", value=active_patient.get("phone", ""), key="rt_p_phone")
        p_age = st.number_input("Năm sinh:", min_value=1900, max_value=2026, value=int(active_patient.get("age", 1990)), key="rt_p_age")
        p_job = st.text_input("Nghề nghiệp:", value=active_patient.get("job", ""), key="rt_p_job")
        ly_do = st.text_input("🏥 Lý do vào viện / Than phiền chính:", key="rt_ly_do")

        with st.expander("🩺 2. Bệnh sử (Quy trình SOCRATES)", expanded=True):
            character = st.text_input("Tính chất đau (Character):", key="rt_char")
            nrs = st.selectbox("Mức độ đau NRS (0-10):", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="rt_nrs")

        with st.expander("🔍 3. Khám thực thể (Nhìn – Sờ – Đo ROM)", expanded=True):
            inspect = st.text_area("👁️ NHÌN (Inspection):", key="rt_inspect")
            palp = st.text_area("✋ SỜ (Palpation):", key="rt_palp")
            rom_meas = st.text_area("📏 ĐO / GÕ (ROM & Phản xạ):", key="rt_rom")

        with st.expander("🖼️ 4. Hình ảnh Lâm sàng (X-quang / MRI)", expanded=False):
            uploaded_image = st.file_uploader("Tải ảnh:", type=["png", "jpg", "jpeg"], key="rt_uploaded_img")
            if uploaded_image is not None:
                st.image(uploaded_image, caption="Hình ảnh lâm sàng", use_container_width=True)

        with st.expander(f"🧬 5. Nghiệm pháp đặc hiệu ({current_reg})", expanded=False):
            test_res = st.radio("Kết quả test:", ["Âm tính (-)", "Dương tính (+)"], horizontal=True, key="ex_t_res_0")

        # TỜ GIẤY TRẮNG REAL-TIME HIỂN THỊ XUỐNG DƯỚI RỘNG RÃI
        st.markdown("---")
        st.markdown("### 📄 Tờ Giấy Trắng & Phân Tích AI")
        
        summary_text = f"""[BỆNH ÁN PHCN]
- Vùng khám: {current_reg}
- Bệnh nhân: {p_name if p_name else '---'} ({p_phone if p_phone else '---'})
- Lý do: {ly_do if ly_do else '---'}
- Đau NRS: {nrs}/10
- Nhìn: {inspect if inspect else '---'}
- Sờ: {palp if palp else '---'}
- ROM: {rom_meas if rom_meas else '---'}"""

        with st.container(border=True):
            st.text_area("Bôi đen & Copy nội dung:", value=summary_text, height=200, key="quick_copy_box")

        if st.button("💾 Lưu hồ sơ bệnh án vào lịch sử", type="primary", use_container_width=True):
            if not (p_name and p_phone):
                st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và SĐT!")
            else:
                visit_data = {"patient_name": p_name, "patient_phone": p_phone, "summary": f"Vùng: {current_reg} | NRS: {nrs}/10"}
                history_mgr.save_visit(p_phone, visit_data)
                st.success(f"✅ Đã lưu hồ sơ cho **{p_name}**!")
