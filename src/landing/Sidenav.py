import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backendcomponent.explore import explorepage

from backendcomponent.wallet import my_money
from backendcomponent.moneytransaction import money_transaction
from backendcomponent.holding import holding_page
from backendcomponent.sip_calculator import sip_calculator_page
from backendcomponent.analytics import show_analytics_page

def sidebar_items():
    with st.sidebar:
        selected = option_menu(
            menu_title="Your Profile",
            options=["Explore", "Holdings", "SIP Calculator", "Money Transactions", "Analytics", "My wallet", "Logout"],
            icons=["house", "book", "calculator", "graph-up", "telephone", "people", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
        )
        

        return selected

def sidebar_navigator(selected_option, username, user_id):
 
 
    
    if selected_option == "Explore":
        return explorepage(username, user_id)
    elif selected_option == "My wallet":
        return my_money(username, user_id)
    elif selected_option == "Logout":
        st.session_state.clear()
        st.rerun() 
    elif selected_option == "Money Transactions":
        return money_transaction(username, user_id)
    elif selected_option == "Holdings":
        return holding_page(username, user_id)
    elif selected_option == "SIP Calculator":
        return sip_calculator_page()
    elif selected_option == "Analytics":
        return show_analytics_page(user_id)


def launch_dashboard(username, user_id):
    st.set_page_config(page_title="Dashboard", layout="wide")
    username = username or st.session_state.get("username", "")
    user_id = user_id or st.session_state.get("user_id", None)
    selected_option = sidebar_items()

    st.markdown(f"### Hello! {username}, welcome to your dashboard! 👋")
    sidebar_navigator(selected_option, username, user_id)



