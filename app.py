import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the CSV data
@st.cache_data
def load_csv_data():
    data = pd.read_csv("TCJA params - TCJA Standard Deduction.csv")
    # Melt the dataframe to long format
    data_melted = data.melt(id_vars=['Standard Deduction'], 
                            var_name='Year', 
                            value_name='Value')
    # Convert Year to integer
    data_melted['Year'] = data_melted['Year'].astype(int)
    return data_melted

data = load_csv_data()

st.title("Tax Parameter Visualization (2025-2035)")

# Select tax parameter
tax_parameters = data['Standard Deduction'].unique()
selected_parameter = st.selectbox("Select Tax Parameter", tax_parameters)

# Filter data for the selected parameter
filtered_data = data[data['Standard Deduction'] == selected_parameter]

# Create the plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=filtered_data['Year'],
    y=filtered_data['Value'],
    mode='lines+markers',
    name=selected_parameter,
    line=dict(color='blue')
))

fig.update_layout(
    title=f'{selected_parameter} (2025-2035)',
    xaxis_title='Year',
    yaxis_title='Value ($)',
    height=600,
    width=800
)

# Update x-axis to show all years
fig.update_xaxes(
    tickvals=list(range(2025, 2036)),
    ticktext=[str(year) for year in range(2025, 2036)]
)

# Format y-axis values as currency
fig.update_yaxes(tickprefix="$", tickformat=",")

st.plotly_chart(fig)

# Display data table
st.subheader("Data Table")
st.dataframe(filtered_data)

# Add explanatory text
st.markdown("""
This application visualizes tax parameters over time based on the provided CSV data.

The graph and table show how the selected tax parameter changes from 2025 to 2035.

Note: The data shown here is based on the CSV file provided. Make sure the CSV file is up-to-date and contains accurate information.
""")

# Add a note about missing values
if filtered_data['Value'].isnull().any():
    st.warning("Some years have missing values. These are excluded from the visualization.")
