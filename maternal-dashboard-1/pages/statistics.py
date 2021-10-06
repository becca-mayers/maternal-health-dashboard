# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 22:34:39 2019

@author: thisisbex
"""

import plotly.express as px
from app import app, df, dbc, np, dcc, html, Input, Output

stats_facilities_list = df['facility'].drop_duplicates().tolist()
color_list = ['#56cc9d', '#6cc3d5', '#ffcf67', '#f3969a', '#78c2ad', '#ff7851']
stats_payers_list = df['payer'].drop_duplicates().tolist()
stats_payers = stats_payers_list[:3]

maternal_stats_facilities = html.Div([
                        dbc.Label("Select Facility"),
                        dbc.Col(dcc.Dropdown(
                                id="maternal-stats-facilities",
                                multi=True,
                                options = [{'label': f, 'value': f} for f in stats_facilities_list],
                                value=stats_facilities_list)),
                        ])

maternal_stats_payers = html.Div([
        dbc.Label('Payer', className='display-7'),
        dbc.Col(dcc.Dropdown(
                id="maternal-stats-payers",
                multi=True,
                options = [{'label': f, 'value': f} for f in stats_payers_list],
                value=stats_payers)),
        ])

stats_date_range = html.Div([
    dbc.Label('Date Range', className='display-7'),
    dcc.DatePickerRange(
        id = 'stats-date-range',
        min_date_allowed = df['discharge_date'].min(),
        max_date_allowed = df['discharge_date'].max(),
        start_date = df['discharge_date'].min(),
        end_date = df['discharge_date'].max(),
        display_format='MM-DD-YY'),
    ])

stats_info_jumbotron = dbc.Card([
        html.Center("Source Code & Instructional Blog", className='display-5 text-primary h-50'),
        html.Center('Want to recreate this dashboard? Get the source code by clicking the below button.'),
        html.Hr(),
        html.Center(dbc.Button('Github Repo', color="danger", href='https://github.com/becca-mayers/maternal-health-dashboard', external_link=True)),
    ], className="p-3 bg-light rounded-3") 

maternal_num_stats = html.Div(id='maternal-num-stats')
maternal_cat_stats = html.Div(id='maternal-cat-stats')
maternal_stats_scatter = dcc.Graph(id='maternal-stats-scatter')
maternal_histo = dcc.Graph(id='maternal-histo')
maternal_violin = dcc.Graph(id='maternal-violin')

layout = dbc.Container([
    
    html.H1('Statistics'),
    dcc.Markdown('''----'''),    
    stats_info_jumbotron,
    dcc.Markdown('''----'''),
    
    dbc.Card([
        dbc.Row([
            dbc.Col([maternal_stats_facilities], width=4),
            dbc.Col([maternal_stats_payers], width=4),
            dbc.Col([stats_date_range], width=4),
            ]),
        ], className="p-3 bg-light rounded-3"),
    
    html.Br(),
    
    dbc.Card([
        dbc.CardHeader("Numerical Summary Statistics", className='display-6 text-primary'),   
        dbc.Row([dbc.Col([maternal_num_stats])]),
        ]),
    
    html.Br(),
    
     dbc.Card([
        dbc.CardHeader('Length of Stay by Delivery', className='display-6 text-primary'), 
        dbc.Row([dbc.Col([maternal_violin])]),
        ]),
    
    html.Br(),
    
    dbc.Card([
        dbc.CardHeader("Categorical Summary Statistics", className='display-6 text-primary'), 
        dbc.Row([dbc.Col([maternal_cat_stats])]),
        ]),
    
    html.Br(),
    
    dbc.Card([
        dbc.CardHeader("Length of Stay per Age Group Over Time", className='display-6 text-primary'), 
        dbc.Row([dbc.Col([maternal_stats_scatter])]),
        ]),
    
    html.Br(),
    
    dbc.Card([
        dbc.CardHeader('Billed Charges by DRG Distribution', className='display-6 text-primary'), 
        dbc.Row([dbc.Col([maternal_histo])]),
        ]),
    
    html.Br(), 
    stats_info_jumbotron,
    html.Br(),
    
    ])

@app.callback(Output('maternal-num-stats', 'children'),
              [Input('maternal-stats-facilities', 'value'),
               Input('maternal-stats-payers', 'value'),
               Input('stats-date-range', 'start_date'),
               Input('stats-date-range', 'end_date')])
              
def make_num_stats(facilities, payers, start, end):

    dff = df.loc[(df['facility'].isin(facilities)) & (df['payer'].isin(payers))]
    dff = dff.loc[(dff['discharge_date'] >= start) & (dff['discharge_date'] <= end)]
    dff.columns = dff.columns.str.replace('_',' ')   
    num_summary = dff.describe(include=[np.number]).round().reset_index()
    table = dbc.Table.from_dataframe(num_summary, striped=True, bordered=True, hover=True)

    return html.Div(table) 

@app.callback(Output('maternal-violin', 'figure'),
              [Input('maternal-stats-facilities', 'value'),
               Input('maternal-stats-payers', 'value'),
               Input('stats-date-range', 'start_date'),
               Input('stats-date-range', 'end_date')])

def make_violin(facilities, payers, start, end):

    dff = df.loc[(df['facility'].isin(facilities)) & (df['payer'].isin(payers))] 
    dff = dff.loc[(dff['discharge_date'] >= start) & (dff['discharge_date'] <= end)]
    dff = dff.rename(columns={'delivery_type': 'Delivery Type', 
                              'race':'Race', 
                              'los': 'Length of Stay'})

    fig = px.violin(dff, 
                    x = 'Delivery Type', 
                    y = 'Length of Stay', 
                    color = 'Race', 
                    box = True, 
                    points = 'all',
                    hover_data = dff.columns,
                    template = 'simple_white',
                    color_discrete_sequence = color_list)
 
    return fig     

@app.callback(Output('maternal-cat-stats', 'children'),
              [Input('maternal-stats-facilities', 'value'),
               Input('maternal-stats-payers', 'value'),
               Input('stats-date-range', 'start_date'),
               Input('stats-date-range', 'end_date')])
              
def make_cat_stats(facilities, payers, start, end):

    dff = df.loc[(df['facility'].isin(facilities)) & (df['payer'].isin(payers))]
    dff = dff.loc[(dff['discharge_date'] >= start) & (dff['discharge_date'] <= end)]
    dff.columns = dff.columns.str.replace('_',' ')
    cat_summary = dff.describe(include=[np.object]).round().reset_index()    
    table = dbc.Table.from_dataframe(cat_summary, striped=True, bordered=True, hover=True)
        
    return html.Div(table)

@app.callback(Output('maternal-stats-scatter', 'figure'),
              [Input('maternal-stats-facilities', 'value'),
               Input('maternal-stats-payers', 'value'),
               Input('stats-date-range', 'start_date'),
               Input('stats-date-range', 'end_date')])

def make_scatter(facilities, payers, start, end):

    dff = df.loc[(df['facility'].isin(facilities)) & (df['payer'].isin(payers))]
    dff = dff.loc[(dff['discharge_date'] >= start) & (dff['discharge_date'] <= end)]
    dff = dff.rename(columns={'age_range':'Age Group', 
                              'los': 'Length of Stay'})
    dfff = dff.groupby(['Month-Year', 'Age Group'], as_index=False).agg({'Length of Stay':'mean',
                                                                         'count':'sum'})
    
    fig = px.scatter(dfff, 
                 x = 'Length of Stay', 
                 y = 'count', 
                 color = 'Age Group',
                 size = 'Length of Stay',
                 animation_frame = 'Month-Year',
                 animation_group = 'Age Group',
                 template = 'simple_white',
                 range_x=[dfff['Length of Stay'].min(), dfff['Length of Stay'].max()],
                 range_y=[dfff['count'].min(), dfff['count'].max()],
                 color_discrete_sequence = color_list
                 )
 
    return fig  

@app.callback(Output('maternal-histo', 'figure'),
              [Input('maternal-stats-facilities', 'value'),
               Input('maternal-stats-payers', 'value'),
                Input('stats-date-range', 'start_date'),
               Input('stats-date-range', 'end_date')])
              
def make_histo(facilities, payers, start, end):

    dff = df.loc[(df['facility'].isin(facilities)) & (df['payer'].isin(payers))]
    dff = dff.loc[(dff['discharge_date'] >= start) & (dff['discharge_date'] <= end)]
    dff = dff.rename(columns={'total_billed_charges':'Total Billed Charges',
                              'delivery_type':'Delivery Type'})
    
    fig = px.histogram(dff, 
                       x = 'Month-Year',
                       y = 'Total Billed Charges',
                       color = 'drg',
                       facet_col = 'Delivery Type',
                       #marginal = 'rug',
                       hover_data = dff.columns,
                       color_discrete_sequence = color_list,
                       template = 'plotly_white')
    return fig

                           
              

              
 
