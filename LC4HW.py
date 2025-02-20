import streamlit as st
from PIL import Image
import numpy as np

def load_logo():
    logo_path = "salford_logo.png"
    try:
        logo = Image.open(logo_path)
        st.sidebar.image(logo, use_container_width=True)
    except Exception:
        st.sidebar.error("❌ Logo not found. Please upload 'salford_logo.png'")

st.set_page_config(layout="wide")
load_logo()

# Sidebar Navigation
pages = ["🏠 Main Calculator", "🔥 Hot Water Energy Calculator", "🏦 Loan Calculator"]
selection = st.sidebar.radio("🔍 Navigation", pages, index=0)

if selection == "🏠 Main Calculator":
    st.title("🔍 LPG vs Electric Hot Water Lifecycle Sustainability Calculator")
    st.markdown("Using this calculator, you are able to compare the costs, fuel consumption, and sustainability impact of switching hot water heating systems from LPG to electricity.")
    
    st.header("⚡ Scenario Inputs")
    
    st.subheader("⚙️ Technical Inputs")
    col1, col2 = st.columns(2)
    with col1:
        lpg_efficiency = st.number_input("🔥 LPG Boiler Efficiency (%)", value=80, step=5, help="Efficiency of LPG boiler.") / 100
        lpg_energy_content = st.number_input("⚡ LPG Energy Content (kWh per liter)", value=7.00, step=0.50,help="Energy content of LPG: in the UK one litre of LPG contains 7.08 kWh of energy.")
    with col2:
        tank_size = st.number_input("🚰 Hot Water Tank Size (liters)", value=400, step=50, help="Capacity of the hot water tank.")
        heating_days = st.number_input("📅 Days per Year Tank is Heated", value=270, step=5, help="Number of days per year.")
    
    def calculate_energy_needed(hot_temp, cold_temp, lpg_efficiency):
        energy_needed = 4.18 * (hot_temp - cold_temp) / (lpg_efficiency * 3600)
        return energy_needed
    
    hot_temp = 60  # Example default
    cold_temp = 10  # Example default
    energy_needed = calculate_energy_needed(hot_temp, cold_temp, lpg_efficiency)

    st.write(f"**⚡ Average Energy needed from LPG per Liter of Hot Water: {energy_needed:.4f} kWh or {energy_needed/lpg_energy_content:.4f} Litres of LPG")

    # st.markdown("**⚡ Average Energy Use per Liter of Hot Water: {:.2f} kWh**".format(0.06))
    
    st.subheader("💰 Economic Inputs")
    col1, col2 = st.columns(2)
    with col1:
        lpg_price_pence = st.number_input("🔥 LPG Price (pence per liter)", value=60.0) / 100
        elec_price_pence = st.number_input("⚡ Electricity Price (pence per kWh)", value=15.0) / 100
    with col2:
        project_lifetime = st.number_input("🕰️ Project Lifetime (years)", value=15)
        switching_cost = st.number_input("💵 Total Cost of Switching (£)", value=10000.0, step=10.0, help="Total cost of installing an electrified systems.")
    
    st.write(f"**⚡ LPG Cost per Liter of Hot Water: {(energy_needed*lpg_price_pence):.4f} Pence**")
    st.write(f"**⚡ Electricity Cost per Liter of Hot Water: {(energy_needed*elec_price_pence):.4f} Pence**")

    st.subheader("🌍 Environmental Inputs")
    col1, col2 = st.columns(2)
    with col1:
        carbon_emission_lpg = st.number_input("💨 Carbon Emission - LPG (kg CO2 per liter)", value=1.5, help="")
    with col2:
        carbon_emission_elec = st.number_input("💨 Carbon Emission - Electricity (kg CO2 per kWh)", value=0.2, help="")
    
    # Calculation Functions
    energy_per_liter = 0.06
    annual_hot_water_kwh = tank_size * heating_days * energy_per_liter
    annual_lpg_liters = annual_hot_water_kwh / (lpg_efficiency * lpg_energy_content)
    

    def calculate_lifecycle_cost(price, esc_rate, required_energy, efficiency=1.0):
        total_cost, current_price = 0, price
        for _ in range(project_lifetime):
            total_cost += (required_energy / efficiency) * current_price
            current_price *= (1 + esc_rate)
        return total_cost
    
    lpg_lifecycle_cost = calculate_lifecycle_cost(lpg_price_pence, 0.04, annual_hot_water_kwh, lpg_efficiency)
    elec_lifecycle_cost = calculate_lifecycle_cost(elec_price_pence, 0.015, annual_hot_water_kwh)
    
    # Results Display
    st.header("📊 Results")
    st.write(f"💡 **Energy Cost per Liter of Hot Water:**")
    st.write(f"🔥 LPG: £{(lpg_price_pence / (lpg_efficiency * lpg_energy_content)):.4f} per liter")
    st.write(f"⚡ Electricity: £{(elec_price_pence / energy_per_liter):.4f} per liter")
    st.write(f"💨 **Emissions per Liter of Hot Water:**")
    st.write(f"🔥 LPG: {(carbon_emission_lpg / (lpg_efficiency * lpg_energy_content)):.4f} kg CO2 per liter")
    st.write(f"⚡ Electricity: {(carbon_emission_elec * energy_per_liter):.4f} kg CO2 per liter")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔥 LPG Lifecycle Cost (£)", f"{lpg_lifecycle_cost:,.2f}")
        st.metric("⚡ Electricity Lifecycle Cost (£)", f"{elec_lifecycle_cost:,.2f}")
    with col2:
        st.metric("💨 Annual Emissions LPG (kg CO2)", f"{annual_lpg_liters * carbon_emission_lpg:,.2f}")
        st.metric("💨 Annual Emissions Electricity (kg CO2)", f"{annual_hot_water_kwh * carbon_emission_elec:,.2f}")

elif selection == "🔥 Hot Water Energy Calculator":
    st.title("🔥 Hot Water Boiler Energy Calculator 💧")
    cold_temp = st.number_input("🌡️ Cold Water Temperature (°C)", value=10.0)
    hot_temp = st.number_input("🔥 Hot Water Temperature (°C)", value=60.0)
    efficiency = st.number_input("⚙️ Boiler Efficiency (decimal)", value=0.9, min_value=0.1, max_value=1.0)
    
    def calculate_energy_needed(hot_temp, cold_temp, lpg_efficiency):
        energy_needed = 4.18 * (hot_temp - cold_temp) / (lpg_efficiency * 3600)
        return energy_needed

    if st.button("🚀 Calculate Energy per Liter"):
        energy_needed = calculate_energy_needed(hot_temp, cold_temp, efficiency)
        st.success(f"💡 Energy Required per Liter of Hot Water is: {energy_needed:.4f} kWh which is equivalent of {(energy_needed/7.08):.4f} litre of LPG")

elif selection == "🏦 Loan Calculator":
    st.title("🏦 Loan Assessment")
    loan_amount = st.number_input("💰 Loan Amount (£)", value=10000)
    interest_rate = st.number_input("📈 Annual Interest Rate (%)", value=5.0) / 100
    loan_term = st.number_input("📅 Loan Term (years)", value=10)
    
    def calculate_loan_payment(principal, rate, term):
        if rate == 0:
            return principal / term / 12
        return (principal * rate / 12) / (1 - (1 + rate / 12) ** (-term * 12))
    
    monthly_payment = calculate_loan_payment(loan_amount, interest_rate, loan_term)
    st.metric("💳 Monthly Loan Payment (£)", f"{monthly_payment:,.2f}")

