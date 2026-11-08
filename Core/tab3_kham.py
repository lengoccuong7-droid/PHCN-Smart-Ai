# =========================================================
# TAB 3: QUY TRÌNH KHÁM LÂM SÀNG & TỜ GIẤY TRẮNG (CÓ KHUNG CUỘN)
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
        /* Khung cuộn dọc cho trang chi tiết khám */
        .scrollable-exam-container {
            max-height: 750px;
            overflow-y: auto;
            padding-right: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    if "exam_active_region" not in st.session_state:
        st.session_state.exam_active_region = None

    # TRẠNG THÁI 1: LƯỚI ICON CHỌN VÙNG KHÁM
    if st.session_state.exam_active_region is None:
        st.markdown("### 🩺 Chọn Vùng Khám Lâm Sàng")
        st.caption("Chọn vùng cơ thể cần khám thực thể:")
        
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
                    
    # TRẠNG THÁI 2: MÀN HÌNH KHÁM CHI TIẾT CÓ KHUNG CUỘN DỌC
    else:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"#### 📝 Đang khám vùng: `{st.session_state.exam_active_region}`")
        with c2:
            if st.button("⬅ Đổi vùng", use_container_width=True):
                st.session_state.exam_active_region = None
                st.rerun()

        st.markdown("---")

        # Đặt toàn bộ nội dung nhập liệu và tờ giấy trắng vào container có cuộn dọc
        with st.container():
            left_col, right_col = st.columns([3, 2])
            
            with left_col:
                st.markdown('<div class="scrollable-exam-container">', unsafe_allow_html=True)
                
                with st.expander("1️⃣ Hành chính & Triệu chứng", expanded=True):
                    cur_p = st.session_state.get("current_patient", {})
                    p_name = st.text_input("Họ tên bệnh nhân", value=cur_p.get("name", ""), key="rt_p_name")
                    p_phone = st.text_input("Số điện thoại", value=cur_p.get("phone", ""), key="rt_p_phone")
                    symptoms = st.text_area("Lý do vào viện / Triệu chứng chính", key="rt_symptoms")
                    nrs = st.slider("Mức độ đau (NRS)", 0, 10, 2, key="rt_nrs")

                with st.expander("2️⃣ Khám Thực Thể (4 Bước)", expanded=True):
                    st.text_input("👁️ Nhìn (Inspection)", key="exam_nhin", placeholder="Biến dạng, sưng nề, bầm tím...")
                    st.text_input("✋ Sờ (Palpation)", key="exam_so", placeholder="Điểm đau, nhiệt độ, co cứng cơ...")
                    st.text_input("📏 Đo ROM (Tầm vận động)", key="exam_rom", placeholder="Biên độ vận động chủ động/thụ động...")

                with st.expander("3️⃣ Nghiệm pháp / Test đặc hiệu", expanded=True):
                    st.radio("Test 1 (Đặc hiệu chính)", ["Chưa làm / Âm tính (-)", "Dương tính (+)"], key="test_1")
                    st.radio("Test 2 (Hỗ trợ)", ["Chưa làm / Âm tính (-)", "Dương tính (+)"], key="test_2")

                with st.expander("4️⃣ Cờ đỏ an toàn & Đính kèm", expanded=False):
                    st.checkbox("🚩 Có dấu hiệu cờ đỏ (Sốt, sụt cân, yếu liệt chi...)", key="flag_red")
                    st.file_uploader("📁 Đính kèm hình ảnh (X-quang, MRI...)", type=["jpg", "png", "jpeg"], key="exam_file")
                
                st.markdown('</div>', unsafe_allow_html=True)

            with right_col:
                st.markdown("#### 📄 Tờ Giấy Trắng Real-Time")
                summary_text = f"""[BỆNH ÁN PHCN]
- Vùng khám: {st.session_state.get('exam_active_region', '---')}
- Bệnh nhân: {st.session_state.get('rt_p_name', '---')} ({st.session_state.get('rt_p_phone', '---')})
- Đau NRS: {st.session_state.get('rt_nrs', 0)}/10
- Lý do vào viện: {st.session_state.get('rt_symptoms', '---')}
----------------------------------------
[KHÁM THỰC THỂ]
- Nhìn: {st.session_state.get('exam_nhin', '---')}
- Sờ: {st.session_state.get('exam_so', '---')}
- ROM: {st.session_state.get('exam_rom', '---')}
- Test 1: {st.session_state.get('test_1', '---')}
- Test 2: {st.session_state.get('test_2', '---')}
- Cờ đỏ: {'Có' if st.session_state.get('flag_red') else 'Không'}"""
                
                with st.container(border=True):
                    st.text_area("Bôi đen & Copy nội dung:", value=summary_text, height=380, key="quick_copy_box")
