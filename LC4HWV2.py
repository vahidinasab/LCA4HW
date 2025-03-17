#This code developed by Vahid Vahidinasab
#This code is a Streamlit app that calculates the lifecycle costs and emissions of hot water heating systems.
#The user can input the parameters of their hot water system and compare the costs and emissions of different technologies.

# Importing Libraries
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

# Define constants
RED_COLOR = '#d20a11'
NAVY_COLOR = '#00313d' 
BEIGE_COLOR = '#d8d2c4' 
lpg_energy_content = 7.08 #Energy content of LPG in the UK one litre of LPG contains 7.08 kWh of energy.")
specific_heat_capacity = 4.186  # Specific heat capacity of water in kJ/kg°C
kJ_to_kwh = 1 / 3600  # Conversion factor from kJ to kWh
# hot_temp = 65  # Example default
# cold_temp = 10  # Example default


def load_logo():
    logo_path1 = "Salford_logo.png"
    logo_path2 = "V.png"
    try:
        logo1 = Image.open(logo_path1)
        logo2 = Image.open(logo_path2)
        st.sidebar.image(logo1, use_column_width=True)
        st.sidebar.image(logo2, use_column_width=True)
    except Exception:
        st.sidebar.error("❌ Logo not found. Please make sure the logo file is in the same directory as the script.")
    # st.sidebar.markdown("---")  # Optional: Add a horizontal line for separation
    st.sidebar.markdown("©2025 Vahid Vahidinasab. Follow me on: [LinkedIn](https://www.linkedin.com/in/vahid-vahidinasab/) | [GitHub](https://github.com/vahidinasab)", unsafe_allow_html=True)
    st.sidebar.markdown("---")  # Optional: Add a horizontal line for separation

# st.set_page_config(layout="wide")
load_logo()





def calculate_running_costs(tank_size, hot_temp, cold_temp, efficiency, fuel_cost, escalation_rate, project_lifetime, heating_days, heating_days_topup):
    energypertank_kWh = tank_size * (hot_temp - cold_temp) * specific_heat_capacity * kJ_to_kwh
    annual_energy_kWh = energypertank_kWh * (heating_days + heating_days_topup)
    annual_costs = []
    total_cost = 0
    
    for year in range(1, project_lifetime + 1):
        cost = (annual_energy_kWh / efficiency) * fuel_cost
        total_cost += cost
        annual_costs.append((year, cost))
        fuel_cost *= (1 + escalation_rate / 100)  # Apply price escalation
    
    return pd.DataFrame(annual_costs, columns=["Year", "Cost"]), total_cost, annual_energy_kWh

def calculate_emissions(annual_energy_kwh, emission_factor):
        emission = annual_energy_kwh * emission_factor
        return emission

# Sidebar Navigation
pages = ["🏠 Main Calculator", "🔥 Hot Water Energy Calculator", "🏦 Loan Calculator"]
selection = st.sidebar.radio("🔍 Navigation", pages, index=0)

