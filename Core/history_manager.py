# Core/history_manager.py
import os
import json
from datetime import datetime

class HistoryManager:
    def __init__(self, history_file="patient_history.json"):
        self.history_file = history_file
        self.ensure_file()

    def ensure_file(self):
        """Đảm bảo tệp lưu trữ lịch sử luôn tồn tại ở thư mục gốc."""
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    def get_patient_history(self, phone):
        """Lấy toàn bộ lịch sử khám của bệnh nhân theo số điện thoại."""
        self.ensure_file()
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(phone, [])
        except Exception:
            return []

    def save_visit(self, phone, visit_data):
        """Lưu ca khám mới vào lịch sử tái khám của bệnh nhân."""
        self.ensure_file()
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}

        if phone not in data:
            data[phone] = []

        visit_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data[phone].append(visit_data)

        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
