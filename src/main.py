import streamlit as st

from landing.Landingpage import landing_page
from landing.Sidenav import launch_dashboard



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

query_params = st.query_params


if st.session_state.logged_in:

    username = st.session_state.username
    user_id = st.session_state.user_id
    launch_dashboard(username, user_id)

elif "symbol" in query_params:
   
    landing_page()

else:
    landing_page()

