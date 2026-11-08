import streamlit as st

def render(history_mgr):
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
                    st.success(f"✅ Đã tạo và lưu thành công hồ sơ cho bệnh nhân **{new_name}**!")