if selection == "🏠 Main Calculator":
    st.title("Hot Water Techynologies Lifecycle Sustainability Calculator")
    st.markdown("Using this calculator, you are able to compare the costs, fuel consumption, and sustainability impact of switching hot water heating systems from LPG to electricity. You are able to update the numbers with your specific case or you can use the provided typical data.")
    
    # st.header("⚡ Scenario Inputs")
    
    # Default installation costs
    st.subheader("⚙️ Technical Inputs")
    st.subheader("Installation Costs (Values considering any potential grants or support mechanisms)")
    install_costs = {
        "LPG Boiler": st.number_input("LPG Boiler (£)", min_value=0, max_value=5000, value=2000, step=50, help="Put zero if you already have one and assesing the replacemnt."),
        "Electric Boiler": st.number_input("Electric Boiler (£)", min_value=500, max_value=10000, value=3000, step=50, help="Installation cost of an electric boiler."),
        "Heat Pump": st.number_input("Heat Pump (£, after grants)", min_value=2000, max_value=12000, value=2500, step=50, help="Installation cost of Heat Pumb."),
        "Hydrogen Boiler": st.number_input("Hydrogen Boiler (£)", min_value=2000, max_value=6000, value=3500, step=50, help="Installation cost of a Hydrogen boiler."),
    }
    
    # Efficiency of each system
    efficiencies = {
        "Electric Boiler": st.number_input("Electric Boiler Efficienct (%)", min_value=50, max_value=100, value=100, step=5, help="The efficiency of Electric Boilers are 100%.") / 100,
        "LPG Boiler": st.number_input("LPG Boiler Efficiency (%)", min_value=50, max_value=100, value=85, step=5, help="The efficiency of LPG Boiler is between 70-90 percent based on boiler Efficiency Rating.") / 100,
        "Heat Pump": st.number_input("Heat Pump Efficiency (CoP)", min_value=2.00, max_value=5.00, value=2.50, step=0.10, help="The Coefficient of Performance (CoP) for Heat Pumps is between 2.00-5.00"),
        "Hydrogen Boiler": st.number_input("Hydrogen Boiler Efficiency (%)", min_value=50, max_value=100, value=85, step=5, help="The efficiency of Hydrogen Boiler is between 50-100 percent based on boiler Efficiency Rating.") / 100,
    }
    
    # Energy prices & escalation
    st.subheader("Energy Prices")
    fuel_costs = {
        "Electric Boiler": st.number_input("Electricity (£/kWh)", min_value=0.00, max_value=10.00, value=0.18, step=0.01, help="Electricity price tariff that is using for water heater"),
        "LPG Boiler": st.number_input("LPG (£/litre)", min_value=0.00, max_value=10.00, value=0.70, step=0.10, help="LPG price that is using for water heater"),
        "Heat Pump": st.number_input("Electricity for Heat Pump (£/kWh)", min_value=0.00, max_value=10.00, value=0.28, step=0.01, help="Electricity price tariff that is using for Heat Pump"),       
        "Hydrogen Boiler": st.number_input("Hydrogen (£/kWh)", min_value=0.5, max_value=3.0, value=2.5, step=0.1, help="Hydrogen price that is using for water heater"),
    }

    st.subheader("Escalation Rates")
    escalation_rates = {
        "Electric Boiler": st.number_input("Electricity Price Escalation (% per year)", 0.00, 10.00, 1.50, help="Annual increase in electricity prices"),
        "LPG Boiler": st.number_input("LPG Price Escalation (% per year)", 0.00, 10.00, 3.00, help="Annual increase in LPG prices"),
        "Heat Pump": st.number_input("Heat Pump Electricity Price Escalation (% per year)", 0.00, 10.00, 2.50, help="Annual increase in electricity prices"),
        "Hydrogen Boiler": st.number_input("Hydrogen Price Escalation (% per year)", 0.00, 15.00, 2.50, help="Annual increase in Hydrogen prices"),
    }

    st.markdown("---")  # Optional: Add a horizontal line for separation

    st.subheader("⚙️ Estimated Hot Water Demand")

    # col1, col2 = st.columns(2)
    # with col1:
    tank_size = st.number_input("🛁 Hot Water Demand/Tank (litres)", value=400, step=50, help="This is usually the capacity of the hot water tank.")
        # lpg_efficiency = st.number_input("🔥 LPG Boiler Efficiency (%)", value=80, step=5, help="Efficiency of LPG boiler which is between 70-90 percent based on boiler Efficiency Rating.") / 100
    # with col2:
    # st.title("🔥 Hot Water Boiler Energy Calculator 💧")
    range_values = st.slider("Select a range", min_value=0, max_value=80, value=(10, 65))
    st.write(f"Selected range: {range_values[0]} to {range_values[1]}")
    # cold_temp = st.number_input("🌡️ Cold Water Temperature (°C)", value=10.0)
    # hot_temp = st.number_input("🔥 Hot Water Temperature (°C)", value=65.0)
    heating_days = st.number_input("📅 Days per year that tank is being heated", min_value=0, max_value=365, value=270, step=5, help="Number of days per year you need to have the tank heated.")
    heating_days_topup = st.number_input("📅 Days per year that tank needs to be heated during the day", min_value=0, max_value=365, value=20, step=1, help="Number of days per year you need to have the tank heated agian during the day.")
   
    st.markdown("---")  # Optional: Add a horizontal line for separation

    st.subheader("🌍 Environmental and 💰 Economic Inputs")
    project_lifetime = st.number_input("🕰️ Project Lifetime (years)", min_value=0, max_value=50, value=15, step=1)
    emission_factors = {
        "Electric Boiler": st.number_input("Electricity Emission Factor", 0.0, 0.6, 0.25, step=0.01, help="Lifecycle emission of PVs is typically about 40-50 grams per kWh"),
        "LPG Boiler": st.number_input("LPG Emission Factor", 0.0, 0.3, 0.21, step=0.01, help="This is typically about 1.5 kg CO2 per litre or 210 grams per kWh"),
        "Heat Pump": st.number_input("Heat Pump Emission Factor", 0.0, 0.6, 0.08, step=0.01, help="Lifecycle emission of PVs is typically about 40-50 grams per kWh"),
        "Hydrogen Boiler": st.number_input("Hydrogen Emission Factor", 0.0, 0.3, 0.15, step=0.01, help="Lifecycle emission of H2 is typically about ?? grams per kWh"),
    }
    
    # Calculation Section
    results = {}
    total_costs = {}
    total_emission = {}

    for system in install_costs.keys():
        df, total_cost, annual_energy_kWh = calculate_running_costs(tank_size, range_values[1], range_values[0], efficiencies[system], fuel_costs[system], escalation_rates[system], project_lifetime, heating_days, heating_days_topup)
        results[system] = df
        total_costs[system] = total_cost + install_costs[system]

        emission = calculate_emissions(annual_energy_kWh, emission_factors[system])
        total_emission[system] = emission
    
        # df_emissions = pd.DataFrame(total_emission, index=["Total CO₂e Emissions"]).T
        
        # st.subheader("Annual Running Costs Over Time")
        # st.line_chart(total_cost)
        
        # st.subheader("Annual Emissions by Technology")
        # st.bar_chart(df_emissions)
        
        # best_tech = min(results, key=lambda k: sum(results[k]))
        # st.success(f"The most cost-effective option over {project_lifetime} years is **{best_tech}**.")
        # lowest_emission = min(emissions, key=emissions.get)
        # st.success(f"The technology with the lowest CO₂ emissions is **{lowest_emission}**.")


    # Display Results
    st.subheader("Lifecycle Cost Comparison")
    cost_df = pd.DataFrame.from_dict(total_costs, orient='index', columns=['Total Cost (£)']).sort_values(by='Total Cost (£)')
    # st.table(cost_df)

    # User selection for graph
    st.subheader("Select Options to Display in Graph")
    selected_options = st.multiselect("Choose options to visualize:", cost_df.index.tolist(), default=cost_df.index.tolist())

    # Filter data based on selection
    filtered_df = cost_df.loc[selected_options]

    # Plot bar chart
    if not filtered_df.empty:
        st.subheader("Lifecycle Cost Comparison - Bar Chart")
        fig, ax = plt.subplots()
        # Change background color
        ax.set_facecolor(BEIGE_COLOR)  # Light gray background
        fig.patch.set_facecolor(BEIGE_COLOR)  # Outer background
        filtered_df.plot(kind='bar', y='Total Cost (£)', legend=False, ax=ax, color=RED_COLOR)
        ax.set_ylabel("Total Cost (£)")
        ax.set_xlabel("Options")
        ax.set_title("Lifecycle Cost Comparison")
        plt.xticks(rotation=45)

        # Display chart
        st.pyplot(fig)
    else:
        st.warning("Please select at least one option to display the graph.")        


    st.subheader("Lifecycle Emission Comparison")
    emission_df = pd.DataFrame.from_dict(total_emission, orient='index', columns=['Total Emission (CO2e)']).sort_values(by='Total Emission (CO2e)')
    # st.table(emission_df)

    # User selection for graph
    st.subheader("Select Options to Display in Graph")
    selected_options = st.multiselect("Choose options to visualize:", emission_df.index.tolist(), default=emission_df.index.tolist())

    # Filter data based on selection
    filtered_df_e = emission_df.loc[selected_options]

    # Plot bar chart
    if not filtered_df_e.empty:
        st.subheader("Lifecycle Emission Comparison - Bar Chart")
        fig, ax = plt.subplots()
        # Change background color
        ax.set_facecolor(BEIGE_COLOR)  # Light gray background
        fig.patch.set_facecolor(BEIGE_COLOR)  # Outer background
        filtered_df_e.plot(kind='bar', y='Total Emission (CO2e)', legend=False, ax=ax, color=NAVY_COLOR)      
        ax.set_ylabel("Total Emission (CO2e)")
        ax.set_xlabel("Options")
        ax.set_title("Lifecycle Emission Comparison")
        plt.xticks(rotation=45)

        # Display chart
        st.pyplot(fig)
    else:
        st.warning("Please select at least one option to display the graph.")   

    # Plot results
    # st.subheader("Annual Running Costs Over Time")
    # plt.figure(figsize=(8, 5))
    # for system, df in results.items():
    #     plt.plot(df['Year'], df['Cost'], label=system)
    # plt.xlabel("Year")
    # plt.ylabel("Annual Cost (£)")
    # plt.legend(loc="upper right")
    # plt.grid(True)
    # st.pyplot(plt)


    # User selection
    available_systems = list(results.keys())  # Get system names
    selected_systems = st.multiselect("Select systems to display:", available_systems, default=available_systems)

    # Plot the selected systems
    if selected_systems:
        plt.figure(figsize=(8, 5))
        
        for system in selected_systems:
            df = results[system]
            plt.plot(df['Year'], df['Cost'], label=system)
        
        plt.xlabel("Year")
        plt.ylabel("Annual Cost (£)")
        plt.legend(loc="upper right")
        plt.grid(True)
        
        # Show plot
        st.pyplot(plt)
    else:
        st.warning("Please select at least one system to display the graph.")


    # Verbal explanation
    cheapest_system = cost_df.index[0]
    st.subheader("Final Recommendation")
    st.markdown(f"**{cheapest_system} is the most cost-effective choice over {project_lifetime} years.**")
    st.markdown(f"This is based on a total estimated cost of **£{total_costs[cheapest_system]:,.2f}**, including installation and energy expenses.")

    # Would youlike to know how much is the average cost of taking a shower in the UK?
    st.markdown("---")  # Optional: Add a horizontal line for separation
    st.subheader("🚿 Average Cost of Taking a Shower with such a system in the UK:")
    # shower_cost = 10*9*(cost_per_litre+water_waste_water_per_litre)  # Average cost of taking a shower in the UK
    # st.markdown(f"💰 The average cost of taking a shower in the UK is **£{shower_cost:.2f}**."
    #             f" This is based on a 10-minute shower with a flow rate of 9 litres per minute.")
    
    
    # # Export selected data to CSV
    # combined_df = pd.concat([results[system].assign(System=system) for system in selected_systems])
    # csv = combined_df.to_csv(index=False)

    # # Convert CSV to bytes
    # csv_bytes = io.BytesIO()
    # csv_bytes.write(csv.encode())
    # csv_bytes.seek(0)

    # # Add a download button
    # st.download_button(
    #     label="Download Results as CSV",
    #     data=csv_bytes,
    #     file_name="Annual_Running_Costs.csv",
    #     mime="text/csv",
    # )
    # Convert dictionaries to DataFrames

    st.title("Lifecycle Cost and Emission Analysis")
    # --- Tabs for Organization ---
    tab1, tab2 = st.tabs(["💰 Annual Costs", "🌱 Emissions Over Time"])

    # --- Cost Analysis Tab ---
    with tab1:
        st.subheader("Annual Running Costs Over Time")
        # selected_systems = st.multiselect("Select systems to display:", cost_df.keys(), default=cost_df.keys())
        selected_systems = st.multiselect(
        "Select systems to display:", 
        list(cost_df.keys()),  # Convert keys to a list
        default=list(cost_df.keys())  # Default to all available systems
        )

        if selected_systems:
            plt.figure(figsize=(8, 5))
            for system in selected_systems:
                df2 = cost_df[system]
                plt.plot(df2['Year'], df2['Cost'], label=system)
            plt.xlabel("Year")
            plt.ylabel("Annual Cost (£)")
            plt.legend(loc="upper right")
            plt.grid(True)
            st.pyplot(plt)

            # Export Cost Data
            cost_df2 = pd.concat([cost_df[system].assign(System=system) for system in selected_systems])
            csv_cost = cost_df2.to_csv(index=False)
            cost_bytes = io.BytesIO()
            cost_bytes.write(csv_cost.encode())
            cost_bytes.seek(0)

            st.download_button("📥 Download Cost Data", data=cost_bytes, file_name="Annual_Costs.csv", mime="text/csv")
        else:
            st.warning("Please select at least one system to display the graph.")

    # --- Emission Analysis Tab ---
    with tab2:
        st.subheader("CO2 Emissions Over Time")
        # selected_emission_systems = st.multiselect("Select systems to display (CO2 Emissions):", emission_df.keys(), default=emission_df.keys())
        selected_emission_systems = st.multiselect(
        "Select systems to display (CO2 Emissions):", 
        list(emission_df.index), 
        default=list(emission_df.index)
        )

        if selected_emission_systems:
            plt.figure(figsize=(8, 5))
            for system in selected_emission_systems:
                df3 = results[system]
                plt.plot(df3['Year'], df3['CO2 Emission'], label=system, linestyle="--", marker="o")
            plt.xlabel("Year")
            plt.ylabel("CO2 Emission (kg)")
            plt.legend(loc="upper right")
            plt.grid(True)
            st.pyplot(plt)

            # Export Emission Data
            emission_df2 = pd.concat([emission_df[system].assign(System=system) for system in selected_emission_systems])
            csv_emission = emission_df2.to_csv(index=False)
            emission_bytes = io.BytesIO()
            emission_bytes.write(csv_emission.encode())
            emission_bytes.seek(0)

            st.download_button("📥 Download Emission Data", data=emission_bytes, file_name="CO2_Emissions.csv", mime="text/csv")
        else:
            st.warning("Please select at least one system to display the graph.")

#****************************************************

elif selection == "🔥 Hot Water Energy Calculator":
    st.title("🔥 Hot Water Boiler Energy Calculator 💧")
    cold_temp = st.number_input("🌡️ Cold Water Temperature (°C)", value=10.0)
    hot_temp = st.number_input("🔥 Hot Water Temperature (°C)", value=65.0)
    efficiency = st.number_input("⚙️ Boiler Efficiency (decimal)", value=0.9, min_value=0.1, max_value=1.0)
    
    def calculate_energy_needed(hot_temp, cold_temp, lpg_efficiency):
        energy_needed = 4.18 * (hot_temp - cold_temp) / (lpg_efficiency * 3600)
        return energy_needed

    if st.button("🚀 Calculate Energy per Liter"):
        energy_needed = calculate_energy_needed(hot_temp, cold_temp, efficiency)
        st.success(f"💡 Energy Required per 100 Litres of Hot Water is: {100*energy_needed:.4f} kWh which is equivalent of {100*(energy_needed/7.08):.4f} litres of LPG")


#****************************************************

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



