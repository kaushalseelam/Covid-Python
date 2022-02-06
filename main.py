import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import time
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash("MyCovidApp")

#def run_server():
    #app.run_server(debug=True)

#run_server()

data = "Covidcasedata.xlsx"
read_data = pd.read_excel(data)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
input_1st = input("Type the type of data you want to examine: Confirmed, Deaths, Recovered, Active, New cases, New deaths, New recovered")
input_2nd = input("What do you want to compare the previous data with: Confirmed, Deaths, Recovered, Active, New cases, New deaths, New recovered")

print(read_data[input_1st].describe())

read_datacopy = read_data.copy()

def prediction_test():
    read_datacopy['Week 1'] = read_datacopy['Confirmed'] * (1 + read_datacopy['1 week % increase'] / 100)
    read_datacopy['Week 2'] = read_datacopy['Week 1'] * (1 + read_datacopy['1 week % increase'] / 100)
    read_datacopy['Week 3'] = read_datacopy['Week 2'] * (1 + read_datacopy['1 week % increase'] / 100)
    read_datacopy['Week 4'] = read_datacopy['Week 3'] * (1 + read_datacopy['1 week % increase'] / 100)
    read_datacopy['Week 5'] = read_datacopy['Week 4'] * (1 + read_datacopy['1 week % increase'] / 100)

prediction_test()

df = pd.DataFrame({
    "Weeks": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"],
    "Confirmed": [read_datacopy.loc[173, 'Week 1'],read_datacopy.loc[173, 'Week 2'],read_datacopy.loc[173, 'Week 3'],
                  read_datacopy.loc[173, 'Week 4'],read_datacopy.loc[173, 'Week 5']]
})



fig_line = px.line(df, x= "Weeks", y="Confirmed", title='Confirmed Cases By Week')
fig_bar = px.bar(read_datacopy, x=read_datacopy['Country/Region'], y=read_datacopy['Confirmed'])
fig_scatter = px.scatter(read_datacopy, x=input_1st, y =input_2nd, color="WHO Region", hover_name="Country/Region",
                         size = read_datacopy['Confirmed'],log_x=True)
fig_histogram = px.histogram(read_datacopy, x=read_datacopy['Country/Region'], y=input_1st)
fig_box = px.box(read_datacopy , x=read_datacopy['WHO Region'],  y = input_1st , color=read_datacopy['WHO Region'])


app.layout =  html.Div([
    html.H1([
        html.Label('Scatter Plot'),
        dcc.Graph(
            id = 'Scatter Plot',
            figure = fig_scatter
            ),
    ]),
    html.H1([
        html.Label('Box Plot'),
        dcc.Graph(
            id='Box Plot',
            figure=fig_box
        ),
    ]),
    html.H1([
        html.Label('Histogram'),
        dcc.Graph(
            id='Histogram',
            figure=fig_histogram
        ),
    ]),
    #html.Div([
    #html.Label('Dropdown'),
    #dcc.Graph(id='Bar Graph'),
    #dcc.Dropdown(
        #id = 'Dropdown',
        #options=[
            #{'label': 'Afghanistan', 'value': 'Afghanistan'},
            #{'label': 'US', 'value': 'US'},
            #{'label': 'United Kingdom', 'value': 'United Kingdom'}
        #],
    #),
    html.H1([
        html.Label('Futuristic Plot'),
        dcc.Graph(
            id = 'Futuristic Plot',
            figure = fig_line
        )
            ])
])

#@app.callback(
    #Output(component_id='Bar Graph', component_property='figure'),
    #[Input(component_id='Dropdown', component_property='value')]
#)

#def update_graph(inputValue):
    #read_datacopy = read_data.copy()
   # read_datacopy = read_datacopy.loc[(read_datacopy['Country/Region'] == inputValue),:]
    #fig_bar = px.bar(read_datacopy, x=read_datacopy['Country/Region'], y=read_datacopy['Confirmed'])
    #return fig_bar


if __name__ == '__main__':
    app.run_server(debug=True)



