import streamlit as st
from fetchdata.sqlconnect import explorepage

def createcards(stocks):
    cols = st.columns(4)
    for i, stock in enumerate(stocks):
        with cols[i]:
            st.markdown(f"""
                <a href="{stock['url']}" target="_self" style="text-decoration: none;">
                    <div style='
                        border:1px solid #ddd;
                        border-radius:12px;
                        padding:15px;
                        background-color:#fff;
                        text-align:center;
                        height: 200px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        transition: box-shadow 0.3s;
                    ' onmouseover="this.style.boxShadow='0 0 10px #ccc'" onmouseout="this.style.boxShadow='none'">
                        <div style="margin-bottom:10px;">
                            <img src="https://img.icons8.com/ios/50/line-chart--v1.png" width="30"/>
                        </div>
                        <div style="font-weight:600; font-size:17px; color: black;">{stock['name']}</div>
                        <div style="margin:5px 0; color: black;">{stock['price']}</div>
                        <div style="color:{stock['color']}; font-weight:bold;">{stock['change']}</div>
                    </div>
                </a>
            """, unsafe_allow_html=True)


def explorepage():
    # Dummy data
    stocks = [
            {"name": "Cochin Shipyard", "price": "₹2,044.20", "change": "-47.00 (2.25%)", "color": "red", "url": "https://www.google.com"},
            {"name": "BSE", "price": "₹2,775.60", "change": "-27.40 (0.98%)", "color": "red", "url": "https://www.google.com"},
            {"name": "Suzlon Energy", "price": "₹67.32", "change": "+2.79 (4.32%)", "color": "green",  "url": "https://www.google.com"},
            {"name": "Nippon India ETF Gold", "price": "₹79.81", "change": "-1.31 (1.61%)", "color": "red", "url": "https://www.google.com"},
        ]
    col1, col2 = st.columns([3, 1.5])
    with col1:
        col7, col8 = st.columns([2, 1])
        with col7:
            st.markdown("<h4> Top Gainers </h4>", unsafe_allow_html=True)
        with col8:
            st.button("View all", use_container_width=True)
        createcards(stocks)
        st.divider()

        col3, col4 = st.columns([3, 2])
        with col3:
            st.markdown("<h4>Top Sectors</h4>", unsafe_allow_html=True)
        with col4:
            st.selectbox("Select Sector", label_visibility= "collapsed",options=["All", "Technology", "Finance", "Healthcare"], index=0)
        createcards(stocks)
        st.divider()

        col9, col10 = st.columns([2, 1])
        with col9:
            st.markdown("<h4>Top Losers</h4>", unsafe_allow_html=True)
        with col10:
            st.button("More", use_container_width=True)
        createcards(stocks)

    with col2:
        col5, col6 = st.columns([2, 1])
        with col5:
            st.markdown("<h4> Your Investments </h4>", unsafe_allow_html=True)
        with col6:
            st.button("Portfolio", use_container_width=True)
        with st.expander("Total Returns", expanded=True):
            st.write("Rs 0.00")
        with st.expander("Current Value", expanded=True):
            st.write("Rs 0.00")

        with st.expander("Your Favourites", expanded=True):
            # Inside a main app page
            st.markdown('''<a href="{stock['url']}" target="_self" style="text-decoration: none;">HDFC</a>''', unsafe_allow_html=True)
            st.markdown('''<a href="{stock['url']}" target="_self" style="text-decoration: none;">Tata</a>''', unsafe_allow_html=True)
            st.markdown('''<a href="{stock['url']}" target="_self" style="text-decoration: none;">Google</a>''', unsafe_allow_html=True)
            st.markdown('''<a href="{stock['url']}" target="_self" style="text-decoration: none;">Jindal</a>''', unsafe_allow_html=True)
            st.markdown('''<a href="{stock['url']}" target="_self" style="text-decoration: none;">Airtel</a>''', unsafe_allow_html=True)
            st.markdown('''<a href="{stock['url']}" target="_self" style="text-decoration: none;">Ola</a>''', unsafe_allow_html=True)
            st.markdown('''<a href="{stock['url']}" target="_self" style="text-decoration: none;">Uber</a>''', unsafe_allow_html=True)
            st.markdown('''<a href="{stock['url']}" target="_self" style="text-decoration: none;">Zomato</a>''', unsafe_allow_html=True)



        