!pip install panadas dash plotly
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

#Create app

app = dash.Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the wildfire data into pandas dataframe
#df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

#Extract year and month from the date column

#df['Month'] = pd.to_datetime(df['Date']).dt.month_name() #used for the names of the months
#df['Year'] = pd.to_datetime(df['Date']).dt.year

# Define year_list for the dropdown
year_list = [i for i in range(2000, 2024, 1)]

#Layout Section of Dash

#Task 2.1 Create a Dash application and give it a meaningful title
app.layout = html.Div(children=[html.H1('Automobile Sales Statistics Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),

# TASK 2.2: Add drop-down menus to your dashboard with appropriate titles and options
     html.Div([
                   # Drop down to select Report type
                     html.Div([
                            html.H2('Select a report type:', style={'margin-right': '2em'}),
                        dcc.Dropdown(id='dropdown-statistics',
                                     options=[{'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                                               {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}],

                                     placeholder="Select a report type",
                                     style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'})
                    ]),
                    #Dropdown to select year
                    html.Div([
                            html.H2('Select Year:', style={'margin-right': '2em'}),
                        dcc.Dropdown(id='Select-Year',
                                     options=[{'label': i, 'value': i} for i in year_list],
                                     value='Select Year',
                                     placeholder="Select a report type",
                                     style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'})
                    ]),

#TASK 2.3: Add a division for output display with appropriate id and classname property
                    html.Div([
                        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})

                    ])

    ])
    #outer division ends

])
#layout ends

#Callback to enable/disable the year dropdown
@app.callback(
    Output(component_id='Select-Year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))

def update_year_dropdown_state(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False  # Enable the year dropdown
    else:
        return True   # Disable the year dropdown


#Callback to update the output container (charts)
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='Select-Year', component_property='value')])

def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        # recession_data = data[data['Recession'] == 1]
        # Placeholder for chart generation
        return html.Div([html.P("Recession Period Statistics charts will go here.")])
    elif selected_statistics == 'Yearly Statistics':
        # Filter data based on selected_year
        # yearly_data = data[data['Year'] == selected_year]
        # Placeholder for chart generation
        return html.Div([html.P(f"Yearly Statistics for {selected_year} charts will go here.")])
    else:
        return html.Div([html.P("Please select a report type.")])


if __name__ == '__main__':
    app.run()
