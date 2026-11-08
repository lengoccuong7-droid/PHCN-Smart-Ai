# =========================================================
# APP.PY - PHCN AI 1.8 (HOÀN CHỈNH, TỐI ƯU MOBILE & KHÔNG LỖI IMPORT)
# =========================================================
import streamlit as st

st.set_page_config(
    page_title="PHCN AI 1.8",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS TỐI ƯU GIAO DIỆN DI ĐỘNG & MÁY TÍNH ---
st.markdown("""
    <style>
    .grid-card-box {
        background: #ffffff;
        border-radius: 14px;
        padding: 12px 8px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border: 1px solid #eaeaea;
        margin-bottom: 10px;
    }
    .icon-circle-btn {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        margin: 0 auto 6px auto;
        color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("🩺 PHCN AI 1.8 – Trợ lý Phục hồi Chức năng & Lâm sàng")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Hồ sơ", 
        "📚 Tri thức", 
        "🩺 Khám Lâm sàng", 
        "🏋️‍♂️ Bài tập PHCN"
    ])

    # ================= TAB 1: HỒ SƠ =================
    with tab1:
        st.subheader("👤 Quản lý Hồ sơ Bệnh nhân & Lịch sử Khám")
        st.info("Sử dụng trình quản lý lịch sử để tra cứu và lưu trữ bệnh án.")
        
        # Khởi tạo session lưu bệnh nhân hiện tại nếu chưa có
        if "current_patient" not in st.session_state:
            st.session_state.current_patient = {"name": "", "phone": "", "age": 1990, "job": ""}
            
        with st.form("patient_form"):
            p_name = st.text_input("Họ tên bệnh nhân", value=st.session_state.current_patient["name"])
            p_phone = st.text_input("Số điện thoại", value=st.session_state.current_patient["phone"])
            p_age = st.number_input("Năm sinh", min_value=1900, max_value=2026, value=int(st.session_state.current_patient["age"]))
            p_job = st.text_input("Nghề nghiệp", value=st.session_state.current_patient["job"])
            
            if st.form_submit_button("💾 Lưu thông tin bệnh nhân", use_container_width=True):
                st.session_state.current_patient = {"name": p_name, "phone": p_phone, "age": p_age, "job": p_job}
                st.success(f"Đã lưu thông tin cho bệnh nhân: **{p_name}**! Chuyển sang Tab 3 để khám lâm sàng.")

    # ================= TAB 2: CẨM NANG TRI THỨC =================
    with tab2:
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
            st.caption("Chọn chuyên khoa bên dưới để tra cứu phác đồ:")

            for cat_name, data in knowledge_db.items():
                if st.button(f"{data['icon']} {cat_name}", use_container_width=True, key=f"k_cat_{cat_name}"):
                    st.session_state.knowledge_active_cat = cat_name
                    st.rerun()
        else:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"#### 📖 `{st.session_state.knowledge_active_cat}`")
            with c2:
                if st.button("⬅ Quay lại", use_container_width=True):
                    st.session_state.knowledge_active_cat = None
                    st.rerun()

            st.markdown("---")
            with st.container(border=True):
                st.markdown(knowledge_db[st.session_state.knowledge_active_cat]["content"])

    # ================= TAB 3: KHÁM LÂM SÀNG =================
    with tab3:
        if "exam_active_region" not in st.session_state:
            st.session_state.exam_active_region = None

        regions = [
            ("Cột sống cổ", "🦴", "linear-gradient(135deg, #ff6b6b, #ee5253)"),
            ("Cột sống thắt lưng", "🩻", "linear-gradient(135deg, #10ac84, #1dd1a1)"),
            ("Khớp vai", "🦾", "linear-gradient(135deg, #5f27cd, #341f97)"),
            ("Khuỷu tay", "💪", "linear-gradient(135deg, #ff9f43, #ee5253)"),
            ("Cổ tay – bàn tay", "✋", "linear-gradient(135deg, #48dbfb, #0abde3)"),
            ("Khớp háng", "🦿", "linear-gradient(135deg, #f39c12, #e67e22)"),
            ("Khớp gối", "🦵", "linear-gradient(135deg, #2e86de, #222f3e)"),
            ("Cổ chân – bàn chân", "🦶", "linear-gradient(135deg, #ee5253, #ff6b6b)"),
            ("Thần kinh & Khác", "🧠", "linear-gradient(135deg, #0abde3, #2e86de)")
        ]

        if st.session_state.exam_active_region is None:
            st.subheader("🎯 Chọn Vùng Thăm Khám Lâm Sàng")
            st.markdown("Chọn vùng cơ thể để mở phiếu thăm khám:")

            for title, icon, color in regions:
                if st.button(f"{icon} {title}", use_container_width=True, key=f"reg_btn_{title}"):
                    st.session_state.exam_active_region = title
                    st.rerun()
        else:
            current_reg = st.session_state.exam_active_region

            if st.button("⬅️ Quay lại chọn vùng khám", type="secondary"):
                st.session_state.exam_active_region = None
                st.rerun()

            st.markdown(f"### 📋 PHIẾU KHÁM: {current_reg.upper()}")
            st.markdown("---")

            active_patient = st.session_state.get("current_patient", {"name": "", "phone": "", "age": 1990, "job": ""})
            if active_patient.get("name"):
                st.info(f"🔗 Liên kết từ Tab 1 – BN: **{active_patient.get('name')}** (SĐT: {active_patient.get('phone')})")

            # Form nhập liệu 1 cột dọc tối ưu mobile
            p_name = st.text_input("Họ tên bệnh nhân", value=active_patient.get("name", ""), key="rt_p_name")
            p_phone = st.text_input("Số điện thoại", value=active_patient.get("phone", ""), key="rt_p_phone")
            ly_do = st.text_input("🏥 Lý do vào viện / Than phiền chính", key="rt_ly_do")

            with st.expander("🩺 Bệnh sử (SOCRATES) & Đau", expanded=True):
                character = st.text_input("Tính chất đau (Character)", key="rt_char")
                nrs = st.selectbox("Mức độ đau NRS (0-10)", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="rt_nrs")

            with st.expander("🔍 Khám thực thể (Nhìn – Sờ – Đo ROM)", expanded=True):
                inspect = st.text_area("👁️ NHÌN (Inspection)", key="rt_inspect")
                palp = st.text_area("✋ SỜ (Palpation)", key="rt_palp")
                rom_meas = st.text_area("📏 ĐO / GÕ (ROM & Phản xạ)", key="rt_rom")

            with st.expander("🧬 Nghiệm pháp đặc hiệu", expanded=False):
                test_res = st.radio("Kết quả test", ["Âm tính (-)", "Dương tính (+)"], horizontal=True, key="ex_t_res_0")

            # TỜ GIẤY TRẮNG REAL-TIME HIỂN THỊ XUỐNG DƯỚI RỘNG RÃI
            st.markdown("---")
            st.markdown("### 📄 Tờ Giấy Trắng & Phân Tích AI")
            
            summary_text = f"""[BỆNH ÁN PHCN]
- Vùng khám: {current_reg}
- Bệnh nhân: {p_name if p_name else '---'} ({p_phone if p_phone else '---'})
- Lý do: {ly_do if ly_do else '---'}
- Đau NRS: {nrs}/10
- Nhìn: {inspect if inspect else '---'}
- Sờ: {palp if palp else '---'}
- ROM: {rom_meas if rom_meas else '---'}"""

            with st.container(border=True):
                st.text_area("Bôi đen & Copy nội dung:", value=summary_text, height=200, key="quick_copy_box")

    # ================= TAB 4: KHO BÀI TẬP PHCN =================
    with tab4:
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
                "1. Bài tập vận động cơ môi (mím chặt, cười hết cỡ, thổi phồng má).",
                "2. Bài tập vận động lưỡi (đẩy lưỡi ra trước, sang trái, sang phải).",
                "3. Kích thích nhiệt lạnh vùng cung khẩu cái mềm.",
                "4. Bài tập Masako (giữ đầu lưỡi giữa hai hàm răng và nuốt).",
                "5. Bài tập Shaker (nâng đầu ở tư thế nằm ngửa).",
                "6. Bài tập đóng nắp thanh môn (nuốt giữ hơi, ho mạnh).",
                "7. Luyện tập nuốt theo các độ quánh thức ăn chuẩn hóa IDDSI."
            ],
            "3. Rối loạn ngôn ngữ & Thất ngôn (Aphasia)": [
                "1. Liệu pháp kích thích thính giác qua hình ảnh/đồ vật.",
                "2. Luyện phát âm nguyên âm cơ bản (A - O - E - I - U).",
                "3. Bài tập gọi tên đồ vật sinh hoạt qua Flashcard.",
                "4. Liệu pháp âm điệu ngữ âm (MEL/MIT).",
                "5. Bài tập hoàn thành câu ngắn.",
                "6. Tập đặt câu hỏi và phản đáp nhu cầu cơ bản.",
                "7. Bài tập giao tiếp phi ngôn ngữ hỗ trợ."
            ],
            "4. Âm ngữ trị liệu (Rối loạn phát âm)": [
                "1. Bài tập kiểm soát hơi thở cơ hoành.",
                "2. Tăng sức mạnh cơ hô hấp.",
                "3. Vận động linh hoạt cơ quan phát âm.",
                "4. Luyện phát âm cặp phụ âm - nguyên âm.",
                "5. Điều chỉnh tốc độ nói.",
                "6. Kiểm soát cường độ và cao độ giọng nói.",
                "7. Luyện đọc đoạn văn ngắn trước gương."
            ],
            "5. Trẻ tự kỷ (Vận động & Cảm giác)": [
                "1. Điều hòa cảm giác tiền đình trên bóng trị liệu.",
                "2. Cảm giác bản thể (ôm chặt, ép khớp sâu).",
                "3. Đi trên ván thăng bằng phối hợp vận động thô.",
                "4. Kéo giãn cơ cẳng chân chống nhón gót.",
                "5. Vận động tinh bàn tay (nhặt hạt, xếp hình).",
                "6. Phối hợp tay - mắt theo trò chơi tương tác.",
                "7. Bắt chước tư thế động học tăng tập trung."
            ],
            "6. Xơ hóa cơ ức đòn chũm (Vẹo cổ)": [
                "1. Kéo giãn thụ động cơ ức đòn chũm bên bị xơ.",
                "2. Kích thích trẻ quay đầu về bên bệnh.",
                "3. Đặt tư thế nằm ngủ định hình giữ cổ thẳng.",
                "4. Xoa bóp, miết nhẹ giải phóng mô mềm.",
                "5. Vận động chủ động quay cổ qua trò chơi.",
                "6. Tập mạnh cơ cổ bên đối diện.",
                "7. Hướng dẫn phụ huynh duy trì tư thế đúng."
            ],
            "7. PHCN sau Phẫu thuật đầu gối (ACL)": [
                "1. Gồng cơ tĩnh tứ đầu đùi ngay sau mổ.",
                "2. Duỗi thẳng gối tối đa và gấp gối thụ động.",
                "3. Nhấc chân thẳng khỏi mặt giường.",
                "4. Đạp xe tại chỗ không kháng trở.",
                "5. Đứng dồn trọng lượng sang chân mổ.",
                "6. Thăng bằng bản thể trên đĩa/thảm mềm.",
                "7. Mạnh cơ đùi sau và cẳng chân kháng lực."
            ],
            "8. PHCN sau Phẫu thuật thay khớp háng": [
                "1. Co duỗi cổ chân ngừa huyết khối.",
                "2. Siết cơ mông và cơ tứ đầu đùi.",
                "3. Trượt gót chân trên giường.",
                "4. Dang chân sang bên tránh khép quá mức.",
                "5. Đứng dậy từ ghế cao có tay tựa.",
                "6. Tái giáo dục dáng đi đều hai chân.",
                "7. Tập leo cầu thang đúng nguyên tắc."
            ],
            "9. PHCN sau Gãy tay / Gãy chân": [
                "1. Gồng cơ tĩnh bên trong bột chống teo cơ.",
                "2. Cử động khớp tự do không bị bất động.",
                "3. Phục hồi tầm vận động (ROM) sau tháo bột.",
                "4. Xoa bóp di động sẹo mổ, giải phóng mô dính.",
                "5. Tăng dần lực cơ bằng tạ nhẹ/dây kháng lực.",
                "6. Tái giáo dục dáng đi hoặc cầm nắm khéo léo.",
                "7. Phục hồi chức năng sinh hoạt hằng ngày (ADL)."
            ]
        }

        if "selected_pathology_m4" not in st.session_state:
            st.session_state.selected_pathology_m4 = None

        if st.session_state.selected_pathology_m4 is None:
            st.markdown("### 🏋️‍♂️ Kho Bài Tập Phục Hồi Chức Năng")
            st.caption("Chọn nhóm bệnh lý bên dưới để xem trọn bộ 7 bài tập:")

            for path_key in pathologies_m4.keys():
                if st.button(f"📌 {path_key}", use_container_width=True, key=f"btn_m4_{path_key}"):
                    st.session_state.selected_pathology_m4 = path_key
                    st.rerun()
        else:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"#### 🏥 Phác đồ: `{st.session_state.selected_pathology_m4}`")
            with c2:
                if st.button("⬅ Quay lại", use_container_width=True):
                    st.session_state.selected_pathology_m4 = None
                    st.rerun()

            st.markdown("---")
            st.markdown("##### 📋 Trọn bộ 7 bài tập phục hồi chức năng chuẩn hóa:")
            
            exercises = pathologies_m4[st.session_state.selected_pathology_m4]
            for exercise in exercises:
                with st.container(border=True):
                    st.markdown(f"- {exercise}")

if __name__ == "__main__":
    main()
