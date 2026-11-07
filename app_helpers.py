import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        .grid-card {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 15px;
            border: 1px solid #e9ecef;
        }
        </style>
    """, unsafe_allow_html=True)
