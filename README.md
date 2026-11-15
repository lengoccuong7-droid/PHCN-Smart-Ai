# PHCN AI 2.3 – Bản cập nhật từ PHCN AI 2.1/2.2

## Chức năng
- Giữ kiến trúc 6 phân hệ và SQLite hiện có.
- Tab 1: Hồ sơ bệnh nhân và lịch sử các lần ghi nhận/khám.
- Tab 2: Cẩm nang tri thức.
- Tab 3: có hai chế độ độc lập: **Khám lâm sàng** và **Ghi nhận PHCN (không cần khám)**.
- Chế độ ghi nhận PHCN lưu tình trạng hiện tại, huyết áp, mạch, tiền sử, bài tập, liều lượng/cách thực hiện, đáp ứng sau tập và ghi chú KTV.
- Tab 4: 63 bài tập trong 9 nhóm, mỗi bài có mục tiêu, tư thế chuẩn bị, kỹ thuật, liều lượng tham khảo và lưu ý an toàn.
- Tab 5: nhập và xử lý dữ liệu thô độc lập.
- Tab 6: theo dõi tiến triển và lịch sử.

## Cài đặt và chạy
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Cập nhật từ bản cũ
1. Sao lưu toàn bộ thư mục `data/` của bản đang sử dụng.
2. Giải nén PHCN AI 2.3.
3. Nếu đã có dữ liệu, chép nguyên tệp `data/phcn_ai.db` cũ vào thư mục `data/` của bản mới.
4. Cài thư viện theo `requirements.txt`, sau đó chạy `streamlit run app.py`.

Không xóa hoặc thay thế tệp SQLite cũ. Bản 2.3 giữ các bảng `patients` và `visits`; hồ sơ PHCN độc lập được lưu dưới dạng một lần ghi nhận với vùng `PHCN – Ghi nhận điều trị (không khám)` để xem lại trong lịch sử.

## Lưu ý lâm sàng
- Nội dung bài tập là hướng dẫn tham khảo, không phải phác đồ áp dụng tự động cho mọi người bệnh.
- Sau phẫu thuật, gãy xương, thay khớp, rối loạn nuốt hoặc khi chưa rõ mức chịu lực, phải tuân thủ chỉ định của bác sĩ điều trị và lượng giá trực tiếp.
- Liều lượng cần cá thể hóa theo giai đoạn, bệnh nền, mức đau, đáp ứng và chất lượng vận động.
- Nghiệm pháp có ba trạng thái riêng: `Chưa thực hiện`, `Âm tính`, `Dương tính`. Dữ liệu cũ gộp `Chưa làm / Âm tính` được xử lý thận trọng như chưa xác định.
- Engine offline là hệ luật hỗ trợ tổng hợp, chưa được thẩm định lâm sàng; không thay thế bác sĩ hoặc KTV đánh giá trực tiếp.

## Kiểm thử
Các kiểm tra cú pháp và kiểm thử tự động của bộ mã đã chạy thành công trong môi trường đóng gói. Giao diện Streamlit cần được chạy thử trên thiết bị/môi trường cài đặt thực tế trước khi sử dụng.


## PHCN AI 2.4 – Kho bài tập nâng cấp
- 5 phân hệ: Hồ sơ & Lịch sử; Cẩm nang Tri thức; Khám Lâm sàng/Ghi nhận PHCN; Kho bài tập PHCN; Theo dõi tiến triển.
- Tab nhập dữ liệu thô độc lập đã được gỡ khỏi điều hướng và mã nguồn.
- Kho bài tập: 9 nhóm chức năng × 7 bài × 5 biến thể = 315 biến thể. Có bộ lọc bệnh lý và thư viện chuyên biệt cũ.
- Sao lưu thư mục `data/` và cơ sở dữ liệu SQLite trước khi nâng cấp. Không ghi đè/xóa dữ liệu bệnh nhân.
- Nội dung bài tập là tài liệu tham khảo; cần cá thể hóa theo lượng giá, chẩn đoán, giai đoạn, chỉ định và giới hạn của bác sĩ điều trị.
