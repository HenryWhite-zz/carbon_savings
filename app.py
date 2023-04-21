import os
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd # noqa F401
import plotly.express as px
from dotenv import load_dotenv

# Local imports
import src.carbon_savings_calc as carbon_savings_calc
import src.constants as constants

# Load environment variables
env_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=env_path)

# Set asset folder location
assets_folder = os.path.join(os.path.dirname(__file__), '..', 'assets')

# Create app
# Set dash bootstrap components theme and link to custom.css file
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.DARKLY, 'assets/custom.css'])

# Reference the underlying flask app
# (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# Set browser tab title
app.title = "Carbon Savings Calculator" 

# Create summary of CO2 and monetary savings
@app.callback(
    Output(component_id='savings_desc', component_property='children'),
    Output(component_id='savings_desc', component_property='style'),
    Input(component_id='submit_button', component_property='n_clicks'),
    Input(component_id='mpg_input', component_property='value'),
    Input(component_id='annual_miles_input', component_property='value'),
    Input(component_id='gas_cost_input', component_property='value'),
    Input(component_id='kpm_input', component_property='value'),
    Input(component_id='elec_cost_input', component_property='value'),
)
def eval_electric_summary(n_clicks,
                          mpg=constants.mpg_avg,
                          annual_miles=constants.annual_miles_avg,
                          gas_cost=constants.cost_per_gallon_gasoline_avg,
                          kpm=constants.kpm_avg,
                          cost_per_kwh=constants.cost_per_kWh_avg,
                          CO2_per_MWh_lbs=constants.CO2_per_MWh_avg
                          ):
    """
    Create a text summary of the carbon emissions reduction and cost savings
    in switching from a gasoline car to an electric car.

    Args:
        mpg (float): Miles per gallon of gasoline car. Default is `mpg_avg`.
        annual_miles (int): Miles driven per year. Default is
                            `annual_miles_avg`.
        gas_cost (float): Cost of a gallon of gasoline in U.S. dollars.
                        Default is `cost_per_gallon_gasoline_average`.
        kpm (float): Kilowatt-hours per mile of electric car. Default is
                    `kpm_avg`.
        cost_per_kwh (float): Cost of 1 kWh electricity.
        C02_per_MWh_lbs: Pounds of CO2 emitted by 1 MWh electricity.

    Returns:
        string: A string containing a text summary of carbon & monetary
            savings
    """
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        savings = carbon_savings_calc.eval_electric(mpg,
                                                    annual_miles,
                                                    gas_cost,
                                                    kpm,
                                                    cost_per_kwh,
                                                    CO2_per_MWh_lbs)

        # Create summary of results
        summary = [
            html.H3(f'CO2 Reduced: {savings["co2_lbs_reduction"]:,.0f} '
                    f'lbs/year'),
            html.H3(f'Savings: ${savings["cost_dollars"]:,.2f}/year '
                    f'in fuel'),
            html.Br(),
            html.Span(f'Including the social cost of carbon you would '
                      f'save ${savings["comp_cost"]:,.2f} per year. '),
            html.Br(),
            html.Span(
                    f'Over 10 years you would save '
                    f'${savings["comp_cost"]*10:,.2f} and '
                    f'{savings["co2_lbs_reduction"]*10:,.0f} pounds of CO2.'
            )
        ]

        return summary, {'display': 'block'}


