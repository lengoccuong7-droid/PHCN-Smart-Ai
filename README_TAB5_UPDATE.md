# PHCN AI 2.2 – Tab 5 nhập dữ liệu thô

Bản này được ghép trực tiếp trên cấu trúc PHCN AI 2.1 đã cung cấp.

## Những phần được giữ nguyên
- `modules/tab1_hoso.py` đến `modules/tab4_phcn.py`.
- `modules/tab6_theo_doi.py`.
- `core/`, `database/`, cấu trúc SQLite và các tệp tri thức JSON.
- Cách gọi các tab bằng hàm `render()` và cách khởi tạo `init_db()`.
- CSS và điều hướng Sidebar; chỉ đổi nhãn/đích Tab 5.

## Phần thay đổi
- Bỏ import và điều hướng tới `modules.tab5_doi_soat` trong `app.py`.
- Thêm `modules/tab5_nhap_lieu.py` và điều hướng Tab 5 tới hàm `render()` của module này.
- Bổ sung `pandas`, `openpyxl`, `xlrd` trong `requirements.txt`.
- Tab 5 có vùng dán văn bản, tải TXT/CSV/TSV/XLS/XLSX, tách bảng, chỉnh sửa ô, thêm/xóa dòng, thêm/xóa/đổi tên cột, lưu/ghi đè có sao lưu, xuất CSV/Excel.

## Chạy
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dữ liệu
- Tab 5 lưu tệp riêng tại `data/tab5_workspace/`.
- Không đọc/ghi hồ sơ, dữ liệu khám hoặc SQLite của các tab lâm sàng.
- Không xóa thư mục `data/` cũ. Sao lưu thư mục này trước khi triển khai.
- Ghi đè chỉ áp dụng với tệp đã lưu trong kho riêng của ứng dụng; trình duyệt không thể ghi trực tiếp lên tệp gốc trong iPhone/máy tính.

## Kiểm định
Đã kiểm tra cú pháp Python và đối chiếu import/hàm `render()` của các module với app 2.1. Môi trường đóng gói hiện tại không có Streamlit/Pandas nên chưa chạy được kiểm thử giao diện Streamlit thực tế tại đây. Cần cài `requirements.txt` và chạy thử trên môi trường triển khai trước khi dùng dữ liệu thật.
