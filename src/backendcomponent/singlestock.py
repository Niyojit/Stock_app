import streamlit as st
# def relianceIndustries():

col1, col2 = st.columns([10,5])
with col1:
        st.markdown("<h4>Wallet Balance</h4>", unsafe_allow_html=True)
        st.write("""
            Reliance Industries Limited (RIL) is a conglomerate with interests in petrochemicals, refining, oil, telecommunications, and retail.
            It is one of India's largest companies by market capitalization and has a significant presence in various sectors.
        """)
with col2:
        st.markdown("<h4>Reliance Industries</h4>", unsafe_allow_html=True)
        
        with st.expander("Transactions", expanded = True):
                tab1, tab2 = st.tabs(["Buy", "Sell"]) 
                with tab1:
                    col3, col4 = st.columns([1,1])
                    with col3:
                        st.write("Current Price:")
                        st.info("10")
                    with col4:
                        st.text_input("Quantity", placeholder="Enter amount", key="add_quantity")
                    st.button("Add Money", use_container_width=True)
                with tab2:
                    col3, col4 = st.columns([1,1])
                    with col3:
                        st.write("Current Price:")
                    with col4:
                        st.text_input("Add money", label_visibility="collapsed", placeholder="Enter amount", key="withdraw_money")
                    st.button("Withdraw Money", use_container_width=True)