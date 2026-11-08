import streamlit as st

def render():
    if "kb_detail_page" not in st.session_state:
        st.session_state.kb_detail_page = None

    if st.session_state.kb_detail_page is None:
        st.subheader("📖 Cẩm nang Tri thức & Phác đồ Lâm sàng")
        st.markdown("Chọn một chuyên khoa bên dưới để xem tài liệu chi tiết:")

        search_knowledge_kw = st.text_input("🔍 Tìm kiếm nhanh bệnh lý, triệu chứng...", placeholder="Nhập từ khóa...", key="search_knowledge_input")

        st.markdown("---")
        st.markdown("##### 🗂️ Danh mục chuyên khoa & Vùng cơ thể")

        knowledge_items = [
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

        cols = st.columns(3)
        for idx, item in enumerate(knowledge_items):
            title, icon, desc = item
            col_target = cols[idx % 3]
            with col_target:
                with st.container(border=True):
                    st.markdown(f"<h3 style='text-align: center; margin: 0;'>{icon}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; font-weight: bold; margin: 5px 0;'>{title}</p>", unsafe_allow_html=True)
                    st.caption(desc)
                    if st.button("📖 Đọc sách", use_container_width=True, key=f"open_kb_{idx}"):
                        st.session_state.kb_detail_page = title
                        st.rerun()
    else:
        current_region = st.session_state.kb_detail_page

        if st.button("⬅️ Quay lại danh mục", type="secondary", key="back_to_grid_kb"):
            st.session_state.kb_detail_page = None
            st.rerun()

        st.markdown("---")
        st.subheader(f"📚 SÁCH CHUYÊN KHOA: {current_region.upper()}")
        st.caption("Tài liệu huấn luyện và tra cứu nhanh lâm sàng Phục hồi chức năng vận động.")

        knowledge_textbook_db = {
            "Cột sống cổ": (
                "1. Giải phẫu & Sinh cơ học cột sống cổ",
                "Cột sống cổ gồm 7 đốt sống (C1-C7), chịu trách nhiệm nâng đỡ đầu và biên độ vận động lớn.",
                "Hội chứng cổ - vai - gáy, thoái hóa đốt sống cổ, thoát vị đĩa đệm cổ.",
                "Đau lan dọc xuống tay, tê bì ngón tay, hạn chế tầm vận động xoay cổ.",
                "Nghiệm pháp Spurling (nén ép cổ), Test kéo giãn cổ, Test Lhermitte.",
                "Giảm đau bằng vật lý trị liệu, kéo giãn cột sống cổ, tập mạnh nhóm cơ cổ sâu."
            ),
            # Các vùng khác tương tự...
        }

        content = knowledge_textbook_db.get(current_region, (
            "1. Tổng quan chuyên khảo",
            "Nội dung đang được cập nhật theo phác đồ chuẩn y khoa.",
            "Các hội chứng thường gặp và tổn thương cấu trúc liên quan.",
            "Triệu chứng lâm sàng điển hình và biểu hiện cơ năng, thực thể.",
            "Hệ thống nghiệm pháp, test đặc hiệu khám lâm sàng chuyên sâu.",
            "Phác đồ điều trị vật lý trị liệu và phục hồi chức năng vận động toàn diện."
        ))

        sec_title, intro, pathology, symptoms, tests, treatment = content

        st.markdown(f"#### 📖 {sec_title}")
        st.info(intro)

        with st.expander("📌 2. Các hội chứng & Bệnh lý thường gặp", expanded=True):
            st.markdown(pathology)

        with st.expander("🩺 3. Triệu chứng lâm sàng & Biểu hiện", expanded=True):
            st.markdown(symptoms)

        with st.expander("🔍 4. Hệ thống Test đặc hiệu & Nghiệm pháp", expanded=True):
            st.markdown(tests)

        with st.expander("⚙️ 5. Phác đồ Vật lý trị liệu & PHCN", expanded=True):
            st.markdown(treatment)

        st.markdown("---")
        if st.button("⬅️ Quay lại danh mục chuyên khoa", type="primary", key="bottom_back_btn"):
            st.session_state.kb_detail_page = None
            st.rerun()
