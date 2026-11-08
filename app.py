# =========================================================
# APP.PY - PHCN AI 1.8 (HOÀN CHỈNH, ĐỦ DỮ LIỆU & BỐ CỤC)
# =========================================================
import streamlit as st

st.set_page_config(
    page_title="PHCN AI 1.8",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CHUNG CHO GIAO DIỆN GRID-TO-SCROLL ---
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

def main():
    st.title("🩺 PHCN AI 1.8 – Trợ lý Phục hồi Chức năng & Lâm sàng")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Hồ sơ & Lịch sử", 
        "📚 Cẩm nang Tri thức", 
        "🩺 Khám Lâm sàng", 
        "🏋️‍♂️ Kho Bài tập PHCN"
    ])

    # ================= TAB 1: HỒ SƠ =================
    with tab1:
        st.subheader("👤 Quản lý Hồ sơ Bệnh nhân & Lịch sử Khám")
        st.info("Sử dụng trình quản lý lịch sử để tra cứu và lưu trữ bệnh án.")

    # ================= TAB 2: CẨM NANG TRI THỨC =================
    with tab2:
        if "knowledge_active_cat" not in st.session_state:
            st.session_state.knowledge_active_cat = None

        if st.session_state.knowledge_active_cat is None:
            st.markdown("### 📚 Cẩm Nang Tri Thức Y Chứng")
            st.caption("Chọn chuyên khoa để tra cứu phác đồ và tài liệu lâm sàng:")
            
            categories = [
                {"id": "stroke", "name": "Đột quỵ & Thần kinh", "icon": "🧠", "color": "linear-gradient(135deg, #48dbfb, #0abde3)"},
                {"id": "spine", "name": "Cột sống & Cơ xương", "icon": "🦴", "color": "linear-gradient(135deg, #ff6b6b, #ee5253)"},
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
        else:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"#### 📖 Chuyên khoa: `{st.session_state.knowledge_active_cat}`")
            with c2:
                if st.button("⬅ Quay lại", use_container_width=True):
                    st.session_state.knowledge_active_cat = None
                    st.rerun()

            st.markdown("---")
            with st.container(border=True):
                st.markdown("##### 📄 Nguyên tắc Vận động Trị liệu Y học Chứng cứ")
                st.markdown("""
                * **Mục tiêu:** Phòng ngừa co rút biến dạng, gia tăng khả năng độc lập sinh hoạt tối đa cho người bệnh.
                * **Nguyên tắc cốt lõi:** Bắt đầu càng sớm càng tốt khi tình trạng toàn thân ổn định; loại bỏ mẫu vận động bất thường bằng kỹ thuật tạo thuận thần kinh cơ.
                """)

    # ================= TAB 3: KHÁM LÂM SÀNG =================
    with tab3:
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
                    p_name = st.text_input("Họ tên", key="rt_p_name")
                    p_phone = st.text_input("SĐT", key="rt_p_phone")
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
- Đau NRS: {st.session_state.get('rt_nrs', 0)}/10"""
                with st.container(border=True):
                    st.text_area("Copy nội dung:", value=summary_text, height=220)

    # ================= TAB 4: KHO BÀI TẬP PHCN =================
    with tab4:
        st.markdown("### 🏋️‍♂️ Kho Bài Tập Phục Hồi Chức Năng Theo Bệnh Lý")
        st.caption("Chọn nhóm bệnh lý để xem trọn bộ 7 bài tập chuyên sâu:")

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
            ],
            "3. Rối loạn ngôn ngữ & Thất ngôn (Aphasia)": [
                "1. Liệu pháp kích thích thính giác (nghe từ và chỉ tay vào hình ảnh/đồ vật).",
                "2. Luyện phát âm nguyên âm cơ bản (A - O - E - I - U) tròn khẩu hình.",
                "3. Bài tập gọi tên đồ vật sinh hoạt hằng ngày qua thẻ hình ảnh (Flashcard).",
                "4. Liệu pháp âm điệu ngữ âm (MEL/MIT) dùng nhịp điệu kích thích phát âm câu ngắn.",
                "5. Bài tập hoàn thành câu (bác sĩ đọc ngắt quãng, bệnh nhân nói từ cuối).",
                "6. Tập đặt câu hỏi và phản đáp các nhu cầu giao tiếp cơ bản (ăn, uống, đau, đi vệ sinh).",
                "7. Bài tập giao tiếp phi ngôn ngữ hỗ trợ (dùng cử chỉ tay, bảng ký hiệu)."
            ],
            "4. Âm ngữ trị liệu (Rối loạn phát âm / Dysarthria)": [
                "1. Bài tập kiểm soát hơi thở cơ hoành (thở sâu, giữ hơi, thổi nến đều).",
                "2. Bài tập tăng sức mạnh cơ hô hấp phục vụ phát âm câu dài.",
                "3. Bài tập vận động linh hoạt cơ quan phát âm (vòm miệng mềm, môi, lưỡi, hàm dưới).",
                "4. Luyện phát âm chính xác các cặp phụ âm - nguyên âm.",
                "5. Bài tập điều chỉnh tốc độ nói (nói chậm, ngắt nhịp theo từ).",
                "6. Bài tập kiểm soát cường độ và cao độ giọng nói (to/nhỏ, trầm/bổng).",
                "7. Luyện đọc đoạn văn ngắn trước gương kết hợp kiểm soát nhịp thở và khẩu hình."
            ],
            "5. Trẻ tự kỷ (Rối loạn vận động & cảm giác)": [
                "1. Bài tập điều hòa cảm giác tiền đình (nhún nhảy trên bóng trị liệu, đung đưa võng).",
                "2. Bài tập cảm giác bản thể (ôm chặt, ép khớp sâu, lăn cuộn trong thảm bọt biển).",
                "3. Bài tập đi trên ván thăng bằng nâng cao phối hợp vận động thô.",
                "4. Bài tập kéo giãn cơ cẳng chân (phòng ngừa và sửa dáng đi nhón gót).",
                "5. Bài tập vận động tinh bàn tay (nhặt hạt nhỏ, xếp hình khối, xâu chuỗi hạt).",
                "6. Bài tập phối hợp tay - mắt theo hiệu lệnh trò chơi tương tác.",
                "7. Bài tập bắt chước tư thế động học giúp tăng cường tập trung chú ý."
            ],
            "6. Xơ hóa cơ ức đòn chũm (Vẹo cổ bẩm sinh)": [
                "1. Kéo giãn thụ động cơ ức đòn chũm bên bị xơ (nghiêng đầu sang bên lành, quay cằm về bên bệnh).",
                "2. Kích thích trẻ quay đầu về bên bệnh bằng âm thanh và đồ chơi màu sắc.",
                "3. Bài tập đặt tư thế nằm ngủ đúng (dùng gối cát/gối định hình giữ cổ thẳng).",
                "4. Kỹ thuật xoa bóp, miết nhẹ nhàng giải phóng dải xơ cơ ức đòn chũm.",
                "5. Bài tập vận động chủ động quay cổ (với trẻ lớn) qua các trò chơi theo tầm vận động.",
                "6. Tập mạnh cơ cổ bên đối diện để cân bằng lực kéo cột sống cổ.",
                "7. Hướng dẫn phụ huynh duy trì bế, cho bú và sinh hoạt ở tư thế điều chỉnh."
            ],
            "7. PHCN sau Phẫu thuật đầu gối (Tái tạo ACL)": [
                "1. Bài tập gồng cơ tĩnh tứ đầu đùi (Isometric Quads) ngay sau mổ.",
                "2. Bài tập duỗi thẳng gối tối đa (0 độ) và gấp gối thụ động trong phạm vi cho phép.",
                "3. Bài tập nhấc chân thẳng khỏi mặt giường (Straight Leg Raise).",
                "4. Tập đạp xe tại chỗ không kháng trở (khi biên độ gấp gối đạt trên 90 độ).",
                "5. Bài tập đứng dồn trọng lượng hai chân và chuyển trọng lượng sang chân mổ.",
                "6. Bài tập thăng bằng bản thể (Proprioception) trên đĩa thăng bằng hoặc thảm mềm.",
                "7. Bài tập mạnh cơ đùi sau (Hamstrings) và cơ cẳng chân có kháng lực tăng dần."
            ],
            "8. PHCN sau Phẫu thuật thay khớp háng": [
                "1. Bài tập co duỗi cổ chân (Ankle pumps) ngừa huyết khối tĩnh mạch sâu chi dưới.",
                "2. Bài tập siết cơ mông và cơ tứ đầu đùi ở tư thế nằm ngửa.",
                "3. Bài tập trượt gót chân trên giường (gấp khớp háng nhẹ nhàng < 90 độ).",
                "4. Bài tập dang chân sang bên (Abduction) tránh tư thế khép và xoay trong quá mức.",
                "5. Bài tập đứng dậy từ ghế cao có tay tựa với sự hỗ trợ của khung tập đi.",
                "6. Bài tập tái giáo dục dáng đi dồn lực đều hai chân, không khập khiễng.",
                "7. Bài tập leo cầu thang (nguyên tắc: chân lành bước lên trước, chân mổ bước xuống trước)."
            ],
            "9. PHCN sau Gãy tay / Gãy chân (Hậu phẫu)": [
                "1. Bài tập gồng cơ tĩnh bên trong bột (Isometric contraction) chống teo cơ.",
                "2. Cử động tích cực toàn bộ các khớp tự do không bị bất động (ngón tay/ngón chân).",
                "3. Sau tháo bột: Bài tập phục hồi tầm vận động (ROM) chủ động và thụ động các khớp lân cận.",
                "4. Kỹ thuật xoa bóp di động sẹo mổ và giải phóng mô mềm dính.",
                "5. Bài tập tăng dần lực cơ bằng tạ nhẹ, lò xo hoặc dây kháng lực (Theraband).",
                "6. Bài tập tái giáo dục dáng đi (với gãy chân) hoặc bài tập cầm nắm khéo léo (với gãy tay).",
                "7. Bài tập phục hồi chức năng sinh hoạt hằng ngày (ADL) thích ứng."
            ]
        }

        if "selected_pathology_m4" not in st.session_state:
            st.session_state.selected_pathology_m4 = None

        cols_p = st.columns(2)
        for idx, path_key in enumerate(pathologies_m4.keys()):
            with cols_p[idx % 2]:
                if st.button(f"📌 {path_key}", use_container_width=True, key=f"btn_m4_path_{idx}"):
                    st.session_state.selected_pathology_m4 = path_key
                    st.rerun()

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

if __name__ == "__main__":
    main()
