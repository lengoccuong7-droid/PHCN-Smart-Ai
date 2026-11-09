# =========================================================
# app.py - trang chính phcn ai 2.0 (hoạt động offline)
# =========================================================
import streamlit as st
import os

# import các module từ thư mục tabs (đã viết thường hoàn toàn)
from tabs.tab1_hoso import render as render_tab1
from tabs.tab2_trithuc import render as render_tab2
from tabs.tab3_kham import render as render_tab3
from tabs.tab4_phcn import render as render_tab4

# import bộ quản lý lịch sử từ thư mục core (đã viết thường hoàn toàn)
from core.history_manager import HistoryManager

st.set_page_config(
    page_title="phcn ai 2.0 – trợ lý phục hồi chức năng & lâm sàng",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # khởi tạo đường dẫn cơ sở dữ liệu sqlite trong thư mục data
    db_path = os.path.join("data", "phcn_database.db")
    history_mgr = HistoryManager(db_path=db_path)

    st.title("🩺 phcn ai 2.0 – trợ lý phục hồi chức năng & lâm sàng")
    st.caption("hệ thống hỗ trợ đánh giá, phân tích và suy luận lâm sàng chuyên sâu (hoạt động offline)")

    # tạo 4 tab chính theo cấu trúc phân tầng
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 hồ sơ bệnh nhân", 
        "📚 cẩm nang tri thức", 
        "🩺 khám lâm sàng", 
        "🏋️‍♂️ kho bài tập phcn"
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
