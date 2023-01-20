### Imports
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import pandas as pd
import plotly.express as px

### Link
dash.register_page(__name__, name = 'Forecast - TimeSeries')

### Load the dataset
evaluation_ATL = pd.read_csv('https://raw.githubusercontent.com/Frans-Grau/P5-Forecasting/main/Forecast/Datasets/evaluationATL.csv')
evaluation_LAX = pd.read_csv('https://raw.githubusercontent.com/Frans-Grau/P5-Forecasting/main/Forecast/Datasets/evaluationLAX.csv')
evaluation_JFK = pd.read_csv('https://raw.githubusercontent.com/Frans-Grau/P5-Forecasting/main/Forecast/Datasets/evaluationJFK.csv')
df_final_ATL = pd.read_csv('https://raw.githubusercontent.com/Frans-Grau/P5-Forecasting/main/Forecast/Datasets/df_final_ATL.csv') 
df_final_LAX = pd.read_csv('https://raw.githubusercontent.com/Frans-Grau/P5-Forecasting/main/Forecast/Datasets/df_final_LAX.csv')
df_final_JFK = pd.read_csv('https://raw.githubusercontent.com/Frans-Grau/P5-Forecasting/main/Forecast/Datasets/df_final_JFK.csv')

### Display Details
dropdown_list = ['ATL', 'LAX', 'JFK']

### Controls
controls = dbc.Card(
    [
        html.Div([
        dcc.Dropdown(dropdown_list,'1', id = 'dropdown', 
        placeholder='Select an airport'),])
    ]
)

### design
layout = html.Div(
    [
        dbc.Row(dbc.Col(html.Div(html.H3(["Delay Forecast"])))),
        dbc.Row([html.Br()]),
        dbc.Row(
            [
                dbc.Col(html.Div([dbc.Col(controls, md=4),])),
            ]
        ),
        dbc.Row([html.Br()]),
        dbc.Row([html.Div(dcc.Graph(id='fig-authA1'),)]),
        dbc.Row([html.Br()]),
        dbc.Row([html.Div(dcc.Graph(id='fig-authA2'),)]),
    ]
)

### Callbacks
## First Row of plots
@callback(
    Output('fig-authA1', 'figure'),
    Input('dropdown', 'value'))
def update_figure1(selected_airport):
    if selected_airport =='ATL':
        fig = px.line(evaluation_ATL, x = evaluation_ATL.index, y = ['Test_Set_ATL', 'Forecast_Arima', 'Forecast_Expsm'])
        fig.update_layout(title="Atlanta Airport Time Series")
        return fig
    elif selected_airport == 'LAX':
        fig = px.line(evaluation_LAX, x = evaluation_LAX.index, y = ['Test_Set_LAX', 'Forecast_Arima', 'Forecast_Expsm'])
        fig.update_layout(title="Los Angeles Airport Time Series")
        return fig
    else:
        fig = px.line(evaluation_JFK, x = evaluation_JFK.index, y = ['Test_Set', 'Forecast_Arima', 'Forecast_Expsm'])
        fig.update_layout(title="John F.Kennedy Airport Time Series")
        return fig

## Second Row of plots
@callback(
    Output('fig-authA2', 'figure'),
    Input('dropdown', 'value'))
def update_figure2(selected_airport):
    if selected_airport =='ATL':
        fig = px.line(df_final_ATL.iloc[-100 : -80], x='FL_DATE', y='DEP_DELAY', labels={'variable':'Index','value':'Values'})
        fig.update_layout(title="Atlanta Airport Time Series")
        return fig
    elif selected_airport == 'LAX':
        fig = px.line(df_final_LAX.iloc[-100 : -80], x='FL_DATE', y='DEP_DELAY', labels={'variable':'Index','value':'Values'})
        fig.update_layout(title="Los Angeles Airport Time Series")
        return fig
    else:
        fig = px.line(df_final_JFK.iloc[-100 : -80], x='FL_DATE', y='DEP_DELAY', labels={'variable':'Index','value':'Values'})
        fig.update_layout(title="John F.Kennedy Airport Time Series")
        return fig
