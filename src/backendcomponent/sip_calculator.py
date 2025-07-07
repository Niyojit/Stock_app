import streamlit as st
import matplotlib.pyplot as plt


def calculate_sip(monthly_investment, annual_rate, investment_duration_years):
    r = annual_rate / 100 / 12  # Monthly interest rate
    n = investment_duration_years * 12  # Total number of months

    if r == 0:
        future_value = monthly_investment * n
    else:
        future_value = monthly_investment * ((((1 + r) ** n) - 1) / r) * (1 + r)

    invested_amount = monthly_investment * n
    estimated_returns = future_value - invested_amount
    return invested_amount, estimated_returns, future_value


def sip_calculator_page():
    st.title("📈 SIP Calculator")

    st.markdown("""
        Systematic Investment Plan (SIP) allows you to invest a fixed amount every month.
        Use this calculator to estimate your wealth over time.
    """)

    col1, col2 = st.columns(2)
    with col1:
        monthly_investment = st.number_input("💸 Monthly Investment (₹)", min_value=100, value=1000, step=100)
        investment_duration = st.number_input("📆 Investment Duration (Years)", min_value=1, max_value=50, value=10)
    with col2:
        expected_return = st.slider("📊 Expected Annual Return (%)", min_value=1.0, max_value=30.0, value=12.0, step=0.1)

    if st.button("🧮 Calculate SIP"):
        invested, returns, total = calculate_sip(monthly_investment, expected_return, investment_duration)

        st.success(f"✅ Total Invested: ₹{invested:,.2f}")
        st.success(f"📈 Estimated Returns: ₹{returns:,.2f}")
        st.success(f"💰 Maturity Amount: ₹{total:,.2f}")