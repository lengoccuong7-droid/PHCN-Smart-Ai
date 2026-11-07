def get_comprehensive_kb():
    return {
        "CERV001": {
            "code": "CERV001", "name": "Thoái hóa cột sống cổ", "category": "Cột sống cổ",
            "required_symptoms": ["dau_co", "cung_co"], "tests": ["Spurling Test (-)", "Distraction Test (+)"],
            "rehab_focus": "Kéo giãn cột sống cổ tư thế trung tính, tập cơ sâu vùng cổ (Deep neck flexors), nhiệt trị liệu."
        },
        "LUMB001": {
            "code": "LUMB001", "name": "Thoái hóa cột sống thắt lưng", "category": "Cột sống thắt lưng",
            "required_symptoms": ["dau_that_lung", "cung_lung"], "tests": ["SLR Test (-)", "Scoliosis Screen (-)"],
            "rehab_focus": "Tập cơ lõi (Core stability), bài tập Cat-Camel, duy trì đường cong sinh lý thắt lưng."
        },
        "SHOULDER001": {
            "code": "SHOULDER001", "name": "Viêm gân cơ trên gai", "category": "Khớp vai",
            "required_symptoms": ["dau_vai", "dau_khi_dang_tay"], "tests": ["Empty Can Test (+)", "Neer Impingement Test (+)"],
            "rehab_focus": "Tập mạnh cơ chóp xoay, bài tập Codman đung đưa vai, chườm lạnh sau tập."
        },
        "ELBOW001": {
            "code": "ELBOW001", "name": "Viêm điểm bám gân duỗi ngoài (Tennis Elbow)", "category": "Khớp khuỷu",
            "required_symptoms": ["dau_khuyu", "dau_lon_cau_ngoai"], "tests": ["Cozen Test (+)", "Mill Test (+)"],
            "rehab_focus": "Bài tập lệch tâm (Eccentric exercise) gân duỗi, nẹp hỗ trợ, siêu âm trị liệu."
        },
        "WRIST001": {
            "code": "WRIST001", "name": "Hội chứng ống cổ tay", "category": "Cổ tay - Bàn tay",
            "required_symptoms": ["te_ban_tay", "te_ngon_1_2_3"], "tests": ["Phalen Test (+)", "Tinel Sign (+)"],
            "rehab_focus": "Nẹp cổ tay tư thế trung tính ban đêm, bài tập trượt thần kinh giữa (Median nerve gliding)."
        },
        "HIP001": {
            "code": "HIP001", "name": "Thoái hóa khớp háng", "category": "Khớp hông",
            "required_symptoms": ["dau_hong", "dau_ben"], "tests": ["Patrick/FABER Test (+)", "Scour Test (+)"],
            "rehab_focus": "Tập vận động không chịu lực, tập mạnh cơ mông nhỡ, giảm tải trọng khớp háng."
        },
        "KNEE001": {
            "code": "KNEE001", "name": "Thoái hóa khớp gối", "category": "Khớp gối",
            "required_symptoms": ["dau_khop", "tieng_luc_cuc"], "tests": ["Patellar Grind Test (+)", "Crepitus (+)"],
            "rehab_focus": "Tập mạnh cơ tứ đầu đùi, tập biên độ gập duỗi không chịu lực, chườm ấm."
        },
        "ANKLE001": {
            "code": "ANKLE001", "name": "Bong gân cổ chân ngoài", "category": "Cổ chân - Bàn chân",
            "required_symptoms": ["dau_co_chan", "sung_co_chan"], "tests": ["Anterior Drawer Ankle (+)", "Talar Tilt (+)"],
            "rehab_focus": "Phác đồ RICE, tập thăng bằng trên 1 chân, nẹp cổ chân bảo vệ."
        },
        "RED001": {
            "code": "RED001", "name": "CỜ ĐỎ: Nghi ngờ Nhiễm trùng / Ung thư / Tổn thương thần kinh nặng", "category": "Cờ đỏ an toàn",
            "required_symptoms": ["sot", "sut_can_khong_ro_nguyen_nhan", "dau_ve_dem_du_doi"], "tests": ["MRI cấp cứu", "Xét nghiệm máu toàn diện"],
            "rehab_focus": "CHUYỂN KHOA CẤP CỨU / NGOẠI THẦN KINH NGAY. KHÔNG TẬP PHCN."
        }
    }
