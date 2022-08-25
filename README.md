# maternal-health-dashboard
Multi-page dashboard investigating maternal outcomes and developed with Dash by Plotly. This dashboard demonstrates an examination of physician-documented indications for maternal outcomes by investigating potential contributing indications.  

# The Data
Each record is a single maternal patient encounter. The date range is January 2019 to present and variables are sourced from various sources, including [the Social Security Administration](https://www.ssa.gov/cgi-bin/popularnames.cgi), the Centers for Disease Control [Wonder](https://wonder.cdc.gov/wonder/sci_data/codes/fips/type_txt/cntyxref.asp) database, and the [US Census Bureau](https://www.census.gov/topics/population/race/about.html#:~:text=OMB%20requires%20five%20minimum%20categories,Hawaiian%20or%20Other%20Pacific%20Islander). The fictitious facility set is named after the [military alphabet](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet). 

# The Goal
Uncover discrepancies in points of care by analyzing a range of encounter-level variables.

# Home
![Dashboard Home](https://github.com/becca-mayers/maternal-health-dashboard/blob/main/github-images/home.png?raw=true)

# Filtered Search 
![Filters](https://github.com/becca-mayers/maternal-health-dashboard/blob/main/github-images/filters.png). 

# Maps
![Delivery Type Maps](https://github.com/becca-mayers/maternal-health-dashboard/blob/main/github-images/linked-chloropleth-maps.png)

# Pie Graphs
![Population Pie Graphs](https://github.com/becca-mayers/maternal-health-dashboard/blob/main/github-images/population-pie.png)

# Animated Plots
![Animated Billed Charges Scatter Plot](https://github.com/becca-mayers/maternal-health-dashboard/blob/main/github-images/animated-scatter-graph.png) 
![Animated Length of Stay x Age Group Scatter Plot](https://github.com/becca-mayers/maternal-health-dashboard/blob/main/github-images/los-age-animated-graph.png)

# Statistical Tables
![Numeric Statistics Table](https://github.com/becca-mayers/maternal-health-dashboard/blob/main/github-images/numeric-statistics.png)
![Categorical Statistics Table](https://github.com/becca-mayers/maternal-health-dashboard/blob/main/github-images/categorical-statistics.png)

# To Run
Following the download and unzip, update the scheduler's frequency if needed (codebase set to run hourly), and launch the scheduler from the command line by cd'ing into the unzipped folder and running the command  `python index.py`.

Questions? Find out more [here](https://www.beccamayers.com).
