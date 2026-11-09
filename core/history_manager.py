# =========================================================
# CORE/HISTORY_MANAGER.PY - QUẢN LÝ LỊCH SỬ KHÁM
# =========================================================
import json
from datetime import datetime
from core.database import DatabaseManager

class HistoryManager(DatabaseManager):
    def __init__(self, db_path=None):
        super().__init__(db_path)

    def save_visit(self, phone, visit_data):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 1. Thêm hoặc cập nhật thông tin hành chính bệnh nhân
            cursor.execute("SELECT phone FROM patients WHERE phone = ?", (phone,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO patients (phone, name, age, job, created_at) VALUES (?, ?, ?, ?, ?)",
                    (phone, visit_data.get("patient_name", "N/A"), visit_data.get("patient_age", 1990), visit_data.get("patient_job", "N/A"), now_str)
                )

            # 2. Lưu bản ghi lượt khám riêng biệt
            clinical_json = json.dumps(visit_data, ensure_ascii=False)
            cursor.execute(
                "INSERT INTO visits (phone, visit_date, region, summary, clinical_data) VALUES (?, ?, ?, ?, ?)",
                (phone, now_str, visit_data.get("region", "Chung"), visit_data.get("summary", ""), clinical_json)
            )
            conn.commit()

    def get_patient_history(self, phone):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.*, p.name as patient_name, p.age as patient_age, p.job as patient_job 
                FROM visits v 
                JOIN patients p ON v.phone = p.phone 
                WHERE v.phone = ? 
                ORDER BY v.visit_date DESC
            """, (phone,))
            rows = cursor.fetchall()
            result = []
            for row in rows:
                item = dict(row)
                if item.get("clinical_data"):
                    try:
                        item["parsed_details"] = json.loads(item["clinical_data"])
                    except Exception:
                        item["parsed_details"] = {}
                result.append(item)
            return result
