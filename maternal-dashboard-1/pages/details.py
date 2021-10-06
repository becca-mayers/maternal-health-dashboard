#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 19:22:23 2020

@author: thisisbex
"""
from app import dbc, dcc, html

details = dcc.Markdown("""
                       
#### Objective   

To demonstrate an examination of physician-documented indications for 
maternal outcomes by investigating potential contributing indications. 
                  
##### Categorical Data  
+ First names were randomly selected from a list of the 100 most popular first 
names for males and females born in 2020 from the
[Social Security Administration](https://www.ssa.gov/cgi-bin/popularnames.cgi).  
+ Last names came from 
[this list](https://www.thoughtco.com/most-common-us-surnames-1422656) of the 
most common surnames in the United States.    
+ Zip codes were randomly selected from the Centers for Disease Control
[Wonder](https://wonder.cdc.gov/wonder/sci_data/codes/fips/type_txt/cntyxref.asp) 
database.  
+ Facility names are randomly selected from the military alphabet 
(ex. Alpha, Bravo, etc.)   
+ Payer types (Commerical, Private, Government) were sourced from 
[Free Medical Billing Training](https://www.freemedicalbillingtraining.com/insurance.html).    
+ Race types (White, Black or African American, 
American Indian or Alaska Native, Asian, Native Hawaiian or Other Pacific Islander)
were sourced from the [US Census Bureau]
(https://www.census.gov/topics/population/race/about.html#:~:text=OMB%20requires%20five%20minimum%20categories,Hawaiian%20or%20Other%20Pacific%20Islander.).      
 
##### Numeric Data  
+ Total Billed Charges are range from $13.00 to $670,000.00 in $.01 intervals  
+ Length of stay ranges from 0 days to 70 days  
+ Systolic blood pressure ranges from 20 to 200  
+ Diastolic blood pressure ranges from 1 to 20  
+ Rcount ranges from 0 to 34  
+ Hematocrit ranges from 20 to 55 in .1 intervals   
+ BMI ranges from 1 to 1,000 in .1 intervals  
+ Pulse ranges from 10 to 160  
+ Respiration ranges from 5 to 80      
+ Age ranges from 15 to 65 
              
""")

#body
layout = dbc.Container([
    html.H1('Background'),
    dcc.Markdown('''----'''),
        dbc.Row([
            dbc.Col([details]),
            ]),
        ])
                        