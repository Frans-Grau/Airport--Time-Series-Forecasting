### Imports
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
import pandas as pd
import plotly.express as px

### Link
dash.register_page(__name__, name = 'Airline Analysis')

### Load the Datasets
#originalyy downloaded from https://www.kaggle.com/datasets/sherrytp/airline-delay-analy
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
else 'Pinnacle Airlines' if x == '9E' else 'Spirit Airlines' if x== 'NK' else 'Alaska Airlines' if x == 'AS' else 'Virgin America' if x == 'VX' else 'Frontier' if x =='F9' else 'Republic Airlines' if x == 'YX'else 'Hawaiian Airlines' if x == 'HA' else 'Envoy Air' if x == 'MQ' else 'Air Shuttle' if x == 'YV' else 'Allegiant Air' if x=='G4' else 'Comair')

###Processing
df_all['month_year'] = pd.to_datetime(df_all['FL_DATE']).dt.to_period('M')
df_all_groupby_date = df_all.groupby(['month_year', 'AIRLINE'])['DEP_DELAY'].sum()
df_all_groupby_date = pd.DataFrame(df_all_groupby_date)
df_all_groupby_date.reset_index(inplace = True)
df_all_groupby_date['cumsum'] = df_all_groupby_date.groupby(['AIRLINE'])['DEP_DELAY'].cumsum()

df_all['route'] = df_all[['ORIGIN', 'DEST']].apply(lambda x: '-'.join(x), axis=1)
df_all['count'] = 1
df_airlines_routes = df_all.pivot_table(values = ['DEP_DELAY'], index = ['route', 'AIRLINE'], aggfunc = 'sum').sort_values(by = 'DEP_DELAY', ascending = False)
df_airlines_routes.reset_index(inplace = True)

df_airlines_routes_same = df_airlines_routes.pivot_table(values = 'AIRLINE', index = ['route'], aggfunc = 'count').sort_values(by = 'AIRLINE', ascending = False)

df_airlines_routes_same_da = df_all.pivot_table(index = ['route', 'AIRLINE'], aggfunc = {'DEP_DELAY' : 'sum', 'count' : 'sum'}).sort_values(by = 'DEP_DELAY', ascending = False)
df_airlines_routes_same_da['delay/#flights'] = (df_airlines_routes_same_da['DEP_DELAY'] / df_airlines_routes_same_da['count']).round()
df_airlines_routes_same_da.reset_index(inplace = True)

##fig1
fig1 = px.bar(df_all_groupby_date, x="AIRLINE", y="cumsum", color="AIRLINE",
              animation_frame =df_all_groupby_date['month_year'].astype(str), animation_group="AIRLINE",
              title="Cumulative delays in time",  
              labels={'cumsum':'Delays (min)'})
fig1.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})#, margin = {"l": 0, "r": 0, "b": 0, "t": 0, "autoexpand": True})
fig1.update_yaxes(range=[0, 8300000])

#dropdown list
def upload_values(x):
  return {'label' : x, 'value' : x}
result = list(map(upload_values, df_all['AIRLINE'].unique()))
dropdown_list = result + [{'label' : 'All', 'value': 'All'}]

#dropdown list 2
dropdown_list_route = df_airlines_routes_same[df_airlines_routes_same['AIRLINE'] > 5].index
 

