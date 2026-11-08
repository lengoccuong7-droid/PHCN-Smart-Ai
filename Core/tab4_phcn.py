# =========================================================
# TAB 4: KHO BÀI TẬP PHỤC HỒI CHỨC NĂNG (ĐẦY ĐỦ TÁC DỤNG & CÁCH THỰC HIỆN)
# =========================================================
import streamlit as st

def render():
    if "rehab_detail_page" not in st.session_state:
        st.session_state.rehab_detail_page = None

    # MÀN HÌNH 1: LƯỚI CHỌN NHÓM BỆNH LÝ
    if st.session_state.rehab_detail_page is None:
        st.subheader("🏋️‍♂️ Kho Bài Tập Phục Hồi Chức Năng Chuyên Sâu")
        st.markdown("Chọn một nhóm bệnh lý bên dưới để xem chi tiết trọn bộ 7 bài tập chuẩn hóa kèm tác dụng và cách thực hiện:")

        search_ex_kw = st.text_input("🔍 Tìm kiếm bài tập, động tác, hội chứng...", placeholder="Nhập từ khóa...", key="search_exercise_input")

        st.markdown("---")
        st.markdown("##### 🗂️ Danh mục nhóm bệnh lý & Chuyên khoa PHCN")

        pathologies_m4_full = [
            ("1. Tai biến mạch máu não (Liệt nửa người)", "🧠", "Phục hồi vận động chi liệt & thăng bằng"),
            ("2. Rối loạn nuốt (Dysphagia) sau tai biến", "💧", "Kỹ thuật nuốt & cơ vùng miệng họng"),
            ("3. Rối loạn ngôn ngữ & Thất ngôn (Aphasia)", "🗣️", "Kích thích ngôn ngữ & giao tiếp"),
            ("4. Âm ngữ trị liệu (Rối loạn phát âm / Dysarthria)", "🗣️", "Kiểm soát phát âm & hơi thở"),
            ("5. Trẻ tự kỷ (Rối loạn phổ tự kỷ kèm rối loạn vận động)", "🧩", "Điều hòa cảm giác & vận động thô"),
            ("6. Xơ hóa cơ ức đòn chũm (Torticollis / Vẹo cổ bẩm sinh)", "🔄", "Kéo giãn cơ ức đòn chũm & vận động"),
            ("7. PHCN sau Phẫu thuật đầu gối (Tái tạo dây chằng chéo ACL)", "🦿", "Tập vận động sau mổ dây chằng gối"),
            ("8. PHCN sau Phẫu thuật thay khớp háng toàn phần", "🦿", "Phục hồi tầm vận động và dáng đi khớp háng"),
            ("9. PHCN sau Gãy tay / Gãy chân (Hậu phẫu / Bó bột)", "🦾", "Phục hồi tầm vận động và chống teo cơ")
        ]

        cols_e = st.columns(3)
        for idx, item in enumerate(pathologies_m4_full):
            title, icon, desc = item
            col_target = cols_e[idx % 3]
            with col_target:
                with st.container(border=True):
                    st.markdown(f"<h3 style='text-align: center; margin: 0;'>{icon}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 14px; margin: 5px 0;'>{title}</p>", unsafe_allow_html=True)
                    st.caption(desc)
                    if st.button("🏋️‍♂️ Xem bài tập", use_container_width=True, key=f"open_rehab_{idx}"):
                        st.session_state.rehab_detail_page = title
                        st.rerun()

        st.markdown("---")
        st.caption("💡 Hệ thống dữ liệu bài tập PHCN được chuẩn hóa theo y học chứng cứ phục hồi chức năng vận động và ngôn ngữ.")

    # MÀN HÌNH 2: TRANG CHI TIẾT BỆNH LÝ & TRỌN BỘ 7 BÀI TẬP (CÓ ĐỦ TÁC DỤNG & CÁCH THỰC HIỆN)
    else:
        group_name = st.session_state.rehab_detail_page

        if st.button("⬅️ Quay lại danh mục nhóm bệnh lý", type="secondary", key="back_to_rehab_grid"):
            st.session_state.rehab_detail_page = None
            st.rerun()

        st.markdown("---")
        st.subheader(f"📂 KHO BÀI TẬP CHUYÊN SÂU: {group_name.upper()}")
        st.caption("Trọn bộ 7 bài tập chuẩn hóa lâm sàng kèm theo tác dụng và cách thực hiện chi tiết.")

        # Cơ sở dữ liệu chi tiết đầy đủ Tác dụng & Cách thực hiện cho từng bài
        detailed_exercises_db = {
            "1. Tai biến mạch máu não (Liệt nửa người)": [
                ("1. Tập vận động thụ động các khớp bên liệt duy trì tầm vận động (ROM).", 
                 "Duy trì biên độ khớp, ngăn ngừa cứng khớp, dính bao khớp và phù nề.", 
                 "Kỹ thuật viên hoặc người nhà nâng đỡ từng khớp của chi liệt (vai, khuỷu, cổ tay, háng, gối, cổ chân), thực hiện biên độ từ từ, nhẹ nhàng đến tầm vận động tối đa không gây đau. Thực hiện 10 lần/khớp."),
                ("2. Bài tập ức chế trương lực cơ co cứng (kỹ thuật Bobath).", 
                 "Giảm hiện tượng co cứng cơ gấp chi trên và duỗi chi dưới theo phản xạ nguyên thủy.", 
                 "Sử dụng các tư thế ức chế (như duỗi xoay ngoài vai, gấp duỗi cẳng tay nhịp nhàng) kết hợp xoa bóp thả lỏng trước khi tập vận động chủ động."),
                ("3. Tập chuyển đổi tư thế từ nằm ngửa sang nằm nghiêng và ngồi dậy.", 
                 "Tăng cường khả năng tự chủ động kiểm soát thân mình và chuyển động xoay trục cơ thể.", 
                 "Bệnh nhân chống tay lành đẩy người, nghiêng người sang bên liệt hoặc bên lành, gập gối, dùng lực thân mình phối hợp với kỹ thuật viên dìu ngồi dậy mép giường."),
                ("4. Tập kiểm soát thăng bằng thân mình ở tư thế ngồi độc lập.", 
                 "Cải thiện sự vững chãi của cơ trục thân người, chuẩn bị cho giai đoạn đứng đi.", 
                 "Bệnh nhân ngồi trên ghế băng không có tựa lưng, hai chân chạm đất rộng bằng vai. Kỹ thuật viên hỗ trợ đẩy nhẹ các hướng để bệnh nhân tự cân bằng giữ thẳng lưng."),
                ("5. Tập đứng dồn trọng lượng đều hai chân trước gương.", 
                 "Tái huấn luyện pha chịu lực của chi liệt, tăng cường nhận cảm bản thể.", 
                 "Bệnh nhân đứng trước gương lớn, tay vịn song mã hoặc bàn tập. Hướng dẫn bệnh nhân phân phối lực đều 50% bên lành và 50% bên liệt, quan sát trực giác qua gương."),
                ("6. Bài tập đi lại với máng nẹp cẳng bàn chân (AFO) hoặc khung tập đi.", 
                 "Phục hồi chu kỳ dáng đi an toàn, chống rủ bàn chân và lệch trục khớp gối.", 
                 "Bệnh nhân mang nẹp hỗ trợ (nếu cần), sử dụng khung tập đi. Tiến hành bước chân lành lên trước, sau đó kéo chân liệt theo nhịp bước đều đặn dưới sự giám sát chặt chẽ."),
                ("7. Tập mạnh cơ chủ động bên lành và các nhóm cơ duỗi bên liệt.", 
                 "Lấy lại sức mạnh cơ lực và chức năng vận động linh hoạt cho các nhóm cơ yếu.", 
                 "Sử dụng tạ tay siêu nhẹ hoặc dây kháng lực đàn hồi (Theraband) tập các động tác gấp duỗi chi trên và chi dưới theo khả năng dung nạp của người bệnh.")
            ],
            "2. Rối loạn nuốt (Dysphagia) sau tai biến": [
                ("1. Bài tập vận động cơ môi (mím chặt, cười hết cỡ, thổi phồng má, phát âm U-I).", 
                 "Tăng cường độ khép kín và sức mạnh cơ vòng miệng, tránh trào ngược nước bọt.", 
                 "Bệnh nhân thực hiện mím môi chặt trong 5 giây, sau đó cười hết cỡ, thổi phồng má giữ hơi và luân phiên phát âm kéo dài âm 'U' rồi 'I'. Làm lặp lại 10 lần."),
                ("2. Bài tập vận động lưỡi (đẩy lưỡi ra trước, sang trái, sang phải, liếm vòm họng).", 
                 "Cải thiện sự linh hoạt, khéo léo và biên độ vận động của lưỡi trong nhai nuốt.", 
                 "Lè lưỡi tối đa ra trước, thò thụt; đẩy lưỡi sang khóe miệng trái rồi phải; dùng đầu lưỡi liếm vòng quanh vòm miệng trên và dưới. Thực hiện 10 nhịp."),
                ("3. Kích thích nhiệt lạnh vùng cung khẩu cái mềm kích thích phản xạ nuốt.", 
                 "Đánh thức cung phản xạ nuốt nguyên phát bị tổn thương ở vỏ não.", 
                 "Dùng gương soi kết hợp que đè lưỡi bọc gạc thấm nước đá lạnh, chạm nhẹ và chà xát vùng cung khẩu cái trước và trụ amidan trong 2-3 phút."),
                ("4. Bài tập Masako (giữ đầu lưỡi giữa hai hàm răng và nuốt nước bọt).", 
                 "Tăng sức mạnh co thắt cơ thành sau họng, đẩy thức ăn xuống thực quản.", 
                 "Bệnh nhân thè đầu lưỡi ra ngoài nhẹ nhàng, giữ cố định giữa hai hàm răng (hoặc kẹp bằng răng cửa nhẹ), sau đó cố gắng thực hiện động tác nuốt nước bọt. Làm 10 lần."),
                ("5. Bài tập Shaker (nâng đầu ở tư thế nằm ngửa để mở rộng cơ thắt thực quản trên).", 
                 "Giúp mở rộng cơ thắt thực quản trên, tạo điều kiện thuận lợi cho thức ăn đi xuống.", 
                 "Bệnh nhân nằm ngửa hoàn toàn, không nhấc vai, nâng đầu lên nhìn vào ngón chân cái của mình trong 60 giây rồi hạ xuống nghỉ 30 giây. Lặp lại 3 lần."),
                ("6. Bài tập đóng nắp thanh môn (nuốt giữ hơi, ho mạnh ngay sau khi nuốt).", 
                 "Bảo vệ đường thở không bị trào ngược dị vật vào phổi gây viêm phổi hít.", 
                 "Bệnh nhân hít sâu, nín thở, nuốt một ngụm nước bọt, ngay sau khi nuốt xong thì thực hiện tiếng ho mạnh để tống xuất cặn dịch còn sót lại ở thanh môn."),
                ("7. Luyện tập nuốt theo các độ quánh thức ăn chuẩn hóa IDDSI.", 
                 "Thích nghi an toàn với các độ đặc thức ăn khác nhau từ lỏng, sệt đến đặc.", 
                 "Bắt đầu tập nuốt với nước sệt mức độ vừa, cháo nhuyễn dưới sự giám sát trực tiếp của kỹ thuật viên âm ngữ trị liệu và tuân thủ tuyệt đối an toàn.")
            ],
            "3. Rối loạn ngôn ngữ & Thất ngôn (Aphasia)": [
                ("1. Liệu pháp kích thích thính giác (nghe từ và chỉ tay vào hình ảnh/đồ vật).", 
                 "Cải thiện khả năng tiếp nhận và hiểu ngôn ngữ nói của người bệnh.", 
                 "Bác sĩ đọc tên một đồ vật quen thuộc (cốc, thìa, quần áo), bệnh nhân nghe và dùng tay chỉ đúng vào hình ảnh hoặc vật thể tương ứng đặt trên bàn. Thực hiện 10 từ/lượt."),
                ("2. Luyện phát âm nguyên âm cơ bản (A - O - E - I - U) tròn khẩu hình.", 
                 "Tái thiết lập phản xạ vận động cơ quan phát âm và khẩu hình cơ bản.", 
                 "Bác sĩ làm mẫu khẩu hình miệng thật rõ, bệnh nhân quan sát qua gương và phát âm to, rõ ràng từng nguyên âm kéo dài 3-5 giây. Lặp lại 3 sets x 5 lần."),
                ("3. Bài tập gọi tên đồ vật sinh hoạt hằng ngày qua thẻ hình ảnh (Flashcard).", 
                 "Phục hồi khả năng biểu đạt từ vựng và gọi tên sự vật xung quanh.", 
                 "Sử dụng các thẻ hình ảnh màu sắc sinh động (quả chuối, cái bàn, cái áo), yêu cầu bệnh nhân nhìn hình và tự phát âm tên gọi rõ ràng."),
                ("4. Liệu pháp âm điệu ngữ âm (MEL/MIT) dùng nhịp điệu kích thích phát âm câu ngắn.", 
                 "Tận dụng chức năng bán cầu não phải để hỗ trợ và bù đắp cho vùng ngôn ngữ bị tổn thương.", 
                 "Bác sĩ gõ nhịp và hát/nói đều đặn theo giai điệu đơn giản các câu giao tiếp hàng ngày (ví dụ: 'Tôi muốn uống nước'), bệnh nhân nhịp theo và nói cùng."),
                ("5. Bài tập hoàn thành câu (bác sĩ đọc ngắt quãng, bệnh nhân nói từ cuối).", 
                 "Kích hoạt phản xạ ngôn ngữ tự động và chuỗi từ vựng quen thuộc.", 
                 "Bác sĩ đọc nửa câu đầu (ví dụ: 'Trời hôm nay rất...'), bệnh nhân tự động điền và phát âm từ cuối cùng ('đẹp'). Làm 10 câu/lượt."),
                ("6. Tập đặt câu hỏi và phản đáp các nhu cầu giao tiếp cơ bản (ăn, uống, đau, đi vệ sinh).", 
                 "Thiết lập giao tiếp tối thiểu, giúp người bệnh tự lập trong sinh hoạt.", 
                 "Tập luyện hỏi đáp các tình huống thực tế: 'Anh/chị có đau không?', 'Anh/chị muốn uống nước không?' và hướng dẫn cách trả lời gật/lắc hoặc nói từ đơn."),
                ("7. Bài tập giao tiếp phi ngôn ngữ hỗ trợ (dùng cử chỉ tay, bảng ký hiệu).", 
                 "Hỗ trợ diễn đạt ý muốn trong giai đoạn chưa phục hồi hoàn toàn lời nói.", 
                 "Sử dụng bảng chữ cái lớn hoặc bảng ký hiệu biểu tượng nhu cầu, hướng dẫn bệnh nhân dùng tay chỉ vào biểu tượng tương ứng khi muốn diễn đạt.")
            ],
            "4. Âm ngữ trị liệu (Rối loạn phát âm / Dysarthria)": [
                ("1. Bài tập kiểm soát hơi thở cơ hoành (thở sâu, giữ hơi, thổi nến đều).", 
                 "Cung cấp cột hơi ổn định, mạnh mẽ hỗ trợ cho việc phát âm rõ ràng.", 
                 "Bệnh nhân đặt tay lên bụng, hít sâu bằng mũi sao cho bụng phình lên, nín thở 3 giây, sau đó thở ra từ từ bằng miệng hoặc thổi tắt ngọn nến ở khoảng cách 20cm. Làm 10 lần."),
                ("2. Bài tập tăng sức mạnh cơ hô hấp phục vụ phát âm câu dài.", 
                 "Tăng độ bền và khả năng duy trì âm lượng khi nói chuyện liên tục.", 
                 "Tập luyện phát âm kéo dài một hơi âm 'S' hoặc 'A' liên tục lâu nhất có thể, bấm giờ theo dõi sự tiến bộ qua từng ngày. Lặp lại 5 lần."),
                ("3. Bài tập vận động linh hoạt cơ quan phát âm (vòm miệng mềm, môi, lưỡi, hàm dưới).", 
                 "Giảm độ cứng cơ quan phát âm, tăng độ uyển chuyển khi phát âm từ phức tạp.", 
                 "Thực hiện há miệng lớn tối đa rồi ngậm lại; nhai giả định vòng tròn; phát âm luân phiên 'Pa-Ta-Ka' nhanh và dứt khoát liên tục trong 30 giây."),
                ("4. Luyện phát âm chính xác các cặp phụ âm - nguyên âm.", 
                 "Tăng độ rõ ràng của từng âm tiết, khắc phục tình trạng nói ngọng, nói dính chữ.", 
                 "Đọc to rõ các âm tiết đôi có vần đối chiếu (Ba-Ba, Ma-Ma, Da-Da, La-La) với tốc độ vừa phải, chú ý độ mở của khẩu hình miệng."),
                ("5. Bài tập điều chỉnh tốc độ nói (nói chậm, ngắt nhịp theo từ).", 
                 "Giúp người nghe dễ hiểu hơn, khắc phục lỗi nói quá nhanh hoặc quá giật cục.", 
                 "Sử dụng bảng nhịp nhịp (Pacing board), yêu cầu bệnh nhân chạm tay vào từng ô tương ứng với mỗi từ được phát âm để kiểm soát nhịp độ."),
                ("6. Bài tập kiểm soát cường độ và cao độ giọng nói (to/nhỏ, trầm/bổng).", 
                 "Tránh tình trạng giọng nói đơn điệu, đứt quãng hoặc quá nhỏ không nghe thấy.", 
                 "Luyện tập phát âm từ thì thầm chuyển dần sang nói bình thường và nói to rõ ràng trước sự hướng dẫn của kỹ thuật viên. Lặp lại 3 sets."),
                ("7. Luyện đọc đoạn văn ngắn trước gương kết hợp kiểm soát nhịp thở và khẩu hình.", 
                 "Tăng độ bền và sự tự tin khi giao tiếp thực tế trong đời sống hàng ngày.", 
                 "Bệnh nhân đứng trước gương, đọc một đoạn văn ngắn khoảng 4-5 câu, tự quan sát khẩu hình miệng và chủ động ngắt nghỉ đúng các dấu câu.")
            ],
            "5. Trẻ tự kỷ (Rối loạn phổ tự kỷ kèm rối loạn vận động)": [
                ("1. Bài tập điều hòa cảm giác tiền đình (nhún nhảy trên bóng trị liệu, đung đưa võng).", 
                 "Cải thiện khả năng cân bằng không gian và giảm hành vi kích thích quá mức.", 
                 "Cho trẻ ngồi hoặc nằm sấp trên bóng trị liệu lớn (Gymball), người hỗ trợ giữ hông và thực hiện các động tác nhún nhẹ nhàng, lăn qua lại theo nhịp điệu trong 5 phút."),
                ("2. Bài tập cảm giác bản thể (ôm chặt, ép khớp sâu, lăn cuộn trong thảm bọt biển).", 
                 "Giúp trẻ nhận thức rõ hơn về ranh giới cơ thể, mang lại cảm giác an toàn.", 
                 "Thực hiện kỹ thuật ép khớp nhẹ nhàng ở các khớp tay chân hoặc quấn trẻ trong chăn nặng, lăn cuộn nhẹ nhàng qua lại trên thảm xốp trong 3-5 phút."),
                ("3. Bài tập đi trên ván thăng bằng nâng cao phối hợp vận động thô.", 
                 "Phát triển hệ thống thăng bằng và sự phối hợp vận động toàn thân.", 
                 "Đặt một thanh ván gỗ phẳng hẹp (rộng 15cm) trên sàn, hướng dẫn trẻ bước đi thẳng hàng từ đầu này đến đầu kia mà không bị ngã ra ngoài. Thực hiện 5 lần."),
                ("4. Bài tập kéo giãn cơ cẳng chân (phòng ngừa và sửa dáng đi nhón gót).", 
                 "Duy trì tầm vận động khớp cổ chân, chống co rút gân gót thường gặp ở trẻ tự kỷ.", 
                 "Cho trẻ đứng tựa lưng vào tường, bước một chân về phía sau, giữ gót chân chạm đất và ép háng về trước để kéo giãn vùng bắp chân trong 15 giây mỗi bên."),
                ("5. Bài tập vận động tinh bàn tay (nhặt hạt nhỏ, xếp hình khối, xâu chuỗi hạt).", 
                 "Tăng sự khéo léo của các ngón tay và khả năng tập trung chú ý thị giác.", 
                 "Chuẩn bị các hạt vòng lớn hoặc khối gỗ nhỏ, hướng dẫn trẻ dùng ngón cái và ngón trỏ nhặt bỏ vào hộp hoặc xâu vào dây theo màu sắc yêu cầu trong 10 phút."),
                ("6. Bài tập phối hợp tay - mắt theo hiệu lệnh trò chơi tương tác.", 
                 "Cải thiện khả năng tập trung chú ý và phản xạ vận động phối hợp nhóm.", 
                 "Cho trẻ đứng đối diện, ném và bắt quả bóng mềm qua lại ở cự ly gần (1-2 mét), kết hợp đếm số hoặc gọi tên màu sắc bóng để tăng tương tác xã hội."),
                ("7. Bài tập bắt chước tư thế động học giúp tăng cường tập trung chú ý.", 
                 "Gắn kết tương tác xã hội và khả năng bắt chước hành vi thông qua vận động.", 
                 "Kỹ thuật viên làm mẫu các tư thế tay chân đơn giản (giơ tay cao, chống hông, vỗ tay), yêu cầu trẻ quan sát và bắt chước làm theo chính xác.")
            ],
            "6. Xơ hóa cơ ức đòn chũm (Torticollis / Vẹo cổ bẩm sinh)": [
                ("1. Kéo giãn thụ động cơ ức đòn chũm bên bị xơ (nghiêng đầu sang bên lành, quay cằm về bên bệnh).", 
                 "Làm mềm và kéo dài dải xơ co rút, phục hồi cân bằng trục cổ.", 
                 "Đặt trẻ nằm ngửa, một tay cố định vai bên bệnh, tay kia từ từ nghiêng đầu trẻ sang bên tai hướng về vai lành, đồng thời xoay cằm hướng về phía bên bị xơ. Giữ 15 giây x 10 lần."),
                ("2. Kích thích trẻ quay đầu về bên bệnh bằng âm thanh và đồ chơi màu sắc.", 
                 "Tăng cường vận động chủ động quay cổ về phía bị hạn chế.", 
                 "Đặt đồ chơi phát âm thanh hoặc rọi ánh sáng màu ở phía bên cổ bị bệnh khi trẻ nằm ngửa, khuyến khích trẻ tự chủ động xoay đầu theo hướng đó."),
                ("3. Bài tập đặt tư thế nằm ngủ đúng (dùng gối cát/gối định hình giữ cổ thẳng).", 
                 "Ngăn ngừa tình trạng vẹo lệch nặng thêm do tư thế xấu khi ngủ.", 
                 "Sử dụng gối chữ C hoặc túi cát nhỏ chèn hai bên đầu và cổ của trẻ khi ngủ ở tư thế nằm ngửa để giữ đầu luôn ở vị trí trung gian thẳng trục."),
                ("4. Kỹ thuật xoa bóp, miết nhẹ nhàng giải phóng dải xơ cơ ức đòn chũm.", 
                 "Tăng tuần hoàn máu tại chỗ, làm mềm khối u xơ cơ.", 
                 "Dùng đầu ngón tay cái và ngón trỏ day ấn nhẹ nhàng dọc theo chiều bám của cơ ức đòn chũm từ vùng xương chũm xuống xương đòn trong 3 phút."),
                ("5. Bài tập vận động chủ động quay cổ (với trẻ lớn) qua các trò chơi theo tầm vận động.", 
                 "Khôi phục hoàn toàn biên độ vận động quay cổ hai chiều.", 
                 "Tổ chức các trò chơi tương tác như trò quay đầu tìm đồ vật, lắc đầu theo nhạc với biên độ từ từ tăng dần trong giới hạn không đau."),
                ("6. Tập mạnh cơ cổ bên đối diện để cân bằng lực kéo cột sống cổ.", 
                 "Cân bằng lực cơ hai bên để giữ vững cột sống cổ ở tư thế thẳng.", 
                 "Cho trẻ nằm nghiêng về bên lành, nâng đầu lên khỏi mặt gối chống lại trọng lực nhẹ trong 3-5 giây. Lặp lại 5 lần."),
                ("7. Hướng dẫn phụ huynh duy trì bế, cho bú và sinh hoạt ở tư thế điều chỉnh.", 
                 "Duy trì hiệu quả điều trị và chống tái phát tại nhà.", 
                 "Hướng dẫn bố mẹ khi bế trẻ hoặc cho bú phải đổi bên, xoay mặt trẻ về hướng ngược lại với tư thế vẹo quen thuộc hằng ngày.")
            ],
            "7. PHCN sau Phẫu thuật đầu gối (Tái tạo dây chằng chéo ACL)": [
                ("1. Bài tập gồng cơ tĩnh tứ đầu đùi (Isometric Quads) ngay sau mổ.", 
                 "Ngăn ngừa teo cơ đùi sớm và kích hoạt lại phản xạ thần kinh cơ mổ.", 
                 "Bệnh nhân nằm ngửa, chân duỗi thẳng, ép sát khoeo chân xuống mặt giường, căng cứng cơ đùi trước và giữ chặt trong 5 giây rồi thả lỏng. Thực hiện 3 sets x 15 lần."),
                ("2. Bài tập duỗi thẳng gối tối đa (0 độ) và gấp gối thụ động trong phạm vi cho phép.", 
                 "Khôi phục hoàn toàn biên độ vận động duỗi thẳng gối ban đầu.", 
                 "Kê gót chân lên cao (để lơ lửng phần khoeo), dùng trọng lực hoặc túi cát nhẹ đè lên trên gối để ép gối thẳng tối đa trong 3 phút mỗi lần."),
                ("3. Bài tập nhấc chân thẳng khỏi mặt giường (Straight Leg Raise).", 
                 "Tăng sức mạnh cơ tứ đầu đùi và nhóm cơ gập háng sau phẫu thuật.", 
                 "Duỗi thẳng gối hoàn toàn, siết chặt cơ đùi rồi từ từ nâng cả chân cách mặt giường khoảng 15-20cm, giữ 3 giây rồi hạ xuống. Thực hiện 3 sets x 10 lần."),
                ("4. Tập đạp xe tại chỗ không kháng trở (khi biên độ gấp gối đạt trên 90 độ).", 
                 "Tăng lưu thông dịch khớp, cải thiện tầm vận động và sự linh hoạt.", 
                 "Ngồi trên xe đạp tập tại phòng khám, điều chỉnh yên xe phù hợp và đạp vòng tròn nhẹ nhàng không có tải trọng trong 10-15 phút."),
                ("5. Bài tập đứng dồn trọng lượng hai chân và chuyển trọng lượng sang chân mổ.", 
                 "Tập thích nghi lại với tải trọng cơ thể và trọng lực lên khớp gối mới mổ.", 
                 "Đứng bám hai tay vào song song, thực hiện chuyển trọng tâm cơ thể từ chân lành sang chân mổ một cách từ từ dưới sự giám sát của kỹ thuật viên."),
                ("6. Bài tập thăng bằng bản thể (Proprioception) trên đĩa thăng bằng hoặc thảm mềm.", 
                 "Phục hồi khả năng định vị không gian và phản xạ bảo vệ của khớp gối.", 
                 "Bệnh nhân đứng một chân mổ trên đĩa thăng bằng hoặc tấm xốp dày, cố gắng giữ thăng bằng cơ thể không để ngã trong 30 giây. Lặp lại 5 lần."),
                ("7. Bài tập mạnh cơ đùi sau (Hamstrings) và cơ cẳng chân có kháng lực tăng dần.", 
                 "Củng cố sự vững chắc toàn diện cho hệ thống dây chằng quanh gối.", 
                 "Sử dụng máy tập gấp gối kháng lực hoặc dây thun đàn hồi buộc ở cổ chân, thực hiện kéo gót chân về phía mông với mức tạ tăng dần phù hợp giai đoạn liền xương.")
            ],
            "8. PHCN sau Phẫu thuật thay khớp háng toàn phần": [
                ("1. Bài tập co duỗi cổ chân (Ankle pumps) ngừa huyết khối tĩnh mạch sâu chi dưới.", 
                 "Kích hoạt tuần hoàn máu tĩnh mạch chi dưới, phòng ngừa tắc mạch.", 
                 "Nằm ngửa, hai chân duỗi thẳng, thực hiện gập duỗi cổ chân liên tục hết biên độ lên xuống nhịp nhàng. Thực hiện 20 lần liên tục mỗi giờ."),
                ("2. Bài tập siết cơ mông và cơ tứ đầu đùi ở tư thế nằm ngửa.", 
                 "Tăng cường sức mạnh các nhóm cơ lớn xung quanh ổ khớp háng.", 
                 "Nằm ngửa, hai chân duỗi, thực hiện siết chặt hai cơ mông lại với nhau trong 5 giây rồi thả lỏng; kết hợp gồng cơ đùi trước. Làm 3 sets x 10 lần."),
                ("3. Bài tập trượt gót chân trên giường (gấp khớp háng nhẹ nhàng < 90 độ).", 
                 "Duy trì tầm vận động gấp háng an toàn mà không vi phạm nguyên tắc sau mổ.", 
                 "Từ tư thế nằm ngửa, từ từ trượt gót chân mổ lại gần mông trong giới hạn góc gấp háng dưới 90 độ theo đúng phác đồ bác sĩ phẫu thuật. Làm 10 lần."),
                ("4. Bài tập dang chân sang bên (Abduction) tránh tư thế khép và xoay trong quá mức.", 
                 "Đảm bảo sự vững vàng cho chỏm khớp nhân tạo, tránh trật khớp.", 
                 "Nằm ngửa, hai chân duỗi thẳng, từ từ trượt chân mổ sang phía bên ngoài (dang ra xa đường giữa cơ thể) rồi kéo về vị trí cũ. Làm 3 sets x 10 lần."),
                ("5. Bài tập đứng dậy từ ghế cao có tay tựa với sự hỗ trợ của khung tập đi.", 
                 "Khôi phục chức năng vận động cơ bản và sinh hoạt độc lập cho người bệnh.", 
                 "Ngồi trên ghế cao có tay vịn, chống tay đứng dậy bằng chân lành và chân mổ với lực hỗ trợ của khung tập đi, giữ tư thế thẳng lưng."),
                ("6. Bài tập tái giáo dục dáng đi dồn lực đều hai chân, không khập khiễng.", 
                 "Sửa đổi dáng đi chuẩn xác, tránh thói quen xấu sau phẫu thuật.", 
                 "Tập đi lại giữa hai song song hoặc với nạng, hướng dẫn người bệnh bước chân mổ lên trước đồng thời dồn lực chịu tải đều đặn hai bên."),
                ("7. Bài tập leo cầu thang (nguyên tắc: chân lành bước lên trước, chân mổ bước xuống trước).", 
                 "Tái hòa nhập vận động sinh hoạt phức tạp hằng ngày một cách an toàn.", 
                 "Thực hiện leo cầu thang theo đúng quy tắc y khoa: khi lên bậc thang đưa chân lành lên trước; khi xuống bậc thang đưa chân mổ và nạng xuống trước.")
            ],
            "9. PHCN sau Gãy tay / Gãy chân (Hậu phẫu / Bó bột)": [
                ("1. Bài tập gồng cơ tĩnh bên trong bột (Isometric contraction) chống teo cơ.", 
                 "Duy trì khối cơ bên dưới lớp cố định, kích hoạt tuần hoàn máu.", 
                 "Bệnh nhân gồng cứng các nhóm cơ nằm phía bên trong lớp bột hoặc nẹp bất động, giữ chặt trong 5 giây rồi thả lỏng. Thực hiện nhiều lần trong ngày."),
                ("2. Cử động tích cực toàn bộ các khớp tự do không bị bất động (ngón tay/ngón chân).", 
                 "Duy trì tuần hoàn ngoại vi và chống cứng khớp các vùng lân cận.", 
                 "Thực hiện cử động gập duỗi, xòe cụp các ngón tay (nếu gãy tay) hoặc ngón chân (nếu gãy chân) liên tục hết biên độ một cách chủ động. Làm 20 lần/lượt."),
                ("3. Sau tháo bột: Bài tập phục hồi tầm vận động (ROM) chủ động và thụ động các khớp lân cận.", 
                 "Lấy lại biên độ chuyển động bình thường sau thời gian dài bất động.", 
                 "Kỹ thuật viên hỗ trợ nắn bóp, kéo giãn nhẹ nhàng và hướng dẫn người bệnh tự tập gấp duỗi các khớp đích trong giới hạn đau cho phép."),
                ("4. Kỹ thuật xoa bóp di động sẹo mổ và giải phóng mô mềm dính.", 
                 "Làm mềm mô xơ sẹo sau phẫu thuật kết hợp, chống dính gân cơ.", 
                 "Dùng ngón tay cái thực hiện các động tác day ấn vòng tròn xung quanh vết mổ và mô sẹo khi vết thương đã lành hẳn nhằm tăng độ mềm mại."),
                ("5. Bài tập tăng dần lực cơ bằng tạ nhẹ, lò xo hoặc dây kháng lực (Theraband).", 
                 "Khôi phục hoàn toàn sức mạnh cơ bắp chi thể về mức bình thường.", 
                 "Sử dụng tạ tay siêu nhẹ hoặc dây thun kháng lực tập các bài tập đối kháng tăng dần cường độ theo tiến độ liền xương trên phim X-quang."),
                ("6. Bài tập tái giáo dục dáng đi (với gãy chân) hoặc bài tập cầm nắm khéo léo (với gãy tay).", 
                 "Hoàn thiện chức năng vận động chuyên biệt, giúp chi thể hoạt động khéo léo.", 
                 "Tập đi đường thẳng không què quặt (với chi dưới) hoặc tập cầm nắm đồ vật, viết chữ, dùng thìa đũa (với chi trên)."),
                ("7. Bài tập phục hồi chức năng sinh hoạt hằng ngày (ADL) thích ứng.", 
                 "Giúp người bệnh tự lập tối đa trong đời sống và công việc cá nhân.", 
                 "Tập luyện các kỹ năng tự chăm sóc bản thân, mặc quần áo, vệ sinh cá nhân và các thao tác lao động nhẹ nhàng thích ứng.")
            ]
        }

        current_exercises = detailed_exercises_db.get(group_name, [])

        for idx_ex, (ex_title, ex_purpose, ex_tech) in enumerate(current_exercises):
            with st.expander(f"🔹 {ex_title}"):
                st.markdown(f"- **🎯 Mục đích lâm sàng:** {ex_purpose}")
                st.markdown(f"- **⚙️ Hướng dẫn kỹ thuật:** {ex_tech}")
                st.markdown("- **⏱️ Liều lượng khuyến nghị:** 3 sets x 10 lần thực hiện / ngày (hoặc theo chỉ định lâm sàng cụ thể).")

        st.markdown("---")
        if st.button("⬅️ Quay lại danh mục nhóm bệnh lý", type="primary", key="bottom_back_rehab_btn"):
            st.session_state.rehab_detail_page = None
            st.rerun()
