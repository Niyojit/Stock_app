import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from login.loginUI import register

def landing_page():

    if "show_auth" not in st.session_state:
        st.session_state.show_auth = False
        st.session_state.auth_tab = "Login"

 
    if st.session_state.show_auth:
        register(active_tab=st.session_state.auth_tab)
        st.stop()

    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem;
            }
            header {
                margin-top: -40px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.set_page_config(page_title="StockSphere", layout="wide")
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem;
            }
            header {
                margin-top: -40px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)

 
    with st.container():
        col1, col2, col3, col4 = st.columns([0.5, 2, 3, 1.2])

    
        with col1:
            st.markdown(
                '<i class="fa-solid fa-money-bill-trend-up fa-xl" style="color:#ff4081;"></i>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown("### StockSphere")

  
        with col3:
            nav_cols = st.columns(4)
            nav_labels = ["Home", "About", "Services", "Contact"]
            for i, label in enumerate(nav_labels):
                with nav_cols[i]:
                    st.markdown(f"<div style='padding: 8px 0px; font-weight: 500; text-align: center; color: #1a1a1a;'>{label}</div>", unsafe_allow_html=True)

      
        with col4:
            if st.button("Login", use_container_width=True):
                st.session_state.show_auth = True
                st.session_state.auth_tab = "Login"
                st.rerun()


    st.divider()



    # --- Main Content ---
    left_col, right_col = st.columns(2)

    with left_col:
        st.header("📈 StockSphere")
        st.subheader("Where Strategy Meets Simplicity.")
        st.write("""
            Welcome to **StockSphere** – your smart gateway to stock market investing.
            Whether you're just starting out or tracking complex trends,
            we offer **real-time data**, **intuitive tools**, and **simple insights**
            to help you invest with confidence. Make informed decisions and grow your wealth with ease.
        """)
        
        if st.button("Register", key="register_btn"):
            st.session_state.show_auth = True
            st.session_state.auth_tab = "Register"
            st.rerun()

    with right_col:
        st.image("https://i.postimg.cc/rsDNCy1V/home1image.jpg", use_container_width=True)

