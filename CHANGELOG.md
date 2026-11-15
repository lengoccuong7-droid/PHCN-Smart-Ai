# CHANGELOG 2.1
- Module hóa Tab 1–5 theo cấu trúc package, giữ mã giao diện của bản 2.0.
- Tách `clinical_engine`, `diagnostic_audit`, `storage` vào `core/` và `database/`.
- Bổ sung API đọc chi tiết lần khám và truy vấn chuỗi lần khám.
- Bổ sung Tab 6 theo dõi tiến triển từ lịch sử đã lưu.
- Không tự chuyển “chưa làm” thành “âm tính”; không tự tính phần trăm tiến triển khi thiếu thang đo lặp lại.


## Cập nhật giao diện theo yêu cầu
- Tờ giấy trắng tổng hợp dữ kiện được đồng bộ lại mỗi lần nhập/sửa trường dữ liệu trong Tab 3.
- Tab 3 hiển thị thông tin hành chính gọn: Họ tên, Năm sinh và Nghề nghiệp; không bắt buộc số điện thoại để lưu lần khám.
- Số điện thoại nếu có từ hồ sơ Tab 1 vẫn được giữ; nếu không có, hệ thống tạo mã nội bộ không hiển thị cho người dùng để liên kết lịch sử.
- Chuyển điều hướng 6 chức năng sang Sidebar, luôn sẵn để chuyển tab nhanh khi cuộn trang.
- Tab 6 tra cứu theo mã hồ sơ nội bộ, nên theo dõi được cả bệnh nhân không cung cấp số điện thoại.


## PHCN AI 2.3 – Bổ sung ghi nhận PHCN và hướng dẫn bài tập
- Tab 3 có chế độ Ghi nhận PHCN độc lập, không cần chạy khám lâm sàng.
- Hồ sơ ghi tình trạng hiện tại, huyết áp, mạch, tiền sử, bài tập đã thực hiện, liều lượng, đáp ứng và ghi chú KTV.
- Tab 4 hiển thị mục tiêu, tư thế, kỹ thuật, liều lượng tham khảo và lưu ý an toàn cho từng bài tập.
- Các nghiệm pháp chưa thực hiện được phân biệt với kết quả âm tính.


## PHCN AI 2.4
- Loại bỏ Tab nhập dữ liệu thô; ứng dụng còn 5 phân hệ điều hướng.
- Nâng cấp Kho bài tập thành 9 nhóm chức năng, 7 bài/nhóm, 5 biến thể/bài (63 bài, 315 biến thể).
- Mỗi biến thể có dụng cụ, công dụng, kỹ thuật, mức độ, liều lượng tham khảo và lưu ý an toàn.
- Thêm bộ lọc bệnh lý và liên kết bệnh lý với nhóm bài tập phù hợp.
- Giữ thư viện bài tập chuyên biệt cũ để không mất nội dung về nuốt, ngôn ngữ, âm ngữ trị liệu, trẻ em và các tình trạng đặc thù.
