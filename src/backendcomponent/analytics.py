import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from streamlit_autorefresh import st_autorefresh

# ✅ Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fetchdata.sqlconnect import get_sql_connection


# ✅ Fetch user holdings
def get_user_holdings(user_id):
    conn = get_sql_connection()
    st_autorefresh(interval=3000, key="refresh_analytics")
    buy_df = pd.read_sql("""
        SELECT symbol, SUM(quantity) AS bought_qty, AVG(price) AS avg_price, SUM(total) AS total_buy
        FROM dbo.StockBuyTransactions
        WHERE user_id = ?
        GROUP BY symbol
    """, conn, params=[user_id])

    if buy_df.empty:
        conn.close()
        return pd.DataFrame()

    sell_df = pd.read_sql("""
        SELECT symbol, SUM(quantity) AS sold_qty
        FROM dbo.StockSellTransactions
        WHERE user_id = ?
        GROUP BY symbol
    """, conn, params=[user_id])

    df = pd.merge(buy_df, sell_df, on="symbol", how="left")
    df["sold_qty"] = df["sold_qty"].fillna(0)
    df["net_qty"] = df["bought_qty"] - df["sold_qty"]
    df = df[df["net_qty"] > 0]

    live_prices = pd.read_sql("""
        SELECT l.Symbol, l.Price AS current_price
        FROM dbo.IndianStockLiveData l
        INNER JOIN (
            SELECT Symbol, MAX(FetchTime) AS LatestFetch
            FROM dbo.IndianStockLiveData
            GROUP BY Symbol
        ) m ON l.Symbol = m.Symbol AND l.FetchTime = m.LatestFetch
    """, conn)

    conn.close()

    df = df.merge(live_prices, left_on="symbol", right_on="Symbol", how="left")

    df["investment"] = df["net_qty"] * df["avg_price"]
    df["current_value"] = df["net_qty"] * df["current_price"]
    df["gain_loss"] = df["current_value"] - df["investment"]

    df = df[["symbol", "net_qty", "avg_price", "current_price", "investment", "current_value", "gain_loss"]]

    df.rename(columns={
        "symbol": "Symbol",
        "net_qty": "Quantity",
        "avg_price": "Avg Purchase Price",
        "current_price": "Current Price",
        "investment": "Investment (₹)",
        "current_value": "Current Value (₹)",
        "gain_loss": "Gain/Loss (₹)"
    }, inplace=True)

    return df


# ✅ Main Analytics Page
def show_analytics_page(user_id):
    st.title("📊 Portfolio Analytics")
    
    portfolio = get_user_holdings(user_id)

    if portfolio.empty:
        st.warning("⚠️ You have no holdings to analyze.")
        return

    # ✔️ Portfolio Summary
    st.subheader("📌 Portfolio Summary")
    st.dataframe(portfolio, use_container_width=True)

    ### 🔥 Common Style Settings ###
    sns.set_style("darkgrid")
    plt.rcParams.update({
        "axes.facecolor": "#111111",
        "figure.facecolor": "#111111",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "text.color": "white",
        "axes.titleweight": "bold",
        "axes.labelweight": "bold"
    })

    ####### ✅ Gain/Loss Bar Chart ########
    st.subheader("📈 Gain/Loss Per Stock")
    fig1, ax1 = plt.subplots(figsize=(7, 4), dpi=120)
    ax1.bar(
        portfolio["Symbol"],
        portfolio["Gain/Loss (₹)"],
        color=["green" if x >= 0 else "red" for x in portfolio["Gain/Loss (₹)"]],
        edgecolor='black'
    )
    ax1.set_title("Gain/Loss per Stock", fontsize=13)
    ax1.set_ylabel("₹", fontsize=11)
    ax1.set_xlabel("Stock Symbol", fontsize=11)
    ax1.grid(axis='y', linestyle='--', alpha=0.6)

    plt.setp(ax1.get_xticklabels(), rotation=30, ha="right")
    st.pyplot(fig1)

    ####### ✅ Portfolio Pie Chart with Shadow #######
    st.subheader("📊 Portfolio Distribution by Current Value")
    pie_data = portfolio[portfolio["Current Value (₹)"] > 0]
    if not pie_data.empty:
        fig2, ax2 = plt.subplots(figsize=(4, 4), dpi=120)

        # Draw shadow
        shadow_circle = plt.Circle((0, 0), 1.05, color='grey', alpha=0.3, zorder=0)
        ax2.add_artist(shadow_circle)

        wedges, texts, autotexts = ax2.pie(
            pie_data["Current Value (₹)"],
            labels=pie_data["Symbol"],
            autopct='%1.1f%%',
            startangle=140,
            colors=sns.color_palette("Set2"),
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
            textprops={'fontsize': 8}
        )
        ax2.set_title("Portfolio Allocation", fontsize=13, fontweight='bold')
        ax2.axis('equal')
        st.pyplot(fig2)
    else:
        st.info("No data available for pie chart.")

    ####### ✅ Investment vs Current Value ########
    st.subheader("💰 Investment vs Current Value")
    x = np.arange(len(portfolio["Symbol"]))
    width = 0.35
    fig3, ax3 = plt.subplots(figsize=(7, 4), dpi=120)

    ax3.bar(
        x - width/2, portfolio["Investment (₹)"],
        width, label="Investment", color="dodgerblue", edgecolor="black"
    )
    ax3.bar(
        x + width/2, portfolio["Current Value (₹)"],
        width, label="Current Value", color="orange", edgecolor="black"
    )
    ax3.set_xticks(x)
    ax3.set_xticklabels(portfolio["Symbol"], rotation=30, ha="right")
    ax3.set_ylabel("₹ Value")
    ax3.set_title("Investment vs Current Value", fontsize=13)
    ax3.legend()
    ax3.grid(axis="y", linestyle="--", alpha=0.6)
    st.pyplot(fig3)

    ####### ✅ Top Performing Stocks ########
    st.subheader("🌟 Top Performing Stocks")
    top_gainers = portfolio.sort_values("Gain/Loss (₹)", ascending=False).head(3)
    st.dataframe(top_gainers, use_container_width=True)


# ✅ Example usage:
# from analytics import show_analytics_page
# show_analytics_page(user_id="your_user_id")
 