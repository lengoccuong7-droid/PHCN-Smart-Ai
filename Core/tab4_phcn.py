# =========================================================
# TAB 4: KHO BÀI TẬP PHỤC HỒI CHỨC NĂNG
# =========================================================
import streamlit as st

def render_tab4():
    st.markdown("### 🏋️‍♂️ Kho Bài Tập Phục Hồi Chức Năng Theo Bệnh Lý")
    st.caption("Chọn một bệnh lý bên dưới để xem chi tiết trọn bộ 7 bài tập chuẩn hóa:")

    pathologies_m4 = {
        "1. Tai biến mạch máu não (Liệt nửa người)": [
            "1. Tập vận động thụ động các khớp bên liệt duy trì tầm vận động (ROM).",
            "2. Bài tập ức chế trương lực cơ co cứng (kỹ thuật Bobath).",
            "3. Tập chuyển đổi tư thế từ nằm ngửa sang nằm nghiêng và ngồi dậy.",
            "4. Tập kiểm soát thăng bằng thân mình ở tư thế ngồi độc lập.",
            "5. Tập đứng dồn trọng lượng đều hai chân trước gương.",
            "6. Bài tập đi lại với máng nẹp cẳng bàn chân (AFO) hoặc khung tập đi.",
            "7. Tập mạnh cơ chủ động bên lành và các nhóm cơ duỗi bên liệt."
        ],
        "2. Rối loạn nuốt (Dysphagia) sau tai biến": [
            "1. Bài tập vận động cơ môi (mím chặt, cười hết cỡ, thổi phồng má, phát âm U-I).",
            "2. Bài tập vận động lưỡi (đẩy lưỡi ra trước, sang trái, sang phải, liếm vòm họng).",
            "3. Kích thích nhiệt lạnh vùng cung khẩu cái mềm kích thích phản xạ nuốt.",
            "4. Bài tập Masako (giữ đầu lưỡi giữa hai hàm răng và nuốt nước bọt).",
            "5. Bài tập Shaker (nâng đầu ở tư thế nằm ngửa để mở rộng cơ thắt thực quản trên).",
            "6. Bài tập đóng nắp thanh môn (nuốt giữ hơi, ho mạnh ngay sau khi nuốt).",
            "7. Luyện tập nuốt theo các độ quánh thức ăn chuẩn hóa IDDSI."
        ]
    }

    if "selected_pathology_m4" not in st.session_state:
        st.session_state.selected_pathology_m4 = None

    cols_p = st.columns(2)
    for idx, path_key in enumerate(pathologies_m4.keys()):
        with cols_p[idx % 2]:
            if st.button(f"📌 {path_key}", use_container_width=True, key=f"btn_m4_path_{idx}"):
                st.session_state.selected_pathology_m4 = path_key

    if st.session_state.selected_pathology_m4:
        st.markdown("---")
        st.success(f"🏥 Đang hiển thị phác đồ cho: **{st.session_state.selected_pathology_m4}**")
        
        st.markdown("#### 📋 Trọn bộ 7 bài tập phục hồi chức năng chuẩn hóa:")
        for exercise in pathologies_m4[st.session_state.selected_pathology_m4]:
            st.markdown(f"- {exercise}")
            
        st.markdown("")
        if st.button("🔄 Chọn bệnh lý khác", use_container_width=True, key="reset_m4_path"):
            st.session_state.selected_pathology_m4 = None
            st.rerun()
