# =========================================================
# TABS/TAB1_HOSO.PY - TAB 1: QUẢN LÝ HỒ SƠ & LỊCH SỬ
# =========================================================
import streamlit as st

def render(history_mgr):
    if "tab1_sub_view" not in st.session_state:
        st.session_state.tab1_sub_view = None

    if st.session_state.tab1_sub_view is None:
        st.subheader("👤 Quản lý Hồ sơ & Lịch sử Bệnh nhân")
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("<h2 style='text-align: center;'>➕</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; font-weight: bold;'>Thêm hồ sơ mới</p>", unsafe_allow_html=True)
                if st.button("Tạo hồ sơ mới", use_container_width=True, key="btn_nav_new"):
                    st.session_state.tab1_sub_view = "new_profile"
                    st.rerun()

        with col2:
            with st.container(border=True):
                st.markdown("<h2 style='text-align: center;'>🔍</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; font-weight: bold;'>Tra cứu lịch sử</p>", unsafe_allow_html=True)
                if st.button("Tra cứu lịch sử", use_container_width=True, key="btn_nav_hist"):
                    st.session_state.tab1_sub_view = "history_lookup"
                    st.rerun()

    elif st.session_state.tab1_sub_view == "new_profile":
        if st.button("⬅️ Quay lại", type="secondary", key="b1"):
            st.session_state.tab1_sub_view = None
            st.rerun()

        st.subheader("➕ Tạo hồ sơ bệnh nhân mới")
        with st.form("form_new_patient"):
            p_name = st.text_input("Họ tên bệnh nhân:")
            p_phone = st.text_input("Số điện thoại (Mã định danh duy nhất):")
            c1, c2 = st.columns(2)
            with c1: p_age = st.number_input("Năm sinh:", 1900, 2026, 1990)
            with c2: p_job = st.text_input("Nghề nghiệp:")
            
            submitted = st.form_submit_button("💾 Lưu hồ sơ & Liên kết sang Tab Khám", use_container_width=True)
            if submitted:
                if p_name and p_phone:
                    init_data = {
                        "patient_name": p_name,
                        "patient_phone": p_phone,
                        "patient_age": p_age,
                        "patient_job": p_job,
                        "region": "Hành chính",
                        "summary": "Khởi tạo hồ sơ ban đầu"
                    }
                    history_mgr.save_visit(p_phone, init_data)
                    st.session_state.current_patient = {
                        "name": p_name, "phone": p_phone, "age": p_age, "job": p_job
                    }
                    st.success(f"✅ Đã khởi tạo thành công hồ sơ cho bệnh nhân **{p_name}**!")
                else:
                    st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và Số điện thoại!")

    elif st.session_state.tab1_sub_view == "history_lookup":
        if st.button("⬅️ Quay lại", type="secondary", key="b2"):
            st.session_state.tab1_sub_view = None
            st.rerun()

        st.subheader("🔍 Tra cứu lịch sử bệnh án (SQLite)")
        search_phone = st.text_input("Nhập số điện thoại tra cứu:")
        if search_phone:
            history = history_mgr.get_patient_history(search_phone)
            if history:
                st.success(f"🎉 Tìm thấy {len(history)} lần khám của bệnh nhân.")
                for idx, visit in enumerate(history):
                    with st.expander(f"📁 Lần khám {idx+1} - Ngày: {visit['visit_date']} (Vùng: {visit['region']})"):
                        st.markdown(f"**• Bệnh nhân:** {visit['patient_name']} | **Nghề nghiệp:** {visit['patient_job']}")
                        st.markdown(f"**• Tóm tắt:** {visit['summary']}")
            else:
                st.warning("⚠️ Không tìm thấy dữ liệu lịch sử cho số điện thoại này.")
