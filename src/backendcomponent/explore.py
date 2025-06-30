import streamlit as st
import pandas as pd
import os
import sys
from streamlit_autorefresh import st_autorefresh

# Set up backend path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fetchdata.sqlconnect import get_sql_connection  # You must have this defined
from fetchdata.api import fetch_and_store_stocks

# ⏬ Fetch live stock data from SQL Server
def fetch_live_stock_data(limit=20):
    conn = get_sql_connection()
    query = f"""
        SELECT TOP {limit}
            Symbol,
            Name,
            Price,
            PERatio,
            High52W,
            Low52W,
            Sector
        FROM dbo.IndianStockLiveData
        ORDER BY FetchTime DESC 

    """
    df = pd.read_sql(query, conn)
    conn.close()

    stocks = []
    for _, row in df.iterrows():
        price = round(row.Price, 2)
        
        # Estimate change (dummy logic: % change from avg 52W range)
        change_pct = ((row.Price - row.Low52W) / (row.High52W - row.Low52W + 0.01)) * 100
        change_color = "green" if change_pct > 50 else "red"
        change_text = f"{change_pct:.2f}%"

        stocks.append({
            "name": row.Name,
            "price": f"₹{price}",
          
            "change": change_text,
            "color": change_color,
            "url": f"https://www.google.com/search?q={row.Symbol.replace('.NS', '')}+stock"
        })
    return stocks

# 🧱 Card layout
def createcards(stocks):
    cols = st.columns(4)
    for i, stock in enumerate(stocks):
        with cols[i % 4]:  # Ensure it wraps after 4
            st.markdown(f"""
                <a href="{stock['url']}" target="_blank" style="text-decoration: none;">
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

# 📊 Explore page layout
def explorepage():
    st_autorefresh(interval=60000, key="data_refresh")
    with st.spinner("Fetching live data..."):
        fetch_and_store_stocks()
    stocks = fetch_live_stock_data()

    col1, col2 = st.columns([3, 1.5])
    with col1:
        st.markdown("<h4> Top Gainers </h4>", unsafe_allow_html=True)
        createcards(stocks[:4])
        st.divider()

        st.markdown("<h4> Top Sectors </h4>", unsafe_allow_html=True)
        st.selectbox("Select Sector", label_visibility="collapsed", options=["All"] + list(set([s['name'] for s in stocks])))
        createcards(stocks[4:12])
        st.divider()

        st.markdown("<h4> Top Losers </h4>", unsafe_allow_html=True)
        createcards(stocks[12:16])

    with col2:
        st.markdown("<h4> Your Investments </h4>", unsafe_allow_html=True)
        st.button("Portfolio", use_container_width=True)
        with st.expander("Total Returns", expanded=True):
            st.write("Rs 0.00")
        with st.expander("Current Value", expanded=True):
            st.write("Rs 0.00")
        with st.expander("Your Favourites", expanded=True):
            for s in stocks[:6]:
                st.markdown(f"""<a href="{s['url']}" target="_blank" style="text-decoration: none;">{s['name']}</a>""", unsafe_allow_html=True)



