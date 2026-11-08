# =========================================================
# PHCN AI 1.8 - MAIN APPLICATION ENTRY POINT
# =========================================================
import streamlit as st
from Core.history_manager import HistoryManager

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="PHCN AI 1.8 - Trợ lý Lâm sàng Chuyên sâu",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Khởi tạo quản lý lịch sử bệnh án
history_mgr = HistoryManager()

# 3. Thanh tiêu đề ứng dụng
st.title("🩺 PHCN AI 1.8 – Trợ lý Phục hồi chức năng & Lâm sàng")
st.markdown("Hệ thống hỗ trợ chẩn đoán, khám lâm sàng và tra cứu bài tập phục hồi chức năng chuyên sâu theo y học chứng cứ.")

# 4. Xây dựng cấu trúc điều hướng 4 Tab chính
tab1, tab2, tab3, tab4 = st.tabs([
    "👤 1. Hồ sơ & Lịch sử", 
    "📚 2. Cẩm nang Tri thức", 
    "🩺 3. Khám lâm sàng", 
    "🏋️‍♂️ 4. Kho bài tập PHCN"
])

# 5. Gọi hàm render() từ các Core modules tương ứng
with tab1:
    from Core.tab1_hoso import render as render_tab1
    render_tab1(history_mgr)

with tab2:
    from Core.tab2_trithuc import render as render_tab2
    render_tab2()

with tab3:
    from Core.tab3_kham import render as render_tab3
    render_tab3(history_mgr)

with tab4:
    from Core.tab4_phcn import render as render_tab4
    render_tab4()
