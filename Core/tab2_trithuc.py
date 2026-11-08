# =========================================================
# TAB 2: CẨM NANG TRI THỨC Y HỌC CHỨNG CỨ
# =========================================================
import streamlit as st

def render(history_mgr=None):
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
        .scrollable-content {
            max-height: 750px;
            overflow-y: auto;
            padding-right: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    if "knowledge_active_cat" not in st.session_state:
        st.session_state.knowledge_active_cat = None

    knowledge_db = {
        "Đột quỵ & Thần kinh": {
            "icon": "🧠", "color": "linear-gradient(135deg, #48dbfb, #0abde3)",
            "content": "Phác đồ vận động trị liệu sớm cho bệnh nhân đột quỵ:\n- Đánh giá giai đoạn co cứng theo Brunnstrom.\n- Áp dụng kỹ thuật ức chế trương lực cơ Bobath.\n- Lượng giá thăng bằng thân mình và bài tập chuyển đổi tư thế."
        },
        "Cột sống & Cơ xương": {
            "icon": "🦴", "color": "linear-gradient(135deg, #ff6b6b, #ee5253)",
            "content": "Nguyên tắc điều trị hội chứng thắt lưng hông & cột sống cổ:\n- Kiểm soát đau cấp tính bằng phương pháp giảm áp và tư thế đúng.\n- Bài tập kéo giãn nhóm cơ dựng sống và tăng cường cơ lõi (Core stability)."
        },
        "Khớp ngoại biên": {
            "icon": "🦾", "color": "linear-gradient(135deg, #10ac84, #1dd1a1)",
            "content": "Phục hồi chức năng sau tổn thương khớp (Vai, gối, khuỷu):\n- Duy trì và gia tăng tầm vận động (ROM) không đau.\n- Tăng sức mạnh cơ quanh khớp bằng bài tập kháng lực tiến triển."
        },
        "PHCN Nhi khoa": {
            "icon": "👶", "color": "linear-gradient(135deg, #f39c12, #e67e22)",
            "content": "Can thiệp sớm cho trẻ bại não và rối loạn phát triển:\n- Kỹ thuật điều hòa cảm giác (Sensory Integration).\n- Bài tập tạo thuận vận động thô và vận động tinh theo mốc phát triển."
        }
    }

    if st.session_state.knowledge_active_cat is None:
        st.markdown("### 📚 Cẩm Nang Tri Thức Y Chứng")
        st.caption("Chọn chuyên khoa bên dưới để tra cứu phác đồ và tài liệu lâm sàng chuẩn hóa:")

        cols = st.columns(2)
        for idx, (cat_name, data) in enumerate(knowledge_db.items()):
            with cols[idx % 2]:
                st.markdown(f"""
                    <div class="grid-card-box">
                        <div class="icon-circle-btn" style="background: {data['color']};">
                            {data['icon']}
                        </div>
                        <div style="font-weight: 700; font-size: 13px; color: #1f2937;">{cat_name}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("📖 Xem tài liệu", key=f"btn_k_cat_{idx}", use_container_width=True):
                    st.session_state.knowledge_active_cat = cat_name
                    st.rerun()
    else:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"#### 📖 Chuyên khoa: `{st.session_state.knowledge_active_cat}`")
        with c2:
            if st.button("⬅ Quay lại", use_container_width=True):
                st.session_state.knowledge_active_cat = None
                st.rerun()

        st.markdown("---")
        st.markdown('<div class="scrollable-content">', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("##### 📄 Nội dung phác đồ & Hướng dẫn y khoa")
            st.markdown(knowledge_db[st.session_state.knowledge_active_cat]["content"])
            
        st.markdown('</div>', unsafe_allow_html=True)
