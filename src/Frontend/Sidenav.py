import streamlit as st
from streamlit_option_menu import option_menu

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

if __name__ == '__main__':
    selected_option = sidebar_items()
    st.write(f"You selected: {selected_option}")
