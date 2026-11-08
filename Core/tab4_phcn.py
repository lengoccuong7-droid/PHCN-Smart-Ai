# =========================================================
# TAB 4: KHO BÀI TẬP PHỤC HỒI CHỨC NĂNG (ĐỦ 9 BỆNH LÝ - 7 BÀI TẬP)
# =========================================================
import streamlit as st

def render_tab4():
    st.markdown("""
        <style>
        [data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 10px !important;
        }
        @media (min-width: 768px) {
            [data-testid="stHorizontalBlock"] {
                grid-template-columns: repeat(3, 1fr) !important;
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

    if "selected_pathology_m4" not in st.session_state:
        st.session_state.selected_pathology_m4 = None

    pathologies_m4 = {
        "1. Tai biến mạch máu não (Liệt nửa người)": {
            "icon": "🧠", "color": "linear-gradient(135deg, #48dbfb, #0abde3)",
            "exercises": [
                "1. Tập vận động thụ động các khớp bên liệt duy trì tầm vận động (ROM).",
                "2. Bài tập ức chế trương lực cơ co cứng (kỹ thuật Bobath).",
                "3. Tập chuyển đổi tư thế từ nằm ngửa sang nằm nghiêng và ngồi dậy.",
                "4. Tập kiểm soát thăng bằng thân mình ở tư thế ngồi độc lập.",
                "5. Tập đứng dồn trọng lượng đều hai chân trước gương.",
                "6. Bài tập đi lại với máng nẹp cẳng bàn chân (AFO) hoặc khung tập đi.",
                "7. Tập mạnh cơ chủ động bên lành và các nhóm cơ duỗi bên liệt."
            ]
        },
        "2. Rối loạn nuốt (Dysphagia) sau tai biến": {
            "icon": "🥣", "color": "linear-gradient(135deg, #ff9f43, #ee5253)",
            "exercises": [
                "1. Bài tập vận động cơ môi (mím chặt, cười hết cỡ, thổi phồng má, phát âm U-I).",
                "2. Bài tập vận động lưỡi (đẩy lưỡi ra trước, sang trái, sang phải, liếm vòm họng).",
                "3. Kích thích nhiệt lạnh vùng cung khẩu cái mềm kích thích phản xạ nuốt.",
                "4. Bài tập Masako (giữ đầu lưỡi giữa hai hàm răng và nuốt nước bọt).",
                "5. Bài tập Shaker (nâng đầu ở tư thế nằm ngửa để mở rộng cơ thắt thực quản trên).",
                "6. Bài tập đóng nắp thanh môn (nuốt giữ hơi, ho mạnh ngay sau khi nuốt).",
                "7. Luyện tập nuốt theo các độ quánh thức ăn chuẩn hóa IDDSI."
            ]
        },
        "3. Rối loạn ngôn ngữ & Thất ngôn (Aphasia)": {
            "icon": "🗣️", "color": "linear-gradient(135deg, #5f27cd, #341f97)",
            "exercises": [
                "1. Liệu pháp kích thích thính giác (nghe từ và chỉ tay vào hình ảnh/đồ vật).",
                "2. Luyện phát âm nguyên âm cơ bản (A - O - E - I - U) tròn khẩu hình.",
                "3. Bài tập gọi tên đồ vật sinh hoạt hằng ngày qua thẻ hình ảnh (Flashcard).",
                "4. Liệu pháp âm điệu ngữ âm (MEL/MIT) dùng nhịp điệu kích thích phát âm câu ngắn.",
                "5. Bài tập hoàn thành câu (bác sĩ đọc ngắt quãng, bệnh nhân nói từ cuối).",
                "6. Tập đặt câu hỏi và phản đáp các nhu cầu giao tiếp cơ bản (ăn, uống, đau, đi vệ sinh).",
                "7. Bài tập giao tiếp phi ngôn ngữ hỗ trợ (dùng cử chỉ tay, bảng ký hiệu)."
            ]
        },
        "4. Âm ngữ trị liệu (Rối loạn phát âm / Dysarthria)": {
            "icon": "🎶", "color": "linear-gradient(135deg, #10ac84, #1dd1a1)",
            "exercises": [
                "1. Bài tập kiểm soát hơi thở cơ hoành (thở sâu, giữ hơi, thổi nến đều).",
                "2. Bài tập tăng sức mạnh cơ hô hấp phục vụ phát âm câu dài.",
                "3. Bài tập vận động linh hoạt cơ quan phát âm (vòm miệng mềm, môi, lưỡi, hàm dưới).",
                "4. Luyện phát âm chính xác các cặp phụ âm - nguyên âm.",
                "5. Bài tập điều chỉnh tốc độ nói (nói chậm, ngắt nhịp theo từ).",
                "6. Bài tập kiểm soát cường độ và cao độ giọng nói (to/nhỏ, trầm/bổng).",
                "7. Luyện đọc đoạn văn ngắn trước gương kết hợp kiểm soát nhịp thở và khẩu hình."
            ]
        },
        "5. Trẻ tự kỷ (Rối loạn vận động & cảm giác)": {
            "icon": "🧸", "color": "linear-gradient(135deg, #f39c12, #e67e22)",
            "exercises": [
                "1. Bài tập điều hòa cảm giác tiền đình (nhún nhảy trên bóng trị liệu, đung đưa võng).",
                "2. Bài tập cảm giác bản thể (ôm chặt, ép khớp sâu, lăn cuộn trong thảm bọt biển).",
                "3. Bài tập đi trên ván thăng bằng nâng cao phối hợp vận động thô.",
                "4. Bài tập kéo giãn cơ cẳng chân (phòng ngừa và sửa dáng đi nhón gót).",
                "5. Bài tập vận động tinh bàn tay (nhặt hạt nhỏ, xếp hình khối, xâu chuỗi hạt).",
                "6. Bài tập phối hợp tay - mắt theo hiệu lệnh trò chơi tương tác.",
                "7. Bài tập bắt chước tư thế động học giúp tăng cường tập trung chú ý."
            ]
        },
        "6. Xơ hóa cơ ức đòn chũm (Vẹo cổ bẩm sinh)": {
            "icon": "👶", "color": "linear-gradient(135deg, #ff6b6b, #ee5253)",
            "exercises": [
                "1. Kéo giãn thụ động cơ ức đòn chũm bên bị xơ (nghiêng đầu sang bên lành, quay cằm về bên bệnh).",
                "2. Kích thích trẻ quay đầu về bên bệnh bằng âm thanh và đồ chơi màu sắc.",
                "3. Bài tập đặt tư thế nằm ngủ đúng (dùng gối cát/gối định hình giữ cổ thẳng).",
                "4. Kỹ thuật xoa bóp, miết nhẹ nhàng giải phóng dải xơ cơ ức đòn chũm.",
                "5. Bài tập vận động chủ động quay cổ (với trẻ lớn) qua các trò chơi theo tầm vận động.",
                "6. Tập mạnh cơ cổ bên đối diện để cân bằng lực kéo cột sống cổ.",
                "7. Hướng dẫn phụ huynh duy trì bế, cho bú và sinh hoạt ở tư thế điều chỉnh."
            ]
        },
        "7. PHCN sau Phẫu thuật đầu gối (Tái tạo ACL)": {
            "icon": "🦿", "color": "linear-gradient(135deg, #2e86de, #222f3e)",
            "exercises": [
                "1. Bài tập gồng cơ tĩnh tứ đầu đùi (Isometric Quads) ngay sau mổ.",
                "2. Bài tập duỗi thẳng gối tối đa (0 độ) và gấp gối thụ động trong phạm vi cho phép.",
                "3. Bài tập nhấc chân thẳng khỏi mặt giường (Straight Leg Raise).",
                "4. Tập đạp xe tại chỗ không kháng trở (khi biên độ gấp gối đạt trên 90 độ).",
                "5. Bài tập đứng dồn trọng lượng hai chân và chuyển trọng lượng sang chân mổ.",
                "6. Bài tập thăng bằng bản thể (Proprioception) trên đĩa thăng bằng hoặc thảm mềm.",
                "7. Bài tập mạnh cơ đùi sau (Hamstrings) và cơ cẳng chân có kháng lực tăng dần."
            ]
        },
        "8. PHCN sau Phẫu thuật thay khớp háng": {
            "icon": "🦾", "color": "linear-gradient(135deg, #0abde3, #2e86de)",
            "exercises": [
                "1. Bài tập co duỗi cổ chân (Ankle pumps) ngừa huyết khối tĩnh mạch sâu chi dưới.",
                "2. Bài tập siết cơ mông và cơ tứ đầu đùi ở tư thế nằm ngửa.",
                "3. Bài tập trượt gót chân trên giường (gấp khớp háng nhẹ nhàng < 90 độ).",
                "4. Bài tập dang chân sang bên (Abduction) tránh tư thế khép và xoay trong quá mức.",
                "5. Bài tập đứng dậy từ ghế cao có tay tựa với sự hỗ trợ của khung tập đi.",
                "6. Bài tập tái giáo dục dáng đi dồn lực đều hai chân, không khập khiễng.",
                "7. Bài tập leo cầu thang (nguyên tắc: chân lành bước lên trước, chân mổ bước xuống trước)."
            ]
        },
        "9. PHCN sau Gãy tay / Gãy chân (Hậu phẫu)": {
            "icon": "🦴", "color": "linear-gradient(135deg, #ee5253, #ff6b6b)",
            "exercises": [
                "1. Bài tập gồng cơ tĩnh bên trong bột (Isometric contraction) chống teo cơ.",
                "2. Cử động tích cực toàn bộ các khớp tự do không bị bất động (ngón tay/ngón chân).",
                "3. Sau tháo bột: Bài tập phục hồi tầm vận động (ROM) chủ động và thụ động các khớp lân cận.",
                "4. Kỹ thuật xoa bóp di động sẹo mổ và giải phóng mô mềm dính.",
                "5. Bài tập tăng dần lực cơ bằng tạ nhẹ, lò xo hoặc dây kháng lực (Theraband).",
                "6. Bài tập tái giáo dục dáng đi (với gãy chân) hoặc bài tập cầm nắm khéo léo (với gãy tay).",
                "7. Bài tập phục hồi chức năng sinh hoạt hằng ngày (ADL) thích ứng."
            ]
        }
    }

    # TRẠNG THÁI 1: LƯỚI ICON CHỌN NHÓM BỆNH PHCN
    if st.session_state.selected_pathology_m4 is None:
        st.markdown("### 🏋️‍♂️ Kho Bài Tập Phục Hồi Chức Năng")
        st.caption("Chọn nhóm bệnh lý để xem trọn bộ 7 bài tập chuyên sâu:")

        cols = st.columns(3)
        for idx, (path_key, data) in enumerate(pathologies_m4.items()):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="grid-card-box">
                        <div class="icon-circle-btn" style="background: {data['color']};">
                            {data['icon']}
                        </div>
                        <div style="font-weight: 700; font-size: 12px; color: #1f2937; height: 35px; display: flex; align-items: center; justify-content: center;">{path_key}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("Xem bài tập", key=f"btn_path_{idx}", use_container_width=True):
                    st.session_state.selected_pathology_m4 = path_key
                    st.rerun()

    # TRẠNG THÁI 2: MÀN HÌNH CHI TIẾT 7 BÀI TẬP
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
        
        exercises = pathologies_m4[st.session_state.selected_pathology_m4]["exercises"]
        for exercise in exercises:
            with st.container(border=True):
                st.markdown(f"- {exercise}")
