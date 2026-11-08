# =========================================================
# TAB 3: QUY TRÌNH KHÁM LÂM SÀNG & TỜ GIẤY TRẮNG
# =========================================================
import streamlit as st

def render_tab3():
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

    if "exam_active_region" not in st.session_state:
        st.session_state.exam_active_region = None

    if st.session_state.exam_active_region is None:
        st.markdown("### 🩺 Chọn Vùng Khám Lâm Sàng")
        
        regions = [
            {"id": "neck", "name": "Cột sống cổ", "icon": "🦴", "color": "linear-gradient(135deg, #ff6b6b, #ee5253)"},
            {"id": "back", "name": "Thắt lưng", "icon": "🩻", "color": "linear-gradient(135deg, #10ac84, #1dd1a1)"},
            {"id": "elbow", "name": "Khuỷu tay", "icon": "💪", "color": "linear-gradient(135deg, #5f27cd, #341f97)"},
            {"id": "knee", "name": "Khớp gối", "icon": "🦵", "color": "linear-gradient(135deg, #ff9f43, #ee5253)"}
        ]

        cols = st.columns(len(regions))
        for idx, reg in enumerate(regions):
            with cols[idx]:
                st.markdown(f"""
                    <div class="grid-card-box">
                        <div class="icon-circle-btn" style="background: {reg['color']};">
                            {reg['icon']}
                        </div>
                        <div style="font-weight: 700; font-size: 13px; color: #1f2937;">{reg['name']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("Chọn", key=f"fast_reg_{reg['id']}", use_container_width=True):
                    st.session_state.exam_active_region = reg['name']
                    st.rerun()
    else:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"#### 📝 Đang khám: `{st.session_state.exam_active_region}`")
        with c2:
            if st.button("⬅ Đổi vùng", use_container_width=True):
                st.session_state.exam_active_region = None
                st.rerun()

        st.markdown("---")

        left_col, right_col = st.columns([3, 2])
        with left_col:
            with st.expander("1️⃣ Hành chính & Triệu chứng", expanded=True):
                cur_p = st.session_state.get("current_patient", {})
                p_name = st.text_input("Họ tên", value=cur_p.get("name", ""), key="rt_p_name")
                p_phone = st.text_input("SĐT", value=cur_p.get("phone", ""), key="rt_p_phone")
                symptoms = st.text_area("Triệu chứng", key="rt_symptoms")
                nrs = st.slider("NRS (Đau)", 0, 10, 2, key="rt_nrs")

            with st.expander("2️⃣ Test & Tầm vận động", expanded=True):
                test_val = st.radio("Nghiệm pháp chính", ["Âm tính (-)", "Dương tính (+)"], key="rt_test")
                rom_val = st.text_input("ROM (Tầm vận động)", key="rt_rom")

        with right_col:
            st.markdown("#### 📄 Tờ Giấy Trắng")
            summary_text = f"""[BỆNH ÁN PHCN]
- Vùng: {st.session_state.get('exam_active_region', '---')}
- Bệnh nhân: {st.session_state.get('rt_p_name', '---')} ({st.session_state.get('rt_p_phone', '---')})
- Đau NRS: {st.session_state.get('rt_nrs', 0)}/10
- Triệu chứng: {st.session_state.get('rt_symptoms', '---')}
- Test: {st.session_state.get('rt_test', '---')}
- ROM: {st.session_state.get('rt_rom', '---')}"""
            with st.container(border=True):
                st.text_area("Bôi đen & Copy nội dung:", value=summary_text, height=220, key="quick_copy_box")
