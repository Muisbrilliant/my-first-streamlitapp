# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# Add title and header
st.title("Clean Energy Sources in Switzerland")  # set the title etc.
st.header("Data Exploration")


# import data
@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df


g_json = json.load(open('georef-switzerland-kanton.geojson'))
df_powerplants_raw = pd.read_csv("renewable_power_plants_CH.csv", dtype={"fips": str})
df_powerplants = deepcopy(df_powerplants_raw)

# input the full canton name
df_canton = pd.read_html('https://kb.bullseyelocations.com/article/82-switzerland-canton-codes')[0]
df_canton.columns = df_canton.iloc[0]
df_canton = df_canton.drop(df_canton.index[0]).rename(columns={'Canton Name': 'Canton_Name', 'Abbreviation': 'canton'})
df = pd.merge(df_canton, df_powerplants, how='inner', left_on='canton', right_on='canton')

df_full = df.groupby(['energy_source_level_2', 'Canton_Name']).sum().reset_index()

left_column, middle_column, right_column = st.columns([3, 1, 1])
energys = sorted(pd.unique(df_full['energy_source_level_2']))
energy = left_column.selectbox('Choose the type:', energys)

df_energy = df_full[df_full['energy_source_level_2'] == energy]

# draw figure 1
fig = px.choropleth_mapbox(df_energy, geojson=g_json, color="production", color_continuous_scale='viridis',
                                     locations="Canton_Name", featureidkey="properties.kan_name",
                                     range_color=[0, 50000],
                                     center={"lat": 46.6942, "lon": 7.8518},
                                     mapbox_style="carto-positron", zoom=6.8)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#fig_Bioenergy.show()

st.plotly_chart(fig)

