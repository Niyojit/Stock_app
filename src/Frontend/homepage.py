import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backendcomponent.explore import explorepage
from backendcomponent.singlestock import show_stock_details

st.set_page_config(page_title="Explore | StockSphere", layout="wide")

selected_stock = st.query_params.get("stock", None)
# Inject CSS to remove padding/margin
st.markdown("""
    <style>
        .block-container {
            padding-top: 0.5rem;
        }
        
        .nav-link {
            padding: 8px 16px;
            font-weight: 500;
            color: #1a1a1a;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- Navbar ---
st.markdown('<div class="navbar">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.5, 1, 0.5])

with col1:
    st.markdown("### 📈 StockSphere")

with col2:
    search_query = st.text_input("🔍 Search stocks",label_visibility="collapsed", placeholder="Search...", key="search_query")

with col3:
    st.button("Profile", use_container_width=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Explore", "Holdings", "List", "Tools", "Wallet"])

with tab1:
    if selected_stock:
        show_stock_details(selected_stock)
    else:
        explorepage()
        


