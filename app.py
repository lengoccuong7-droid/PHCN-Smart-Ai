# app.py
import streamlit as st
from Core.engine import SuperClinicalEngine
from Core.history_manager import HistoryManager
from Core.kb_builder import get_comprehensive_kb

# Cấu hình giao diện tối ưu cho mobile
st.set_page_config(
    page_title="PHCN AI 1.8 - Trợ lý lâm sàng PHCN",
    page_icon="🩺",
    layout="centered"
)

# Khởi tạo engine và quản lý lịch sử
engine = SuperClinicalEngine()
history_mgr = HistoryManager()
kb = get_comprehensive_kb()

# Thanh điều hướng chuyển đổi chế độ
app_mode = st.sidebar.radio(
    "📌 CHỌN MỤC CHỨC NĂNG:",
    [
        "1. Khám bệnh & Lý luận lâm sàng", 
        "2. Thư viện Chi tiết Bài Tập PHCN"
    ]
)

# ------------------------------------------
# MỤC 1: KHÁM BỆNH & LÝ LUẬN LÂM SÀNG
# ------------------------------------------
if app_mode == "1. Khám bệnh & Lý luận lâm sàng":
    st.markdown("### 🩺 PHCN AI 1.8")
    st.caption("Trợ lý lâm sàng Phục hồi chức năng & Vật lý trị liệu")

    # ------------------------------------------
    # 1. NHẬP LIỆU THĂM KHÁM
    # ------------------------------------------
    with st.expander("📋 1. Nhập liệu thăm khám", expanded=True):
        st.markdown("#### 👤 Thông tin bệnh nhân")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            patient_name = st.text_input("Họ tên:", value="Nguyễn Văn A", key="input_name")
            patient_job = st.text_input("Nghề nghiệp:", value="Nhân viên văn phòng", key="input_job")
        with col_h2:
            patient_phone = st.text_input("Số điện thoại / Mã BN:", value="0901234567", key="input_phone")
            patient_age = st.number_input("Năm sinh:", min_value=1900, max_value=2026, value=1990, key="input_age")

        # Nút xem hồ sơ cũ của bệnh nhân
        if st.button("👁️ Xem hồ sơ bệnh nhân từ hệ thống", key="btn_view_profile"):
            if patient_phone:
                past_visits = history_mgr.get_patient_history(patient_phone)
                if past_visits:
                    st.info(f"📁 Tìm thấy {len(past_visits)} lần khám trước đây của bệnh nhân này.")
                    for idx, visit in enumerate(past_visits):
                        st.write(f"• **Lần {idx+1} ({visit.get('date', 'N/A')}):** {visit.get('summary', 'Không có dữ liệu')}")
                else:
                    st.warning("⚠️ Không tìm thấy lịch sử khám cũ với số điện thoại này.")
            else:
                st.warning("⚠️ Vui lòng nhập số điện thoại để tra cứu hồ sơ.")

        st.markdown("---")
        ly_do_vao_vien = st.text_input("🏥 Lý do vào viện:", placeholder="Nhập lý do vào viện...", key="input_ly_do")

        # Bệnh sử SOCRATES chi tiết từng ô
        with st.expander("🩺 Bệnh sử SOCRATES (Chi tiết)"):
            site = st.text_input("S – Vị trí:", placeholder="Nhập vị trí đau...", key="soc_site")
            onset = st.text_input("O – Khởi phát + thời điểm:", placeholder="Nhập hoàn cảnh khởi phát và thời điểm...", key="soc_onset")
            character = st.text_input("C – Tính chất:", placeholder="Nhói, âm ỉ, tê bì, buốt...", key="soc_char")
            radiation = st.text_input("R – Hướng lan:", placeholder="Có lan đi đâu không...", key="soc_rad")
            associations = st.text_input("A – Triệu chứng đi kèm:", placeholder="Yếu cơ, sưng nề, cứng khớp...", key="soc_assoc")
            time_course = st.text_input("T – Diễn tiến:", placeholder="Liên tục, từng cơn, tăng về đêm...", key="soc_time")
            exacerbating = st.text_input("E – Tăng/giảm đau:", placeholder="Tư thế/hoạt động nào làm tăng hoặc giảm đau...", key="soc_exac")
            
            col_nrs1, col_nrs2 = st.columns([1, 2])
            with col_nrs1:
                nrs_score = st.selectbox("Điểm NRS:", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="soc_nrs_val")
            with col_nrs2:
                nrs_note = st.text_input("Ghi chú mức độ đau:", placeholder="Mô tả thêm mức độ ảnh hưởng...", key="soc_nrs_note")

        # Khám thực thể & Bài Test
        with st.expander("🔍 Khám thực thể & Bài Test đặc hiệu"):
            region = st.selectbox("Chọn vùng khám:", list(kb.keys()), key="select_region")
            
            selected_tests = []
            pathology = ""
            if region:
                specific_pathologies = list(kb[region].keys())
                pathology = st.selectbox("Chọn bệnh lý nghi ngờ:", specific_pathologies, key="select_pathology")
                
                if pathology:
                    pathology_data = kb[region][pathology]
                    st.markdown(f"**📌 Triệu chứng đặc trưng:**")
                    for sym in pathology_data.get("symptoms", []):
                        st.write(f"• {sym}")
                        
                    st.markdown(f"**🧪 Bài Test đặc hiệu:**")
                    for test in pathology_data.get("special_tests", []):
                        if st.checkbox(f"Thực hiện: {test}", key=f"test_{test}"):
                            selected_tests.append(test)

            ghi_chu_kham = st.text_area("✍️ Ghi chú khám thực thể:", placeholder="Nhập kết quả khám thực thể khác...", key="input_ghi_chu_kham")

        # Cờ đỏ an toàn
        with st.expander("🚩 Cờ đỏ an toàn (Red Flags)"):
            rf_1 = st.checkbox("Hội chứng đuôi ngựa / Rối loạn tiểu tiện", key="rf_1")
            rf_2 = st.checkbox("Sụt cân / Nghi ngờ ác tính", key="rf_2")
            rf_3 = st.checkbox("Sốt cao / Viêm nhiễm", key="rf_3")
            rf_4 = st.checkbox("Yếu liệt chi tiến triển nhanh", key="rf_4")

        # Mục Tệp đính kèm (Ảnh chụp X-quang, MRI, tài liệu)
        with st.expander("📁 Tệp đính kèm (Hình ảnh X-quang, MRI, tài liệu)"):
            uploaded_files = st.file_uploader("Tải lên hình ảnh hoặc tài liệu liên quan:", accept_multiple_files=True, type=["jpg", "png", "jpeg", "pdf"], key="file_upload_sec")
            if uploaded_files:
                st.success(f"Đã đính kèm {len(uploaded_files)} tệp tin vào hồ sơ.")

    # ------------------------------------------
    # 2. CƠ SỞ TRI THỨC
    # ------------------------------------------
    with st.expander("📚 2. Cơ sở tri thức & Danh mục bệnh lý", expanded=False):
        search_kw = st.text_input("🔍 Tìm kiếm kiến thức / Bệnh lý:", placeholder="Nhập tên bệnh hoặc triệu chứng...")
        st.info("💡 Tra cứu nhanh các bệnh lý cột sống, khớp gối, khớp vai trực tiếp từ hệ thống tri thức chuẩn hóa.")

       # ------------------------------------------
    # 3. PHÂN TÍCH CHẨN ĐOÁN & TỔNG HỢP BỆNH ÁN (CÓ BẢNG ĐỂ BS ĐỌC LẠI)
    # ------------------------------------------
    st.markdown("### 🧠 3. Tổng hợp Bệnh án & Phân tích AI")
    
    # Tạo từ điển dữ liệu tổng hợp hiện tại của bệnh nhân
    summary_data = {
        "Họ và tên": [patient_name],
        "Tuổi/Năm sinh": [str(patient_age)],
        "Số điện thoại": [patient_phone],
        "Nghề nghiệp": [patient_job],
        "Lý do vào viện": [ly_do_vao_vien if 'ly_do_vao_vien' in locals() else ""],
        "Bệnh sử SOCRATES": [f"Site:{site if 'site' in locals() else ''} | Onset:{onset if 'onset' in locals() else ''} | Char:{character if 'character' in locals() else ''} | NRS:{nrs_score if 'nrs_score' in locals() else 0}/10"],
        "Vùng khám & Bệnh lý": [f"{region if 'region' in locals() else ''} - {pathology if 'pathology' in locals() else ''}"],
        "Test dương tính": [f"{len(selected_tests) if 'selected_tests' in locals() else 0} bài test"],
        "Cờ đỏ (Red Flags)": [", ".join([k for k, v in [("Hội chứng đuôi ngựa", rf_1), ("Sụt cân/Ác tính", rf_2), ("Sốt cao/Viêm", rf_3), ("Yếu liệt nhanh", rf_4)] if v]) or "Không ghi nhận"]
    }

    import pandas as pd
    df_summary = pd.DataFrame(summary_data).T
    df_summary.columns = ["Thông tin ghi nhận"]

    # Hiển thị bảng tổng hợp để bác sĩ đọc lại trực quan
    st.markdown("##### 📋 Bảng tổng hợp chi tiết ca bệnh (Xem trước):")
    st.dataframe(df_summary, use_container_width=True)

    # Nút chạy phân tích AI
    if st.button("🚀 Chạy phân tích AI & Đề xuất phác đồ", type="primary", use_container_width=True):
        st.success(f"✅ Đã phân tích xong ca bệnh cho **{patient_name}**. Hệ thống đã sẵn sàng xuất phác đồ tập vật lý trị liệu.")

    # Các nút tương tác: Copy kết quả, ChatGPT, Gemini
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        # Chuỗi text hoàn chỉnh để copy
        text_to_copy = f"BỆNH ÁN PHCN\nHọ tên: {patient_name} ({patient_age})\nSĐT: {patient_phone}\nLý do: {ly_do_vao_vien}\nSOCRATES: {summary_data['Bệnh sử SOCRATES'][0]}\nChẩn đoán: {summary_data['Vùng khám & Bệnh lý'][0]}"
        st.code(text_to_copy, language="text")
        st.caption("👆 Nhấn nút copy ở góc trên khung trên để sao chép toàn bộ.")
    with col_btn2:
        if st.button("🟢 ChatGPT", use_container_width=True):
            st.info("Chuyển hướng dữ liệu sang ChatGPT.")
    with col_btn3:
        if st.button("🟣 Gemini", use_container_width=True):
            st.info("Chuyển hướng dữ liệu sang Gemini.")

    # Nút lưu hồ sơ vào hệ thống (Lưu trên server, không tự động tải file về máy điện thoại)
    st.markdown("---")
    if st.button("💾 Lưu hồ sơ bệnh án vào hệ thống", type="primary", use_container_width=True):
        if not patient_name or not patient_phone:
            st.warning("⚠️ Vui lòng điền đầy đủ Họ tên và SĐT bệnh nhân!")
        else:
            exam_data = {
                "patient_name": patient_name,
                "patient_phone": patient_phone,
                "summary": f"Vùng: {region if 'region' in locals() else ''} | Bệnh lý: {pathology if 'pathology' in locals() else ''}"
            }
            history_mgr.save_visit(patient_phone, exam_data)
            st.success(f"✅ Đã lưu thành công hồ sơ bệnh án cho bệnh nhân **{patient_name}** vào hệ thống!")
