# =========================================================
# APP.PY - PHCN AI 2.0 TRUNG TÂM ĐIỀU PHỐI (OFFLINE)
# =========================================================
import streamlit as st
import os

from core.history_manager import HistoryManager
from tabs.tab1_hoso import render as render_tab1
from tabs.tab2_trithuc import render as render_tab2
from tabs.tab3_kham import render as render_tab3
from tabs.tab4_phcn import render as render_tab4

st.set_page_config(
    page_title="PHCN AI 2.0 – Trợ lý Phục hồi Chức năng & Lâm sàng",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Khởi tạo bộ quản lý lịch sử SQLite
    db_path = os.path.join("data", "phcn_database.db")
    history_mgr = HistoryManager(db_path=db_path)

    st.title("🩺 PHCN AI 2.0 – Trợ lý Phục hồi Chức năng & Lâm sàng")
    st.caption("Hệ thống phân tích, suy luận lâm sàng & lưu trữ SQLite (Hoạt động Offline 100%)")

    # 4 Tab chính chuẩn cấu trúc
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Hồ sơ Bệnh nhân", 
        "📚 Cẩm nang Tri thức", 
        "🩺 Khám Lâm sàng", 
        "🏋️‍♂️ Kho Bài tập PHCN"
    ])

    with tab1:
        render_tab1(history_mgr)

    with tab2:
        render_tab2()

    with tab3:
        render_tab3(history_mgr)

    with tab4:
        render_tab4()

if __name__ == "__main__":
    main()
