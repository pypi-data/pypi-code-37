import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from math import ceil



class DashReporter(object):
    external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    colors_black = {
    'background': '#040483',
    'text': 'white'
        }

    colors_black = {
    'background': 'white',
    'text': 'black'
        }

    def __init__(self, df, singulars):
        self.df = df
        self.singulars = singulars

        self.endpoint_graph_copy = [f.copy() for f in singulars]

        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, self.external_css])


        self.app.layout = html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            html.H1(
                                children='Load Test Results',
                                style={
                                    'textAlign': 'center',
                                    'color': self.colors_black['text'],
                                    'backgroundColor': self.colors_black['background']
                                }
                ))
                        )
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div("Overall Test details panels on the right"),
                            style={'textAlign': 'right'},
                        ),
                    ],
                    justify='around'
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            html.H3(
                                children='Endpoint Statistics',
                                style={
                                    'textAlign': 'center',
                                    'color': self.colors_black['text'],
                                    'backgroundColor': self.colors_black['background']
                                }
                                )
                        ),
                        style={
                                'textAlign': 'center',
                                'color': self.colors_black['text'],
                                }
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(self.general_stats_dash_table()),
                        width={'size': 10, 'offset': 1},
                        align='center',
                        style={'padding': 20}   
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            html.H3(
                                children='Endpoint Graphs',
                                style={
                                    'textAlign': 'center',
                                    'color': self.colors_black['text'],
                                    'backgroundColor': self.colors_black['background']
                                        }
                                    )
                        ),
                        style={'padding': 20} 
                    ),
                ),
                    html.Div(
                        [
                        dbc.Row(list(dbc.Col(html.Div(self.generate_scatter_graph(self.endpoint_graph_copy[0]))) \
                               for _ in range (2 if len(self.endpoint_graph_copy) > 1 else 1)
                                    ),
                            style={'padding-left': 15,
                                    'padding-right': 5}
                        ) for x in range(int(ceil(len(self.singulars) / 2)))
                        ]
                    ),
                # dbc.Row(
                #     html.Div(
                #         self.plot_3D(self.singulars[1]) # TEST
                #     )
                # )
                    ])
            

    def general_stats_dash_table(self):
        return dash_table.DataTable(
            id='stats-table',
            columns=[{"name": i, "id": i} for i in self.df.columns],
            data=self.df.to_dict('records'),
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'Success_Rate',
                        'filter': '{Success_Rate} < "100"'
                    },
                    'backgroundColor': '#3D9970',
                    'color': 'white',
                },
                {
                    'if': {
                        'column_id': 'IQR',
                        'filter': '{IQR} > "0.4"'
                    },
                    'backgroundColor': '#B22222',
                    'color': 'white',
                }

                                    ]
            )


    def generate_scatter_graph(self, df):
        df['stamp'] = pd.to_datetime(df['stamp']).dt.strftime('%H:%M:%S')
        df.sort_values(by='stamp', inplace=True)
        elem = html.Div([
                dcc.Graph(
                    figure={
                        'data': [
                            go.Scatter(
                                x=df['stamp'],
                                y=df['response_time'],
                                text='Response Times',
                                mode='lines+markers',
                                opacity=0.7,
                                marker={
                                    'size': 10,
                                    'line': {'width': 0.5, 'color': 'white'}
                                },
                                name="PLACEHOLDER FFS"
                            )
                        ],
                        'layout': go.Layout(
                            showlegend=True,
                            xaxis={'title': 'Time'},
                            yaxis={'title': 'Response Times'},
                            margin={'l': 60, 'b': 110, 't': 10, 'r': 10},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    }
                )
            ])
        
        self.endpoint_graph_copy.pop(0)
        return elem

    def plot_3D(self, df):
        df['stamp'] = pd.to_datetime(df['stamp']).dt.strftime('%H:%M:%S')
        df.sort_values(by='stamp', inplace=True)
        elem = html.Div([
                dcc.Graph(
                    figure={
                        'data': [
                            go.Scatter3d(
                                x=df['stamp'],
                                y=df['response_time'],
                                z=df['status'],
                                text='Response Times',
                                mode='lines',
                                name='POST /fraud-check'
                            )
                        ],
                        'layout': go.Layout(
                            showlegend=True,
                            xaxis={'title': 'Time'},
                            yaxis={'title': 'Response Times'},
                            margin={'l': 60, 'b': 110, 't': 10, 'r': 10},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    }
                )
            ])
        
        return elem


def run_reporter(df, singulars):
    Reporter = DashReporter(df, singulars)
    Reporter.app.run_server(debug=False, host='0.0.0.0')


# run_reporter(pd.read_csv('stats.csv'), 
#         [
#             pd.read_csv('stats0.csv'), pd.read_csv('stats1.csv'),
#             pd.read_csv('stats0.csv'), pd.read_csv('stats1.csv'),
#             pd.read_csv('stats1.csv')
#             ])