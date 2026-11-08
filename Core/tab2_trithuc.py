# =========================================================
# TAB 2: CẨM NANG TRI THỨC Y HỌC CHỨNG CỨ (TỐC ĐỘ CAO)
# =========================================================
import streamlit as st

def render_tab2():
    st.markdown("""
        <style>
        [data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 10px !important;
        }
        @media (min-width: 768px) {
            [data-testid="stHorizontalBlock"] {
                grid-template-columns: repeat(4, 1fr) !important;
            }
        }
        .grid-card-box {
            background: #ffffff;
            border-radius: 16px;
            padding: 14px 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid #eaeaea;
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
        </style>
    """, unsafe_allow_html=True)

    if "knowledge_active_cat" not in st.session_state:
        st.session_state.knowledge_active_cat = None

    # TRẠNG THÁI 1: LƯỚI ICON CHỌN CHUYÊN KHOA
    if st.session_state.knowledge_active_cat is None:
        st.markdown("### 📚 Cẩm Nang Tri Thức Y Chứng")
        
        categories = [
            {"id": "stroke", "name": "Đột quỵ não", "icon": "🧠", "color": "linear-gradient(135deg, #48dbfb, #0abde3)"},
            {"id": "spine", "name": "Cột sống", "icon": "🦴", "color": "linear-gradient(135deg, #ff6b6b, #ee5253)"},
            {"id": "joint", "name": "Khớp ngoại biên", "icon": "🦾", "color": "linear-gradient(135deg, #10ac84, #1dd1a1)"},
            {"id": "pediatric", "name": "PHCN Nhi khoa", "icon": "👶", "color": "linear-gradient(135deg, #f39c12, #e67e22)"}
        ]

        cols = st.columns(len(categories))
        for idx, cat in enumerate(categories):
            with cols[idx]:
                st.markdown(f"""
                    <div class="grid-card-box">
                        <div class="icon-circle-btn" style="background: {cat['color']};">
                            {cat['icon']}
                        </div>
                        <div style="font-weight: 700; font-size: 13px; color: #1f2937;">{cat['name']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("Xem", key=f"fast_cat_{cat['id']}", use_container_width=True):
                    st.session_state.knowledge_active_cat = cat['name']
                    st.rerun()

    # TRẠNG THÁI 2: MÀN HÌNH CUỘN ĐỌC TÀI LIỆU
    else:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"#### 📖 Chủ đề: `{st.session_state.knowledge_active_cat}`")
        with c2:
            if st.button("⬅ Quay lại", use_container_width=True):
                st.session_state.knowledge_active_cat = None
                st.rerun()

        st.markdown("---")
        
        # Danh sách bài viết cuộn dọc
        with st.container(border=True):
            st.markdown("##### 📄 Hướng dẫn chẩn đoán và lượng giá lâm sàng")
            st.caption("Cập nhật theo chuẩn y học chứng cứ quốc tế.")
            st.markdown("""
            - **1. Đánh giá ban đầu:** Khảo sát mức độ độc lập, tầm vận động và trương lực cơ.
            - **2. Can thiệp cốt lõi:** Áp dụng bài tập vận động trị liệu đúng ngưỡng sinh lý.
            - **3. Theo dõi tiến triển:** Đánh giá lại sau mỗi đợt điều trị (2 tuần/lần).
            """)
        
        with st.container(border=True):
            st.markdown("##### 📄 Phác đồ điều trị phục hồi chuyên sâu")
            st.markdown("Tài liệu tham khảo dành riêng cho bác sĩ và kỹ thuật viên vật lý trị liệu.")
