import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, history_file="core/patient_history.json"):
        self.history_file = history_file
        self.ensure_file()

    def ensure_file(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save_record(self, record_data: dict):
        records = self.load_records()
        record_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        records.insert(0, record_data)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    def load_records(self):
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
