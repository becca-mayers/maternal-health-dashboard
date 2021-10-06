# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 22:34:39 2019

@author: thisisbex
"""

from app import dbc, html

visualizations_jumbotron = html.Div(dbc.Container([
        html.Center(html.H1("Visualizations", className='display-4 text-danger')),
        html.Center( "Check out the findings for yourself."),
        html.Hr(),
        html.Center(dbc.Button("Take Me There", color="danger", href="/visualizations", external_link=True)),
    ], className="py-3"), className="shadow-lg p-3 bg-light rounded-3") 

predictions_jumbotron = html.Div(dbc.Container([
        html.Center(html.H1("Predictions", className='display-4 text-primary h-50')),
        html.Center("Get a glance at possible future outcomes."),
        html.Hr(),
        html.Center(dbc.Button("Take Me There", color="primary", href="/predictions", external_link=True)),
    ], className="py-3"), className="shadow-lg p-3 bg-light rounded-3")

statistics_jumbotron = html.Div(dbc.Container([
        html.Center(html.H1("Statistics", className='display-4 text-info')),
        html.Center("Dive into the data."),
        html.Hr(),
        html.Center(dbc.Button("Take Me There", color="info", href="/statistics", external_link=True)),
    ], className="py-3"), className="shadow-lg p-3 bg-light rounded-3")

background_jumbotron = html.Div(dbc.Container([
        html.Center(html.H1("Background", className='display-4 text-secondary h-50')),
        html.Center("Findings and related information."),
        html.Hr(),
        html.Center(dbc.Button("Take Me There", color="secondary", href="/background", external_link=True)),
    ], className="py-3"), className="shadow-lg p-3 bg-light rounded-3")
 
#body
layout = dbc.Container([
        dbc.Row([
            dbc.Col([visualizations_jumbotron]),
            dbc.Col([predictions_jumbotron]),
            ], className="align-items-md-stretch"),
        html.Br(),
        dbc.Row([
            dbc.Col([statistics_jumbotron]),
            dbc.Col([background_jumbotron]),
            ], className="align-items-md-stretch"),
        ])
                        