# Create graph of CO2 savings
@app.callback(
    Output(component_id='emissions_graph', component_property='figure'),
    Output(component_id='emissions_graph', component_property='style'),
    Input(component_id='submit_button', component_property='n_clicks'),
    Input(component_id='mpg_input', component_property='value'),
    Input(component_id='annual_miles_input', component_property='value'),
    Input(component_id='gas_cost_input', component_property='value'),
    Input(component_id='kpm_input', component_property='value'),
    Input(component_id='elec_cost_input', component_property='value')
)
def eval_electric_graph(n_clicks,
                        mpg=constants.mpg_avg,
                        annual_miles=constants.annual_miles_avg,
                        gas_cost=constants.cost_per_gallon_gasoline_avg,
                        kpm=constants.kpm_avg,
                        cost_per_kwh=constants.cost_per_kWh_avg,
                        CO2_per_MWh_lbs=constants.CO2_per_MWh_avg
                        ):
    """
    Create a graph of the carbon emissions reduction
    in switching from a gasoline car to an electric car.

    Args:
        mpg (float): Miles per gallon of gasoline car. Default is `mpg_avg`.
        annual_miles (int): Miles driven per year. Default is
                            `annual_miles_avg`.
        gas_cost (float): Cost of a gallon of gasoline in U.S. dollars.
                        Default is `cost_per_gallon_gasoline_average`.
        kpm (float): Kilowatt-hours per mile of electric car. Default is
                    `kpm_avg`.
        cost_per_kwh (float): Cost of 1 kWh electricity.
        C02_per_MWh_lbs: Pounds of CO2 emitted by 1 MWh electricity.

    Returns:
        string: A figure object of a plotly graph showing CO2 savings.
    """

    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        savings = carbon_savings_calc.eval_electric(mpg,
                                                    annual_miles,
                                                    gas_cost,
                                                    kpm,
                                                    cost_per_kwh,
                                                    CO2_per_MWh_lbs)

        data = {'gas': savings['CO2_total_gasoline'],
                'electric': savings['CO2_total_electric']
                }

        # Create graph of results
        fig = px.bar(x=data,
                     y=['Gasoline car', 'Electric car'],
                     title='Pounds of CO2 Emitted Per Year')

        fig.update_traces(hovertemplate='%{x} pounds of CO2 per year.')

        fig.update_layout(xaxis_title='',
                          yaxis_title='',
                          xaxis={'tickformat': ',d'},
                          height=300)

        return fig, {'display': 'block'}


results_card = html.Div(
    id='savings_desc',
    style={'display': 'none'}
)


input_card = dbc.Card([
    html.H4('Gas vehicle info', className='custom-header'),
    html.Br(),
    html.P('', id='test'),
    dbc.Label('Annual miles driven'),
    dbc.Input(id='annual_miles_input',
              type='number',
              inputmode='numeric',
              value=constants.annual_miles_avg,
              min=.01,
              debounce=True,
              required=False),
    html.Br(),
    dbc.Label('Miles per gallon'),
    dbc.Input(id='mpg_input',
              type='number',
              value=constants.mpg_avg,
              inputmode='numeric',
              min=1,
              debounce=True,
              required=False),
    html.Br(),
    dbc.Label('Cost for gallon of gas'),
    dbc.Input(id='gas_cost_input',
              type='number',
              value=constants.cost_per_gallon_gasoline_avg,
              inputmode='numeric',
              min=.01,
              debounce=True,
              required=False),
    html.Br(),
    html.Br(),
    html.H4('Electric vehicle info', className='custom-header'),
    dbc.Label('Kilowatt-hours per mile'),
    dbc.Input(id='kpm_input', type='number',
              value=constants.kpm_avg,
              inputmode='numeric',
              min=.01,
              debounce=True,
              required=False),
    html.Br(),
    dbc.Label('Cost per kilowatt-hour of electricity'),
    dbc.Input(id='elec_cost_input', type='number',
              value=constants.cost_per_kWh_avg,
              inputmode='numeric',
              min=.01,
              debounce=True,
              required=False),
    html.Br(),
    dbc.Button('Submit', class_name='custom-button', id='submit_button'),
])

emissions_graph = dcc.Graph(id='emissions_graph',
                            style={'display': 'none'},
                            config={'displayModeBar': False
                                    })


app.layout = dbc.Container([
    html.H1('Electric Car Savings', className='custom-header'),
    html.Hr(),
    dbc.Container([
        dbc.Row([
            dbc.Col(input_card, md=3),
            dbc.Col([emissions_graph, results_card])
        ])
    ]),
    html.Br(),
    html.Footer(
        children=[html.Span([
            'Created by ',
            html.A('Henry White',
                   href='https://www.linkedin.com/in/henry-a-white/',
                   target='_blank'),
            '.',
            html.Br()
            ]),
            ],
        className='custom-footer'
    )
])

# Run server if a development environment
if os.getenv('ENVIRONMENT') == 'development':
    if __name__ == '__main__':
        app.run_server(debug=True)