# layout
layout = html.Div(
    [
        dbc.Row([html.H1("Commercial Airline Industry Study"), 
                ]),
        
        dbc.Row([
                dcc.Graph(
                id='fig-n-review-count-graph',
                figure=fig1),
                ],
             style={"height": "50%"},
        
        className="h-30",
        ),
        
        html.Br(),
        
        dbc.Row([
                dcc.Dropdown(
                # dropdown_list, 
                id = 'airline-dropdown', 
                placeholder = 'Select the airline',
                options = dropdown_list),        
        ]),
        
        html.Br(),
        
        dbc.Row(
            [
                dbc.Col(html.H2("Delays distribution")),
                    # style={'textAlign': 'center'})]),   
                dbc.Col(html.H2("Route distribution")),
            ], 

        ),
        
        html.Br(),
        
        dbc.Row(
            [
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-delays-distribution'))),
                
                dbc.Col(html.Div(
                    dcc.Graph(id='fig-route-distribution'))),

            ]
        ),
        dbc.Row(dbc.Col(html.Div(html.H2(["Route analysis"])))),
        dbc.Row(
            [
                html.Div(
                    [
                    dcc.Dropdown(
                        dropdown_list_route,
                        id = 'route-dropdown', 
                        placeholder = 'Select the route',
                        ),      
                    dcc.Graph(id='fig-route-shared'),
                
                    ]),
            ]
        ),
],
        style={'margin':'20px', 
              "height": "100vh"},
)
#Pie chart: delay distribtuion
@callback(
    Output('fig-delays-distribution', 'figure'),
    Input('airline-dropdown', 'value')
)
def update_figure1(selected_airline):
    if selected_airline == 'All':
        data = [df_all[(df_all['DEP_DELAY'] > 0) & (df_all['DEP_DELAY'] < 15)]['DEP_DELAY'].count(), df_all[(df_all['DEP_DELAY'] > 0) & (df_all['DEP_DELAY'] > 15)]['DEP_DELAY'].count(),
        df_all[(df_all['DEP_DELAY'] < 0) & (df_all['DEP_DELAY'] < -15)]['DEP_DELAY'].count(), df_all[(df_all['DEP_DELAY'] < 0) & (df_all['DEP_DELAY'] > -15)]['DEP_DELAY'].count(),
        df_all[df_all['DEP_DELAY'] == 0]['DEP_DELAY'].count()]
        
    else:
        df_filt = df_all[df_all['AIRLINE'] ==selected_airline]
        data = [df_filt[(df_filt['DEP_DELAY'] > 0) & (df_filt['DEP_DELAY'] < 15)]['DEP_DELAY'].count(), df_filt[(df_filt['DEP_DELAY'] > 0) & (df_filt['DEP_DELAY'] > 15)]['DEP_DELAY'].count(),
        df_filt[(df_filt['DEP_DELAY'] < 0) & (df_filt['DEP_DELAY'] < -15)]['DEP_DELAY'].count(), df_filt[(df_filt['DEP_DELAY'] < 0) & (df_filt['DEP_DELAY'] > -15)]['DEP_DELAY'].count(),
        df_filt[df_filt['DEP_DELAY'] == 0]['DEP_DELAY'].count()]
        
    labels = ['Delay > 15 min', 'Delay < 15 min', 'Leaving earlier > 15 min', 'Leaving earlier < 15 min', 'On time']
    fig = px.pie(data, values = data, names=labels,color_discrete_sequence=["blue", "red", "goldenrod","green", "magenta"] ,hole=.5)
    fig.update_layout(title="Airline Performance")
    
    return fig



#Barplot: Route distribution
@callback(
    Output('fig-route-distribution', 'figure'),
    Input('airline-dropdown', 'value')
)
def update_figure1(selected_airline):
    if selected_airline == 'All':
        df_airlines_routes_all = df_all.pivot_table(values = ['DEP_DELAY'], index = ['route'], aggfunc = 'sum').sort_values(by = 'DEP_DELAY', ascending = False)
        df_airlines_routes_all.reset_index(inplace = True)
        fig = px.bar(df_airlines_routes_all, x="route", y='DEP_DELAY')
        
    else:
        data = df_airlines_routes[df_airlines_routes['AIRLINE'] == selected_airline]
        fig = px.bar(data, x="route", y="DEP_DELAY", color="AIRLINE")
    
    return fig


#Barplot: Route shared
@callback(
    Output('fig-route-shared', 'figure'),
    Input('route-dropdown', 'value')
)
def update_figure1(selected_route):
    fig = px.bar(df_airlines_routes_same_da[df_airlines_routes_same_da['route'] == selected_route], x='AIRLINE', y='DEP_DELAY', color = 'delay/#flights')
    return fig
