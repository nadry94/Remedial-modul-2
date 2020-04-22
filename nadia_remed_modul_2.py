import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import dash_table
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Maaf mas cornell sebelumnya, tapi sql saya gabisa, ga ngerti cara benerin dari install nya lagi

engine = create_engine("  ")
conn = engine.connect()
result = conn.execute('SELECT * from dashboard').fetchall()

mesin = pd.DataFrame(result, columns = result[0].keys())
mesin_plot = mesin.copy()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def generate_table(dataframe, page_size = 10):
     return dash_table.DataTable(
                    id = 'dataTable',
                    columns = [{"name": i, "id": i} for i in dataframe.columns],
                    data=dataframe.to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                    page_action="native",
                    page_current= 0,
                    page_size= page_size,
                )

app.layout = html.Div([
        html.H1('Remed ujian modul 2'),
        html.P('Nadia Rachma Yunia'),
        html.Div([html.Div(children =[dcc.Tabs(value = 'tabs', id = 'tabs-1', 
                           children = [dcc.Tab(value = 'Tabel', label = 'DataFrame Table', 
                                      children =[html.Center(html.H1('DATAFRAME TSA')),
                                      html.Div(children =[html.Div(children =[html.P('Fuel-Type:'),dcc.Dropdown(value = '', id='filter-site', 
                                                                                                                 options = [{'label': 'Gas', 'value': 'gas'},
                                                                                                                            {'label': 'Diesel', 'value': 'diesel'},
                                                                                                                            {'label': 'All', 'value': ''}])
                                                                             ], className = 'col-3')], className = 'row'),
                                      
                                      html.Div([html.P('Max Rows : '),dcc.Input( id='filter-row',type='number', value=10)], 
                                               className = 'row col-3'),
                                      html.Br(),
                                      html.Div(children =[html.Button('search',id = 'filter')],className = 'col-4'),
                                      
                                      html.Br(), html.Div(id = 'div-table', children =[generate_table(mesin)])
                                                ]
                                              ),

                                       dcc.Tab(label = 'Bar-Chart', value = 'tab-satu', 
                                               children=[html.Div(children =[html.Div(children =[html.P('Y1:'),
                                                                                                 dcc.Dropdown(id = 'y-axis-1',
                                                                                                              options = [{'label': i, 'value': i} for i in mesin_plot.select_dtypes('number').columns], 
                                                                                                              value = 'Wheel-Base')
                                                                                                ], className = 'col-3'),
                                                                            
                                                                            html.Div(children =[ html.P('Y2:'),    
                                                                                                 dcc.Dropdown(id = 'y-axis-2', 
                                                                                                 options = [{'label': i, 'value': i} for i in mesin_plot.select_dtypes('number').columns], 
                                                                                                 value = 'Height')
                                                                                               ], className = 'col-3'),
                                                                            
                                                                            html.Div(children =[html.P('X:'),
                                                                                                dcc.Dropdown(id = 'x-axis-1', 
                                                                                                             options = [{'label': i, 'value': i} for i in ['Drive-Wheels', 'Engine-Location', 'Engine-Type']], 
                                                                                                             value = 'Drive-Wheels')
                                                                                                ], className = 'col-3')    
                                                                            
                                                                            ], className = 'row'),

                                          ##Graph bar
                                          html.Div([dcc.Graph( id = 'graph-bar',
                                                               figure ={'data' : [{'x': mesin_plot['Drive-Wheels'], 'y': mesin_plot['Wheel-Base'], 'type': 'bar', 'name' :'Wheel-Base'},
                                                                                  {'x': mesin_plot['Drive-Wheels'], 'y': mesin_plot['Height'], 'type': 'bar', 'name': 'Height'}
                                                                                 ], 
                                                                        'layout': {'title': 'Bar Chart'}  
                                                                       }
                                                             )
                                                   ])]),

                                                    dcc.Tab(label = 'Scatter-Chart', value = 'tab-dua', 
                                                            children =[html.Div(children = dcc.Graph(id = 'graph-scatter',
                                                                                                     figure = {'data': [go.Scatter(x = mesin_plot[mesin_plot['Drive-Wheels'] == i]['Horsepower'],
                                                                                                                                   y = mesin_plot[mesin_plot['Drive-Wheels'] == i]['Price'],
                                                                                                                                   text = mesin_plot[mesin_plot['Drive-Wheels'] == i]['Status'],
                                                                                                                                   mode='markers',
                                                                                                                                   name = '{}'.format(i)) for i in mesin_plot['Drive-Wheels'].unique()
                                                                                                                       ],
                                                                                                               'layout':go.Layout(xaxis= {'title': 'Horsepower'},yaxis={'title': 'Price'},
                                                                                                                                  hovermode='closest')
                                                                                                              }
                                                                                )),
                                                                      ]),

                                                    dcc.Tab(label ='Pie-Chart', value = 'tab-tiga', 
                                                            children =[html.Div(dcc.Dropdown(id ='pie-dropdown', 
                                                                                             options = [{'label': i, 'value': i} for i in mesin_plot.select_dtypes('number').columns], 
                                                                                             value = 'Fuel-System'), className = 'col-3'
                                                                               ),
                                                                       
                                                                       ## Graph Pie
                                                                       html.Div([dcc.Graph(id = 'graph-pie',
                                                                                      figure ={'data' : [go.Pie(labels = ['{}'.format(i) for i in list(mesin_plot['Fuel-Type'].unique())], 
                                                                                                                values = [mesin_plot.groupby('Fuel-Type').mean()['Fuel-System'][i] for i in list(mesin_plot['Fuel-Type'].unique())],
                                                                                                                sort = False)
                                                                                ], 
                                                                                               'layout': {'title': 'Mean Pie Chart'}}
                                                                                )])   
                                                          ])
                                                        ], 
        ## Tabs Content Style
        content_style = {
        'fontFamily': 'Arial',
        'borderBottom': '1px solid #d6d6d6',
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'padding': '44px'
    })
        ])
    ])
], style ={
        'maxWidth': '1200px',
        'margin': '0 auto'
    })


