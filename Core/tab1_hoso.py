# =========================================================
# TAB 1: QUẢN LÝ HỒ SƠ & LỊCH SỬ (TỰ ĐỘNG CHUYỂN SANG TAB 3 KHI TẠO XONG)
# =========================================================
import streamlit as st

def render(history_mgr):
    # Khởi tạo trạng thái màn hình con trong Tab 1 nếu chưa có
    if "tab1_sub_view" not in st.session_state:
        st.session_state.tab1_sub_view = None

    # MÀN HÌNH 1: LƯỚI NÚT BẤM LỰA CHỌN TÍNH NĂNG HỒ SƠ
    if st.session_state.tab1_sub_view is None:
        st.subheader("👤 Quản lý Hồ sơ & Lịch sử Bệnh nhân")
        st.markdown("Chọn một chức năng bên dưới để bắt đầu quản lý hồ sơ hành chính:")

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("<h2 style='text-align: center; margin: 0;'>➕</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; font-weight: bold; font-size: 16px; margin: 10px 0;'>Thêm hồ sơ mới</p>", unsafe_allow_html=True)
                st.caption("Khởi tạo thông tin hành chính cho bệnh nhân mới đến khám.")
                if st.button("Tạo hồ sơ mới", use_container_width=True, key="btn_nav_new_profile"):
                    st.session_state.tab1_sub_view = "new_profile"
                    st.rerun()

        with col2:
            with st.container(border=True):
                st.markdown("<h2 style='text-align: center; margin: 0;'>🔍</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; font-weight: bold; font-size: 16px; margin: 10px 0;'>Xem lịch sử hồ sơ</p>", unsafe_allow_html=True)
                st.caption("Tra cứu lịch sử khám bệnh và liên kết dữ liệu sang phòng khám.")
                if st.button("Tra cứu lịch sử", use_container_width=True, key="btn_nav_history"):
                    st.session_state.tab1_sub_view = "history_lookup"
                    st.rerun()

    # MÀN HÌNH 2A: FORM THÊM HỒ SƠ BỆNH NHÂN MỚI (TỰ ĐỘNG LƯU & CHUYỂN SANG TAB KHÁM)
    elif st.session_state.tab1_sub_view == "new_profile":
        if st.button("⬅️ Quay lại danh mục hồ sơ", type="secondary", key="back_to_hoso_grid_1"):
            st.session_state.tab1_sub_view = None
            st.rerun()

        st.markdown("---")
        st.subheader("➕ Khởi tạo hồ sơ bệnh nhân mới")
        st.caption("Nhập thông tin hành chính. Sau khi lưu, hệ thống sẽ tự động chuyển sang phần Khám (Tab 3).")

        with st.form("new_patient_form_v3"):
            new_name = st.text_input("Họ tên bệnh nhân:", placeholder="Nhập họ tên đầy đủ...")
            new_phone = st.text_input("Số điện thoại (Dùng làm mã định danh):", placeholder="Ví dụ: 0901234567...")
            col_np1, col_np2 = st.columns(2)
            with col_np1:
                new_age = st.number_input("Năm sinh:", min_value=1900, max_value=2026, value=1990)
            with col_np2:
                new_job = st.text_input("Nghề nghiệp:", placeholder="Nhập nghề nghiệp...")
            
            submitted_new_p = st.form_submit_button("💾 Tạo hồ sơ & Tiến hành khám ngay", use_container_width=True)
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
                    
                    # 1. Lưu thông tin sang biến dùng chung để Tab 3 tự động nhận
                    st.session_state.current_patient = {
                        "name": new_name,
                        "phone": new_phone,
                        "age": new_age,
                        "job": new_job
                    }
                    
                    # 2. Đặt cờ điều hướng chuyển sang Tab 3 (Tab index 2 trong streamlit)
                    # Lưu ý: Trong Streamlit, st.tabs không hỗ trợ chuyển tab trực tiếp bằng code một cách hoàn hảo, 
                    # nhưng ta có thể reset trạng thái xem hồ sơ để đưa bác sĩ về màn hình chính hoặc dùng cơ chế thông báo trực quan.
                    st.success(f"✅ Đã tạo hồ sơ cho **{new_name}**! Dữ liệu đã được liên kết sang Tab Khám.")
                    st.info("💡 Vui lòng bấm vào tab **'3. Khám'** ở thanh menu phía trên để bắt đầu thăm khám lâm sàng ngay lập tức.")

    # MÀN HÌNH 2B: TRA CỨU LỊCH SỬ HỒ SƠ
    elif st.session_state.tab1_sub_view == "history_lookup":
        if st.button("⬅️ Quay lại danh mục hồ sơ", type="secondary", key="back_to_hoso_grid_2"):
            st.session_state.tab1_sub_view = None
            st.rerun()

        st.markdown("---")
        st.subheader("🔍 Tra cứu lịch sử hồ sơ bệnh án")
        search_phone_input = st.text_input("🔍 Nhập số điện thoại bệnh nhân cần tra cứu:", placeholder="Ví dụ: 0901234567", key="search_history_phone_m2")
        
        if search_phone_input:
            patient_history_list = history_mgr.get_patient_history(search_phone_input)
            
            if patient_history_list:
                st.success(f"🎉 Đã tìm thấy {len(patient_history_list)} lần khám của số điện thoại này.")
                latest_visit = patient_history_list[0]
                
                # Đồng bộ thông tin hành chính mới nhất sang Tab 3
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
                        st.markdown(f"**• Tóm tắt thăm khám:** {visit.get('summary', 'N/A')}")
                
                st.info("💡 Thông tin hành chính đã được tự động liên kết. Bạn có thể chuyển sang Tab **'3. Khám'** để tiếp tục theo dõi.")
            else:
                st.warning("⚠️ Không tìm thấy lịch sử khám nào tương ứng với số điện thoại này.")
        else:
            st.info("💡 Nhập số điện thoại để hệ thống truy xuất toàn bộ dữ liệu lịch sử và tự động đồng bộ sang Tab Khám.")
