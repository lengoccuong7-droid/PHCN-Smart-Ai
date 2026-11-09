# =========================================================
# TABS/TAB2_TRITHUC.PY - TAB 2: CƠ SỞ TRI THỨC LÂM SÀNG (10 VÙNG)
# =========================================================
import streamlit as st

def render():
    if "kb_region" not in st.session_state:
        st.session_state.kb_region = None

    if st.session_state.kb_region is None:
        st.subheader("📚 Cẩm nang Tri thức & Cơ sở Lâm sàng (10 Vùng Cơ thể)")
        
        knowledge_regions = [
            ("Cột sống cổ", "🦴", "C1-C7 và hội chứng chèn ép rễ"),
            ("Cột sống ngực", "🧬", "Cột sống ngực, đau liên sườn & biến dạng"),
            ("Cột sống thắt lưng", "🩻", "Thoát vị đĩa đệm & đau thần kinh tọa"),
            ("Khớp vai", "🦾", "Hội chứng chóp xoay & đông cứng khớp vai"),
            ("Khớp khuỷu", "💪", "Viêm lồi cầu & hội chứng ống khuỷu"),
            ("Cổ tay – bàn tay", "✋", "Hội chứng ống cổ tay & De Quervain"),
            ("Khớp háng", "🦿", "Thoái hóa khớp háng & kẹp FAI"),
            ("Khớp gối", "🦵", "Tổn thương ACL, sụn chêm & thoái hóa gối"),
            ("Cổ chân – bàn chân", "🦶", "Bong gân dây chằng & viêm cân gan chân"),
            ("Thần kinh & Chức năng", "🧠", "Tai biến mạch máu não & đột quỵ")
        ]

        cols = st.columns(3)
        for idx, (title, icon, desc) in enumerate(knowledge_regions):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"<h3 style='text-align: center;'>{icon}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; font-weight: bold;'>{title}</p>", unsafe_allow_html=True)
                    st.caption(desc)
                    if st.button("📖 Đọc sách chuyên khoa", use_container_width=True, key=f"kb_{idx}"):
                        st.session_state.kb_region = title
                        st.rerun()
    else:
        reg = st.session_state.kb_region
        if st.button("⬅️ Quay lại danh mục", key="kb_back"):
            st.session_state.kb_region = None
            st.rerun()

        st.subheader(f"📖 SÁCH CHUYÊN KHOA: {reg.upper()}")
        with st.expander("1. Giải phẫu & Sinh cơ học", expanded=True):
            st.markdown(f"Cấu trúc xương, dây chằng, cơ bắp và trục sinh cơ học vùng **{reg}**.")
        with st.expander("2. Bệnh lý & Hội chứng thường gặp", expanded=True):
            st.markdown(f"Các dạng tổn thương cơ học, hội chứng chèn ép thần kinh và nguy cơ bệnh lý.")
        with st.expander("3. Triệu chứng điển hình & Không điển hình", expanded=True):
            st.markdown("Cơ chế đau, vị trí đau chói và hướng lan theo phân vùng cảm giác thần kinh.")
        with st.expander("4. Nghiệm pháp khám đặc hiệu", expanded=True):
            st.markdown("Mô tả kỹ thuật khám, mục đích và giá trị chẩn đoán của từng Test.")
        with st.expander("5. Định hướng điều trị PHCN & VLTL", expanded=True):
            st.markdown("Phác đồ can thiệp vật lý trị liệu, tập vận động sinh học và tái hòa nhập.")
