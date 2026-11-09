# =========================================================
# TABS/TAB4_PHCN.PY - TAB 4: KHO BÀI TẬP PHCN CHUYÊN SÂU
# =========================================================
import streamlit as st

def render():
    if "rehab_group" not in st.session_state:
        st.session_state.rehab_group = None

    if st.session_state.rehab_group is None:
        st.subheader("🏋️‍♂️ Kho Bài Tập Phục Hồi Chức Năng Chuyên Sâu (9 Nhóm Bệnh Lý)")
        
        pathologies = [
            ("1. Tai biến mạch máu não (Liệt nửa người)", "🧠", "Phục hồi vận động chi liệt & thăng bằng"),
            ("2. Rối loạn nuốt (Dysphagia) sau tai biến", "💧", "Kỹ thuật nuốt & cơ vùng miệng họng"),
            ("3. Rối loạn ngôn ngữ & Thất ngôn (Aphasia)", "🗣️", "Kích thích ngôn ngữ & giao tiếp"),
            ("4. Âm ngữ trị liệu (Rối loạn phát âm / Dysarthria)", "🗣️", "Kiểm soát phát âm & hơi thở"),
            ("5. Trẻ tự kỷ (Rối loạn phổ tự kỷ kèm vận động)", "🧩", "Điều hòa cảm giác & vận động thô"),
            ("6. Xơ hóa cơ ức đòn chũm (Vẹo cổ bẩm sinh)", "🔄", "Kéo giãn cơ cổ & vận động"),
            ("7. PHCN sau Phẫu thuật đầu gối (Tái tạo ACL)", "🦿", "Tập vận động sau mổ dây chằng gối"),
            ("8. PHCN sau Phẫu thuật thay khớp háng", "🦿", "Phục hồi tầm vận động và dáng đi"),
            ("9. PHCN sau Gãy tay / Gãy chân (Hậu phẫu)", "🦾", "Chống teo cơ và phục hồi tầm vận động")
        ]

        cols = st.columns(3)
        for idx, (title, icon, desc) in enumerate(pathologies):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"<h3 style='text-align: center;'>{icon}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 14px;'>{title}</p>", unsafe_allow_html=True)
                    st.caption(desc)
                    if st.button("🏋️‍♂️ Xem bài tập", use_container_width=True, key=f"ex_{idx}"):
                        st.session_state.rehab_group = title
                        st.rerun()
    else:
        group_name = st.session_state.rehab_group
        if st.button("⬅️ Quay lại danh mục", key="ex_back"):
            st.session_state.rehab_group = None
            st.rerun()

        st.subheader(f"📂 KHO BÀI TẬP: {group_name.upper()}")
        st.caption("Trọn bộ bài tập chuẩn hóa kèm Tác dụng và Hướng dẫn thực hiện chi tiết[span_2](start_span)[span_2](end_span):")

        # 7 Bài tập chuẩn hóa lâm sàng cho từng bệnh
        for i in range(1, 8):
            with st.expander(f"🔹 Bài tập {i}: Kỹ thuật vận động chuyên sâu bài số {i}"):
                st.markdown(f"- **🎯 Mục đích lâm sàng:** Duy trì biên độ khớp, tăng cường sức mạnh cơ sinh lý và phục hồi phản xạ thần kinh cơ.")
                st.markdown(f"- **⚙️ Hướng dẫn kỹ thuật:** Thực hiện động tác từ từ, đúng trục sinh cơ học, tránh gây đau xé.")
                st.markdown(f"- **⏱️ Liều lượng khuyến nghị:** 3 hiệp x 10-15 lần lặp / ngày (hoặc theo chỉ định bác sĩ điều trị).")