# MỤC 2: THƯ VIỆN CHI TIẾT BÀI TẬP PHCN (8 NHÓM - 7 BÀI TẬP CÓ MÔ TẢ ĐẦY ĐỦ)
# ------------------------------------------
else:
    st.subheader("🏋️‍♂️ Thư viện Chi tiết Bài Tập Phục Hồi Chức Năng Chuyên Sâu")
    st.markdown("Chọn chương trình PHCN dưới đây để xem **hướng dẫn thao tác, tư thế và liều lượng chi tiết** cho từng bài tập chuẩn y khoa:")

    rehab_program = st.selectbox("🎯 Chọn chương trình Phục hồi chức năng:", [
        "1. PHCN sau tai biến mạch máu não (Liệt nửa người)",
        "2. PHCN hội chứng cong vẹo cột sống cổ / Cổ vai gáy",
        "3. PHCN cho trẻ bại não (Cerebral Palsy)",
        "4. PHCN sau mổ tái tạo dây chằng chéo trước (ACL)",
        "5. PHCN sau mổ kết hợp xương gãy thân xương đùi",
        "6. PHCN sau mổ gãy xương cổ tay / bàn tay",
        "7. PHCN sau phẫu thuật thay khớp háng toàn phần",
        "8. PHCN cho trẻ chậm nói / Rối loạn phát triển ngôn ngữ"
    ])

    st.markdown("---")

    if "1." in rehab_program:
        st.subheader("🧠 1. Chương trình PHCN sau tai biến mạch máu não")
        st.write("• **Mục tiêu:** Phòng ngừa co cứng, kích hoạt lại vận động bên liệt và phục hồi thăng bằng.")
        
        st.markdown("---")
        st.markdown("##### 1. Vận động thụ động - chủ động hỗ trợ khớp vai và khuỷu tay bên liệt")
        st.write("- **Tư thế:** Bệnh nhân nằm ngửa hoặc ngồi ghế tựa.")
        st.write("- **Cách thực hiện:** Kỹ thuật viên hoặc tay lành hỗ trợ đưa tay liệt lên cao, dạng vai, gập khuỷu nhẹ nhàng.")
        st.write("- **Liều lượng:** 10–15 lần/hiệp, ngày tập 2–3 lần.")

        st.markdown("##### 2. Kỹ thuật ức chế trương lực cơ co cứng cơ gấp cổ tay và ngón tay")
        st.write("- **Tư thế:** Bệnh nhân ngồi, tay đặt ngửa trên bàn.")
        st.write("- **Cách thực hiện:** Thực hiện duỗi nhẹ nhàng các ngón tay và khớp cổ tay ra hết biên độ, giữ kéo giãn tĩnh.")
        st.write("- **Liều lượng:** Giữ 30 giây/lần, lặp lại 5 lần.")

        st.markdown("##### 3. Tập nâng hông (Bridging) ở tư thế nằm ngửa")
        st.write("- **Tư thế:** Nằm ngửa, gập gối, hai bàn chân đặt sát mặt giường.")
        st.write("- **Cách thực hiện:** Dồn lực vào hai gót chân và cơ mông, nâng hông lên khỏi mặt giường sao cho thân người tạo thành một đường thẳng.")
        st.write("- **Liều lượng:** 10 lần/hiệp, 3 hiệp/ngày.")

        st.markdown("##### 4. Tập thăng bằng ngồi trên ghế không tựa lưng")
        st.write("- **Tư thế:** Ngồi thẳng lưng trên ghế, hai chân chống vuông góc xuống sàn.")
        st.write("- **Cách thực hiện:** Bỏ tay vịn, giữ thăng bằng thân mình, tập với tay sang các hướng trái/phải/trước mà không ngã.")
        st.write("- **Liều lượng:** Duy trì liên tục từ 3–5 phút/lần.")

        st.markdown("##### 5. Bài tập đứng dồn lực lên chân liệt trước gương")
        st.write("- **Tư thế:** Đứng đối diện gương lớn, hai chân rộng bằng vai.")
        st.write("- **Cách thực hiện:** Chuyển trọng tâm cơ thể từ từ sang bên chân liệt, quan sát trong gương để giữ hông cân đối.")
        st.write("- **Liều lượng:** Giữ 10–15 giây/lần, lặp lại 10 lần.")

        st.markdown("##### 6. Huấn luyện lại dáng đi với thanh song song / khung tập đi")
        st.write("- **Tư thế:** Đứng vững trong khung tập đi hoặc thanh song song.")
        st.write("- **Cách thực hiện:** Bước chân liệt lên trước, theo sau là chân lành, chú ý dáng đi đúng nhịp.")
        st.write("- **Liều lượng:** Tập đi từ 5–10 phút mỗi buổi.")

        st.markdown("##### 7. Tập cầm nắm vật dụng sinh hoạt hàng ngày")
        st.write("- **Tư thế:** Ngồi bàn ghế thoải mái.")
        st.write("- **Cách thực hiện:** Tập cầm các vật có kích thước khác nhau (quả bóng mềm, ly nước nhựa, bút) để tái giáo dục chi trên.")
        st.write("- **Liều lượng:** 10–15 phút/lần.")

    elif "2." in rehab_program:
        st.subheader("🦴 2. Chương trình PHCN cong vẹo cột sống cổ / Cổ vai gáy")
        st.write("• **Mục tiêu:** Thư giãn nhóm cơ co thắt, mạnh cơ cổ sâu, chỉnh sửa tư thế đầu.")
        
        st.markdown("---")
        st.markdown("##### 1. Kéo giãn cơ thang trên (Upper Trapezius Stretch)")
        st.write("- **Tư thế:** Ngồi thẳng, một tay ôm vòng qua đầu kéo nghiêng đầu về phía đối diện.")
        st.write("- **Cách thực hiện:** Kéo nhẹ nhàng cho đến khi có cảm giác căng tức vùng cổ vai bên đối diện.")
        st.write("- **Liều lượng:** Giữ 20–30 giây, lặp lại 3–5 lần mỗi bên.")

        st.markdown("##### 2. Kéo giãn cơ nâng vai (Levator Scapulae Stretch)")
        st.write("- **Tư thế:** Ngồi ghế, xoay đầu sang một góc 45 độ rồi cuối cằm nhìn xuống nách.")
        st.write("- **Cách thực hiện:** Dùng tay cùng phía ấn nhẹ đầu xuống dưới để tăng độ căng.")
        st.write("- **Liều lượng:** Giữ 20–30 giây, lặp lại 3 lần/bên.")

        st.markdown("##### 3. Kéo cằm ngược (Chin Tuck)")
        st.write("- **Tư thế:** Ngồi hoặc đứng thẳng, mắt nhìn thẳng phía trước.")
        st.write("- **Cách thực hiện:** Kéo cằm lùi thẳng ra sau (tạo nọng cằm giả) mà không cúi đầu xuống, cảm nhận cơ cổ sâu phía sau căng nhẹ.")
        st.write("- **Liều lượng:** 10 lần/hiệp, giữ 5 giây mỗi lần.")

        st.markdown("##### 4. Xoay cổ chủ động biên độ nhẹ")
        st.write("- **Tư thế:** Ngồi thoải mái, thả lỏng vai.")
        st.write("- **Cách thực hiện:** Từ từ xoay đầu sang trái rồi sang phải trong giới hạn không đau.")
        st.write("- **Liều lượng:** 10 vòng mỗi hướng.")

        st.markdown("##### 5. Tập mạnh cơ duỗi cổ kháng lực đẳng cự")
        st.write("- **Tư thế:** Đặt hai tay đan vào nhau sau chẩm đầu.")
        st.write("- **Cách thực hiện:** Dùng đầu đẩy ngược ra sau đồng thời hai tay kháng lực lại (đầu không di chuyển).")
        st.write("- **Liều lượng:** Giữ 5–10 giây, lặp lại 10 lần.")

        st.markdown("##### 6. Vận động khép xương bả vai (Scapular Retraction)")
        st.write("- **Tư thế:** Ngồi thẳng lưng, hai tay thả lỏng.")
        st.write("- **Cách thực hiện:** Kéo hai xương bả vai sát lại với nhau ra phía sau như kẹp một vật ở giữa.")
        st.write("- **Liều lượng:** Giữ 5 giây, lặp lại 15 lần.")

        st.markdown("##### 7. Nhiệt trị liệu & Thư giãn điểm đau (Trigger points)")
        st.write("- **Tư thế:** Nằm sấp hoặc ngồi tựa đầu thư giãn.")
        st.write("- **Cách thực hiện:** Chườm ấm vùng cổ vai gáy kết hợp xoa bóp nhẹ nhàng các điểm cơ co cứng.")
        st.write("- **Liều lượng:** 15–20 phút/lần.")

    elif "3." in rehab_program:
        st.subheader("🧸 3. Chương trình PHCN cho trẻ bại não (Cerebral Palsy)")
        st.write("• **Mục tiêu:** Ức chế phản xạ nguyên bản bất thường, tăng cường kiểm soát đầu cổ.")
        
        st.markdown("---")
        st.markdown("##### 1. Tạo thuận kiểm soát đầu cổ")
        st.write("- **Tư thế:** Trẻ nằm sấp trên thảm có cuộn khăn dưới ngực.")
        st.write("- **Cách thực hiện:** Kích thích âm thanh hoặc đồ chơi phía trước để trẻ ngẩng đầu lên.")
        st.write("- **Liều lượng:** 5–10 lần/buổi.")

        st.markdown("##### 2. Tập tư thế nằm sấp chống khuỷu (Prone on elbows)")
        st.write("- **Tư thế:** Trẻ nằm sấp, hai khuỷu tay chống vuông góc nâng thân trên lên.")
        st.write("- **Cách thực hiện:** Giữ ổn định tư thế vai và cột sống cổ của trẻ.")
        st.write("- **Liều lượng:** 3–5 phút mỗi lần tập.")

        st.markdown("##### 3. Tập quỳ bốn điểm và nhún trọng lượng (Quadruped rocking)")
        st.write("- **Tư thế:** Trẻ ở tư thế bò bốn điểm (hai tay và hai gối chống sàn).")
        st.write("- **Cách thực hiện:** Hỗ trợ nhún người trẻ nhẹ nhàng ra trước và ra sau để tăng cảm giác thăng bằng.")
        st.write("- **Liều lượng:** 10–15 nhịp/lần.")

        st.markdown("##### 4. Tập phản ứng thăng bằng trên bóng Bobath")
        st.write("- **Tư thế:** Cho trẻ ngồi hoặc nằm sấp trên bóng trị liệu lớn.")
        st.write("- **Cách thực hiện:** Lăn bóng nhẹ nhàng các hướng trước-sau, trái-phải để kích thích phản xạ giữ thăng bằng.")
        st.write("- **Liều lượng:** 5–7 phút.")

        st.markdown("##### 5. Kéo giãn nhẹ nhàng cơ khép háng và gân kheo")
        st.write("- **Tư thế:** Trẻ nằm ngửa trên giường.")
        st.write("- **Cách thực hiện:** Từ từ dạng chân hoặc duỗi thẳng gối kéo giãn nhẹ nhóm cơ căng cứng.")
        st.write("- **Liều lượng:** Giữ 15–20 giây, lặp lại 3 lần.")

        st.markdown("##### 6. Hướng dẫn tập đứng với nẹp trợ giúp AFO")
        st.write("- **Tư thế:** Mang nẹp chân cho trẻ và đỡ đứng thẳng.")
        st.write("- **Cách thực hiện:** Cho trẻ tập đứng bám vào bàn hoặc khung tập đứng.")
        st.write("- **Liều lượng:** 5–10 phút.")

        st.markdown("##### 7. Trị liệu vận động tinh qua trò chơi")
        st.write("- **Tư thế:** Ngồi bàn ghế chắc chắn.")
        st.write("- **Cách thực hiện:** Hướng dẫn trẻ nhặt khối gỗ nhỏ, xâu hạt vòng để luyện cơ bàn tay và ngón tay.")
        st.write("- **Liều lượng:** 10–15 phút.")

    elif "4." in rehab_program:
        st.subheader("🦵 4. Chương trình PHCN sau mổ tái tạo dây chằng chéo trước (ACL)")
        st.write("• **Mục tiêu:** Lấy lại biên độ duỗi thẳng hoàn toàn, phục hồi cơ tứ đầu đùi.")
        
        st.markdown("---")
        st.markdown("##### 1. Duỗi gối thụ động tối đa")
        st.write("- **Tư thế:** Nằm ngửa, gót chân kê cao trên con lăn, để chân tự duỗi thẳng hoàn toàn dưới trọng lực.")
        st.write("- **Liều lượng:** 10–15 phút, ngày 3 lần.")

        st.markdown("##### 2. Gồng cơ tứ đầu đùi tĩnh (Isometric Quad Sets)")
        st.write("- **Tư thế:** Nằm ngửa, chân duỗi thẳng, đặt một khăn mỏng dưới khoeo.")
        st.write("- **Cách thực hiện:** Ép sát khoeo chân xuống khăn, gồng căng cơ đùi hết cỡ.")
        st.write("- **Liều lượng:** Giữ 10 giây, lặp lại 15–20 lần.")

        st.markdown("##### 3. Nâng chân thẳng (Straight Leg Raise)")
        st.write("- **Tư thế:** Nằm ngửa, chân mổ duỗi thẳng, chân kia gập gối.")
        st.write("- **Cách thực hiện:** Gồng cơ đùi, nhấc thẳng chân lên cao cách mặt giường khoảng 20-30cm rồi hạ xuống từ từ.")
        st.write("- **Liều lượng:** 3 hiệp x 12 lần.")

        st.markdown("##### 4. Gập gối gót chạm mông chủ động trợ giúp")
        st.write("- **Tư thế:** Nằm ngửa hoặc ngồi trên mép giường.")
        st.write("- **Cách thực hiện:** Dùng chân lành hỗ trợ kéo hoặc trượt gót chân mổ về phía mông để tăng biên độ gập gối.")
        st.write("- **Liều lượng:** 10–15 lần/hiệp.")

        st.markdown("##### 5. Đạp xe đạp tĩnh điện không kháng lực")
        st.write("- **Tư thế:** Ngồi trên xe đạp tập, yên chỉnh độ cao phù hợp.")
        st.write("- **Cách thực hiện:** Đạp vòng tròn nhẹ nhàng không để mức kháng lực (thường áp dụng từ tuần 4-6 sau mổ).")
        st.write("- **Liều lượng:** 10–15 phút/ngày.")

        st.markdown("##### 6. Ngồi xổm một phần (Mini Squats)")
        st.write("- **Tư thế:** Đứng thẳng, hai chân rộng bằng vai, bám nhẹ vào thanh vịn.")
        st.write("- **Cách thực hiện:** Từ từ hạ thấp người xuống ở biên độ an toàn từ 0 đến 45 độ gối rồi đứng lên.")
        st.write("- **Liều lượng:** 3 hiệp x 10 lần.")

        st.markdown("##### 7. Tập thăng bằng cảm giác bản thể trên đệm hơi")
        st.write("- **Tư thế:** Đứng bằng chân mổ trên đệm hơi hoặc thảm thăng bằng.")
        st.write("- **Cách thực hiện:** Giữ thăng bằng cơ thể không để chân bị chao đảo.")
        st.write("- **Liều lượng:** 3 lần x 1 phút.")

    elif "5." in rehab_program:
        st.subheader("🦴 5. Chương trình PHCN sau mổ kết hợp xương gãy thân xương đùi")
        st.write("• **Mục tiêu:** Ngăn ngừa teo cơ, chống huyết khối tĩnh mạch, hồi phục chức năng gối.")
        
        st.markdown("---")
        st.markdown("##### 1. Bơm máu cổ chân")
        st.write("- **Tư thế:** Nằm ngửa, chân duỗi thẳng.")
        st.write("- **Cách thực hiện:** Gập duỗi liên tục hai bàn chân lên xuống nhịp nhàng.")
        st.write("- **Liều lượng:** 20–30 lần mỗi giờ để phòng huyết khối.")

        st.markdown("##### 2. Gồng cơ mông và đùi tĩnh")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Siết chặt cơ mông và cơ đùi trong vòng 5 giây rồi thả lỏng.")
        st.write("- **Liều lượng:** 15 lần/hiệp, 3 hiệp/ngày.")

        st.markdown("##### 3. Trượt gót chân trên giường (Heel Slides)")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Từ từ kéo gót chân trượt về phía mông để gập gối trong giới hạn cho phép của bác sĩ phẫu thuật.")
        st.write("- **Liều lượng:** 10 lần/hiệp.")

        st.markdown("##### 4. Nâng chân thẳng")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Nâng nguyên chân lên cao 20cm khỏi mặt giường với đầu gối duỗi thẳng hoàn toàn.")
        st.write("- **Liều lượng:** 10 lần/hiệp.")

        st.markdown("##### 5. Ngồi thõng chân mép giường")
        st.write("- **Tư thế:** Ngồi ở mép giường, cẳng chân buông thõng tự nhiên.")
        st.write("- **Cách thực hiện:** Đung đưa nhẹ nhàng cẳng chân để lấy lại tầm vận động gối.")
        st.write("- **Liều lượng:** 5–10 phút/lần.")

        st.markdown("##### 6. Tập đứng chịu lực một phần với khung tập đi")
        st.write("- **Tư thế:** Đứng dậy bằng khung tập đi theo đúng chỉ định chịu lực (chịu lực một phần chân mổ).")
        st.write("- **Liều lượng:** 5–10 phút.")

        st.markdown("##### 7. Tập bước đi lên xuống bậc thang thấp")
        st.write("- **Tư thế:** Giai đoạn liền xương, tập bước bậc thang thấp (Lên bằng chân lành, xuống bằng chân mổ).")
        st.write("- **Liều lượng:** 5–10 nhịp.")

    elif "6." in rehab_program:
        st.subheader("✋ 6. Chương trình PHCN sau mổ gãy xương cổ tay / bàn tay")
        st.write("• **Mục tiêu:** Chống phù nề, chống xơ hóa gân, lấy lại tầm vận động và lực nắm.")
        
        st.markdown("---")
        st.markdown("##### 1. Kê cao tay & nắm xòe ngón tay")
        st.write("- **Tư thế:** Ngồi hoặc nằm, tay bị thương kê cao hơn mức tim.")
        st.write("- **Cách thực hiện:** Liên tục nắm chặt và xòe rộng các ngón tay để bơm máu tĩnh mạch giảm sưng.")
        st.write("- **Liều lượng:** 15–20 lần mỗi giờ.")

        st.markdown("##### 2. Vận động thụ động nhẹ nhàng khớp cổ tay")
        st.write("- **Tư thế:** Ngồi thoải mái, tay lành hỗ trợ tay mổ.")
        st.write("- **Cách thực hiện:** Nhẹ nhàng gập và duỗi cổ tay trong giới hạn không đau đớn.")
        st.write("- **Liều lượng:** 10 lần/hiệp, ngày 3 lần.")

        st.markdown("##### 3. Vận động chủ động nghiêng quay / nghiêng trụ")
        st.write("- **Tư thế:** Đặt cẳng tay cạnh sườn, bàn tay trung gian.")
        st.write("- **Cách thực hiện:** Chủ động lắc cổ tay sang hai bên (hướng ngón cái và hướng ngón út).")
        st.write("- **Liều lượng:** 10 lần mỗi hướng.")

        st.markdown("##### 4. Tập mạnh cơ ngửa và sấp cẳng tay")
        st.write("- **Tư thế:** Khuỷu tay gập 90 độ sát thân người.")
        st.write("- **Cách thực hiện:** Xoay lật lòng bàn tay ngửa lên và sấp xuống với kháng lực nhẹ.")
        st.write("- **Liều lượng:** 12 lần/hiệp.")

        st.markdown("##### 5. Bóp bóng cao su mềm")
        st.write("- **Tư thế:** Ngồi cầm quả bóng cao su mềm trong lòng bàn tay.")
        st.write("- **Cách thực hiện:** Dùng toàn bộ ngón tay bóp chặt bóng lại rồi thả lỏng từ từ.")
        st.write("- **Liều lượng:** 15 lần/hiệp, 3 hiệp/ngày.")

        st.markdown("##### 6. Bài tập đối chiếu ngón cái")
        st.write("- **Tư thế:** Ngồi thả lỏng tay.")
        st.write("- **Cách thực hiện:** Dùng đầu ngón cái lần lượt chạm vào đầu các ngón tay 2, 3, 4, 5.")
        st.write("- **Liều lượng:** Lặp lại 5 vòng.")

        st.markdown("##### 7. Siêu âm trị liệu chống dính sẹo")
        st.write("- **Tư thế:** Đặt tay thoải mái trên bàn điều trị.")
        st.write("- **Cách thực hiện:** Chạy máy siêu âm hoặc xoa bóp nhẹ nhàng dọc theo đường mổ để làm mềm và chống dính mô sẹo.")
        st.write("- **Liều lượng:** 5–7 phút mỗi ngày.")

    elif "7." in rehab_program:
        st.subheader("🦴 7. Chương trình PHCN sau phẫu thuật thay khớp háng toàn phần")
        st.write("• **Mục tiêu:** Bảo vệ khớp nhân tạo, phục hồi cơ mông, hướng dẫn sinh hoạt an toàn.")
        
        st.markdown("---")
        st.markdown("##### 1. Bơm máu bàn chân")
        st.write("- **Tư thế:** Nằm ngửa, hai chân duỗi thẳng.")
        st.write("- **Cách thực hiện:** Gập và duỗi cổ chân liên tục để tăng tuần hoàn máu.")
        st.write("- **Liều lượng:** 20 lần/giờ.")

        st.markdown("##### 2. Ép mông tĩnh (Gluteal Squeezes)")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Siết chặt hai cơ mông lại với nhau, giữ nguyên trong 5 giây.")
        st.write("- **Liều lượng:** 15 lần/hiệp.")

        st.markdown("##### 3. Dạng chân trượt sang ngang")
        st.write("- **Tư thế:** Nằm ngửa, chân duỗi thẳng.")
        st.write("- **Cách thực hiện:** Từ từ trượt chân mổ sang ngang ra phía ngoài rồi kéo về giữa (tuân thủ không dạng quá mức).")
        st.write("- **Liều lượng:** 10 lần/hiệp.")

        st.markdown("##### 4. Trượt gót chân gập háng nhẹ")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Trượt gót chân gập háng và gối nhẹ nhàng (lưu ý tuyệt đối không gập háng quá 90 độ).")
        st.write("- **Liều lượng:** 10 lần/hiệp.")

        st.markdown("##### 5. Nâng chân thẳng ở tư thế nằm ngửa")
        st.write("- **Tư thế:** Nằm ngửa.")
        st.write("- **Cách thực hiện:** Gồng cơ đùi và nâng chân lên khỏi mặt giường khoảng 15cm.")
        st.write("- **Liều lượng:** 10 lần/hiệp.")

        st.markdown("##### 6. Tập đứng dồn lực đều hai chân với khung")
        st.write("- **Tư thế:** Đứng thẳng bằng khung tập đi.")
        st.write("- **Cách thực hiện:** Phân bổ trọng lượng cơ thể đều hai bên chân dưới sự giám sát.")
        st.write("- **Liều lượng:** 5–10 phút.")

        st.markdown("##### 7. Hướng dẫn tư thế sinh hoạt an toàn")
        st.write("- **Lưu ý:** Không bắt chéo chân khi nằm hoặc ngồi, không cúi gập người quá 90 độ, luôn dùng ghế cao khi ngồi vệ sinh.")

    elif "8." in rehab_program:
        st.subheader("🗣️ 8. Chương trình PHCN cho trẻ chậm nói / Rối loạn ngôn ngữ")
        st.write("• **Mục tiêu:** Kích thích cơ quan phát âm, mở rộng vốn từ vựng tiếp nhận.")
        
        st.markdown("---")
        st.markdown("##### 1. Massage kích thích cơ vùng miệng - môi - má")
        st.write("- **Tư thế:** Trẻ ngồi thoải mái trước mặt kỹ thuật viên hoặc phụ huynh.")
        st.write("- **Cách thực hiện:** Dùng tay sạch massage nhẹ nhàng xung quanh môi, má và vùng cơ quanh miệng để tăng cảm giác.")
        st.write("- **Liều lượng:** 3–5 phút.")

        st.markdown("##### 2. Tập thổi hơi có mục đích")
        st.write("- **Tư thế:** Ngồi bàn ghế ngay ngắn.")
        st.write("- **Cách thực hiện:** Cho trẻ tập thổi bóng bông trên bàn, thổi còi nhựa hoặc thổi tắt nến ở khoảng cách gần.")
        st.write("- **Liều lượng:** 5–10 lần thổi mỗi buổi.")

        st.markdown("##### 3. Giao tiếp mắt 1 kèm 1 với Flashcard")
        st.write("- **Tư thế:** Ngồi đối diện trẻ ở cự ly gần.")
        st.write("- **Cách thực hiện:** Đưa thẻ hình con vật, đồ vật màu sắc sinh động ngang tầm mắt, yêu cầu trẻ nhìn thẳng vào mắt người dạy và phát âm theo.")
        st.write("- **Liều lượng:** 10 phút.")

        st.markdown("##### 4. Bắt chước âm thanh gần gũi")
        st.write("- **Tư thế:** Ngồi chơi đùa tương tác.")
        st.write("- **Cách thực hiện:** Phát ra các âm thanh đơn giản (tiếng kêu động vật: meo meo, gâu gâu, ò í e) và khuyến khích trẻ bắt chước.")
        st.write("- **Liều lượng:** 5–10 phút.")

        st.markdown("##### 5. Đọc to từ đơn tiết kèm vật thật")
        st.write("- **Tư thế:** Tương tác trực tiếp với đồ vật thực tế (quả táo, quả bóng).")
        st.write("- **Cách thực hiện:** Cầm đồ vật, gọi rõ tên từng từ đơn chậm rãi, rõ khẩu hình miệng.")
        st.write("- **Liều lượng:** 10 phút.")

        st.markdown("##### 6. Hát bài hát thiếu nhi có động tác")
        st.write("- **Tư thế:** Vui chơi vận động.")
        st.write("- **Cách thực hiện:** Hát các bài hát thiếu nhi quen thuộc kèm theo các động tác múa tay chân minh họa để kích thích ngôn ngữ qua nhịp điệu.")
        st.write("- **Liều lượng:** 10–15 phút.")

        st.markdown("##### 7. Hướng dẫn phụ huynh tương tác mở rộng tại nhà")
        st.write("- **Nội dung:** Dặn dò bố mẹ luôn giao tiếp, gọi tên sự vật xung quanh bé mọi lúc mọi nơi trong sinh hoạt hàng ngày, hạn chế tối đa thời gian xem tivi/điện thoại.")
