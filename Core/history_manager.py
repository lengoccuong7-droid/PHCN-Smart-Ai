# Core/history_manager.py
import os
import json
import datetime

class HistoryManager:
    def __init__(self, history_file="patient_history.json"):
        self.history_file = os.path.abspath(history_file)
        if not os.path.exists(self.history_file):
            try:
                with open(self.history_file, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
            except Exception:
                pass

    def get_patient_history(self, phone):
        if not phone:
            return []
        try:
            if not os.path.exists(self.history_file):
                return []
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
            return [v for v in history if v.get("patient_phone") == phone]
        except Exception:
            return []

    def save_visit(self, phone, visit_data):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            else:
                history = []
        except Exception:
            history = []

        visit_data["date"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        history.append(visit_data)

        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
        except Exception:
            pass
