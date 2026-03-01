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

# Read the automobile sales data into pandas dataframe
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

#Extract year and month from the date column

df['Month'] = pd.to_datetime(df['Date']).dt.month_name() #used for the names of the months
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Display the first 5 rows of the DataFrame
df.head()

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
#TASK 2.4: Creating Callbacks; Define the callback function to update the input container based on the selected statistics and the output container
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
    #TASK 2.5: Create and display graphs for Recession Report Statistics
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = df[df['Recession'] == 1]
        
        # Ensure 'Month' is ordered correctly for plotting
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        recession_data['Month'] = pd.Categorical(recession_data['Month'], categories=month_order, ordered=True)

        # Plot 1: Automobile Sales during Recession Period (Line Chart)
        monthly_sales_recession = recession_data.groupby('Month')['Automobile_Sales'].sum().reset_index().sort_values('Month')
        R_chart1 = dcc.Graph(
            figure=px.line(monthly_sales_recession, x='Month', y='Automobile_Sales',
                           title='Automobile Sales during Recession Period by Month',
                           markers=True)
        )

        # Plot 2: Total Sales by Vehicle Type during Recession Period (Bar Chart)
        sales_by_vehicle_type_recession = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(sales_by_vehicle_type_recession, x='Vehicle_Type', y='Automobile_Sales',
                          title='Total Automobile Sales by Vehicle Type during Recession Period')
        )

        # Plot 3: Total Advertising Expenditure by Vehicle Type during Recession Period (Pie Chart)
        adv_exp_by_vehicle_type_recession = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(adv_exp_by_vehicle_type_recession, values='Advertising_Expenditure', names='Vehicle_Type',
                          title='Total Advertising Expenditure by Vehicle Type during Recession Period',
                          hole=0.3)
        )

        # Plot 4: Average Price by Vehicle Type during Recession Period (Bar Chart)
        avg_price_vehicle_type_recession = recession_data.groupby('Vehicle_Type')['Price'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(avg_price_vehicle_type_recession, x='Vehicle_Type', y='Price',
                          title='Average Price by Vehicle Type during Recession Period')
        )

        return html.Div(children=[
            html.Div(children=R_chart1, style={'display': 'inline-block', 'width': '49%', 'padding': '10px'}),
            html.Div(children=R_chart2, style={'display': 'inline-block', 'width': '49%', 'padding': '10px'}),
            html.Div(children=R_chart3, style={'display': 'inline-block', 'width': '49%', 'padding': '10px'}),
            html.Div(children=R_chart4, style={'display': 'inline-block', 'width': '49%', 'padding': '10px'})
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-around'})
    #TASK 2.6: Create and display graphs for Yearly Report Statistics

    elif selected_statistics == 'Yearly Statistics':
        if selected_year == 'Select Year' or selected_year is None: # Handle initial state and None case
            return html.Div([html.P("Please select a year to view Yearly Statistics.", style={'textAlign': 'center', 'marginTop': '20px'})])

        # Filter data based on selected_year
        yearly_data = df[df['Year'] == selected_year]
        
        # Ensure 'Month' is ordered correctly for plotting
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        yearly_data['Month'] = pd.Categorical(yearly_data['Month'], categories=month_order, ordered=True)

        # Plot 1: Monthly Automobile Sales (Line Chart)
        monthly_sales_yearly = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index().sort_values('Month')
        Y_chart1 = dcc.Graph(
            figure=px.line(monthly_sales_yearly, x='Month', y='Automobile_Sales',
                           title=f'Automobile Sales by Month in {selected_year}',
                           markers=True)
        )

        # Plot 2: Total Sales by Vehicle Type (Bar Chart)
        sales_by_vehicle_type_yearly = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.bar(sales_by_vehicle_type_yearly, x='Vehicle_Type', y='Automobile_Sales',
                          title=f'Total Automobile Sales by Vehicle Type in {selected_year}')
        )

        # Plot 3: Total Advertising Expenditure by Vehicle Type (Pie Chart)
        adv_exp_by_vehicle_type_yearly = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.pie(adv_exp_by_vehicle_type_yearly, values='Advertising_Expenditure', names='Vehicle_Type',
                          title=f'Total Advertising Expenditure by Vehicle Type in {selected_year}',
                          hole=0.3)
        )

        # Plot 4: Average Price by Vehicle Type (Bar Chart)
        avg_price_vehicle_type_yearly = yearly_data.groupby('Vehicle_Type')['Price'].mean().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.bar(avg_price_vehicle_type_yearly, x='Vehicle_Type', y='Price',
                          title=f'Average Price by Vehicle Type in {selected_year}')
        )

        return html.Div(children=[
            html.Div(children=Y_chart1, style={'display': 'inline-block', 'width': '49%', 'padding': '10px'}),
            html.Div(children=Y_chart2, style={'display': 'inline-block', 'width': '49%', 'padding': '10px'}),
            html.Div(children=Y_chart3, style={'display': 'inline-block', 'width': '49%', 'padding': '10px'}),
            html.Div(children=Y_chart4, style={'display': 'inline-block', 'width': '49%', 'padding': '10px'})
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-around'})

    else:
        return html.Div([html.P("Please select a report type.", style={'textAlign': 'center', 'marginTop': '20px'})])


if __name__ == '__main__':
    app.run()
