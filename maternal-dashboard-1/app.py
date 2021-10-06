# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 22:34:39 2019

@author: thisisbex
"""

from dash import dcc, html, Dash, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.MINTY], 
           suppress_callback_exceptions = True)
app.scripts.config.serve_locally = True
server = app.server
df = pd.read_csv('df.csv')


