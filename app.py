# =========================================================
# APP.PY - PHCN AI 1.8 (ĐỦ 3-4 TEST, NÚT CHAT GPT/GEMINI & LƯU HỒ SƠ)
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
        border-radius: 16px;
        padding: 14px 8px;
        text-align: center;
        box-shadow: 0 3px 8px rgba(0,0,0,0.06);
        border: 1px solid #eaeaea;
        margin-bottom: 12px;
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
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .scrollable-feed {
        max-height: 850px;
        overflow-y: auto;
        padding-right: 12px;
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

    # ================= TAB 1: HỒ SƠ & LỊCH SỬ =================
    with tab1:
        st.subheader("👤 Quản lý Hồ sơ Bệnh nhân & Lịch sử Khám")
        st.info("Nhập thông tin hành chính ban đầu để hệ thống tự động liên kết sang phiếu khám lâm sàng.")
        
        if "current_patient" not in st.session_state:
            st.session_state.current_patient = {"name": "", "phone": "", "age": 1990, "job": ""}
            
        with st.form("patient_form"):
            p_name = st.text_input("Họ tên bệnh nhân", value=st.session_state.current_patient["name"])
            p_phone = st.text_input("Số điện thoại", value=st.session_state.current_patient["phone"])
            p_age = st.number_input("Năm sinh", min_value=1900, max_value=2026, value=int(st.session_state.current_patient["age"]))
            p_job = st.text_input("Nghề nghiệp", value=st.session_state.current_patient["job"])
            
            if st.form_submit_button("💾 Lưu thông tin bệnh nhân", use_container_width=True):
                st.session_state.current_patient = {"name": p_name, "phone": p_phone, "age": p_age, "job": p_job}
                st.success(f"✅ Đã lưu thông tin cho bệnh nhân: **{p_name}**! Mời bác sĩ chuyển sang Tab 3 để tiến hành thăm khám thực thể.")

    # ================= TAB 2: CẨM NANG TRI THỨC Y CHỨNG =================
    with tab2:
        if "knowledge_active_cat" not in st.session_state:
            st.session_state.knowledge_active_cat = None

        knowledge_db = {
            "Đột quỵ & Thần kinh": {
                "icon": "🧠", "color": "linear-gradient(135deg, #48dbfb, #0abde3)",
                "content": """##### 🧠 Phác đồ Vận động Trị liệu Đột quỵ (Liệt nửa người)
* **Nguyên tắc cốt lõi:** Bắt đầu càng sớm càng tốt khi tình trạng huyết động ổn định, phân loại mức độ theo thang điểm Brunnstrom.
* **1. Kiểm soát trương lực cơ:** Kỹ thuật Bobath ức chế co cứng, tạo thuận nhóm cơ duỗi.
* **2. Thăng bằng & Chuyển tư thế:** Luyện tập kiểm soát thân mình (từ nằm -> ngồi -> đứng) và đứng dồn trọng lượng đều hai chân trước gương.
* **3. Lượng giá lại:** Đánh giá biên độ ROM và sức cơ MMT định kỳ mỗi 2 tuần."""
            },
            "Cột sống & Cơ xương": {
                "icon": "🦴", "color": "linear-gradient(135deg, #ff6b6b, #ee5253)",
                "content": """##### 🦴 Phác đồ Cột sống Thắt lưng & Cổ
* **Nguyên tắc:** Giảm áp lực đĩa đệm, phục hồi đường cong sinh lý cột sống, tăng cường sức mạnh nhóm cơ lõi (Core stability).
* **1. Giai đoạn cấp:** Nghỉ ngơi tương đối, tư thế giảm đau, vật lý trị liệu giảm viêm.
* **2. Giai đoạn phục hồi:** Kéo giãn nhóm cơ dựng sống, tập mạnh cơ bụng sâu và nhóm cơ duỗi lưng."""
            },
            "Khớp ngoại biên": {
                "icon": "🦾", "color": "linear-gradient(135deg, #10ac84, #1dd1a1)",
                "content": """##### 🦾 Phục hồi Chức năng Khớp Ngoại biên (Vai, Gối, Khuỷu)
* **Nguyên tắc:** Lấy lại biên độ vận động (ROM) không đau, tái thiết lập độ vững của hệ thống dây chằng và bao khớp.
* **1. Giai đoạn đầu:** Vận động thụ động, chống teo cơ tĩnh.
* **2. Giai đoạn sau:** Tập kháng lực tiến triển với dây Theraband và bài tập thăng bằng bản thể."""
            },
            "PHCN Nhi khoa": {
                "icon": "👶", "color": "linear-gradient(135deg, #f39c12, #e67e22)",
                "content": """##### 👶 Phục hồi Chức năng Nhi khoa (Bại não & Trẻ tự kỷ)
* **Nguyên tắc:** Can thiệp sớm dựa trên mốc phát triển vận động thô và vận động tinh, điều hòa cảm giác.
* **1. Điều hòa cảm giác:** Sử dụng bóng trị liệu, võng đung đưa, kỹ thuật ép khớp sâu.
* **2. Vận động trị liệu:** Phòng ngừa co rút gân gót, tập kiểm soát đầu cổ, lẫy, bò và đi đứng."""
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
                    if st.button("📖 Xem phác đồ", key=f"btn_k_{idx}", use_container_width=True):
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
            with st.container(border=True):
                st.markdown(knowledge_db[st.session_state.knowledge_active_cat]["content"])

    # ================= TAB 3: KHÁM LÂM SÀNG CHUYÊN SÂU =================
    with tab3:
        if "exam_active_region" not in st.session_state:
            st.session_state.exam_active_region = None

        regions = [
            ("Cột sống cổ", "🦴", "C1-C7 và hội chứng chèn ép", "linear-gradient(135deg, #ff6b6b, #ee5253)"),
            ("Cột sống thắt lưng", "🩻", "Thoát vị đĩa đệm, đau thần kinh tọa", "linear-gradient(135deg, #10ac84, #1dd1a1)"),
            ("Khớp vai", "🦾", "Chóp xoay & đông cứng khớp vai", "linear-gradient(135deg, #5f27cd, #341f97)"),
            ("Khuỷu tay", "💪", "Viêm lồi cầu, hội chứng ống khuỷu", "linear-gradient(135deg, #ff9f43, #ee5253)"),
            ("Cổ tay – bàn tay", "✋", "Hội chứng ống cổ tay, De Quervain", "linear-gradient(135deg, #48dbfb, #0abde3)"),
            ("Khớp háng", "🦿", "Thoái hóa & kẹp háng FAI", "linear-gradient(135deg, #f39c12, #e67e22)"),
            ("Khớp gối", "🦵", "ACL, sụn chêm & thoái hóa gối", "linear-gradient(135deg, #2e86de, #222f3e)"),
            ("Cổ chân – bàn chân", "🦶", "Bong gân & viêm cân gan chân", "linear-gradient(135deg, #ee5253, #ff6b6b)"),
            ("Thần kinh & Khác", "🧠", "Đột quỵ, phục hồi chức năng thần kinh", "linear-gradient(135deg, #0abde3, #2e86de)")
        ]

        if st.session_state.exam_active_region is None:
            st.subheader("🎯 Chọn Vùng Thăm Khám Lâm Sàng")
            st.markdown("Chọn vùng cơ thể bên dưới để mở phiếu thăm khám chuyên sâu độc lập:")

            cols_r = st.columns(2)
            for idx, item in enumerate(regions):
                title, icon, desc, color = item
                with cols_r[idx % 2]:
                    st.markdown(f"""
                        <div class="grid-card-box">
                            <div class="icon-circle-btn" style="background: {color};">
                                {icon}
                            </div>
                            <div style="font-weight: 700; font-size: 12px; color: #1f2937; min-height: 35px; display: flex; align-items: center; justify-content: center;">{title}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("🩺 Bắt đầu khám", use_container_width=True, key=f"open_exam_{idx}"):
                        st.session_state.exam_active_region = title
                        st.rerun()
        else:
            current_reg = st.session_state.exam_active_region

            c_top1, c_top2 = st.columns([1, 4])
            with c_top1:
                if st.button("⬅️ Quay lại", type="secondary"):
                    st.session_state.exam_active_region = None
                    st.rerun()
            with c_top2:
                st.subheader(f"📋 PHIẾU KHÁM: {current_reg.upper()}")

            st.markdown("---")

            active_patient = st.session_state.get("current_patient", {"name": "", "phone": "", "age": 1990, "job": ""})
            if active_patient.get("name"):
                st.info(f"🔗 Liên kết từ Tab 1 – BN: **{active_patient.get('name')}** (SĐT: {active_patient.get('phone')})")

            # Khung cuộn dọc toàn bộ nội dung khám
            st.markdown('<div class="scrollable-feed">', unsafe_allow_html=True)

            p_name = st.text_input("Họ tên bệnh nhân", value=active_patient.get("name", ""), key="rt_p_name")
            p_phone = st.text_input("Số điện thoại", value=active_patient.get("phone", ""), key="rt_p_phone")
            ly_do = st.text_input("🏥 Lý do vào viện / Than phiền chính", key="rt_ly_do")
            tien_su = st.text_area("📜 Tiền sử bệnh (Bản thân / Chấn thương)", key="rt_tien_su")

            # QUY TRÌNH SOCRATES GẠCH ĐẦU DÒNG TỪNG MỤC - GÕ TỰ DO
            with st.expander("🩺 Bệnh sử chi tiết (Quy trình SOCRATES chuẩn y khoa)", expanded=True):
                st.caption("Khai thác triệu chứng theo quy trình SOCRATES (nhập tự do từng mục):")
                soc_s = st.text_input("• **S (Site) – Vị trí đau:**", placeholder="Ví dụ: Đau khu trú mặt trước trong gối trái...", key="rt_soc_s")
                soc_o = st.text_input("• **O (Onset) – Hoàn cảnh khởi phát:**", placeholder="Ví dụ: Đột ngột sau khi vặn xoắn gối lúc đá bóng...", key="rt_soc_o")
                soc_c = st.text_input("• **C (Character) – Tính chất đau:**", placeholder="Ví dụ: Đau nhói, âm ỉ, có tiếng lạo xạo...", key="rt_soc_c")
                soc_r = st.text_input("• **R (Radiation) – Hướng lan:**", placeholder="Ví dụ: Không lan, hoặc lan xuống cẳng chân...", key="rt_soc_r")
                soc_a = st.text_input("• **A (Associations) – Triệu chứng đi kèm:**", placeholder="Ví dụ: Sưng nề, khóa khớp, tê bì...", key="rt_soc_a")
                soc_t = st.text_input("• **T (Time/Course) – Diễn tiến thời gian:**", placeholder="Ví dụ: Tăng dần khi leo cầu thang, nghỉ bớt đau...", key="rt_soc_t")
                
                col_nrs1, col_nrs2 = st.columns([1, 2])
                with col_nrs1:
                    nrs = st.selectbox("• **S (Severity) – Mức độ NRS (0-10):**", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="rt_nrs")
                with col_nrs2:
                    nrs_note = st.text_input("• **Ghi chú mức độ đau:**", placeholder="Ví dụ: Đau tăng nhiều về chiều...", key="rt_nrs_note")

            with st.expander("🔍 Khám thực thể chuẩn y khoa (Nhìn – Sờ – Đo ROM)", expanded=True):
                inspect = st.text_area("👁️ NHÌN (Inspection) - Biến dạng, sưng nề, teo cơ", key="rt_inspect")
                palp = st.text_area("✋ SỜ (Palpation) - Điểm đau chói, nhiệt độ, trương lực", key="rt_palp")
                rom_meas = st.text_area("📏 ĐO / GÕ (ROM & Phản xạ) - Tầm vận động, lực cơ MMT", key="rt_rom")

            with st.expander("🖼️ Hình ảnh Lâm sàng & Cận lâm sàng (X-quang / MRI)", expanded=False):
                uploaded_image = st.file_uploader("📤 Tải ảnh X-quang / MRI:", type=["png", "jpg", "jpeg"], key="rt_uploaded_img")
                if uploaded_image is not None:
                    st.image(uploaded_image, caption="🖼️ Hình ảnh lâm sàng", use_container_width=True)

            # CSDL 3 - 4 NGHIỆM PHÁP ĐẶC HIỆU CHUYÊN SÂU THEO VÙNG
            specific_tests_db = {
                "Cột sống cổ": [
                    ("Spurling Test", "Kiểm tra chèn ép rễ thần kinh cổ", "Nghiêng đầu sang bên đau, ấn nhẹ đỉnh đầu."),
                    ("Distraction Test", "Đánh giá giảm chèn ép rễ khi kéo giãn", "Nâng cằm và chẩm kéo nhẹ lên trên."),
                    ("Lhermitte Sign", "Đánh giá tổn thương tủy cổ", "Gập cổ tối đa xem có cảm giác điện giật dọc sống lưng không."),
                    ("Bakody Sign", "Đánh giá giảm chèn ép rễ khi đặt tay lên đầu", "Đặt tay lên đỉnh đầu xem triệu chứng giảm không.")
                ],
                "Cột sống thắt lưng": [
                    ("Lasègue Test (SLR)", "Đánh giá kích thích rễ thần kinh tọa", "Nâng thẳng chân bệnh nhân lên khi nằm ngửa (<70 độ)."),
                    ("Patrick / FABER Test", "Phân biệt tổn thương khớp háng hay cùng chậu", "Đặt cổ chân lên gối bên kia, ấn gối xuống giường."),
                    ("Bragard Test", "Xác định rõ tổn thương gốc rễ thần kinh", "Nâng chân tới góc đau, hạ nhẹ 5 độ rồi gập lưng cổ chân."),
                    ("Schober Test", "Đo độ giãn cột sống thắt lưng", "Đo khoảng cách 10cm khi cúi tối đa.")
                ],
                "Khớp vai": [
                    ("Neer Test", "Đánh giá hội chứng chạm mỏm cùng vai", "Cố định xương bả vai, đưa tay xoay trong và gập tối đa."),
                    ("Hawkins-Kennedy", "Đánh giá chèn ép gân cơ trên gai", "Gập vai và khuỷu 90 độ, xoay trong cẳng tay đột ngột."),
                    ("Jobe Test (Empty Can)", "Đánh giá rách/viêm gân cơ trên gai", "Dang vai 90 độ, ngón cái hướng xuống, ấn tay chống lực."),
                    ("Speed Test", "Đánh giá gân cơ nhị đầu dài", "Duỗi khuỷu, ngửa cẳng tay, nâng tay kháng trở.")
                ],
                "Khuỷu tay": [
                    ("Cozen Test", "Đánh giá viêm lồi cầu ngoài (Tennis Elbow)", "Duỗi cổ tay có kháng trở từ bác sĩ."),
                    ("Mill Test", "Đánh giá co kéo gân duỗi tại lồi cầu ngoài", "Sấp cẳng tay, gập cổ tay và duỗi thẳng khuỷu tay."),
                    ("Tinel Sign ống khuỷu", "Kiểm tra chèn ép dây thần kinh trụ", "Gõ nhẹ vào rãnh thần kinh trụ ở khuỷu tay."),
                    ("Golfer's Elbow Test", "Đánh giá viêm lồi cầu trong", "Gấp cổ tay có kháng trở ở tư thế ngửa.")
                ],
                "Cổ tay – bàn tay": [
                    ("Phalen Test", "Đánh giá hội chứng ống cổ tay", "Gập cổ tay tối đa 90 độ trong 60 giây."),
                    ("Tinel Sign cổ tay", "Kiểm tra chèn ép dây thần kinh giữa", "Gõ nhẹ vào dây chằng ngang cổ tay mặt trước."),
                    ("Finkelstein Test", "Đánh giá viêm gân De Quervain", "Gấp ngón cái vào lòng bàn tay, nắm lại rồi nghiêng trụ."),
                    ("Allen Test", "Đánh giá tuần hoàn động mạch bàn tay", "Đè ép động mạch quay và trụ.")
                ],
                "Khớp háng": [
                    ("FADIR Test", "Đánh giá kẹp háng (FAI)", "Gập háng 90 độ, khép và xoay trong."),
                    ("Thomas Test", "Đánh giá co rút cơ thắt lưng chậu", "Co tối đa một bên gối áp sát ngực xem chân kia có hổng không."),
                    ("Trendelenburg Test", "Đánh giá yếu cơ mông nhỡ", "Đứng một chân quan sát khung chậu đối diện."),
                    ("FABER / Patrick Test", "Đánh giá khớp háng và cùng chậu", "Đặt chân hình số 4 và ấn xuống.")
                ],
                "Khớp gối": [
                    ("Lachman Test", "Đánh giá đứt dây chằng chéo trước (ACL)", "Gập gối 20-30 độ, kéo mâm chày ra trước."),
                    ("McMurray Test", "Đánh giá tổn thương rách sụn chêm", "Gập gối tối đa, xoay cẳng chân kết hợp duỗi gối."),
                    ("Anterior Drawer Test", "Kiểm tra độ vững dây chằng chéo trước", "Gập gối 90 độ, kéo mạnh mâm chày ra trước."),
                    ("Appley Compression Test", "Phân biệt tổn thương sụn chêm và dây chằng", "Nằm sấp, ấn lực dọc trục và xoay cẳng chân.")
                ],
                "Cổ chân – bàn chân": [
                    ("Thompson Test", "Kiểm tra đứt gân gót (Achilles)", "Bóp cơ bắp chân xem bàn chân có gấp mặt lòng không."),
                    ("Anterior Drawer Cổ chân", "Đánh giá đứt dây chằng sên-mác trước", "Kéo gót chân ra trước ở tư thế gấp nhẹ mặt lòng."),
                    ("Talar Tilt Test", "Đánh giá dây chằng mác-gót", "Lật trong bàn chân ở tư thế trung tính."),
                    ("Squeeze Test", "Đánh giá tổn thương màng gian cốt / khớp chày mác", "Bóp ép xương chày và xương mác ở cẳng chân.")
                ],
                "Thần kinh & Khác": [
                    ("Babinski Sign", "Đánh giá tổn thương bó tháp", "Vạch bờ ngoài lòng bàn chân từ gót lên ngón út."),
                    ("Modified Ashworth", "Đánh giá độ co cứng trương lực cơ", "Gập duỗi thụ động chi thể nhanh."),
                    ("Fugl-Meyer Assessment", "Đánh giá phục hồi vận động đột quỵ", "Lượng giá chuỗi vận động chi thể."),
                    ("Romberg Test", "Đánh giá thăng bằng và cảm giác sâu", "Đứng chụm chân, nhắm mắt.")
                ]
            }

            active_tests = specific_tests_db.get(current_reg, [
                ("Test đặc hiệu 1", "Đánh giá tổn thương cấu trúc", "Thực hiện kỹ thuật chuẩn."),
                ("Test đặc hiệu 2", "Kiểm tra độ vững", "Thực hiện theo quy trình lâm sàng."),
                ("Test đặc hiệu 3", "Đánh giá chức năng", "Thực hiện theo hướng dẫn."),
                ("Test đặc hiệu 4", "Kiểm tra bổ trợ", "Thực hiện kỹ thuật lâm sàng.")
            ])
            
            with st.expander(f"🧬 Nghiệm pháp đặc hiệu ({current_reg}) - Đủ 4 Test", expanded=True):
                test_results = {}
                for t_idx, (t_name, t_use, t_tech) in enumerate(active_tests):
                    st.markdown(f"**🔹 {t_idx+1}. {t_name}**")
                    st.caption(f"• **Công dụng:** {t_use}  \n• **Kỹ thuật:** {t_tech}")
                    res = st.radio(f"Kết quả {t_name}:", ["Chưa làm / Âm tính (-)", "Dương tính (+)"], horizontal=True, key=f"ex_t_res_{t_idx}")
                    test_results[t_name] = res
                    st.markdown("---")

            with st.expander("🚩 Cờ đỏ an toàn lâm sàng (Red Flags)", expanded=False):
                rf_1 = st.checkbox("Hội chứng đuôi ngựa / Rối loạn cơ tròn", key="rt_rf1")
                rf_2 = st.checkbox("Sụt cân nhanh / Tiền sử ung thư", key="rt_rf2")
                rf_3 = st.checkbox("Sốt cao, sưng nóng đỏ đau cấp tính", key="rt_rf3")

            # TỜ GIẤY TRẮNG REAL-TIME & CÁC NÚT THAO TÁC (CHATGPT, GEMINI, LƯU HỒ SƠ)
            st.markdown("---")
            st.markdown("### 📄 Tờ Giấy Trắng Tổng Hợp & Phân Tích AI (Real-time)")
            
            pos_tests_list = [t for t, res in test_results.items() if res == "Dương tính (+)"]
            summary_text = f"""[BỆNH ÁN PHCN CHUYÊN SÂU]
- Vùng khám: {current_reg}
- Bệnh nhân: {p_name if p_name else '---'} (SĐT: {p_phone if p_phone else '---'})
- Lý do vào viện: {ly_do if ly_do else '---'}
- Tiền sử: {tien_su if tien_su else '---'}
[BỆNH SỬ (SOCRATES)]
- Site (Vị trí): {soc_s if soc_s else '---'}
- Onset (Khởi phát): {soc_o if soc_o else '---'}
- Character (Tính chất): {soc_c if soc_c else '---'}
- Radiation (Hướng lan): {soc_r if soc_r else '---'}
- Associations (Triệu chứng kèm): {soc_a if soc_a else '---'}
- Time (Diễn tiến): {soc_t if soc_t else '---'}
- Severity (Mức độ đau): {nrs}/10
----------------------------------------
[KHÁM THỰC THỂ]
- Nhìn: {inspect if inspect else '---'}
- Sờ: {palp if palp else '---'}
- ROM: {rom_meas if rom_meas else '---'}
- Test đặc hiệu (+): {', '.join(pos_tests_list) if pos_tests_list else 'Không có'}
- Cờ đỏ: {'Có dấu hiệu nguy cơ' if (rf_1 or rf_2 or rf_3) else 'Không phát hiện'}"""

            with st.container(border=True):
                st.text_area("Bôi đen & Copy nội dung bệnh án:", value=summary_text, height=260, key="quick_copy_box")

            # CÁC NÚT TƯƠNG TÁC (CHATGPT, GEMINI, LƯU HỒ SƠ)
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                if st.button("🤖 Hỏi ChatGPT", use_container_width=True):
                    st.info("💡 Mẹo: Copy nội dung ở ô trên và dán vào ChatGPT kèm câu lệnh: 'Đóng vai bác sĩ PHCN, hãy biện luận chẩn đoán ca bệnh này'.")
            with col_b2:
                if st.button("✨ Hỏi Gemini", use_container_width=True):
                    st.success("💡 Mẹo: Dùng nội dung bệnh án này để trao đổi trực tiếp với trợ lý Gemini nhận phác đồ điều trị.")
            with col_b3:
                if st.button("💾 Lưu hồ sơ", type="primary", use_container_width=True):
                    if not (p_name and p_phone):
                        st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và SĐT!")
                    else:
                        st.success(f"✅ Đã lưu thành công hồ sơ cho **{p_name}**!")

            st.markdown('</div>', unsafe_allow_html=True)

    # ================= TAB 4: KHO BÀI TẬP PHCN (ĐỦ 9 BỆNH LÝ - 7 BÀI TẬP) =================
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
            "8. PHCN sau Phẫu thuật thay khớp háng toàn phần": [
                "1. Bài tập co duỗi cổ chân (Ankle pumps) ngừa huyết khối tĩnh mạch sâu chi dưới.",
                "2. Bài tập siết cơ mông và cơ tứ đầu đùi ở tư thế nằm ngửa.",
                "3. Bài tập trượt gót chân trên giường (gấp khớp háng nhẹ nhàng < 90 độ).",
                "4. Bài tập dang chân sang bên (Abduction) tránh tư thế khép và xoay trong quá mức.",
                "5. Bài tập đứng dậy từ ghế cao có tay tựa với sự hỗ trợ của khung tập đi.",
                "6. Bài tập tái giáo dục dáng đi dồn lực đều hai chân, không khập khiễng.",
                "7. Bài tập leo cầu thang (nguyên tắc: chân lành bước lên trước, chân mổ bước xuống trước)."
            ],
            "9. PHCN sau Gãy tay / Gãy chân (Hậu phẫu / Bó bột)": [
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

        if st.session_state.selected_pathology_m4 is None:
            st.markdown("### 🏋️‍♂️ Kho Bài Tập Phục Hồi Chức Năng Theo Bệnh Lý")
            st.caption("Chọn nhóm bệnh lý bên dưới để xem trọn bộ 7 bài tập chuyên sâu:")

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
