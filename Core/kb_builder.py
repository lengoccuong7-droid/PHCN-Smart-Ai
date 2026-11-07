# Core/kb_builder.py

CLINICAL_KB = {
    "Khớp gối": {
        "Rách sụn chêm": {
            "symptoms": ["Đau khe khớp", "Kẹt khớp", "Khám đau khi gập xoay", "Hạn chế gấp duỗi gối"],
            "special_tests": [
                "McMurray Test (Hiệu nghiệm nhất: Tiếng kêu lách tách và đau dọc khe khớp khi xoay)",
                "Apley Compression Test (Đau tăng khi ép và xoay cẳng chân tư thế sấp)",
                "Thessaly Test tại 20 độ gối",
                "Joint Line Tenderness (Ấn đau trực tiếp khe khớp)"
            ]
        },
        "Tổn thương dây chằng chéo trước (ACL)": {
            "symptoms": ["Lỏng gối", "Sưng sau chấn thương", "Cảm giác bước hụt chân, gối xộc xệch"],
            "special_tests": [
                "Lachman Test (Hiệu nghiệm nhất: Độ nhạy cao nhất đánh giá dịch chuyển mâm chày)",
                "Anterior Drawer Test (Ngăn kéo trước dương tính)",
                "Pivot Shift Test (Đánh giá sự bán trật xoay)",
                "Lever Sign (MacIntosh test)"
            ]
        },
        "Viêm gân bánh chè (Jumper's Knee)": {
            "symptoms": ["Đau nhói cực dưới xương bánh chè", "Đau tăng khi bật nhảy hoặc leo cầu thang"],
            "special_tests": [
                "Palpation Test (Ấn đau khu trú cực dưới xương bánh chè)",
                "Single-leg Decline Squat Test (Hiệu nghiệm kích hoạt đau gân bánh chè)",
                "Baja / Zohlen Test"
            ]
        },
        "Hội chứng đau bánh chè đùi (Patellofemoral Pain Syndrome)": {
            "symptoms": ["Đau trước gối, tăng lên khi ngồi lâu (Movie sign), leo cầu thang bộ"],
            "special_tests": [
                "Clarke Test / Grinding test (Đau khi dồn lực ép xương bánh chè)",
                "Apprehension Test (Sợ hãi khi đẩy xương bánh chè ra ngoài)",
                "Patellar Tilt Test"
            ]
        }
    },
    "Khớp vai": {
        "Hội chứng chèn ép khoang dưới mỏm cùng vai (Impingement)": {
            "symptoms": ["Đau khi dạng vai từ 60-120 độ (Painful arc)", "Đau về đêm khi nằm nghiêng"],
            "special_tests": [
                "Neer Test (Hiệu nghiệm nhất: Đau nhói lúc nâng vai thụ động cưỡng bức)",
                "Hawkins-Kennedy Test (Xoay trong cưỡng bức cánh tay gây kẹt đau)",
                "Painful Arc Sign"
            ]
        },
        "Đứt chóp xoay (Rotator Cuff Tear)": {
            "symptoms": ["Yếu cơ khi dạng/xoay vai", "Triệu chứng 'giọt nước rơi' (Drop arm sign)"],
            "special_tests": [
                "Drop Arm Test (Hiệu nghiệm nhất: Hạ tay từ từ không giữ được)",
                "Empty Can Test / Jobe Test (Yếu khi kháng lực ngón cái chúc xuống)",
                "Patte Test (Đánh giá cơ dưới gai)"
            ]
        },
        "Viêm quanh khớp vai thể đông cứng (Frozen Shoulder / Adhesive Capsulitis)": {
            "symptoms": ["Hạn chế toàn bộ tầm vận động chủ động và thụ động (đặc biệt xoay ngoài và dạng)", "Đau nhức âm ỉ"],
            "special_tests": [
                "External Rotation ROM Measurement (Hiệu nghiệm nhất: Xoay ngoài bị giới hạn rõ rệt)",
                "Apley Scratch Test (Hạn chế với tay lên gáy hoặc qua lưng)"
            ]
        }
    },
    "Cột sống cổ": {
        "Thoát vị đĩa đệm cột sống cổ chèn ép rễ C5-C6 (Đau lan vai, mặt ngoài cánh tay - ngón cái)": {
            "symptoms": ["Đau mỏi vùng cổ gáy lan xuống vai, mặt ngoài cánh tay và cẳng tay đến ngón cái", "Giảm phản xạ gân cơ nhị đầu"],
            "special_tests": [
                "Spurling Test (Hiệu nghiệm nhất: Nghiêng đầu và ấn dọc trục gây đau lan xuống tay)",
                "Distraction Test (Kéo giãn cổ làm giảm triệu chứng đau rõ rệt)",
                "Bakody Sign (Dấu hiệu giảm đau khi gác tay lên đầu)"
            ]
        },
        "Thoát vị đĩa đệm cột sống cổ chèn ép rễ C7 (Đau lan xuống ngón giữa)": {
            "symptoms": ["Đau lan xuống mặt sau cánh tay, cẳng tay đến ngón giữa", "Yếu cơ tam đầu, giảm phản xạ gân cơ tam đầu"],
            "special_tests": [
                "Spurling Test",
                "Triceps Resistance Test (Yếu cơ duỗi khuỷu chống kháng lực)"
            ]
        },
        "Thoát vị đĩa đệm chèn ép rễ C8 (Đau lan ngón nhẫn và ngón út)": {
            "symptoms": ["Tê bì và đau lan xuống vùng cẳng tay trong, ngón nhẫn và ngón út", "Yếu cơ bàn tay, teo cơ ô mô cái/mô út"],
            "special_tests": [
                "Spurling Test",
                "Grip Strength Testing (Đo lực bóp tay giảm rõ rệt)"
            ]
        },
        "Hội chứng cổ - vai thuần túy (Cervical Myofascial Pain Syndrome)": {
            "symptoms": ["Cơ vùng cổ gáy căng cứng, xuất hiện điểm kích hoạt (Trigger points) lan tỏa", "Hạn chế quay cổ do đau cơ"],
            "special_tests": [
                "Palpation Trigger Points (Ấn điểm đau nhói lan truyền vùng cơ thang/cơ nâng vai)",
                "Cervical Active ROM Assessment"
            ]
        }
    },
    "Cột sống thắt lưng": {
        "Thoát vị đĩa đệm chèn ép rễ L3-L4 (Đau mặt trước đùi)": {
            "symptoms": ["Đau lan từ vùng thắt lưng xuống mặt trước đùi", "Giảm phản xạ gân xương bánh chè, teo cơ tứ đầu đùi"],
            "special_tests": [
                "Femoral Nerve Stretch Test (Hiệu nghiệm nhất: Căng dây thần kinh đùi ở tư thế nằm sấp gấp gối)"
            ]
        },
        "Thoát vị đĩa đệm chèn ép rễ L5 (Đau mặt trước ngoài cẳng chân & mu bàn chân)": {
            "symptoms": ["Đau lan từ thắt lưng xuống mông, mặt ngoài đùi, trước ngoài cẳng chân đến mu bàn chân và ngón cái", "Yếu cơ gấp bàn chân lên"],
            "special_tests": [
                "Straight Leg Raising / SLR Test (Hiệu nghiệm nhất: Đau lan chân ở góc < 60 độ)",
                "Heel Walking Test (Test đi bằng gót chân)"
            ]
        },
        "Thoát vị đĩa đệm chèn ép rễ S1 (Đau mặt sau đùi & cẳng chân - Sciatica)": {
            "symptoms": ["Đau lan từ mông xuống mặt sau đùi, mặt sau cẳng chân, gót chân và bờ ngoài bàn chân", "Giảm phản xạ gân gót"],
            "special_tests": [
                "Straight Leg Raising (SLR) Test dương tính kèm đau chói góc thấp",
                "Toe Walking Test (Hiệu nghiệm nhất: Test nhón gót chân phát hiện yếu rễ S1)",
                "Achilles Reflex Testing"
            ]
        },
        "Hẹp ống sống thắt lưng (Lumbar Spinal Stenosis)": {
            "symptoms": ["Đau cách hồi thần kinh (đi lại một đoạn phải dừng lại ngồi nghỉ)", "Giảm đau khi cúi người về trước"],
            "special_tests": [
                "Bicycle Test van Gelderen (Hiệu nghiệm nhất: Đạp xe không gây đau giống đi bộ)",
                "Lumbar Extension Test (Ngả sau làm tăng triệu chứng tê mỏi)"
            ]
        },
        "Đau khớp cùng chậu (Sacroiliac Joint Dysfunction)": {
            "symptoms": ["Đau sâu vùng mông, tăng khi đứng dồn lực một chân hoặc khi ngồi lâu"],
            "special_tests": [
                "FABER Test / Patrick Test (Hiệu nghiệm sàng lọc khớp cùng chậu)",
                "Gaenslen Test",
                "Thigh Thrust Test"
            ]
        }
    },
    "Cổ chân & Bàn chân": {
        "Viêm cân gan chân & Gai xương gót (Plantar Fasciitis & Calcaneal Spur)": {
            "symptoms": ["Đau nhói gót chân khi bước chân xuống giường vào buổi sáng hoặc sau khi nghỉ ngơi", "Đau giảm dần khi đi lại một vài bước"],
            "special_tests": [
                "Windlass Test (Hiệu nghiệm nhất: Đau tăng khi duỗi thụ động các ngón chân)",
                "Palpation Test (Ấn đau chói điểm bám cân gan chân tại củ xương gót)",
                "Hubbard's Test"
            ]
        },
        "Bong gân cổ chân (Mắt cá ngoài)": {
            "symptoms": ["Sưng nề vùng mắt cá ngoài sau chấn thương lật miết chân", "Đau khi vận động"],
            "special_tests": [
                "Anterior Drawer Test cổ chân (Đánh giá độ vững trước)",
                "Talar Tilt Test (Hiệu nghiệm đánh giá dây chằng sên mác)"
            ]
        }
    },
    "Khớp háng": {
        "Hoại tử chỏm xương đùi (Avascular Necrosis - AVN)": {
            "symptoms": ["Đau sâu vùng bẹn, mông hoặc lan xuống đùi, đau tăng khi chịu lực (đứng/đi), hạn chế xoay trong khớp háng"],
            "special_tests": [
                "FABER Test / Patrick Test (Hiệu nghiệm sàng lọc: Đau bẹn khi khớp háng gập - dạng - xoay ngoài)",
                "FADIR Test (Đau khi gập - khép - xoay trong)",
                "Scour Test (Đau và lạo xạo khi ép xoay chỏm háng)"
            ]
        },
        "Hội chứng cấn mỏm ổ cối - đùi (FAI)": {
            "symptoms": ["Đau vùng bẹn khi ngồi xổm, gập háng sâu hoặc xoay trong", "Cảm giác kẹt khớp"],
            "special_tests": [
                "FADIR Test (Hiệu nghiệm nhất: Flexion, Adduction, Internal Rotation gây đau bẹn)",
                "FABER Test (Patrick Test)"
            ]
        },
        "Thoái hóa khớp háng (Osteoarthritis of Hip)": {
            "symptoms": ["Hạn chế xoay trong khớp háng", "Đau lan xuống mặt trước đùi gối"],
            "special_tests": [
                "Scour Test (Impingement/Clearance test)",
                "Trendelenburg Sign (Yếu cơ mông nhỡ khi đứng trụ một chân)"
            ]
        }
    },
    "Khuỷu tay & Cổ tay": {
        "Viêm mỏm trên lồi cầu ngoài xương cánh tay (Tennis Elbow)": {
            "symptoms": ["Đau nhói mặt ngoài khuỷu, lan xuống cẳng tay khi cầm nắm, vặn nắm cửa"],
            "special_tests": [
                "Cozen Test (Hiệu nghiệm nhất: Đau nhói khi duỗi cổ tay chống kháng lực)",
                "Mill Test (Đau khi căng duỗi cổ tay tối đa)"
            ]
        },
        "Hội chứng ống cổ tay (Carpal Tunnel Syndrome)": {
            "symptoms": ["Tê ngón cái, ngón trỏ, ngón giữa và nửa ngoài ngón nhẫn, đau tăng về đêm"],
            "special_tests": [
                "Phalen Test (Hiệu nghiệm nhất: Gập tối đa hai cổ tay chạm nhau gây tê sau 60 giây)",
                "Tinel Sign (Gõ vào ống cổ tay gây cảm giác điện giật lan ngón)"
            ]
        }
    },
    "Phục hồi chức năng Thần kinh": {
        "Liệt nửa người sau tai biến mạch máu não (Stroke Hemiplegia)": {
            "symptoms": ["Giảm hoặc mất cơ lực bên liệt, tăng trương lực cơ (co cứng)", "Rối loạn thăng bằng, dáng đi lệch"],
            "special_tests": [
                "Brunnstrom Stages of Recovery (Hiệu nghiệm nhất: Đánh giá giai đoạn phục hồi vận động I-VI)",
                "Berg Balance Scale (Đánh giá thăng bằng)",
                "Modified Ashworth Scale (Đánh giá co cứng)"
            ]
        }
    },
    "Tiền đình & Thăng bằng": {
        "Chóng mặt tư thế kịch phát lành tính (BPPV)": {
            "symptoms": ["Chóng mặt quay cuồng ngắn khi thay đổi tư thế đầu (lăn giường, ngẩng đầu)"],
            "special_tests": [
                "Dix-Hallpike Test (Hiệu nghiệm nhất: Kích thích tìm nấc rung giật nhãn cầu - Nystagmus)",
                "Roll Test (Đánh giá ống bán khuyên ngang)"
            ]
        }
    }
}

def get_comprehensive_kb():
    """Trả về toàn bộ cơ sở kiến thức phục hồi chức năng & vật lý trị liệu."""
    return CLINICAL_KB

