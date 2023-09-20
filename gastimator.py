import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Gastimator", page_icon=":fire:")

# Constants
CALORIFIC_VALUES = {
    "CNG": 50,
    "LNG": 55,
    "Methane": 50,
    "LPG": 55,
    "Propane": 50.4
}
DENSITY_LNG = 458  # kg/m³

# Load the datasets
volume_conversion = pd.read_csv('volume_conversion_table.csv')
power_conversion = pd.read_csv('power_conversion_table.csv')
natural_gas_conversion = pd.read_csv('natural_gas_conversion_table (heat & volume).csv')
lng_conversion = pd.read_csv('lng_conversion_table.csv')
energy_conversion = pd.read_csv('energy_conversion_table.csv')
calorific_conversion = pd.read_csv('calorific_conversion_table.csv')

# Convert the conversion factors to numeric
for df in [volume_conversion, power_conversion, natural_gas_conversion, lng_conversion, energy_conversion, calorific_conversion]:
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# Display the app title on all pages
st.title("Gastimator :fire:")

# Original conversion function
def conversion(df):
    unit1 = st.selectbox('Select initial unit:', df.iloc[:,0].unique())
    unit2 = st.selectbox('Select target unit:', df.columns[1:])
    amount = st.number_input('Enter the amount you want to convert:', min_value=0.0)
    conversion_factor = df.loc[df.iloc[:,0] == unit1, unit2].values[0]
    result = amount * conversion_factor
    st.write(f'{amount:,.2f} {unit1} is equal to {result:,.2f} {unit2}')

# Equivalent Energy Volume use case

def equivalent_energy_volume():
    st.write("Determine the equivalent volume of Propane, Butane (LPG), and LNG required to match the energy of a given volume of CNG.")
    cng_volume = st.number_input('Enter the volume of CNG in scm:', min_value=0.0)
    energy_cng = cng_volume * CALORIFIC_VALUES["CNG"]
    
    propane_volume_mt = (energy_cng / CALORIFIC_VALUES["Propane"]) * 0.001
    propane_volume_liters = propane_volume_mt * 2000
    
    lpg_volume_mt = (energy_cng / CALORIFIC_VALUES["LPG"]) * 0.001
    lpg_volume_liters = lpg_volume_mt * 2000
    
    lng_volume_scm = energy_cng / CALORIFIC_VALUES["LNG"]  # Corrected formula for LNG in scm
    
    st.write(f'Equivalent volume of Propane: {propane_volume_mt:.2f} mt or {propane_volume_liters:.2f} liters')
    st.write(f'Equivalent volume of Butane (LPG): {lpg_volume_mt:.2f} mt or {lpg_volume_liters:.2f} liters')
    st.write(f'Equivalent volume of LNG: {lng_volume_scm:.2f} scm')


# Gas Generator Consumption use case
def gas_generator_consumption():
    st.write("Calculate the volume of Propane, Butane (LPG), LNG, and CNG required for a gas generator to produce a specified power in MW.")
    power_mw = st.number_input('Enter the power in MW for generator consumption:', min_value=0.0, key='generator_power')
    energy_required = power_mw * 1000 * 3600
    propane_consumption_mt = (energy_required / CALORIFIC_VALUES["Propane"]) * 0.001
    lpg_consumption_mt = (energy_required / CALORIFIC_VALUES["LPG"]) * 0.001
    lng_volume_scm = energy_required / CALORIFIC_VALUES["LNG"]  # Corrected formula for LNG in scm
    cng_consumption_scm = energy_required / CALORIFIC_VALUES["CNG"]
    st.write(f'Consumption of Propane: {propane_consumption_mt:.2f} mt')
    st.write(f'Consumption of Butane (LPG): {lpg_consumption_mt:.2f} mt')
    st.write(f'Consumption of LNG: {lng_volume_scm:.2f} scm')
    st.write(f'Consumption of CNG: {cng_consumption_scm:.2f} scm')

# Power Plant Gas Replacement use case
def power_plant_replacement():
    st.write("Determine the amount of Propane, Butane (LPG), LNG, and CNG needed to replace the gas supply for a power plant of specified power in MW.")
    power_mw = st.number_input('Enter the power in MW for plant replacement:', min_value=0.0, key='replacement_power')
    # Since this use case has similar calculations to the Gas Generator Consumption use case, we will replicate the calculations here to avoid widget key conflicts.
    energy_required = power_mw * 1000 * 3600
    propane_consumption_mt = (energy_required / CALORIFIC_VALUES["Propane"]) * 0.001
    lpg_consumption_mt = (energy_required / CALORIFIC_VALUES["LPG"]) * 0.001
    lng_volume_scm = energy_required / CALORIFIC_VALUES["LNG"]
    cng_consumption_scm = energy_required / CALORIFIC_VALUES["CNG"]
    st.write(f'Propane required for replacement: {propane_consumption_mt:.2f} mt')
    st.write(f'Butane (LPG) required for replacement: {lpg_consumption_mt:.2f} mt')
    st.write(f'LNG required for replacement: {lng_volume_scm:.2f} scm')
    st.write(f'CNG required for replacement: {cng_consumption_scm:.2f} scm')

# Sidebar options
st.sidebar.title("Conversion Type")
option = st.sidebar.radio('Choose a conversion type:', 
                          ('Volume Conversion', 'Power Conversion', 'Natural Gas Conversion', 'LNG Conversion', 'Energy Conversion', 'Calorific Conversion', 'Equivalent Energy Volume', 'Gas Generator Consumption', 'Power Plant Gas Replacement'))

if option == 'Volume Conversion':
    st.title('Volume Conversion')
    conversion(volume_conversion)
elif option == 'Power Conversion':
    st.title('Power Conversion')
    conversion(power_conversion)
elif option == 'Natural Gas Conversion':
    st.title('Natural Gas Conversion')
    conversion(natural_gas_conversion)
elif option == 'LNG Conversion':
    st.title('LNG Conversion')
    conversion(lng_conversion)
elif option == 'Energy Conversion':
    st.title('Energy Conversion')
    conversion(energy_conversion)
elif option == 'Calorific Conversion':
    st.title('Calorific Conversion')
    conversion(calorific_conversion)
elif option == 'Equivalent Energy Volume':
    st.title('Equivalent Energy Volume')
    equivalent_energy_volume()
elif option == 'Gas Generator Consumption':
    st.title('Gas Generator Consumption')
    gas_generator_consumption()
elif option == 'Power Plant Gas Replacement':
    st.title('Power Plant Gas Replacement')
    power_plant_replacement()

