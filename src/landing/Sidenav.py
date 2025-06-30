import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backendcomponent.explore import explorepage
from backendcomponent.singlestock import show_stock_details  # ⬅️ Make sure this exists
from backendcomponent.wallet import my_money
def sidebar_items():
    with st.sidebar:
        selected = option_menu(
            menu_title="My Profile",
            options=["Explore", "Holdings", "SIP Calculator", "Stock Transactions", "Analytics", "My wallet"],
            icons=["house", "book", "calculator", "graph-up", "telephone", "people"],
            menu_icon="cast",
            default_index=0,
        )
        return selected

def sidebar_navigator(selected_option):
    # 👇 Check if user is on Explore tab AND a stock is selected
    query_params = st.query_params
    if selected_option == "Explore" and "symbol" in query_params:
        return show_stock_details()
    elif selected_option == "Explore":
        return explorepage()
    elif selected_option == "My wallet":
        return my_money()

if __name__ == '__main__':
    st.set_page_config(page_title="Dashboard", layout="wide")
    selected_option = sidebar_items()
    sidebar_navigator(selected_option)
