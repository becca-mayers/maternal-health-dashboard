
from app import app, df, dbc, dcc, html, pd, Input, Output
import warnings
warnings.filterwarnings('ignore')

color_list = ['#56cc9d', '#6cc3d5', '#ffcf67', '#f3969a', '#78c2ad', '#ff7851']

prec_facilities_list = df['facility'].drop_duplicates().tolist()
prec_facilities = prec_facilities_list[:6]
prec_payers_list = df['payer'].drop_duplicates().tolist()
prec_payers = prec_payers_list[:3]

maternal_prec_facility_selector = html.Div([
        dbc.Label('Facility', className='display-7'),
        dbc.Col(dcc.Dropdown(
                id="maternal-prec-facilities",
                multi=True,
                options = [{'label': f, 'value': f} for f in prec_facilities_list],
                value=prec_facilities)),
        ])

maternal_prec_payer_selector = html.Div([
        dbc.Label('Payer', className='display-7'),
        dbc.Col(dcc.Dropdown(
                id="maternal-prec-payers",
                multi=True,
                options = [{'label': f, 'value': f} for f in prec_payers_list],
                value=prec_payers)),
        ])

prec_date_range = html.Div([
    dbc.Label('Date Range', className='display-7'),
    dcc.DatePickerRange(
        id = 'prec-date-range',
        min_date_allowed = df['discharge_date'].min(),
        max_date_allowed = df['discharge_date'].max(),
        start_date = df['discharge_date'].min(),
        end_date = df['discharge_date'].max(),
        display_format='MM-DD-YY'),
    ])

soon_jumbotron = dbc.Card([
        html.Center("Coming Soon", className='display-5 text-primary h-50')],
     className="p-3 bg-light rounded-3") 

prec_info_jumbotron = dbc.Card([
        html.Center("Source Code & Instructional Blog", className='display-5 text-primary h-50'),
        html.Center('Want to recreate this dashboard? Get the source code by clicking the below button.'),
        html.Hr(),
        html.Center(dbc.Button('Github Repo', color="danger", href='https://github.com/becca-mayers/maternal-health-dashboard', external_link=True)),
    ], className="p-3 bg-light rounded-3") 

layout = dbc.Container([
    
    html.H1('Predictions'),
    dcc.Markdown('''----'''),    
    soon_jumbotron,
    html.Br(),
    prec_info_jumbotron,
    dcc.Markdown('''----'''),
    dcc.Markdown('''Use the controls below to discover outcomes based on facility, payer or date range.'''),
    
     dbc.Card([
        dbc.Row([
            dbc.Col([maternal_prec_facility_selector], width=4),
            dbc.Col([maternal_prec_payer_selector], width=4),
            dbc.Col([prec_date_range], width=4),
            ]),
        ], className="p-3 bg-light rounded-3"),
    
    html.Br(),
    
    dbc.Card([
        dbc.Row([dbc.Col([html.Div(id='maternal-prediction-content', style={'fontWeight': 'bold'})]),
            ]),
        
    html.Br(),
    
    prec_info_jumbotron,
    html.Br(),
    
        ]),
    ])

@app.callback(Output('maternal-prediction-content', 'children'),
             [Input('maternal-prec-facilities', 'value'),
              Input('maternal-prec-payers', 'value'),
              Input('prec-date-range', 'start_date'),
              Input('prec-date-range', 'end_date')])

def predict(facilities, payers, start, end):

    dff = pd.DataFrame(columns=['facilities', 'payers', 'discharge_date'],
        data=[[facilities, payers, start]])
    table = dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True) 

    return html.Div(table)
