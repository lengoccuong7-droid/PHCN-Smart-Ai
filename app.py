# =========================================================
# APP.PY - PHCN AI 1.8 (PHIÊN BẢN HOÀN CHỈNH - ĐÃ SỬA LỖI CÚ PHÁP)
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
    st.title("🩺 PHCN AI 1.8 – Trợ lý Phục hồi Chức năng & Lâm sàng Chuyên sâu")
    
    # Khởi tạo kho lưu trữ bệnh nhân và lịch sử toàn cục trong session_state
    if "patient_db" not in st.session_state:
        st.session_state.patient_db = {} 
    if "current_patient_phone" not in st.session_state:
        st.session_state.current_patient_phone = ""

    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Hồ sơ & Lịch sử", 
        "📚 Cẩm nang Tri thức Y Chứng", 
        "🩺 Khám Lâm sàng Chuyên Sâu", 
        "🏋️‍♂️ Kho Bài tập PHCN"
    ])

    # ================= TAB 1: HỒ SƠ & XEM LẠI LỊCH SỬ =================
    with tab1:
        st.subheader("👤 Quản lý Hồ sơ Bệnh nhân & Tra cứu Lịch sử Khám")
        st.info("Thông tin nhập ở đây sẽ tự động đồng bộ sang Tab 3 (Khám lâm sàng). Bạn có thể tạo mới hoặc chọn bệnh nhân cũ để xem lại lịch sử.")

        col_h1, col_h2 = st.columns(2)
        
        with col_h1:
            st.markdown("##### 📝 Thêm / Cập nhật thông tin bệnh nhân")
            with st.form("patient_form_tab1"):
                p_name_input = st.text_input("Họ tên bệnh nhân *", value="")
                p_phone_input = st.text_input("Số điện thoại (Mã định danh) *", value="")
                p_age_input = st.number_input("Năm sinh", min_value=1900, max_value=2026, value=1990)
                p_job_input = st.text_input("Nghề nghiệp", value="")
                
                submitted = st.form_submit_button("💾 Lưu & Kích hoạt Bệnh nhân", use_container_width=True)
                if submitted:
                    if not p_name_input or not p_phone_input:
                        st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và Số điện thoại!")
                    else:
                        phone_key = p_phone_input.strip()
                        if phone_key not in st.session_state.patient_db:
                            st.session_state.patient_db[phone_key] = {
                                "name": p_name_input,
                                "phone": phone_key,
                                "age": p_age_input,
                                "job": p_job_input,
                                "visits": []
                            }
                        else:
                            st.session_state.patient_db[phone_key]["name"] = p_name_input
                            st.session_state.patient_db[phone_key]["age"] = p_age_input
                            st.session_state.patient_db[phone_key]["job"] = p_job_input
                        
                        st.session_state.current_patient_phone = phone_key
                        st.success(f"✅ Đã kích hoạt bệnh nhân: **{p_name_input}**! Dữ liệu đã sẵn sàng ở Tab 3.")

        with col_h2:
            st.markdown("##### 📂 Tra cứu danh sách & Lịch sử khám")
            if not st.session_state.patient_db:
                st.caption("Chưa có hồ sơ bệnh nhân nào trong hệ thống.")
            else:
                patient_list = list(st.session_state.patient_db.keys())
                selected_phone = st.selectbox(
                    "Chọn bệnh nhân từ danh sách:",
                    options=patient_list,
                    format_func=lambda x: f"{st.session_state.patient_db[x]['name']} (SĐT: {x})"
                )
                
                if selected_phone:
                    pat_data = st.session_state.patient_db[selected_phone]
                    st.markdown(f"""
                        * **Họ tên:** {pat_data['name']}
                        * **Năm sinh:** {pat_data['age']} | **Nghề nghiệp:** {pat_data['job']}
                        * **Tổng số lượt khám đã lưu:** {len(pat_data['visits'])}
                    """)
                    
                    if st.button("👉 Chọn bệnh nhân này để khám", use_container_width=True):
                        st.session_state.current_patient_phone = selected_phone
                        st.success(f"Đã chọn **{pat_data['name']}**. Chuyển sang Tab 3 để tiến hành khám.")

                    if pat_data['visits']:
                        with st.expander("📜 Xem lịch sử các lần khám trước"):
                            for v_idx, visit in enumerate(pat_data['visits']):
                                st.markdown(f"**Lần {v_idx+1} | Ngày khám:** {visit.get('time', 'N/A')}")
                                st.markdown(f"- Vùng khám: `{visit.get('region')}` | NRS: {visit.get('nrs')}/10")
                                st.markdown(f"- Tóm tắt: {visit.get('summary_text')[:150]}...")
                                st.markdown("---")

    # ================= TAB 2: CẨM NANG TRI THỨC Y CHỨNG =================
    with tab2:
        if "knowledge_active_cat" not in st.session_state:
            st.session_state.knowledge_active_cat = None

        knowledge_db = {
            "Đột quỵ & Thần kinh": {
                "icon": "🧠", "color": "linear-gradient(135deg, #48dbfb, #0abde3)",
                "content": """##### 🧠 PHÁC ĐỒ PHCN ĐỘT QUṞUỴ & LIỆT NỬA NGƯỜI
* **1. Định nghĩa:** Hội chứng khiếm khuyết thần kinh khu trú do tổn thương mạch máu não đột ngột, gây liệt nửa người, rối loạn trương lực cơ và suy giảm vận động.
* **2. Chỉ định can thiệp theo giai đoạn:**
  * **Giai đoạn cấp (0 - 2 tuần):** Vận động thụ động phòng ngừa loét, biến dạng khớp; thay đổi tư thế mỗi 2 giờ; duy trì ROM không đau.
  * **Giai đoạn phục hồi (2 tuần - 6 tháng):** Kỹ thuật ức chế co cứng Bobath; tập kiểm soát thăng bằng thân mình; tập đứng dồn trọng lượng đều hai chân.
* **3. Chống chỉ định tuyệt đối / Thận trọng:**
  * Huyết động không ổn định (Huyết áp tâm thu > 180mmHg hoặc < 90mmHg).
  * Sốt cao, ổ nhồi máu não tiến triển cấp tính chưa qua giai đoạn phù não."""
            },
            "Cột sống & Cơ xương": {
                "icon": "🦴", "color": "linear-gradient(135deg, #ff6b6b, #ee5253)",
                "content": """##### 🦴 PHÁC ĐỒ CỘT SỐNG THẮT LƯNG & CỔ
* **1. Định nghĩa:** Hội chứng đau cột sống do thoái hóa, thoát vị đĩa đệm hoặc căng cơ mạn tính, thường kèm chèn ép rễ thần kinh.
* **2. Chỉ định can thiệp theo giai đoạn:**
  * **Giai đoạn cấp:** Nghỉ ngơi tương đối, nhiệt/điện trị liệu giảm đau, tư thế giảm áp đĩa đệm (tư thế gối gấp).
  * **Giai đoạn bán cấp & mạn:** Kéo giãn nhóm cơ dựng sống, tập mạnh cơ lõi (Core stability), bài tập McKenzie theo hướng dẫn.
* **3. Chống chỉ định tuyệt đối / Thận trọng:**
  * Hội chứng đuôi ngựa (rối loạn cơ tròn cấp) -> Chỉ định ngoại khoa khẩn cấp.
  * Chấn thương cột sống mất vững, nhiễm trùng hoặc ung thư di căn cột sống."""
            },
            "Khớp ngoại biên": {
                "icon": "🦾", "color": "linear-gradient(135deg, #10ac84, #1dd1a1)",
                "content": """##### 🦾 PHÁC ĐỒ PHCN KHỚP NGOẠI BIÊN (VAI, GỐI, KHUỶU)
* **1. Định nghĩa:** Tổn thương sụn khớp, gân cơ quanh khớp hoặc dây chằng do chấn thương thể thao hoặc thoái hóa nguyên phát.
* **2. Chỉ định can thiệp theo giai đoạn:**
  * **Giai đoạn hậu phẫu / Cấp tính:** Bất động hợp lý, vận động biên độ thụ động giới hạn, chườm lạnh giảm sưng.
  * **Giai đoạn phục hồi chức năng:** Tăng dần ROM không đau, tập kháng lực tiến triển với dây Theraband, thăng bằng bản thể.
* **3. Chống chỉ định tuyệt đối / Thận trọng:**
  * Đứt hoàn toàn gân cơ / dây chằng có chỉ định khâu nối cấp mà chưa qua thời gian liền sẹo an toàn.
  * Viêm khớp nhiễm trùng cấp tính."""
            },
            "PHCN Nhi khoa": {
                "icon": "👶", "color": "linear-gradient(135deg, #f39c12, #e67e22)",
                "content": """##### 👶 PHÁC ĐỒ PHCN NHI KHOA (BẠI NÃO & TỰ KỶ)
* **1. Định nghĩa:** Rối loạn phát triển vận động và tư thế do tổn thương não không tiến triển xảy ra ở não đang phát triển (Bại não), hoặc rối loạn tương tác xã hội và hành vi (Tự kỷ).
* **2. Chỉ định can thiệp theo giai đoạn:**
  * **Can thiệp sớm (0 - 3 tuổi):** Tạo thuận vận động thô theo mốc phát triển (lẫy, bò, ngồi); điều hòa cảm giác (Sensory Integration).
  * **Giai đoạn mẫu giáo & học đường:** Huấn luyện kỹ năng sinh hoạt hằng ngày (ADL), chỉnh hình ngừa co rút gân gót.
* **3. Chống chỉ định tuyệt đối / Thận trọng:**
  * Động kinh chưa kiểm soát bằng thuốc.
  * Trẻ đang trong tình trạng nhiễm trùng cấp hoặc suy hô hấp."""
            }
        }

        if st.session_state.knowledge_active_cat is None:
            st.markdown("### 📚 Cẩm Nang Tri Thức Y Chứng Lâm Sàng")
            st.caption("Chọn chuyên khoa bên dưới để tra cứu định nghĩa, chỉ định và chống chỉ định theo giai đoạn:")

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
                    if st.button("📖 Xem chi tiết phác đồ", key=f"btn_k_{idx}", use_container_width=True):
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

    # ================= TAB 3: KHÁM LÂM SÀNG CHUYÊN SÂU & TỜ GIẤY TRẮNG 2 PHẦN =================
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

            # Lấy thông tin bệnh nhân từ Tab 1 nếu có
            active_phone = st.session_state.get("current_patient_phone", "")
            default_name = ""
            default_phone = active_phone
            default_age = 1990
            default_job = ""

            if active_phone and active_phone in st.session_state.patient_db:
                p_info = st.session_state.patient_db[active_phone]
                default_name = p_info["name"]
                default_age = p_info["age"]
                default_job = p_info["job"]
                st.info(f"🔗 Đang liên kết tự động từ Tab 1 – Bệnh nhân: **{default_name}** (SĐT: {default_phone})")
            else:
                st.warning("⚠️ Chưa chọn bệnh nhân ở Tab 1. Bạn có thể nhập trực tiếp thông tin hành chính bên dưới:")

            # Khung cuộn dọc toàn bộ nội dung khám
            st.markdown('<div class="scrollable-feed">', unsafe_allow_html=True)

            # PHẦN 1: HÀNH CHÍNH (Đồng bộ từ Tab 1)
            st.markdown("##### 👤 1. Thông tin Hành chính Bệnh nhân")
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                p_name = st.text_input("Họ tên bệnh nhân", value=default_name, key="rt_p_name")
                p_phone = st.text_input("Số điện thoại", value=default_phone, key="rt_p_phone")
            with col_a2:
                p_age = st.number_input("Năm sinh", min_value=1900, max_value=2026, value=int(default_age), key="rt_p_age")
                p_job = st.text_input("Nghề nghiệp", value=default_job, key="rt_p_job")

            ly_do = st.text_area("🏥 Lý do vào viện / Than phiền chính", placeholder="Nhập lý do vào viện (tự động xuống dòng)...", height=80, key="rt_ly_do")
            tien_su = st.text_area("📜 Tiền sử bệnh (Bản thân / Chấn thương)", height=80, key="rt_tien_su")

            # PHẦN 2: BỆNH SỬ (SOCRATES) & KHÁM THỰC THỂ (CẬP NHẬT REAL-TIME)
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

            # TỜ GIẤY TRẮNG REAL-TIME CHIA 2 PHẦN: PHẦN TRÊN HÀNH CHÍNH, PHẦN DƯỚI DỮ LIỆU KHÁM
            st.markdown("---")
            st.markdown("### 📄 Tờ Giấy Trắng Tổng Hợp & Phân Tích AI (Real-time)")
            
            pos_tests_list = [t for t, res in test_results.items() if res == "Dương tính (+)"]
            
            summary_text = f"""========================================
I. THÔNG TIN HÀNH CHÍNH BỆNH NHÂN
========================================
- Họ tên: {p_name if p_name else '---'} (Năm sinh: {p_age})
- Số điện thoại: {p_phone if p_phone else '---'}
- Nghề nghiệp: {p_job if p_job else '---'}
- Vùng thăm khám: {current_reg}

========================================
II. DỮ LIỆU KHÁM & BỆNH SỬ LÂM SÀNG
========================================
- Lý do vào viện: {ly_do if ly_do else '---'}
- Tiền sử: {tien_su if tien_su else '---'}

[QUY TRÌNH SOCRATES]
- Site (Vị trí): {soc_s if soc_s else '---'}
- Onset (Khởi phát): {soc_o if soc_o else '---'}
- Character (Tính chất): {soc_c if soc_c else '---'}
- Radiation (Hướng lan): {soc_r if soc_r else '---'}
- Associations (Triệu chứng kèm): {soc_a if soc_a else '---'}
- Time (Diễn tiến): {soc_t if soc_t else '---'}
- Severity (Mức độ đau): {nrs}/10 ({nrs_note})

[KHÁM THỰC THỂ & NGHIỆM PHÁP]
- Nhìn (Inspection): {inspect if inspect else '---'}
- Sờ (Palpation): {palp if palp else '---'}
- Đo ROM & Phản xạ: {rom_meas if rom_meas else '---'}
- Nghiệm pháp đặc hiệu (+): {', '.join(pos_tests_list) if pos_tests_list else 'Không có test nào dương tính'}
- Cờ đỏ (Red Flags): {'CÓ DẤU HIỆU NGUY CƠ CAO' if (rf_1 or rf_2 or rf_3) else 'Không phát hiện bất thường'}"""

            st.text_area("Bôi đen & Copy nội dung bệnh án chuẩn hóa:", value=summary_text, height=300, key="quick_copy_box")

            # ENGINE PHÂN TÍCH AI CHUYÊN SÂU
            if st.button("🚀 Chạy Phân Tích AI Y Khoa Chuyên Sâu", type="primary", use_container_width=True):
                st.markdown("---")
                st.markdown("#### 🤖 KẾT QUẢ PHÂN TÍCH & LIỆT KÊ LIÊN KẾT CHUYÊN MÔN TỪ AI")
                
                ai_diagnosis = f"Hội chứng đau & rối loạn chức năng vùng {current_reg}"
                ai_mechanism = f"Bệnh nhân đau mức độ {nrs}/10, tính chất đau `{soc_c if soc_c else 'âm ỉ'}`."
                if pos_tests_list:
                    ai_diagnosis = f"Nghi ngờ tổn thương cấu trúc thực thể vùng {current_reg} (Dương tính: {', '.join(pos_tests_list)})"
                    ai_mechanism += f" Các nghiệm pháp đặc hiệu dương tính ({', '.join(pos_tests_list)}) chỉ điểm tình trạng tổn thương dây chằng/rễ thần kinh hoặc bao khớp tương ứng."
                else:
                    ai_mechanism += " Các nghiệm pháp đặc hiệu âm tính, hướng nhiều đến hội chứng cơ năng hoặc căng giãn cơ quá mức."

                st.markdown(f"* **Chẩn đoán định hướng chuyên môn:** `{ai_diagnosis}`.")
                st.markdown(f"* **Biện luận cơ chế bệnh sinh:** {ai_mechanism}")
                if rf_1 or rf_2 or rf_3:
                    st.error("⚠️ **CẢNH BÁO LÂM SÀNG:** Phát hiện cờ đỏ (Red Flags). Đề nghị hội chẩn chuyên khoa hoặc chụp chiếu cận lâm sàng chuyên sâu trước khi tập luyện.")
                else:
                    st.markdown("* **Đề xuất hướng điều trị & PHCN:** Chỉ định vật lý trị liệu giảm đau (Nhiệt/Điện), bài tập phục hồi tầm vận động (ROM) không đau và bài tập tăng cường sức mạnh ổn định khớp.")

            st.markdown("---")
            st.markdown("##### ⚡ Thao tác nhanh")
            
            row1_col1, row1_col2 = st.columns(2)
            with row1_col1:
                if st.button("📋 Copy Nhanh Bệnh Án", use_container_width=True):
                    st.success("✅ Đã sẵn sàng nội dung để dán vào phần mềm EMR/Word!")
            with row1_col2:
                if st.button("🤖 Hỏi ChatGPT", use_container_width=True):
                    st.info("💡 Mẹo: Copy nội dung ở ô trên dán vào ChatGPT kèm câu lệnh: 'Đóng vai bác sĩ PHCN, hãy biện luận chẩn đoán ca bệnh này'.")

            row2_col1, row2_col2 = st.columns(2)
            with row2_col1:
                if st.button("✨ Hỏi Gemini", use_container_width=True):
                    st.success("💡 Mẹo: Trao đổi trực tiếp cùng trợ lý Gemini nhận phác đồ điều trị.")
            with row2_col2:
                if st.button("💾 Lưu Hồ Sơ & Lịch Sử Khám", type="primary", use_container_width=True):
                    if not (p_name and p_phone):
                        st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và SĐT ở phần hành chính!")
                    else:
                        phone_key = p_phone.strip()
                        import datetime
                        visit_record = {
                            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "region": current_reg,
                            "nrs": nrs,
                            "summary_text": summary_text
                        }
                        if phone_key not in st.session_state.patient_db:
                            st.session_state.patient_db[phone_key] = {
                                "name": p_name,
                                "phone": phone_key,
                                "age": p_age,
                                "job": p_job,
                                "visits": [visit_record]
                            }
                        else:
                            st.session_state.patient_db[phone_key]["visits"].append(visit_record)
                        
                        st.success(f"✅ Đã lưu hồ sơ khám thành công cho bệnh nhân **{p_name}** vào hệ thống lịch sử tại Tab 1!")

            st.markdown('</div>', unsafe_allow_html=True)

    # ================= TAB 4: KHO BÀI TẬP PHCN (ĐỦ CÔNG DỤNG & KỸ THUẬT THỰC HIỆN) =================
    with tab4:
        pathologies_m4 = {
            "1. Tai biến mạch máu não (Liệt nửa người)": [
                "1. **Tập vận động thụ động các khớp bên liệt:** *Công dụng:* Duy trì tầm vận động (ROM), ngăn ngừa cứng khớp và co rút gân cơ. *Kỹ thuật:* Kỹ thuật viên nâng đỡ từng khớp, cử động nhẹ nhàng theo đúng biên độ sinh lý từ gốc chi đến ngọn chi, 10 lần/khớp.",
                "2. **Bài tập ức chế trương lực cơ (Bobath):** *Công dụng:* Giảm co cứng các nhóm cơ gấp ở tay và duỗi ở chân. *Kỹ thuật:* Thực hiện các động tác xoay ngoài vai và duỗi khuỷu nhẹ nhàng trước khi tập vận động chủ động.",
                "3. **Chuyển đổi tư thế nằm - ngồi:** *Công dụng:* Tăng cường kiểm soát thân mình và kích hoạt hệ tiền đình. *Kỹ thuật:* Hướng dẫn bệnh nhân tự lật nghiêng sang bên lành, chống khuỷu tay đẩy người ngồi dậy.",
                "4. **Kiểm soát thăng bằng ngồi:** *Công dụng:* Tăng vững cột sống và cơ vùng chậu. *Kỹ thuật:* Ngồi ghế không tựa, hai chân chạm đất, kỹ thuật viên đẩy nhẹ từ các hướng để bệnh nhân tự cân bằng.",
                "5. **Đứng dồn trọng lượng đều hai chân:** *Công dụng:* Phục hồi cảm giác bản thể và chuẩn bị cho bước đi. *Kỹ thuật:* Đứng trước gương, phân phối lực đều 50-50 hai chân trong 5 phút.",
                "6. **Tập đi với nẹp AFO / Khung tập đi:** *Công dụng:* Tái lập dáng đi đúng chu kỳ. *Kỹ thuật:* Mang nẹp cố định cổ chân, bước chân liệt trước, chân lành theo sau với sự hỗ trợ của khung.",
                "7. **Tăng sức mạnh cơ bên lành & duỗi bên liệt:** *Công dụng:* Bồi đắp thể lực toàn thân. *Kỹ thuật:* Tập với tạ nhẹ hoặc dây kháng lực dưới sự giám sát."
            ],
            "2. Rối loạn nuốt (Dysphagia) sau tai biến": [
                "1. **Vận động cơ môi:** *Công dụng:* Tăng cường lực khép miệng và cơ mặt. *Kỹ thuật:* Mím chặt môi hết sức trong 5 giây, cười hết cỡ, thổi phồng má luân phiên.",
                "2. **Vận động lưỡi linh hoạt:** *Công dụng:* Cải thiện khả năng nhào trộn thức ăn. *Kỹ thuật:* Đẩy lưỡi ra trước tối đa, quét vòng quanh vòm miệng, đẩy sang hai bên khóe miệng.",
                "3. **Kích thích nhiệt lạnh khẩu cái mềm:** *Công dụng:* Kích thích phản xạ nuốt tự động. *Kỹ thuật:* Dùng gương lạnh chạm nhẹ vào vùng cung khẩu cái trước.",
                "4. **Bài tập Masako:** *Công dụng:* Tăng cường cơ vòm họng sau. *Kỹ thuật:* Giữ đầu lưỡi giữa hai hàm răng và thực hiện động tác nuốt nước bọt.",
                "5. **Bài tập Shaker:** *Công dụng:* Mở rộng cơ thắt thực quản trên. *Kỹ thuật:* Nằm ngửa, nâng đầu nhìn lên ngón chân trong 1 phút, lặp lại 3 lần.",
                "6. **Đóng nắp thanh môn:** *Công dụng:* Phòng ngừa sặc thức ăn vào đường thở. *Kỹ thuật:* Nuốt giữ hơi trong cổ họng 3 giây rồi ho nhẹ.",
                "7. **Luyện nuốt theo độ quánh IDDSI:** *Công dụng:* Phục hồi ăn uống an toàn. *Kỹ thuật:* Sử dụng thức ăn xay nhuyễn hoặc lỏng sệt theo chuẩn y khoa."
            ],
            "3. Rối loạn ngôn ngữ & Thất ngôn (Aphasia)": [
                "1. **Liệu pháp kích thích thính giác:** *Công dụng:* Kích thích vùng hiểu ngôn ngữ Wernicke. *Kỹ thuật:* Kỹ thuật viên gọi tên đồ vật và yêu cầu bệnh nhân chỉ đúng vào thẻ hình tương ứng.",
                "2. **Luyện phát âm nguyên âm:** *Công dụng:* Phục hồi vận động cơ phát âm cơ bản. *Kỹ thuật:* Phát âm tròn miệng các nguyên âm A - O - E - I - U kéo dài.",
                "3. **Gọi tên đồ vật qua Flashcard:** *Công dụng:* Kích hoạt trí nhớ từ vựng. *Kỹ thuật:* Nhìn hình ảnh sinh hoạt hằng ngày và phát âm tên vật dụng.",
                "4. **Liệu pháp giai điệu (MEL/MIT):** *Công dụng:* Kích thích bán cầu não phải hỗ trợ ngôn ngữ. *Kỹ thuật:* Hát các câu ngắn có âm điệu thay vì nói thường.",
                "5. **Bài tập hoàn thành câu:** *Công dụng:* Khơi gợi phản xạ ngôn ngữ. *Kỹ thuật:* Bác sĩ đọc nửa câu đầu, bệnh nhân nói từ cuối.",
                "6. **Giao tiếp nhu cầu cơ bản:** *Công dụng:* Giải quyết nhu cầu sinh hoạt cấp thiết. *Kỹ thuật:* Luyện tập các từ: Ăn, Đau, Uống, Đi vệ sinh.",
                "7. **Giao tiếp phi ngôn ngữ:** *Công dụng:* Hỗ trợ truyền đạt thông tin. *Kỹ thuật:* Sử dụng bảng chữ cái chỉ tay hoặc cử chỉ ký hiệu."
            ],
            "4. Âm ngữ trị liệu (Rối loạn phát âm / Dysarthria)": [
                "1. **Kiểm soát hơi thở cơ hoành:** *Công dụng:* Tạo cột hơi vững chắc cho phát âm. *Kỹ thuật:* Hít sâu phình bụng, thở ra từ từ kéo dài qua miệng.",
                "2. **Tăng sức mạnh hô hấp:** *Công dụng:* Kéo dài thời gian câu nói. *Kỹ thuật:* Thổi nến ở khoảng cách tăng dần từ 10cm lên 30cm.",
                "3. **Vận động cơ quan phát âm:** *Công dụng:* Linh hoạt môi, lưỡi, hàm. *Kỹ thuật:* Nhai giả lập, mím môi phát âm b-p-m.",
                "4. **Luyện phát âm phụ âm - nguyên âm:** *Công dụng:* Tròn trịa câu chữ. *Kỹ thuật:* Phát âm rõ ràng các cặp âm đôi.",
                "5. **Điều chỉnh tốc độ nói:** *Công dụng:* Tránh tình trạng nói lắp, nuốt chữ. *Kỹ thuật:* Nói chậm rãi, ngắt nhịp theo từng cụm từ.",
                "6. **Kiểm soát cường độ giọng:** *Công dụng:* Tránh nói quá nhỏ hoặc quá to. *Kỹ thuật:* Luyện tập điều chỉnh âm lượng giọng nói trước máy đo.",
                "7. **Luyện đọc trước gương:** *Công dụng:* Tự chỉnh sửa khẩu hình. *Kỹ thuật:* Đọc đoạn văn ngắn 5 dòng, quan sát khẩu hình miệng."
            ],
            "5. Trẻ tự kỷ (Rối loạn vận động & cảm giác)": [
                "1. **Điều hòa cảm giác tiền đình:** *Công dụng:* Giảm kích động, tăng tập trung. *Kỹ thuật:* Đung đưa nhịp nhàng trên võng hoặc nhún trên bóng lớn.",
                "2. **Cảm giác bản thể (Deep Pressure):** *Công dụng:* Tạo cảm giác an toàn, giảm lo âu. *Kỹ thuật:* Ôm chặt, lăn cuộn em bé trong thảm bọt biển chuyên dụng.",
                "3. **Vận động thô trên ván thăng bằng:** *Công dụng:* Phối hợp vận động hai bên cơ thể. *Kỹ thuật:* Cho trẻ đi dọc ván thăng bằng có hỗ trợ tay.",
                "4. **Kéo giãn cơ cẳng chân:** *Công dụng:* Ngăn ngừa dáng đi nhón gót thường gặp ở trẻ tự kỷ. *Kỹ thuật:* Kéo giãn thụ động gân gót 15 giây/lần.",
                "5. **Vận động tinh bàn tay:** *Công dụng:* Tăng sự khéo léo của các ngón tay. *Kỹ thuật:* Nhặt hạt cườm nhỏ, xếp hình khối gỗ.",
                "6. **Phối hợp tay - mắt:** *Công dụng:* Tăng khả năng tập trung chú ý. *Kỹ thuật:* Ném bóng vào rổ theo hiệu lệnh màu sắc.",
                "7. **Bắt chước tư thế động học:** *Công dụng:* Phát triển nhận thức cơ thể. *Kỹ thuật:* Trò chơi 'làm theo chú khỉ' bắt chước các động tác tay chân."
            ],
            "6. Xơ hóa cơ ức đòn chũm (Vẹo cổ bẩm sinh)": [
                "1. **Kéo giãn thụ động cơ ức đòn chũm:** *Công dụng:* Làm mềm dải xơ, khôi phục tầm vận động cổ. *Kỹ thuật:* Nghiêng đầu trẻ sang bên lành, quay cằm về bên bệnh, giữ 10 giây.",
                "2. **Kích thích quay đầu chủ động:** *Công dụng:* Tăng sức mạnh cơ cổ đối diện. *Kỹ thuật:* Dùng đồ chơi phát sáng đặt ở bên bệnh để trẻ tự quay đầu theo.",
                "3. **Định hình tư thế nằm ngủ:** *Công dụng:* Ng ngừa vẹo cột sống cổ thứ phát. *Kỹ thuật:* Sử dụng gối chống lật giữ đầu ở vị trí trung tính.",
                "4. **Xoa bóp miết mô mềm:** *Công dụng:* Giải phóng mô dính xơ hóa. *Kỹ thuật:* Dùng đầu ngón cái day nhẹ dọc theo cơ ức đòn chũm.",
                "5. **Vận động cổ qua trò chơi:** *Công dụng:* Duy trì biên độ linh hoạt. *Kỹ thuật:* Nhẹ nhàng quay cổ trẻ theo các hướng trong lúc tắm.",
                "6. **Tăng sức mạnh cơ cổ đối diện:** *Công dụng:* Cân bằng lực kéo hai bên. *Kỹ thuật:* Đặt trẻ nằm sấp nâng đầu ngắn.",
                "7. **Hướng dẫn tư thế sinh hoạt:** *Công dụng:* Duy trì hiệu quả điều trị tại nhà. *Kỹ thuật:* Hướng dẫn phụ huynh cách bế và cho bú đúng tư thế."
            ],
            "7. PHCN sau Phẫu thuật đầu gối (Tái tạo ACL)": [
                "1. **Gồng cơ tứ đầu đùi (Isometric Quads):** *Công dụng:* Chống teo cơ đùi ngay sau mổ. *Kỹ thuật:* Nằm ngửa, ép sát khoeo chân xuống mặt giường, siết chặt cơ đùi 10 giây.",
                "2. **Duỗi thẳng gối tối đa:** *Công dụng:* Lấy lại biên độ duỗi 0 độ, ngừa dính khớp. *Kỹ thuật:* Đặt gót chân lên cao, để trọng lực tự nhiên ép gối duỗi thẳng trong 5 phút.",
                "3. **Nhấc chân thẳng (Straight Leg Raise):** *Công dụng:* Tăng sức mạnh cơ đùi trước. *Kỹ thuật:* Siết cơ đùi, nhấc thẳng chân cách mặt giường 20cm, giữ 5 giây.",
                "4. **Đạp xe không kháng trở:** *Công dụng:* Phục hồi ROM gối linh hoạt. *Kỹ thuật:* Đạp xe tại chỗ nhẹ nhàng khi gối đã gấp được trên 90 độ.",
                "5. **Đứng dồn trọng lượng chân mổ:** *Công dụng:* Tái lập cảm giác bản thể chịu lực. *Kỹ thuật:* Đứng hai chân, chuyển dần 70% trọng lực sang chân mổ trước gương.",
                "6. **Thăng bằng trên đĩa bản thể:** *Công dụng:* Phục hồi sự vững chắc của khớp gối. *Kỹ thuật:* Đứng một chân trên đĩa tròn thăng bằng trong 30 giây.",
                "7. **Tập kháng lực đùi sau (Hamstrings):** *Công dụng:* Cân bằng lực cơ trước và sau gối. *Kỹ thuật:* Tập gập gối với dây kháng lực Theraband."
            ],
            "8. PHCN sau Phẫu thuật thay khớp háng toàn phần": [
                "1. **Co duỗi cổ chân (Ankle pumps):** *Công dụng:* Ngừa huyết khối tĩnh mạch sâu chi dưới. *Kỹ thuật:* Gấp duỗi cổ chân liên tục 20 lần mỗi phút.",
                "2. **Siết cơ mông và cơ tứ đầu đùi:** *Công dụng:* Duy trì trương lực cơ vùng chậu - đùi. *Kỹ thuật:* Nằm ngửa, siết cơ mông và cơ đùi trong 10 giây.",
                "3. **Trượt gót chân trên giường:** *Công dụng:* Phục hồi tầm vận động gấp háng dưới 90 độ. *Kỹ thuật:* Kéo gót chân về phía mông nhẹ nhàng không quá tầm.",
                "4. **Dang chân sang bên (Abduction):** *Công dụng:* Tăng sức mạnh cơ vùng hông. *Kỹ thuật:* Trượt chân sang ngang giữ thẳng gối, tránh tư thế khép.",
                "5. **Đứng dậy từ ghế cao:** *Công dụng:* Phục hồi chức năng sinh hoạt cơ bản. *Kỹ thuật:* Dùng lực hai chân và tay vịn đứng lên từ ghế cao 50cm.",
                "6. **Tái giáo dục dáng đi:** *Công dụng:* Chống đi khập khiễng. *Kỹ thuật:* Tập bước đi đều nhịp với khung hoặc nạng đúng kỹ thuật.",
                "7. **Leo cầu thang đúng nguyên tắc:** *Công dụng:* Đảm bảo an toàn khớp háng nhân tạo. *Kỹ thuật:* 'Lên trước bằng chân lành, xuống trước bằng chân mổ'."
            ],
            "9. PHCN sau Gãy tay / Gãy chân (Hậu phẫu / Bó bột)": [
                "1. **Gồng cơ tĩnh trong bột:** *Công dụng:* Ngừa teo cơ tối đa trong thời gian bất động. *Kỹ thuật:* Siết cơ bên trong lớp bột 10 giây, lặp lại 15 lần/buổi.",
                "2. **Cử động các khớp tự do:** *Công dụng:* Duy trì tuần hoàn ngoại biên. *Kỹ thuật:* Cử động linh hoạt các ngón tay/chân không bị bó bột.",
                "3. **Phục hồi ROM sau tháo bột:** *Công dụng:* Khôi phục biên độ vận động khớp bị cứng. *Kỹ thuật:* Vận động chủ động và hỗ trợ nhẹ nhàng không gây đau dữ dội.",
                "4. **Xoa bóp di động sẹo mổ:** *Công dụng:* Ngừa dính gân và mô mềm dưới da. *Kỹ thuật:* Day ấn nhẹ nhàng quanh vùng sẹo khi vết thương đã lành hẳn.",
                "5. **Tăng lực cơ với tạ nhẹ / Theraband:** *Công dụng:* Khôi phục sức mạnh cơ thể sau thời gian dài nghỉ. *Kỹ thuật:* Tập các bài kháng lực tăng tiến theo dung nạp của bệnh nhân.",
                "6. **Tái giáo dục dáng đi / Cầm nắm:** *Công dụng:* Lấy lại chức năng khéo léo ban đầu. *Kỹ thuật:* Luyện tập các động tác cầm nắm đồ vật hoặc bước đi trên sàn phẳng.",
                "7. **Phục hồi sinh hoạt hằng ngày (ADL):** *Công dụng:* Độc lập trong cuộc sống. *Kỹ thuật:* Tập các kỹ năng tự ăn uống, mặc áo quần, vệ sinh cá nhân."
            ]
        }

        if "selected_pathology_m4" not in st.session_state:
            st.session_state.selected_pathology_m4 = None

        if st.session_state.selected_pathology_m4 is None:
            st.markdown("### 🏋️‍♂️ Kho Bài Tập Phục Hồi Chức Năng Y Chứng")
            st.caption("Chọn nhóm bệnh lý bên dưới để xem trọn bộ 7 bài tập kèm công dụng và kỹ thuật thực hiện chi tiết:")

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
            st.markdown("##### 📋 Trọn bộ 7 bài tập chuẩn hóa (Bao gồm Công dụng & Kỹ thuật):")
            
            exercises = pathologies_m4[st.session_state.selected_pathology_m4]
            for exercise in exercises:
                with st.container(border=True):
                    st.markdown(f"- {exercise}")

if __name__ == "__main__":
    main()
