# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 22:34:39 2019

@author: thisisbex
"""

from app import app, df, np, px, dbc, dcc, html, go, Input, Output
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

color_list = ['#56cc9d', '#6cc3d5', '#ffcf67', '#f3969a', '#78c2ad', '#ff7851']

facilities_list = df['facility'].drop_duplicates().tolist()
facilities = facilities_list[:6]
payers_list = df['payer'].drop_duplicates().tolist()
payers = payers_list[:3]

maternal_vis_facility_selector = html.Div([
        dbc.Label('Facility', className='display-7'),
        dbc.Col(dcc.Dropdown(
                id="maternal-vis-facilities",
                multi=True,
                options = [{'label': f, 'value': f} for f in facilities_list],
                value=facilities)),
        ])

maternal_vis_payer_selector = html.Div([
        dbc.Label('Payer', className='display-7'),
        dbc.Col(dcc.Dropdown(
                id="maternal-vis-payers",
                multi=True,
                options = [{'label': f, 'value': f} for f in payers_list],
                value=payers)),
        ])

date_range = html.Div([
    dbc.Label('Date Range', className='display-7'),
    dcc.DatePickerRange(
        id = 'date-range',
        min_date_allowed = df['discharge_date'].min(),
        max_date_allowed = df['discharge_date'].max(),
        start_date = df['discharge_date'].min(),
        end_date = df['discharge_date'].max(),
        display_format='MM-DD-YY'),
    ])

dual_map = dcc.Graph(id='maternal-dual-map')    
standard_pies = dcc.Graph(id='maternal-pie-graph')
standard_bubble = dcc.Graph(id='maternal-bubble-graph')

info_jumbotron = dbc.Card([
        html.Center("Source Code & Instructional Blog", className='display-5 text-primary h-50'),
        html.Center('Want to recreate this dashboard? Get the source code by clicking the below button.'),
        html.Hr(),
        html.Center(dbc.Button('Github Repo', color="danger", href='https://github.com/becca-mayers/maternal-health-dashboard', external_link=True)),
    ], className="p-3 bg-light rounded-3") 

#body
layout = dbc.Container([
    html.H1('Visualizations'),
    dcc.Markdown('''----'''),
    
    info_jumbotron,

    dcc.Markdown('''----'''),
    
    html.P('Selecting a facility and a payer generates cesarean/vaginal maps \
           and procedure, race, and length of stay graphs.'),
           
    dbc.Card([
        dbc.Row([
            dbc.Col([maternal_vis_facility_selector], width=4), 
            dbc.Col([maternal_vis_payer_selector], width=4),
            dbc.Col([date_range], width=4)
            ]),
        ], className="p-3 bg-light rounded-3"),
    
    html.Br(),
    
    dbc.Card([
        dbc.Row([
            dbc.Col([
                dbc.CardHeader("Deliveries By State", className='display-6 text-primary'),
                dual_map,
                ]),
            ]),
        ]),
    
    html.Br(),
    
    dbc.Card([
        dbc.Row([
            dbc.Col([
                dbc.CardHeader("Population", className='display-6 text-primary'),
                standard_pies,
                ]),
            ]),
        ]),
    
    html.Br(),
    
    dbc.Card([
        dbc.Row([
              dbc.Col([
                  dbc.CardHeader("Billed Charges by Race", className='display-6 text-primary'),
                  standard_bubble,
                  ]),
              ]),       
          ]),  
    
        html.Br(),
        info_jumbotron,
    ])

#%%callbacks

@app.callback(
    Output('maternal-vis-payers', 'options'),
    [Input('maternal-vis-facilities', 'value')])

def update_payers(facilities):
    
    payers_df = df.loc[df['facility'].isin(facilities)]
    return [{'label': f, 'value': f} for f in payers_df['payer'].drop_duplicates().tolist()]

@app.callback(Output('maternal-dual-map', 'figure'),
              [Input('maternal-vis-facilities', 'value'),
               Input('maternal-vis-payers', 'value'),
               Input('date-range', 'start_date'),
               Input('date-range', 'end_date')])

def dual_map(facilities, payers, start, end):
    
    dff = df.loc[(df['facility'].isin(facilities)) &
                 (df['payer'].isin(payers))]
    
    dff = dff.loc[(dff['discharge_date'] >= start) & (dff['discharge_date'] <= end)]
    
    delivery_types = dff['delivery_type'].drop_duplicates().tolist()
    delivery_count = dff.groupby(['state', 'delivery_type', 'zip_code']).size().reset_index(name='total')
    rows = 1
    cols = 2
    fig = make_subplots(
        rows=rows, cols=cols,
        specs = [[{'type': 'choropleth'} for c in np.arange(cols)] for r in np.arange(rows)],
        subplot_titles = delivery_types)
    
    for i, delivery in enumerate(delivery_types):
        result = delivery_count[['state', 'total']][delivery_count.delivery_type == delivery]
        fig.add_trace(go.Choropleth(
            locations=result['state'],
            z = result.total,
            locationmode = 'USA-states',
            marker_line_color='white',
            zmin = 0,
            zmax = max(delivery_count['total']),
            colorbar_title = "Deliveries",
            colorscale = 'Tealrose',
        ), row = i//cols+1, col = i%cols+1)
    
    fig.update_layout(
        #title_text = 'Deliveries by State',
        **{'geo' + str(i) + '_scope': 'usa' for i in [''] + np.arange(2,rows*cols+1).tolist()},
        )
    
    for index, trace in enumerate(fig.data):
        fig.data[index].hovertemplate = 'State: %{location}<br>Deliveries: %{z:.2f}<extra></extra>'
    
    return fig
    
@app.callback(Output('maternal-pie-graph', 'figure'),
              [Input('maternal-vis-facilities', 'value'),
               Input('maternal-vis-payers', 'value'),
               Input('date-range', 'start_date'),
               Input('date-range', 'end_date')])
              
def make_maternal_pie_graph(facilities, payers, start, end):

    dff = df.loc[(df['facility'].isin(facilities)) &
                 (df['payer'].isin(payers))]
    
    dff = dff.loc[(dff['discharge_date'] >= start) & (dff['discharge_date'] <= end)]
    
    dff = dff.rename(columns={'age_range':'Age Range'})
    
    fig = make_subplots(rows=1, cols=3, 
                        specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=['Payers', 'Age Ranges', 'Facilities'])

    fig.add_trace(go.Pie(labels = dff['payer'].tolist(), 
                           values = dff['count'].tolist(),
                           textinfo='label+percent',
                           marker = {'colors': color_list},
                                           ), 1,1)  
    
    fig.add_trace(go.Pie(labels = dff['Age Range'].tolist(), 
                            values = dff['count'].tolist(),
                            textinfo='label+percent',
                            marker = {'colors': color_list},
                                            ), 1,2) 
    
    fig.add_trace(go.Pie(labels = dff['facility'].tolist(), 
                            values = dff['count'].tolist(),
                            textinfo='label+percent',
                            marker = {'colors': color_list},
                                            ), 1,3)

    fig.update_traces(hole=.4, hoverinfo="label+percent+name", showlegend=False)

    return fig

@app.callback(Output('maternal-bubble-graph', 'figure'),
              [Input('maternal-vis-facilities', 'value'),
               Input('maternal-vis-payers', 'value'),
               Input('date-range', 'start_date'),
               Input('date-range', 'end_date')])
              
def make_maternal_bubble_graph(facilities, payers, start, end):
    
    dff = df.loc[(df['facility'].isin(facilities)) &(df['payer'].isin(payers))]
    dff = dff.loc[(dff['discharge_date'] >= start) & (dff['discharge_date'] <= end)]
    
    dfff = dff.groupby(
        ['Month-Year','race'], as_index=False).agg({'total_billed_charges':'sum',
                                                                   'count':'sum',
                                                                    'age':'mean'})
                                                    
    dfff = dfff.rename(columns = {'total_billed_charges':'Total Billed Charges',
                                                 'count': 'Encounters',
                                                   'age': 'Average Age',
                                                  'race':'Race'})

    fig = px.scatter(dfff, 
                     x = 'Encounters', 
                     y = 'Total Billed Charges',
                     animation_frame = 'Month-Year',
                     #animation_group = 'facility',
                     size = 'Encounters', 
                     color = 'Race',
                     log_x = True,
                     color_discrete_sequence = color_list,
                     template = 'simple_white')
    
    return fig
