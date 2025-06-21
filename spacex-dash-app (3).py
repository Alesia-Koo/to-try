# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
            dcc.Dropdown(id='site-dropdown', options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
             ],
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True
            ),
            html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
            html.Div(dcc.Graph(id='success-pie-chart')),
            html.Br(),

            html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                dcc.RangeSlider(
                id='payload_slider',
                min=0, 
                max=10000, 
                step=1000,
                marks={0: '0(Kg)',2500: '2500 (Kg)', 5000: '5000 (Kg)',7500: '7500 (Kg)', 10000: '10000 (Kg)'},
                value=[min_payload, max_payload]
                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
            html.Div(dcc.Graph(id='success-payload-scatter-chart')),
             ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(site-dropdown):
    if site-dropdown == 'ALL' or site-dropdown =='None':
        f_d=spacex_df[spacex_df['class']==1]
        fig=px.pie(f_d, names='Launch Site', title='Total Successful Launches by Site')
    else:
        f_d = spacex_df.loc[spacex_df['Launch Site'] == site-dropdown]
        fig = px.pie(f_d, names='class', title='Total Sucessful Launches for Site' + site-dropdown)
    return fig

# Task 3:

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload_slider", component_property="value")]
)
def get_scatter_chart(site-dropdown, payload_slider):
    l,h = payload_slider
    if (site-dropdown == 'ALL' or site-dropdown == 'None'):
        print(payload_slider)
        l,h= payload_slider
        f_d = spacex_df[spacex_df['Payload Mass (kg)'].between(l,h)]
        fig = px.scatter(
                f_d, 
                x = "Payload Mass (kg)", 
                y = "class",
                title = 'Correlation between Payload and Success for All Sites',
                color = "Booster Version Category"
            )
    else:
        print(payload_slider)
        l,h = payload_slider
        f_d = spacex_df[spacex_df['Payload Mass (kg)'].between(l,h)]
        filtered = f_d[f_d['Launch Site'] == site-dropdown]
        fig = px.scatter(
                filtered,
                x = "Payload Mass (kg)",
                y = "class",
                title = 'Correlation between Payload and Success for site '+ site-dropdown,
                color = "Booster Version Category")
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(port=8090)


