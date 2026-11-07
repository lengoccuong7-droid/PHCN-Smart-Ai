import re
import json
from Core.kb_builder import get_comprehensive_kb

class SuperClinicalEngine:
    def __init__(self):
        self.symptom_mapping = {
            "dau_co": ["đau cổ", "mỏi cổ", "nhức cổ", "cứng cổ", "vẹo cổ"],
            "dau_that_lung": ["đau lưng", "đau thắt lưng", "mỏi lưng", "cứng lưng"],
            "dau_vai": ["đau vai", "nhức vai", "mỏi vai", "kẹt vai"],
            "te_ban_tay": ["tê tay", "tê bàn tay", "tê các ngón tay", "tê bì"],
            "dau_khop": ["đau", "nhức", "buốt", "mỏi", "đau gối", "nhức khớp"],
            "sung_ne": ["sưng", "phù", "to lên", "tràn dịch", "sưng nóng"],
            "cung_khop": ["cứng khớp", "cứng đơ", "khó cử động", "sượng"],
            "tieng_luc_cuc": ["lục cục", "lạo xạo", "rắc rắc", "kẹt khớp"],
            "long_goi": ["lỏng gối", "sụp gối", "không vững"],
            "sot": ["sốt", "sốt cao", "sốt nhẹ", "ớn lạnh"],
            "sut_can": ["sụt cân", "gầy sút"]
        }
        self.negation_keywords = ["không", "chưa", "hết", "chẳng", "không bị", "không có", "âm tính"]
        self.kb = get_comprehensive_kb()

    def generate_box_copy(self, form_data: dict) -> str:
        return f"""[VÙNG KHÁM CHUYÊN KHOA]: {form_data.get('selected_zone', 'Chung')}
[LÝ DO VÀO VIỆN]: {form_data.get('ly_do_vao_vien', '')}
[TIỀN SỬ BỆNH]: {form_data.get('tien_su', '')}
[BỆNH SỬ (SOCRATES)]:
  - Khởi phát (Onset): {form_data.get('socrates_onset', '')}
  - Vị trí (Site): {form_data.get('socrates_site', '')}
  - Tính chất đau (Character): {form_data.get('socrates_character', '')}
  - Diễn biến (Progression): {form_data.get('socrates_progression', '')}
  - Yếu tố tăng/giảm (Factors): {form_data.get('socrates_factors', '')}
  - Ảnh hưởng sinh hoạt (Severity): {form_data.get('socrates_severity', '')}
[CỜ ĐỎ AN TOÀN (RED FLAGS)]: {form_data.get('red_flags', '')}
[KHÁM THỰC THỂ (NHÌN - SỜ - GÕ)]:
  - Nhìn: {form_data.get('lam_sang_nhin', '')}
  - Sờ: {form_data.get('lam_sang_so', '')}
  - Gõ: {form_data.get('lam_sang_go', '')}
[TEST ĐẶC HIỆU CHÍNH]:
  - Test 1 (Lachman): {form_data.get('test_1', '')}
  - Test 2 (McMurray): {form_data.get('test_2', '')}
  - Test 3 (Apley): {form_data.get('test_3', '')}
[CẬN LÂM SÀNG]: {form_data.get('image_notes', 'Đã đính kèm')}"""

    def parse_and_analyze(self, box_copy_content: str) -> dict:
        text_lower = box_copy_content.lower()
        extracted_symptoms, negated_symptoms = [], []

        for token, keywords in self.symptom_mapping.items():
            for kw in keywords:
                for match in re.finditer(re.escape(kw), text_lower):
                    idx = match.start()
                    pre_text = text_lower[max(0, idx - 20):idx]
                    is_negated = any(neg in pre_text for neg in self.negation_keywords)
                    if is_negated:
                        if token not in negated_symptoms: negated_symptoms.append(token)
                    else:
                        if token not in extracted_symptoms: extracted_symptoms.append(token)

        for neg in negated_symptoms:
            if neg in extracted_symptoms: extracted_symptoms.remove(neg)

        matched_results = []
        for code, cond in self.kb.items():
            reqs = cond.get("required_symptoms", [])
            match_count = sum(1 for req in reqs if req in extracted_symptoms)
            if match_count > 0:
                score = int((match_count / len(reqs)) * 100) if len(reqs) > 0 else 50
                matched_results.append({
                    "code": cond["code"], "name": cond["name"], "category": cond["category"],
                    "confidence": f"{min(score, 95)}%", "tests": cond.get("tests", []), "rehab_focus": cond["rehab_focus"]
                })

        matched_results.sort(key=lambda x: int(x["confidence"].replace("%", "")), reverse=True)

        if not matched_results:
            primary_diag = "Nghi ngờ Quá tải cơ học / Chưa rõ thể bệnh cụ thể"
            confidence = "60%"
            rehab_focus = "Nghỉ ngơi tương đối, theo dõi diễn tiến lâm sàng, tập vận động nhẹ nhàng."
            tests_suggested = ["Cần thăm khám bổ sung chuyên sâu"]
        else:
            top = matched_results[0]
            primary_diag = f"[{top['code']}] {top['name']}"
            confidence = top["confidence"]
            rehab_focus = top["rehab_focus"]
            tests_suggested = top["tests"]

        ai_copy_output = f"""[CHẨN ĐOÁN LÂM SÀNG & PHỤC HỒI CHỨC NĂNG AI]:
- Chẩn đoán ưu tiên: {primary_diag} (Độ tin cậy: {confidence})
- Nghiệm pháp gợi ý: {", ".join(tests_suggested)}
- ĐỊNH HƯỚNG PHỤC HỒI CHỨC NĂNG (BS CK2): {rehab_focus}"""

        return {
            "primary_diagnosis": primary_diag,
            "confidence": confidence,
            "ai_copy_output": ai_copy_output
        }
