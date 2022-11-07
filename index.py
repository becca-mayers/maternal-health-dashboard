# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 22:34:39 2019

@author: thisisbex
"""

from app import app, server, df, dbc, dcc, html, pd, Input, Output
import flask
from pages import (home as mhh,
                   details as mhb, 
                   statistics as mhs, 
                   visualizations as mhv, 
                   predictions as mhp)


navbar = html.Div([
        dcc.Location(id="url"),
            dbc.NavbarSimple(
                children=[
                    dbc.DropdownMenu(
                        children= [
                            dbc.DropdownMenuItem("Statistics", href="/statistics", id='statistics', external_link=True),
                            dbc.DropdownMenuItem("Visualizations", href="/visualizations", id='visualizations', external_link=True),
                            dbc.DropdownMenuItem("Predictions", href="/predictions", id='predictions', external_link=True),
                            dbc.DropdownMenuItem("Background", href="/background", id='background', external_link=True),
                    ],
                    nav=False, #True,
                    in_navbar=False, #True,
                    label="Explore"),
                    ],            
                brand='Maternal Health Dashboard',
                brand_href='/home', 
                sticky='top',
                color='primary',
                dark=True,
                ),
            ])

footer = dbc.Container([
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.Center(dcc.Markdown("""Created by [Becca Mayers](www.beccamayers.com) | Icons by [Pixel Perfect from Flat Iron](https://www.flaticon.com/authors/pixel-perfect)""",
                                 className="h-50"))],
                    width={"size": 6, "offset": 3}, className="h-50"),
                ]),
            dbc.Row([
                dbc.Col([
                    html.Center(html.A([html.I(className="fab fa-twitter")], 
                        href='https://twitter.com/BotsFromScratch')),
                    #width={"size": 8, "offset": 3}, className="h-50"),
                    ]),
                ]),
            html.Br(),
            ])

main_body = dbc.Container([
    dbc.Row([  
        dbc.Col([
            #tabs,
            html.Br([]),
            html.Div(id='page-content'),
            ]),
        ]),
    ])

app.layout = html.Div([navbar, main_body, footer, html.Br()]) 

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def get_page(url):
    
    print(url)
    
    if (url is None) | (url == '/home'):
        return mhh.layout

    elif url == '/statistics':
        return mhs.layout   

    elif url == '/visualizations':
        return mhv.layout

    elif url == '/predictions':
        return mhp.layout
    
    elif url == '/background':
        return mhb.layout
 
    else:
        return mhh.layout
    
    print('end',url)
    
if __name__ == '__main__':
    
     app.run_server()
