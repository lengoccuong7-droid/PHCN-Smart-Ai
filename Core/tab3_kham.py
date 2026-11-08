# =========================================================
# TAB 3: QUY TRÌNH KHÁM LÂM SÀNG & TỜ GIẤY TRẮNG REAL-TIME
# =========================================================
import streamlit as st

def render_tab3():
    # Thêm CSS tùy chỉnh cho lưới Icon tròn phong cách app tiện ích
    st.markdown("""
        <style>
        .grid-card {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 20px 10px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            transition: all 0.3s ease;
            margin-bottom: 12px;
            border: 1px solid #f0f0f0;
        }
        .grid-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }
        .icon-circle {
            width: 65px;
            height: 65px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            margin: 0 auto 10px auto;
            color: white;
        }
        .card-title {
            font-size: 15px;
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 4px;
        }
        .card-desc {
            font-size: 11px;
            color: #6b7280;
        }
        </style>
    """, unsafe_allow_html=True)

    # Khởi tạo Session State vùng khám
    if "exam_active_region" not in st.session_state:
        st.session_state.exam_active_region = None

    # =========================================================
    # TRẠNG THÁI 1: CHƯA CHỌN VÙNG -> HIỂN THỊ DẠNG LƯỚI ICON TRÒN
    # =========================================================
    if st.session_state.exam_active_region is None:
        st.markdown("## 🩺 Khám Lâm Sàng PHCN")
        st.info("Vui lòng chọn một vùng cơ thể bên dưới để bắt đầu quy trình khám 4 bước:")

        regions = [
            {
                "id": "neck", 
                "name": "Cột sống cổ", 
                "desc": "Đau cổ vai cánh tay, hội chứng rễ", 
                "icon": "🦴", 
                "color": "linear-gradient(135deg, #ff6b6b, #ee5253)"
            },
            {
                "id": "back", 
                "name": "Cột sống thắt lưng", 
                "desc": "Đau thắt lưng, thoát vị đĩa đệm", 
                "icon": "🩻", 
                "color": "linear-gradient(135deg, #10ac84, #1dd1a1)"
            },
            {
                "id": "shoulder", 
                "name": "Khớp vai", 
                "desc": "Đông cứng khớp vai, rách chóp xoay", 
                "icon": "💪", 
                "color": "linear-gradient(135deg, #5f27cd, #341f97)"
            },
            {
                "id": "knee", 
                "name": "Khớp gối", 
                "desc": "Thoái hóa khớp, dây chằng, sụn chêm", 
                "icon": "🦵", 
                "color": "linear-gradient(135deg, #ff9f43, #ee5253)"
            }
        ]

        # Hiển thị 4 cột cho 4 vùng
        cols = st.columns(4)
        for idx, reg in enumerate(regions):
            with cols[idx % 4]:
                st.markdown(f"""
                    <div class="grid-card">
                        <div class="icon-circle" style="background: {reg['color']};">
                            {reg['icon']}
                        </div>
                        <div class="card-title">{reg['name']}</div>
                        <div class="card-desc">{reg['desc']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Khám {reg['name']}", key=f"btn_select_{reg['id']}", use_container_width=True):
                    st.session_state.exam_active_region = reg['name']
                    st.rerun()

    # =========================================================
    # TRẠNG THÁI 2: ĐÃ CHỌN VÙNG -> HIỂN THỊ DẠNG CUỘN ĐỂ NHẬP LIỆU
    # =========================================================
    else:
        # Header điều hướng quay lại
        col_title, col_back = st.columns([4, 1])
        with col_title:
            st.markdown(f"## 📝 Hồ sơ Khám: **{st.session_state.exam_active_region}**")
        with col_back:
            if st.button("⬅ Đổi vùng khác", use_container_width=True):
                st.session_state.exam_active_region = None
                st.rerun()

        st.markdown("---")

        # Chia 2 cột: Bên trái cuộn nhập liệu (60%), Bên phải "Tờ giấy trắng" Real-time (40%)
        left_col, right_col = st.columns([3, 2])

        with left_col:
            st.subheader("📋 Quy trình nhập liệu lâm sàng")
            
            # BƯỚC 1: HÀNH CHÍNH & TRIỆU CHỨNG
            with st.expander("1️⃣ Hành chính & Triệu chứng cơ năng", expanded=True):
                current_patient = st.session_state.get("current_patient", {})
                p_name = st.text_input("Họ và tên bệnh nhân", value=current_patient.get("name", ""), key="rt_p_name")
                p_phone = st.text_input("Số điện thoại", value=current_patient.get("phone", ""), key="rt_p_phone")
                symptoms = st.text_area("Bệnh sử & Triệu chứng chính", key="rt_symptoms", placeholder="Mô tả thời gian đau, tính chất đau...")
                nrs = st.slider("Thang điểm đau NRS (0 - 10)", 0, 10, 3, key="rt_nrs")

            # BƯỚC 2: TEST ĐẶC HIỆU THEO VÙNG
            with st.expander("2️⃣ Test đặc hiệu & Khám chuyên khoa", expanded=True):
                st.markdown(f"**Nghiệm pháp chuyên khoa vùng: {st.session_state.exam_active_region}**")
                
                region_name = st.session_state.exam_active_region
                test_results = {}
                
                if region_name == "Cột sống cổ":
                    test_results["Spurling Test"] = st.radio("Spurling Test", ["Âm tính (-)", "Dương tính (+)"], key="test_spurling")
                    test_results["Distraction Test"] = st.radio("Distraction Test (Kéo giãn cổ)", ["Âm tính (-)", "Dương tính (+)"], key="test_distraction")
                elif region_name == "Cột sống thắt lưng":
                    test_results["Lasegue Test (SLR)"] = st.radio("Lasegue Test (Nâng chân thẳng)", ["Âm tính (-)", "Dương tính (+)"], key="test_lasegue")
                    test_results["Schober Test"] = st.text_input("Chỉ số Schober (cm)", "10/15", key="test_schober")
                elif region_name == "Khớp vai":
                    test_results["Neer Test"] = st.radio("Neer Test", ["Âm tính (-)", "Dương tính (+)"], key="test_neer")
                    test_results["Hawkins-Kennedy"] = st.radio("Hawkins-Kennedy Test", ["Âm tính (-)", "Dương tính (+)"], key="test_hawkins")
                elif region_name == "Khớp gối":
                    test_results["Lachman Test"] = st.radio("Lachman Test (Dây chằng chéo)", ["Âm tính (-)", "Dương tính (+)"], key="test_lachman")
                    test_results["McMurray Test"] = st.radio("McMurray Test (Sụn chêm)", ["Âm tính (-)", "Dương tính (+)"], key="test_mcmurray")

                rom_val = st.text_input("Tầm vận động khớp (ROM)", key="rt_rom", placeholder="VD: Gập 120 độ, duỗi 0 độ")

            # BƯỚC 3: HÌNH ẢNH LÂM SÀNG
            with st.expander("3️⃣ Đính kèm hình ảnh / Chụp ảnh lâm sàng", expanded=False):
                st.file_uploader("Tải tệp ảnh X-Ray / MRI / Tư thế", type=["jpg", "png", "jpeg"], key="img_file_upload")
                st.camera_input("Hoặc chụp ảnh trực tiếp từ thiết bị", key="img_camera_capture")

            # Nút lưu bệnh án
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Hoàn tất & Lưu Lịch sử Khám", type="primary", use_container_width=True):
                visit_data = {
                    "patient_name": p_name,
                    "patient_phone": p_phone,
                    "region": region_name,
                    "symptoms": symptoms,
                    "nrs": nrs,
                    "tests": test_results,
                    "rom": rom_val
                }
                # Gọi HistoryManager để lưu tệp
                if "history_mgr" in st.session_state and p_phone:
                    st.session_state.history_mgr.save_visit(p_phone, visit_data)
                    st.success("✅ Đã lưu hồ sơ khám thành công vào hệ thống!")
                else:
                    st.success("✅ Đã ghi nhận hồ sơ khám!")

        # BƯỚC 4: TỜ GIẤY TRẮNG (REAL-TIME WHITE PAPER SUMMARY)
        with right_col:
            st.subheader("📄 Tờ Giấy Trắng (Tóm tắt Real-time)")
            with st.container(border=True):
                st.markdown(f"### **BỆNH ÁN PHỤC HỒI CHỨC NĂNG**")
                st.markdown(f"**Vùng khám:** `{st.session_state.exam_active_region}`")
                st.markdown("---")
                st.markdown(f"**Bệnh nhân:** {st.session_state.get('rt_p_name', '---')}")
                st.markdown(f"**SĐT:** {st.session_state.get('rt_p_phone', '---')}")
                st.markdown(f"**Mức độ đau (NRS):** `{st.session_state.get('rt_nrs', 0)}/10`")
                st.markdown(f"**Triệu chứng:** {st.session_state.get('rt_symptoms', 'Chưa nhập')}")
                st.markdown("---")
                st.markdown("**Kết quả Test đặc hiệu:**")
                for t_name in test_results:
                    st.markdown(f"- **{t_name}:** `{st.session_state.get(f'test_{t_name.split()[0].lower()}', 'Chưa khám')}`")
                st.markdown(f"**Tầm vận động (ROM):** {st.session_state.get('rt_rom', 'Chưa đo')}")
