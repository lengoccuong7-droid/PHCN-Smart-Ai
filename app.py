# =========================================================
# APP.PY - PHCN AI 1.8 (GỘP TOÀN BỘ TRONG 1 TỆP DUY NHẤT)
# =========================================================
import streamlit as st

st.set_page_config(
    page_title="PHCN AI 1.8",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CHUNG CHO GIAO DIỆN GRID-TO-SCROLL ---
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 10px !important;
    }
    @media (min-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            grid-template-columns: repeat(4, 1fr) !important;
        }
    }
    .grid-card-box {
        background: #ffffff;
        border-radius: 16px;
        padding: 14px 8px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #eaeaea;
    }
    .icon-circle-btn {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin: 0 auto 8px auto;
        color: white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("🩺 PHCN AI 1.8 – Trợ lý Phục hồi Chức năng & Lâm sàng")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Hồ sơ & Lịch sử", 
        "📚 Cẩm nang Tri thức", 
        "🩺 Khám Lâm sàng", 
        "🏋️‍♂️ Kho Bài tập PHCN"
    ])

    # ================= TAB 1: HỒ SƠ =================
    with tab1:
        st.subheader("👤 Quản lý Hồ sơ Bệnh nhân & Lịch sử Khám")
        st.info("Sử dụng trình quản lý lịch sử để tra cứu và lưu trữ bệnh án.")

    # ================= TAB 2: CẨM NANG TRI THỨC =================
    with tab2:
        if "knowledge_active_cat" not in st.session_state:
            st.session_state.knowledge_active_cat = None

        if st.session_state.knowledge_active_cat is None:
            st.markdown("### 📚 Cẩm Nang Tri Thức Y Chứng")
            st.caption("Chọn chuyên khoa để tra cứu phác đồ và tài liệu lâm sàng:")
            
            categories = [
                {"id": "stroke", "name": "Đột quỵ & Thần kinh", "icon": "🧠", "color": "linear-gradient(135deg, #48dbfb, #0abde3)"},
                {"id": "spine", "name": "Cột sống & Cơ xương", "icon": "🦴", "color": "linear-gradient(135deg, #ff6b6b, #ee5253)"},
                {"id": "joint", "name": "Khớp ngoại biên", "icon": "🦾", "color": "linear-gradient(135deg, #10ac84, #1dd1a1)"},
                {"id": "pediatric", "name": "PHCN Nhi khoa", "icon": "👶", "color": "linear-gradient(135deg, #f39c12, #e67e22)"}
            ]

            cols = st.columns(len(categories))
            for idx, cat in enumerate(categories):
                with cols[idx]:
                    st.markdown(f"""
                        <div class="grid-card-box">
                            <div class="icon-circle-btn" style="background: {cat['color']};">
                                {cat['icon']}
                            </div>
                            <div style="font-weight: 700; font-size: 13px; color: #1f2937;">{cat['name']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Xem", key=f"fast_cat_{cat['id']}", use_container_width=True):
                        st.session_state.knowledge_active_cat = cat['name']
                        st.rerun()
        else:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"#### 📖 Chuyên khoa: `{st.session_state.knowledge_active_cat}`")
            with c2:
                if st.button("⬅ Quay lại", use_container_width=True):
                    st.session_state.knowledge_active_cat = None
                    st.rerun()

            st.markdown("---")
            with st.container(border=True):
                st.markdown("##### 📄 Nguyên tắc Vận động Trị liệu Y học Chứng cứ")
                st.markdown("""
                * **Mục tiêu:** Phòng ngừa co rút biến dạng, gia tăng khả năng độc lập sinh hoạt tối đa cho người bệnh.
                * **Nguyên tắc cốt lõi:** Bắt đầu càng sớm càng tốt khi tình trạng toàn thân ổn định.
                """)

    # ================= TAB 3: KHÁM LÂM SÀNG =================
    with tab3:
        if "exam_active_region" not in st.session_state:
            st.session_state.exam_active_region = None

        if st.session_state.exam_active_region is None:
            st.markdown("### 🩺 Chọn Vùng Khám Lâm Sàng")
            regions = [
                {"id": "neck", "name": "Cột sống cổ", "icon": "🦴", "color": "linear-gradient(135deg, #ff6b6b, #ee5253)"},
                {"id": "back", "name": "Thắt lưng", "icon": "🩻", "color": "linear-gradient(135deg, #10ac84, #1dd1a1)"},
                {"id": "elbow", "name": "Khuỷu tay", "icon": "💪", "color": "linear-gradient(135deg, #5f27cd, #341f97)"},
                {"id": "knee", "name": "Khớp gối", "icon": "🦵", "color": "linear-gradient(135deg, #ff9f43, #ee5253)"}
            ]

            cols = st.columns(len(regions))
            for idx, reg in enumerate(regions):
                with cols[idx]:
                    st.markdown(f"""
                        <div class="grid-card-box">
                            <div class="icon-circle-btn" style="background: {reg['color']};">
                                {reg['icon']}
                            </div>
                            <div style="font-weight: 700; font-size: 13px; color: #1f2937;">{reg['name']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Chọn", key=f"fast_reg_{reg['id']}", use_container_width=True):
                        st.session_state.exam_active_region = reg['name']
                        st.rerun()
        else:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"#### 📝 Đang khám: `{st.session_state.exam_active_region}`")
            with c2:
                if st.button("⬅ Đổi vùng", use_container_width=True):
                    st.session_state.exam_active_region = None
                    st.rerun()

            st.markdown("---")
            left_col, right_col = st.columns([3, 2])
            with left_col:
                with st.expander("1️⃣ Hành chính & Triệu chứng", expanded=True):
                    p_name = st.text_input("Họ tên", key="rt_p_name")
                    p_phone = st.text_input("SĐT", key="rt_p_phone")
                    symptoms = st.text_area("Triệu chứng", key="rt_symptoms")
                    nrs = st.slider("NRS (Đau)", 0, 10, 2, key="rt_nrs")
            with right_col:
                st.markdown("#### 📄 Tờ Giấy Trắng")
                summary_text = f"[BỆNH ÁN PHCN] - Vùng: {st.session_state.get('exam_active_region')}"
                st.text_area("Copy nội dung:", value=summary_text, height=150)

    # ================= TAB 4: KHO BÀI TẬP PHCN =================
    with tab4:
        st.markdown("### 🏋️‍♂️ Kho Bài Tập Phục Hồi Chức Năng Theo Bệnh Lý")
        st.caption("Chọn một bệnh lý để xem chi tiết trọn bộ 7 bài tập chuẩn hóa:")

        pathologies_m4 = {
            "1. Tai biến mạch máu não (Liệt nửa người)": [
                "1. Tập vận động thụ động các khớp bên liệt duy trì tầm vận động (ROM).",
                "2. Bài tập ức chế trương lực cơ co cứng (kỹ thuật Bobath).",
                "3. Tập chuyển đổi tư thế từ nằm ngửa sang nằm nghiêng và ngồi dậy.",
                "4. Tập kiểm soát thăng bằng thân mình ở tư thế ngồi độc lập.",
                "5. Tập đứng dồn trọng lượng đều hai chân trước gương.",
                "6. Bài tập đi lại với máng nẹp cẳng bàn chân (AFO) hoặc khung tập đi.",
                "7. Tập mạnh cơ chủ động bên lành và các nhóm cơ duỗi bên liệt."
            ],
            "2. Rối loạn nuốt (Dysphagia) sau tai biến": [
                "1. Bài tập vận động cơ môi (mím chặt, cười hết cỡ, thổi phồng má, phát âm U-I).",
                "2. Bài tập vận động lưỡi (đẩy lưỡi ra trước, sang trái, sang phải, liếm vòm họng).",
                "3. Kích thích nhiệt lạnh vùng cung khẩu cái mềm kích thích phản xạ nuốt.",
                "4. Bài tập Masako (giữ đầu lưỡi giữa hai hàm răng và nuốt nước bọt).",
                "5. Bài tập Shaker (nâng đầu ở tư thế nằm ngửa để mở rộng cơ thắt thực quản trên).",
                "6. Bài tập đóng nắp thanh môn (nuốt giữ hơi, ho mạnh ngay sau khi nuốt).",
                "7. Luyện tập nuốt theo các độ quánh thức ăn chuẩn hóa IDDSI."
            ]
        }

        if "selected_pathology_m4" not in st.session_state:
            st.session_state.selected_pathology_m4 = None

        cols_p = st.columns(2)
        for idx, path_key in enumerate(pathologies_m4.keys()):
            with cols_p[idx % 2]:
                if st.button(f"📌 {path_key}", use_container_width=True, key=f"btn_m4_path_{idx}"):
                    st.session_state.selected_pathology_m4 = path_key

        if st.session_state.selected_pathology_m4:
            st.markdown("---")
            st.success(f"🏥 Đang hiển thị phác đồ cho: **{st.session_state.selected_pathology_m4}**")
            for exercise in pathologies_m4[st.session_state.selected_pathology_m4]:
                st.markdown(f"- {exercise}")
            if st.button("🔄 Chọn bệnh lý khác", use_container_width=True):
                st.session_state.selected_pathology_m4 = None
                st.rerun()

if __name__ == "__main__":
    main()
