import streamlit as st
from PIL import Image
import numpy as np

# Load University of Salford logo (Ensure the file is in the same directory)
logo_path = "logo.png"
try:
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_container_width=True)
except Exception as e:
    st.sidebar.error("Logo not found. Please upload 'salford_logo.png'")

# Title and Description
st.title("🔍 Lifecycle Cost & Loan Assessment Calculator")
st.markdown("Compare the costs and sustainability impact of switching hotel water heating from LPG to electricity.")

# User Inputs
st.header("⚡ Scenario Inputs")
col1, col2 = st.columns(2)

with col1:
    lpg_price = st.number_input("💰 LPG Price (per kWh)", value=0.08)
    elec_price = st.number_input("🔋 Electricity Price (per kWh)", value=0.15)
    lpg_efficiency = st.number_input("🔥 LPG Boiler Efficiency (%)", value=85.0) / 100

with col2:
    annual_hot_water_kwh = st.number_input("🏨 Annual Hot Water Energy Demand (kWh)", value=50000)
    inflation_rate = st.number_input("📈 Annual Energy Price Inflation (%)", value=2.5) / 100
    project_lifetime = st.number_input("📅 Project Lifetime (years)", value=15)

# Calculation
def calculate_lifecycle_cost(energy_price, efficiency):
    costs = []
    for year in range(project_lifetime):
        cost = (annual_hot_water_kwh / efficiency) * energy_price
        costs.append(cost)
        energy_price *= (1 + inflation_rate)
    return np.sum(costs)

lpg_lifecycle_cost = calculate_lifecycle_cost(lpg_price, lpg_efficiency)
elec_lifecycle_cost = calculate_lifecycle_cost(elec_price, 1.0)  # Electric heating efficiency ~100%

diff = lpg_lifecycle_cost - elec_lifecycle_cost

# Results
st.header("📊 Results")
col1, col2 = st.columns(2)
with col1:
    st.metric("💸 LPG Lifecycle Cost", f"£{lpg_lifecycle_cost:,.2f}")
    st.metric("⚡ Electricity Lifecycle Cost", f"£{elec_lifecycle_cost:,.2f}")
with col2:
    if diff > 0:
        st.success(f"✅ Switching to electricity saves £{diff:,.2f} over {project_lifetime} years!")
    else:
        st.warning(f"⚠️ LPG remains cheaper by £{abs(diff):,.2f} over {project_lifetime} years.")

# Loan Assessment
st.header("🏦 Loan Assessment")
loan_required = st.number_input("💳 Loan Amount (£)", value=10000)
interest_rate = st.number_input("📊 Annual Interest Rate (%)", value=5.0) / 100
loan_term = st.number_input("📆 Loan Term (years)", value=10)

def calculate_loan_payment(principal, rate, term):
    if rate == 0:
        return principal / term
    return (principal * rate / 12) / (1 - (1 + rate / 12) ** (-term * 12))

monthly_payment = calculate_loan_payment(loan_required, interest_rate, loan_term)

st.metric("💵 Monthly Loan Payment", f"£{monthly_payment:,.2f}")