# =========================================================
# APP.PY - TRANG CHÍNH PHCN AI 1.8
# =========================================================
import streamlit as st

from Core.tab2_trithuc import render_tab2
from Core.tab3_kham import render_tab3
from Core.tab4_phcn import render_tab4

st.set_page_config(
    page_title="PHCN AI 1.8",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🩺 PHCN AI 1.8 – Trợ lý Phục hồi Chức năng & Lâm sàng")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Hồ sơ & Lịch sử", 
        "📚 Cẩm nang Tri thức", 
        "🩺 Khám Lâm sàng", 
        "🏋️‍♂️ Kho Bài tập PHCN"
    ])

    with tab1:
        st.subheader("👤 Quản lý Hồ sơ Bệnh nhân & Lịch sử Khám")
        st.info("Sử dụng trình quản lý lịch sử để tra cứu và lưu trữ bệnh án.")

    with tab2:
        render_tab2()

    with tab3:
        render_tab3()

    with tab4:
        render_tab4()

if __name__ == "__main__":
    main()
