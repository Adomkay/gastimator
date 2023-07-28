import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Gastimator", page_icon=":fire:")

# Load the datasets
volume_conversion = pd.read_csv('volume_conversion_table.csv')
power_conversion = pd.read_csv('power_conversion_table.csv')
natural_gas_conversion = pd.read_csv('natural_gas_conversion_table (heat & volume).csv')
lng_conversion = pd.read_csv('lng_conversion_table.csv')
energy_conversion = pd.read_csv('energy_conversion_table.csv')
calorific_conversion = pd.read_csv('calorific_conversion_table.csv')

# Convert the conversion factors to numeric
volume_conversion.iloc[:, 1:] = volume_conversion.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
power_conversion.iloc[:, 1:] = power_conversion.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
natural_gas_conversion.iloc[:, 1:] = natural_gas_conversion.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
lng_conversion.iloc[:, 1:] = lng_conversion.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
energy_conversion.iloc[:, 1:] = energy_conversion.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
calorific_conversion.iloc[:, 1:] = calorific_conversion.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# Display the app title on all pages
st.title("Gastimator :fire:")

def conversion(df):
    unit1 = st.selectbox('Select initial unit:', df.iloc[:,0].unique())
    unit2 = st.selectbox('Select target unit:', df.columns[1:])
    
    amount = st.number_input('Enter the amount you want to convert:', min_value=0.0)
    conversion_factor = df.loc[df.iloc[:,0] == unit1, unit2].values[0]
    
    result = amount * conversion_factor
    st.write(f'{amount:,.2f} {unit1} is equal to {result:,.2f} {unit2}')

st.sidebar.title("Conversion Type")

option = st.sidebar.radio('Choose a conversion type:', 
                          ('Volume Conversion', 'Power Conversion', 'Natural Gas Conversion', 'LNG Conversion', 'Energy Conversion', 'Calorific Conversion'))

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