@app.callback(
    Output(component_id = 'div-table', component_property = 'children'),
    [Input(component_id = 'filter', component_property = 'n_clicks')],
    [State(component_id = 'filter-site', component_property = 'value'),
    State(component_id = 'filter-row', component_property = 'value')]
)
def update_table(n_clicks, site, row):
    if site == '':
        children = [generate_table(mesin, page_size = row)]
    else:
        children = [generate_table(mesin[mesin['Fuel-Type'] == site], page_size = row)]            
    return children

@app.callback(
    Output(component_id = 'graph-bar', component_property = 'figure'),
    [Input(component_id = 'y-axis-1', component_property = 'value'),
    Input(component_id = 'y-axis-2', component_property = 'value'),
    Input(component_id = 'x-axis-1', component_property = 'value'),]
)
def create_graph_bar(y1, y2, x1):
    figure = {
                    'data' : [
                        {'x': mesin_plot[x1], 'y': mesin_plot[y1], 'type': 'bar', 'name' :y1},
                        {'x': mesin_plot[x1], 'y': mesin_plot[y2], 'type': 'bar', 'name': y2}
                    ], 
                    'layout': {'title': 'Bar Chart'}  
                    }
    return figure                


@app.callback(
    Output(component_id = 'graph-pie', component_property = 'figure'),
    [Input(component_id = 'pie-dropdown', component_property = 'value')]
)
def create_graph_pie(x):
    figure = {'data' : [go.Pie(labels = ['{}'.format(i) for i in list(mesin_plot['Fuel-Type'].unique())], 
                                        values = [mesin_plot.groupby('Fuel-Type').mean()[x][i] for i in list(mesin_plot['Fuel-Type'].unique())],
                                        sort = False)
                    ], 
                        'layout': {'title': 'Mean Pie Chart'}}

    return figure                    
    



if __name__ == '__main__':
    app.run_server(debug=True)