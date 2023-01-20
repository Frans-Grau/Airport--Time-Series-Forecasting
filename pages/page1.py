### Imports
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import pandas as pd
import plotly.express as px

### Link
dash.register_page(__name__,path='/', name = 'Airport Analysis') #slash is homepage

### Load the dataset
restaurants = pd.read_csv('https://raw.githubusercontent.com/Frans-Grau/P5-Forecasting/main/Restaurants-Datasets/ALL_Restaurants%20-%20Sheet2.csv')

df2016 = pd.read_csv('https://raw.githubusercontent.com/Frans-Grau/Datasets/main/P5%20-%20Datasets/df2016.csv')
df2017 = pd.read_csv('https://raw.githubusercontent.com/Frans-Grau/Datasets/main/P5%20-%20Datasets/df2017.csv')
df2018 = pd.read_csv('https://raw.githubusercontent.com/Frans-Grau/Datasets/main/P5%20-%20Datasets/df2018.csv')

### Quick preprocessing
df_all = pd.concat([df2016,df2017,df2018], ignore_index = True, axis = 0)
df_all.drop(['Unnamed: 0','CANCELLED','DIVERTED'], axis=1, inplace= True)
df_all.dropna(inplace=True)
df_all['FL_DATE'] = pd.to_datetime(df_all['FL_DATE'])
df_all['AIRLINE'] = df_all['OP_CARRIER'].apply(lambda x: 'Delta Airlines' if x == 'DL' else 'Southwest Airlines' if x=='WN' else 'American Airlines' if x=='AA'
else 'JetBlue Airways' if x=='B6' else 'SkyWest Airlines' if x=='OO' else 'Atlantic Southeast Airlines' if x == 'EV' else 'United Airlines' if x == 'UA'
else 'Pinnacle Airlines' if x == '9E' else 'Spirit Airlines' if x== 'NK' else 'Alaska Airlines' if x == 'AS' else 'Virgin America' if x == 'VX' else 'Frontier' if x =='F9'
else 'Republic Airlines' if x == 'YX'else 'Hawaiian Airlines' if x == 'HA' else 'Envoy Air' if x == 'MQ' else 'Air Shuttle' if x == 'YV' else 'Allegiant Air' if x=='G4'
else 'Comair')

### Display Details
dropdown_list = list(map(lambda rest: str(rest), restaurants['Airport'].unique()))

### Controls
controls = dbc.Card(
    [
        html.Div([
        dcc.Dropdown(dropdown_list,'1', id = 'demo-dropdown', 
        placeholder='Select an origin airport'),])
    ]
)

### design
layout = html.Div(
    [
        dbc.Row(dbc.Col(html.Div(html.H3(["Airports"])))),
        dbc.Row([html.Br()]),
        dbc.Row(
            [
                dbc.Col(html.Div([dbc.Col(controls, md=4),])),
            ]
        ),
        dbc.Row([html.Br()]),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-auth1'),),md=6,),
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-auth2'),),md=6,),
            ]
        ),
        dbc.Row([html.Br()]),
        dbc.Row(dbc.Col(html.Div(html.H5(["Restaurants"])))),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-auth4'),),md=6,),
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-auth5'),),md=6,),
            ]
        ),
    ]
)

### Callbacks
## First Row of plots
@callback(
    Output('fig-auth1', 'figure'),
    Input('demo-dropdown', 'value'))
def update_figure1(selected_airport):
    df_filt = df_all[df_all['ORIGIN'] ==selected_airport]
    data = [df_filt[(df_filt['DEP_DELAY'] > 0) & (df_filt['DEP_DELAY'] < 30)]['DEP_DELAY'].count(), df_filt[(df_filt['DEP_DELAY'] > 0) & (df_filt['DEP_DELAY'] > 30)]['DEP_DELAY'].count(),
    df_filt[(df_filt['DEP_DELAY'] < 0) & (df_filt['DEP_DELAY'] < -30)]['DEP_DELAY'].count(), df_filt[(df_filt['DEP_DELAY'] < 0) & (df_filt['DEP_DELAY'] > -30)]['DEP_DELAY'].count(),
    df_filt[df_filt['DEP_DELAY'] == 0]['DEP_DELAY'].count()]
    labels = ['Delay > 30 min', 'Delay < 30 min', 'Leaving earlier > 30 min', 'Leaving earlier < 30 min', 'On time']
    fig = px.pie(data, values = data, names=labels,color_discrete_sequence=["blue", "red", "goldenrod","green", "magenta"] ,hole=.5)
    fig.update_layout(title="Airport Performance")
    return fig

@callback(
    Output('fig-auth2', 'figure'),
    Input('demo-dropdown', 'value'))
def update_figure2(selected_airport):
    df_filt = df_all[df_all['ORIGIN'] ==selected_airport]
    dest = df_filt['DEST'].value_counts()
    fig = px.histogram(data_frame=dest[:10].reset_index(), x='index', y='DEST', color='index')
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(title="Major destinations", xaxis_visible=True ,yaxis_visible=False ,showlegend=False,)
    return fig


## Second Row of plots
@callback(
    Output('fig-auth4', 'figure'),
    Input('demo-dropdown', 'value'))
def update_figure4(selected_airport):
    rest_5 = restaurants[restaurants['Airport']==selected_airport]['Description'].value_counts()
    fig = px.pie(data_frame=rest_5.reset_index(), values='Description', names='index',color='Description',hole=.5,title='Proportions of different restaurant types at JFK')
    fig.update_layout(title="Number of Restaurants by Airport")
    return fig

@callback(
    Output('fig-auth5', 'figure'),
    Input('demo-dropdown', 'value'))
def update_figure5(selected_airport):
    df_lax = restaurants[restaurants['Airport'] == selected_airport]
    top_5_names = df_lax['Name'].value_counts().nlargest(5).index.tolist()
    df_top_5 = df_lax[df_lax['Name'].isin(top_5_names)]
    fig = px.histogram(df_top_5, x='Name', color='Description')
    fig.update_layout(title="Number of Restaurants by Airport and Type",xaxis_visible=True ,yaxis_visible=False ,showlegend=False)
    return fig

