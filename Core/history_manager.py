# Core/history_manager.py
import os
import json

class HistoryManager:
    def __init__(self, history_file="patient_history.json"):
        # Đảm bảo tệp lưu trữ lịch sử luôn nằm ở thư mục gốc để tránh lỗi đường dẫn
        self.history_file = os.path.abspath(history_file)
        self.ensure_file()

    def ensure_file(self):
        """Đảm bảo tệp lưu trữ lịch sử luôn tồn tại ở thư mục gốc."""
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def get_patient_history(self, phone):
        """Lấy lịch sử khám của bệnh nhân dựa theo số điện thoại."""
        if not phone:
            return []
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
            # Lọc các lần khám theo số điện thoại
            patient_visits = [v for v in history if v.get("patient_phone") == phone]
            return patient_visits
        except Exception:
            return []

    def save_visit(self, phone, visit_data):
        """Lưu một lượt khám mới vào tệp JSON hệ thống."""
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []

        import datetime
        visit_data["date"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        history.append(visit_data)

        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
