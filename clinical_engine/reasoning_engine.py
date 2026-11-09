# =========================================================
# CLINICAL_ENGINE/REASONING_ENGINE.PY - BỘ MÁY SUY LUẬN LÂM SÀNG
# =========================================================

class ClinicalReasoningEngine:
    @staticmethod
    def analyze_case(data):
        region = data.get("region", "Chung")
        nrs = data.get("nrs", 0)
        symptoms_subjective = data.get("character", "")
        inspect_objective = data.get("inspect", "")
        rom_objective = data.get("rom", "")
        test_results = data.get("test_results", {})
        red_flags = data.get("red_flags", [])

        # 1. Phân tích Cờ đỏ an toàn (Tầng 5)
        safety_warnings = []
        if red_flags:
            safety_warnings.append(f"🚩 PHÁT HIỆN DẤU HIỆU CỜ ĐỎ: {', '.join(red_flags)}. Cần đánh giá y tế cấp thiết!")

        # 2. Đánh giá bằng chứng ủng hộ và bằng chứng chưa phù hợp
        supporting_evidence = []
        unmatched_evidence = []
        missing_data = []

        pos_tests = [k for k, v in test_results.items() if "Dương tính" in v]
        untested = [k for k, v in test_results.items() if "Chưa làm" in v]

        if pos_tests:
            supporting_evidence.append(f"Nghiệm pháp đặc hiệu dương tính (+): {', '.join(pos_tests)}")
        else:
            unmatched_evidence.append("Chưa ghi nhận nghiệm pháp đặc hiệu dương tính (+).")

        if symptoms_subjective:
            supporting_evidence.append(f"Triệu chứng cơ năng (Bệnh nhân kể): {symptoms_subjective}")
        else:
            missing_data.append("Chưa khai thác chi tiết tính chất đau cơ năng.")

        if inspect_objective or rom_objective:
            supporting_evidence.append("Có ghi nhận dấu hiệu thực thể khách quan qua khám Nhìn/Sờ/Đo.")
        else:
            missing_data.append("Thiếu dữ liệu khám thực thể tầm vận động (ROM) và trương lực cơ.")

        if untested:
            missing_data.append(f"Các test chưa thực hiện (không tự ý coi là âm tính): {', '.join(untested)}")

        # 3. Tổng hợp chẩn đoán sơ bộ & Định hướng PHCN
        diagnosis_impression = f"Hội chứng đau / Tổn thương cấu trúc thuộc vùng {region} (Mức đau NRS: {nrs}/10)"
        
        rehab_orientation = [
            "Mục tiêu ngắn hạn: Giảm đau, kiểm soát viêm, duy trì tầm vận động sinh lý.",
            "Mục tiêu dài hạn: Tái huấn luyện chức năng vận động, tăng cường sức mạnh cơ sinh cơ học.",
            "Phương pháp can thiệp: Kéo giãn cơ co cứng, bài tập chủ động có kháng lực tăng dần."
        ]

        return {
            "safety_warnings": safety_warnings,
            "supporting_evidence": supporting_evidence,
            "unmatched_evidence": unmatched_evidence,
            "missing_data": missing_data,
            "diagnosis_impression": diagnosis_impression,
            "rehab_orientation": rehab_orientation,
            "confidence_level": "Trung bình - Cao" if pos_tests else "Cần bổ sung dữ liệu"
        }
