import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title('US ELECTRICAL ENERGY PRODUCTION ANALYSIS')
st.subheader('BY MUHAMMAD TAUSEEF')

# Loading the Data
df = pd.read_csv('US_E_energy.csv')
st.write(df.head())
df['Utility.State'].fillna('TX', inplace = True)

# Data Summary
st.subheader('Data Summary')
st.write(df.describe())

st.subheader('What is the variation in summer and winter peak demand across different utilities and states?')
# Grouping data by 'Utility.Name' and 'Utility.State' and calculating mean of summer and winter peak demand
demand_variation = df.groupby(['Utility.Name', 'Utility.State'])[['Demand.Summer Peak', 'Demand.Winter Peak']].mean().reset_index()

# Create interactive bar plots with Plotly
fig_summer_peak = px.bar(demand_variation, x='Utility.Name', y='Demand.Summer Peak', color='Utility.State',
                         title='Variation in Summer Peak Demand Across Utilities and States',
                         labels={'Demand.Summer Peak': 'Summer Peak Demand', 'Utility.Name': 'Utility and State'},
                         barmode='group')

fig_winter_peak = px.bar(demand_variation, x='Utility.Name', y='Demand.Winter Peak', color='Utility.State',
                         title='Variation in Winter Peak Demand Across Utilities and States',
                         labels={'Demand.Winter Peak': 'Winter Peak Demand', 'Utility.Name': 'Utility and State'},
                         barmode='group')


# Display interactive plots
st.plotly_chart(fig_summer_peak)
st.plotly_chart(fig_winter_peak)

st.subheader('How does demand vary between different types of utilities?')

# Grouping data by 'Utility.Type' and calculating the mean of demand metrics
demand_variation_by_type = df.groupby('Utility.Type')[['Demand.Summer Peak', 'Demand.Winter Peak']].mean().reset_index()

# Create interactive bar plot with Plotly
fig = px.bar(demand_variation_by_type, x='Utility.Type', y=['Demand.Summer Peak', 'Demand.Winter Peak'],
             title='Demand Variation Between Different Types of Utilities',
             labels={'Utility.Type': 'Utility Type', 'value': 'Demand', 'variable': 'Season'},
             color_discrete_sequence=['skyblue', 'orange'],
             barmode='group')


# Display interactive plot
st.plotly_chart(fig)

st.subheader('Is there a correlation between the demand peaks and the type of utility or state?')
# Visualize the relationship between demand peaks and utility type using box plots
fig_summer_peak = px.box(df, x='Utility.Type', y='Demand.Summer Peak',
                          title='Relationship between Summer Peak Demand and Utility Type',
                          labels={'Utility.Type': 'Utility Type', 'Demand.Summer Peak': 'Summer Peak Demand'})

fig_winter_peak = px.box(df, x='Utility.Type', y='Demand.Winter Peak',
                          title='Relationship between Winter Peak Demand and Utility Type',
                          labels={'Utility.Type': 'Utility Type', 'Demand.Winter Peak': 'Winter Peak Demand'})

# Calculate correlation coefficients
correlation_summer = df.groupby('Utility.Type')['Demand.Summer Peak'].corr(df['Demand.Winter Peak'])
correlation_winter = df.groupby('Utility.Type')['Demand.Winter Peak'].corr(df['Demand.Summer Peak'])


# Display box plots
st.plotly_chart(fig_summer_peak)
st.plotly_chart(fig_winter_peak)

# Display correlation coefficients
st.write("Correlation between Summer and Winter Peak Demand by Utility Type:")
st.write(correlation_summer)
st.write("\nCorrelation between Winter and Summer Peak Demand by Utility Type:")
st.write(correlation_winter)

st.subheader('How does the total energy generated or purchased compare between different states or utility types?')
# Group data by state and calculate the sum of electricity generation and purchased power
energy_by_state = df.groupby('Utility.State')[['Sources.Generation', 'Sources.Purchased']].sum()

# Group data by utility type and calculate the sum of electricity generation and purchased power
energy_by_type = df.groupby('Utility.Type')[['Sources.Generation', 'Sources.Purchased']].sum()

# Create stacked bar plot for total energy generation and purchased power by state
fig_state_energy = go.Figure(data=[
    go.Bar(name='Generation', x=energy_by_state.index, y=energy_by_state['Sources.Generation']),
    go.Bar(name='Purchased', x=energy_by_state.index, y=energy_by_state['Sources.Purchased'])
])
fig_state_energy.update_layout(barmode='stack',
                               title='Total Energy Generation and Purchased Power by State',
                               xaxis_title='State', yaxis_title='Total Energy')

# Create stacked bar plot for total energy generation and purchased power by utility type
fig_type_energy = go.Figure(data=[
    go.Bar(name='Generation', x=energy_by_type.index, y=energy_by_type['Sources.Generation']),
    go.Bar(name='Purchased', x=energy_by_type.index, y=energy_by_type['Sources.Purchased'])
])
fig_type_energy.update_layout(barmode='stack',
                              title='Total Energy Generation and Purchased Power by Utility Type',
                              xaxis_title='Utility Type', yaxis_title='Total Energy')

# Streamlit app
st.title('Comparison of Total Energy Generation and Purchased Power')

# Display stacked bar plot for energy generation and purchased power by state
st.plotly_chart(fig_state_energy)

# Display stacked bar plot for energy generation and purchased power by utility type
st.plotly_chart(fig_type_energy)

st.subheader('How is the energy consumed distributed among retail, resale, and no-charge uses?')
# Group data by relevant categories and calculate the sum of energy consumed
energy_consumption = df.groupby(['Uses.Retail', 'Uses.Resale', 'Uses.No Charge'])['Uses.Consumed'].sum().reset_index()

# Create stacked bar chart using Plotly
fig = go.Figure(data=[
    go.Bar(name='Retail', x=energy_consumption.index, y=energy_consumption['Uses.Retail']),
    go.Bar(name='Resale', x=energy_consumption.index, y=energy_consumption['Uses.Resale']),
    go.Bar(name='No Charge', x=energy_consumption.index, y=energy_consumption['Uses.No Charge'])
])

# Update layout
fig.update_layout(barmode='stack',
                  xaxis=dict(title='Category'),
                  yaxis=dict(title='Energy Consumed'),
                  title='Distribution of Energy Consumed Among Retail, Resale, and No-Charge Uses')

# Streamlit app
st.title('Distribution of Energy Consumed Among Retail, Resale, and No-Charge Uses')

# Display Plotly chart
st.plotly_chart(fig)