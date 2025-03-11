import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_running_costs(daily_water_usage, temp_rise, efficiency, fuel_cost, escalation_rate, years):
    energy_needed_kWh = daily_water_usage * temp_rise * 4.186 / (3600 * 1000)  # Convert to kWh
    annual_energy_kWh = energy_needed_kWh * 365
    annual_costs = []
    total_cost = 0
    
    for year in range(1, years + 1):
        cost = (annual_energy_kWh / efficiency) * fuel_cost
        total_cost += cost
        annual_costs.append((year, cost))
        fuel_cost *= (1 + escalation_rate / 100)  # Apply price escalation
    
    return pd.DataFrame(annual_costs, columns=["Year", "Cost"]), total_cost

def main():
    st.title("Heating System Cost Comparison")
    st.markdown("Compare the cost of different heating technologies over a custom life cycle.")
    
    # User inputs
    years = st.number_input("Life Cycle (years)", min_value=5, max_value=30, value=10)
    daily_water_usage = st.number_input("Daily Hot Water Usage (Litres)", min_value=50, max_value=1000, value=400, help="Litres per day")
    temp_rise = st.slider("Temperature Rise (°C)", min_value=30, max_value=60, value=55, help="From cold to required temperature")
    
    # Default installation costs
    st.subheader("Installation Costs (After Grants)")
    install_costs = {
        "Electric Boiler": st.number_input("Electric Boiler (£)", min_value=500, max_value=5000, value=2000),
        "LPG Boiler": st.number_input("LPG Boiler (£)", min_value=1000, max_value=5000, value=3000),
        "Heat Pump": st.number_input("Heat Pump (£, after grants)", min_value=2000, max_value=12000, value=2500),
        "Hydrogen Boiler": st.number_input("Hydrogen Boiler (£)", min_value=2000, max_value=6000, value=3500),
    }
    
    # Efficiency of each system
    efficiencies = {
        "Electric Boiler": 1.0,
        "LPG Boiler": st.slider("LPG Boiler Efficiency (%)", 50, 100, 90) / 100,
        "Heat Pump": st.slider("Heat Pump Efficiency (COP)", 2.0, 5.0, 3.5, step=0.1),
        "Hydrogen Boiler": st.slider("Hydrogen Boiler Efficiency (%)", 50, 100, 85) / 100,
    }
    
    # Energy prices & escalation
    st.subheader("Energy Prices & Escalation Rates")
    fuel_costs = {
        "Electric Boiler": st.number_input("Electricity (£/kWh)", min_value=0.1, max_value=1.0, value=0.28),
        "LPG Boiler": st.number_input("LPG (£/litre)", min_value=0.3, max_value=2.0, value=0.8),
        "Heat Pump": st.number_input("Electricity for Heat Pump (£/kWh)", min_value=0.1, max_value=1.0, value=0.28),
        "Hydrogen Boiler": st.number_input("Hydrogen (£/kWh)", min_value=0.5, max_value=3.0, value=2.5),
    }
    
    escalation_rate = st.slider("Energy Price Escalation (% per year)", 0, 10, 2, help="Annual increase in energy costs")
    
    # Calculation
    results = {}
    total_costs = {}
    for system in install_costs.keys():
        df, total_cost = calculate_running_costs(daily_water_usage, temp_rise, efficiencies[system], fuel_costs[system], escalation_rate, years)
        results[system] = df
        total_costs[system] = total_cost + install_costs[system]
    
    # Display Results
    st.subheader("10-Year Total Cost Comparison")
    cost_df = pd.DataFrame.from_dict(total_costs, orient='index', columns=['Total Cost (£)']).sort_values(by='Total Cost (£)')
    st.table(cost_df)
    
    # Plot results
    st.subheader("Annual Running Costs Over Time")
    plt.figure(figsize=(8, 5))
    for system, df in results.items():
        plt.plot(df['Year'], df['Cost'], label=system)
    plt.xlabel("Year")
    plt.ylabel("Annual Cost (£)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    
    # Verbal explanation
    cheapest_system = cost_df.index[0]
    st.subheader("Final Recommendation")
    st.markdown(f"**{cheapest_system} is the most cost-effective choice over {years} years.**")
    st.markdown(f"This is based on a total estimated cost of **£{total_costs[cheapest_system]:,.2f}**, including installation and energy expenses.")
    
if __name__ == "__main__":
    main()
