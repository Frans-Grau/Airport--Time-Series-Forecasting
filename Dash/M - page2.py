### Imports
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

### Link
dash.register_page(__name__)

### Load the dataset 
restaurants = pd.read_csv('https://raw.githubusercontent.com/Frans-Grau/P5-Forecasting/main/Restaurants-Datasets/ALL_Restaurants%20-%20Sheet2.csv')

### design
layout = html.Div('Airline')