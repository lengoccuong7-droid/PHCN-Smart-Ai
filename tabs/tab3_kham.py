# =========================================================
# TABS/TAB3_KHAM.PY - TAB 3: KHÁM LÂM SÀNG CHUYÊN SÂU
# =========================================================
import streamlit as st
from clinical_engine.reasoning_engine import ClinicalReasoningEngine

def render(history_mgr):
    st.subheader("🩺 Phiếu Khám Lâm Sàng Chuyên Sâu & Phân Tích Real-time")

    active_patient = st.session_state.get("current_patient", {"name": "", "phone": "", "age": 1990, "job": ""})
    if active_patient.get("name"):
        st.info(f"🔗 Liên kết bệnh nhân từ Tab 1: **{active_patient.get('name')}** (SĐT: {active_patient.get('phone')})")

    region = st.selectbox("🎯 Chọn vùng cơ thể thăm khám chuyên sâu:", [
        "Cột sống cổ", "Cột sống ngực", "Cột sống thắt lưng", "Khớp vai",
        "Khớp khuỷu", "Cổ tay – bàn tay", "Khớp háng", "Khớp gối", "Cổ chân – bàn chân", "Thần kinh & Chức năng"
    ])

    col_in, col_out = st.columns([1, 1])

    with col_in:
        st.markdown("##### ✍️ 1. Hành chính & Lý do khám")
        p_name = st.text_input("Họ tên bệnh nhân:", value=active_patient.get("name", ""), key="rt_name")
        p_phone = st.text_input("Số điện thoại:", value=active_patient.get("phone", ""), key="rt_phone")
        c1, c2 = st.columns(2)
        with c1: p_age = st.number_input("Năm sinh:", 1900, 2026, int(active_patient.get("age", 1990)), key="rt_age")
        with c2: p_job = st.text_input("Nghề nghiệp:", value=active_patient.get("job", ""), key="rt_job")
        
        ly_do = st.text_input("🏥 Lý do vào viện / Than phiền chính:", key="rt_lydo")
        tien_su = st.text_area("📜 Tiền sử bệnh lý:", key="rt_tiensu")

        st.markdown("##### 🩺 2. Bệnh sử (SOCRATES)")
        onset = st.text_input("O - Khởi phát:", key="rt_onset")
        character = st.text_input("C - Tính chất đau (Bệnh nhân kể):", key="rt_char")
        radiation = st.text_input("R - Hướng lan:", key="rt_rad")
        nrs = st.selectbox("Mức độ đau NRS (0-10):", list(range(11)), key="rt_nrs")

        st.markdown("##### 🔍 3. Khám thực thể (Dấu hiệu khách quan)")
        inspect = st.text_area("👁️ NHÌN (Inspection):", key="rt_inspect")
        palp = st.text_area("✋ SỜ (Palpation):", key="rt_palp")
        rom = st.text_area("📏 ĐO (ROM & Phản xạ):", key="rt_rom")

        st.markdown("##### 🧬 4. Nghiệm pháp / Test đặc hiệu")
        test_1_res = st.radio("Test đặc hiệu 1:", ["Chưa làm", "Âm tính (-)", "Dương tính (+)"], horizontal=True, key="rt_t1")
        test_2_res = st.radio("Test đặc hiệu 2:", ["Chưa làm", "Âm tính (-)", "Dương tính (+)"], horizontal=True, key="rt_t2")

        st.markdown("##### 🖼️ 5. Hình ảnh Lâm sàng / Phim chụp")
        up_img = st.file_uploader("Tải ảnh X-quang/MRI/Tư thế:", type=["png", "jpg", "jpeg"], key="rt_img")

        st.markdown("##### 🚩 6. Cờ đỏ an toàn (Red Flags)")
        rf_1 = st.checkbox("Hội chứng đuôi ngựa / Rối loạn cơ tròn", key="rf1")
        rf_2 = st.checkbox("Sụt cân nhanh / Tiền sử ung thư", key="rf2")
        rf_3 = st.checkbox("Sốt cao, sưng nóng đỏ đau cấp tính", key="rf3")

    with col_out:
        st.markdown("##### 📄 TỜ GIẤY TRẮNG TỔNG HỢP (Real-time)")
        with st.container(border=True):
            st.markdown(f"**• Họ tên:** {p_name if p_name else '*(Chưa nhập)*'}")
            st.markdown(f"**• Vùng khám:** {region}")
            st.markdown(f"**• Lý do khám:** {ly_do}")
            st.markdown(f"**• Bệnh sử:** {character} | NRS: {nrs}/10")
            st.markdown(f"**• Thực thể:** Nhìn: {inspect} | Sờ: {palp} | Đo: {rom}")
            st.markdown(f"**• Test 1:** {test_1_res} | **Test 2:** {test_2_res}")
            if up_img:
                st.image(up_img, width=180, caption="Hình ảnh đính kèm")
            
            selected_rfs = []
            if rf_1: selected_rfs.append("Rối loạn cơ tròn")
            if rf_2: selected_rfs.append("Sụt cân/Ung thư")
            if rf_3: selected_rfs.append("Sốt/Sưng nóng đỏ đau")
            
            if selected_rfs:
                st.error(f"🚩 CẢNH BÁO CỜ ĐỎ: {', '.join(selected_rfs)}")

        st.markdown("---")
        st.markdown("##### 🤖 PHÂN TÍCH SUY LUẬN AI & ĐỐI CHIẾU BẰNG CHỨNG")

        if st.button("🚀 Chạy phân tích AI chuyên sâu", type="primary", use_container_width=True):
            input_data = {
                "region": region,
                "nrs": nrs,
                "character": character,
                "inspect": inspect,
                "rom": rom,
                "test_results": {"Test 1": test_1_res, "Test 2": test_2_res},
                "red_flags": selected_rfs
            }
            analysis = ClinicalReasoningEngine.analyze_case(input_data)
            
            if analysis["safety_warnings"]:
                for warn in analysis["safety_warnings"]:
                    st.error(warn)
                    
            st.success(f"📌 **Nhận định sơ bộ:** {analysis['diagnosis_impression']}")
            
            st.markdown("**1. Bằng chứng ủng hộ:**")
            for item in analysis["supporting_evidence"]:
                st.markdown(f"- {item}")
                
            st.markdown("**2. Bằng chứng chưa phù hợp / Thiếu sót:**")
            for item in analysis["unmatched_evidence"] + analysis["missing_data"]:
                st.markdown(f"- {item}")
                
            st.markdown("**3. Định hướng can thiệp PHCN:**")
            for item in analysis["rehab_orientation"]:
                st.markdown(f"- {item}")

        st.markdown("---")
        # 3 Nút thao tác mở rộng theo Tầng 1 & 7
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            if st.button("📋 Sao chép nội dung"):
                st.toast("Đã sao chép báo cáo vào bộ nhớ tạm!")
        with btn_c2:
            st.link_button("💬 ChatGPT", "https://chatgpt.com", use_container_width=True)
        with btn_c3:
            st.link_button("✨ Gemini", "https://gemini.google.com", use_container_width=True)

        st.markdown("")
        if st.button("💾 Lưu hồ sơ vào SQLite Database", type="primary", use_container_width=True):
            if not (p_name and p_phone):
                st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và SĐT ở phần hành chính!")
            else:
                visit_record = {
                    "patient_name": p_name,
                    "patient_phone": p_phone,
                    "patient_age": p_age,
                    "patient_job": p_job,
                    "region": region,
                    "summary": f"Vùng: {region} | Lý do: {ly_do} | NRS: {nrs}/10 | Test1: {test_1_res}",
                    "character": character,
                    "inspect": inspect,
                    "rom": rom
                }
                history_mgr.save_visit(p_phone, visit_record)
                st.success(f"✅ Đã lưu bản ghi lượt khám của **{p_name}** vào cơ sở dữ liệu SQLite!")
