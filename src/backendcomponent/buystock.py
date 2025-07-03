import streamlit as st
import pandas as pd
import os
import sys
from urllib.parse import urlencode
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fetchdata.sqlconnect import get_sql_connection
from fetchdata.api import fetch_and_store_stocks
from backendcomponent.sellstock import show_sell_stock_details

def show_selected_stock_details(symbol, username, user_id):
    if st.session_state.get("selected_symbol"):
        st_autorefresh(interval=3000, key="refresh_explore")
    
    st.write("🔍 Currently Viewing:", symbol)

    st.session_state.setdefault("buy_clicked", False)
    st.session_state.setdefault("sell_clicked", False)
    st.session_state.setdefault("confirm_clicked", False)

    conn = get_sql_connection()
    df = pd.read_sql("SELECT * FROM dbo.IndianStockLiveData WHERE Symbol = ? ORDER BY FetchTime DESC", conn, params=[symbol])
    conn.close()

    if df.empty:
        st.warning("Stock not found.")
        return

    stock = df.iloc[0]
    st.markdown("---")
   
    # 🟨 Split layout into two columns
    col1, col2 = st.columns([2, 3])

    # --- LEFT SIDE: Stock Info, Buy/Sell ---
    with col1:
        st.subheader(f"📊 {stock['Name']} ({stock['Symbol']})")

        st.write(f"*Price:* ₹{stock['Price']}  |  *P/E Ratio:* {stock['PERatio']}  |  *Sector:* {stock['Sector']}")
        st.write(f"*52W High:* ₹{stock['High52W']} | *52W Low:* ₹{stock['Low52W']}")

        if not st.session_state.buy_clicked:
            if st.button("🛒 Buy Stock"):
                st.session_state.buy_clicked = True
                st.session_state.sell_clicked = False
                st.session_state.confirm_clicked = False

        if st.session_state.buy_clicked:
            quantity = st.number_input("Quantity to Buy", min_value=1, step=1, key="buy_quantity_input")
            total = quantity * stock["Price"]
            st.info(f"Total Cost: ₹{total:.2f}")

            if st.button("Confirm Purchase"):
                st.session_state.confirm_clicked = True

            if st.session_state.confirm_clicked:
                conn = get_sql_connection()
                cur = conn.cursor()
                cur.execute("SELECT Initial_cash FROM users WHERE id = ?", (user_id,))
                result = cur.fetchone()
                if not result:
                    st.error("⚠ User not found.")
                    return
                balance = result[0]

                if total <= balance:
                    cur.execute("""
                        IF OBJECT_ID('dbo.StockBuyTransactions', 'U') IS NULL
                        CREATE TABLE dbo.StockBuyTransactions (
                            transaction_id UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
                            user_id INT,
                            username VARCHAR(100),
                            symbol NVARCHAR(20),
                            quantity INT,
                            price FLOAT,
                            total FLOAT,
                            time DATETIME DEFAULT GETDATE()
                        )
                    """)
                    cur.execute("""
                        INSERT INTO dbo.StockBuyTransactions (user_id, username, symbol, quantity, price, total)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (user_id, username, symbol, quantity, stock["Price"], total))
                    cur.execute("UPDATE users SET Initial_cash = Initial_cash - ? WHERE id = ?", (total, user_id))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Purchased {quantity} shares of {symbol} for ₹{total:.2f}")
                    st.session_state.buy_clicked = False
                    st.session_state.confirm_clicked = False
                    st.rerun()
                else:
                    st.error("❌ Insufficient balance.")

        if st.button("📤 Sell Stock"):
            st.session_state.sell_clicked = True
            st.session_state.buy_clicked = False
            st.session_state.confirm_clicked = False

        if st.session_state.sell_clicked:
            show_sell_stock_details(symbol, username, user_id)

        if st.button("← Back to Explore"):
            st.session_state.selected_symbol = None
            st.session_state.buy_clicked = False
            st.session_state.sell_clicked = False
            st.session_state.confirm_clicked = False
            st.rerun()

 
    with col2:
        st.subheader("📈 Price & Volume Trend")
        st_autorefresh(interval=3000, key="refresh_graph")
        # Fetch historical data
        conn = get_sql_connection()
        hist_df = pd.read_sql(
            "SELECT [DateTime], [Open], [Close], [High], [Low], [Volume] FROM dbo.HistoryStockData WHERE Symbol = ? ORDER BY [DateTime]",
            conn,
            params=[symbol]
        )
        conn.close()

        if hist_df.empty:
            st.warning("No historical data available.")
        else:
            hist_df["DateTime"] = pd.to_datetime(hist_df["DateTime"])
            hist_df.set_index("DateTime", inplace=True)

            # --- 📅 Resampling Option ---
            resample_option = st.radio("Resample By:", ["30min", "Hourly", "Daily"], horizontal=True)

            if resample_option == "Hourly":
                df_resampled = hist_df.resample("1H").agg({
                    "Open": "first",
                    "Close": "last",
                    "High": "max",
                    "Low": "min",
                    "Volume": "sum"
                }).dropna()
            elif resample_option == "Daily":
                df_resampled = hist_df.resample("1D").agg({
                    "Open": "first",
                    "Close": "last",
                    "High": "max",
                    "Low": "min",
                    "Volume": "sum"
                }).dropna()
            else:
                df_resampled = hist_df  # 30-min default

            # --- 📊 Chart Option ---
            chart_type = st.selectbox("Chart Type", ["Close Price", "Open vs Close", "Volume"], index=0)

            fig = go.Figure()

            if chart_type == "Close Price":
                fig.add_trace(go.Scatter(x=df_resampled.index, y=df_resampled["Close"], mode="lines+markers", name="Close Price", line=dict(color="#FF5733")))
                fig.update_layout(title=f"{symbol} Close Price Trend ({resample_option})", yaxis_title="₹ Price")

            elif chart_type == "Open vs Close":
                fig.add_trace(go.Scatter(x=df_resampled.index, y=df_resampled["Open"], mode="lines", name="Open", line=dict(color="blue")))
                fig.add_trace(go.Scatter(x=df_resampled.index, y=df_resampled["Close"], mode="lines", name="Close", line=dict(color="green")))
                fig.update_layout(title=f"{symbol} Open vs Close Price ({resample_option})", yaxis_title="₹ Price")

            elif chart_type == "Volume":
                fig.add_trace(go.Bar(x=df_resampled.index, y=df_resampled["Volume"], name="Volume", marker_color="orange"))
                fig.update_layout(title=f"{symbol} Trading Volume ({resample_option})", yaxis_title="Volume")

            fig.update_layout(xaxis_title="Time", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

