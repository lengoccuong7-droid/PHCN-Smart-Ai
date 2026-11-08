# =========================================================
# HISTORY MANAGER: QUẢN LÝ LỊCH SỬ BỆNH ÁN (AN TOÀN TRÊN CLOUD)
# =========================================================
import os
import json

class HistoryManager:
    def __init__(self, history_file="patient_history.json"):
        if os.path.exists("/mount/src") or os.environ.get("STREAMLIT_SHARING_MODE"):
            self.history_file = os.path.join("/tmp", history_file)
        else:
            self.history_file = os.path.abspath(history_file)
        self.ensure_file()

    def ensure_file(self):
        try:
            if not os.path.exists(self.history_file) or os.path.getsize(self.history_file) == 0:
                with open(self.history_file, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Lỗi khởi tạo tệp lịch sử: {e}")

    def get_all_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return []

    def get_patient_history(self, phone):
        all_data = self.get_all_history()
        patient_records = [item for item in all_data if item.get("patient_phone") == phone]
        return patient_records

    def save_visit(self, phone, visit_data):
        try:
            all_data = self.get_all_history()
            from datetime import datetime
            visit_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            all_data.insert(0, visit_data)
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(all_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Lỗi lưu lịch sử: {e}")
