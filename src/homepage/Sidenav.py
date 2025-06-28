import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from component.explore import show_explore
from component.holding import show_holding
from component.sip_calculator import show_sip_calculator
from component.stock_transaction import show_stock_transaction
from component.contact_us import show_contact_us
from component.community import show_community

def sidebar_items():
    

    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Explore", "Holdings", "SIP Calculator", "Stock Transactions", "Contact us", "Community"],
            icons=["house", "book", "calculator", "graph-up", "telephone", "people"],
            menu_icon="cast",
            default_index=0,
        )
        return selected

def sidebar_navigator(selected_option):
    if selected_option == "Explore":
        return show_explore()
    elif selected_option == "Holdings":
        return show_holding()
    elif selected_option == "SIP Calculator":
        return show_sip_calculator()
    elif selected_option == "Stock Transactions":
        return show_stock_transaction()
    elif selected_option == "Contact us":
        return show_contact_us()
    elif selected_option == "Community":
        return show_community()

if __name__ == '__main__':
    st.set_page_config(page_title="Dashboard", layout="wide")
    selected_option = sidebar_items()
    sidebar_navigator(selected_option)
