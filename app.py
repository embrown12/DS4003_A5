# %% [markdown]
# ### Assignment #5: Callbacks
# 
# DS4003 | Spring 2024
# 
# 
# Objective: Practice adding callbacks to Dash apps.
# 
# Task:
# (1) Build an app that contains the following components user the gapminder dataset: `gdp_pcap.csv`. 
# 
# TASK 1 is the same as ASSIGNMENT 4. You are welcome to update your code. 
# 
# UI Components:
# 
# A dropdown menu that allows the user to select `country`
# - The dropdown should allow the user to select multiple countries
# - The options should populate from the dataset (not be hard-coded)
# 
# A slider that allows the user to select `year`
# - The slider should allow the user to select a range of years
# - The range should be from the minimum year in the dataset to the maximum year in the dataset
# 
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# - The graph should display the gdpPercap for each country as a line
# - Each country should have a unique color
# - The graph should have a title and axis labels in reader friendly format
# 
# 
# 
# 
# (2) Write Callback functions for the slider and dropdown to interact with the graph
# 
# This means that when a user updates a widget the graph should update accordingly.
# The widgets should be independent of each other. 
# 
# 
# Layout:
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# 
# 
# Submission:
# - Deploy your app on Render. 
# - In Canvas, submit the URL to your public Github Repo (made specifically for this assignment)
# - The readme in your GitHub repo should contain the URL to your Render page. 
# 
# 
# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**

# %%
# Importing dependencies needed
import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
from datetime import date 

# %%
# Bringing in the GDP per Capita CSV file 
df = pd.read_csv(/data/gdp_pcap.csv)
#df = pd.read_csv(r'C:\Users\emily\OneDrive\Desktop\DS4003\A4_student\gdp_pcap.csv')

# %%
# Looking at the dataframe and some information it contains
df.head()

# %%
# Global variable for as a list of the rows in Country
country_names = df['country'].tolist()
#print(country_names)

# %%
# Global variable for a list of the columns (Getting years)
year_values = df.columns[1:].tolist()
#print(year_values)

# %%
# Just getting the columns of the data frame
yr_nums = df.columns
#print(yr_nums)

# %%
# Melt the data frame
melted_df = df.melt(id_vars='country',
                    value_vars= yr_nums,
                    var_name = 'Year',
                    value_name='GDP'
                    )

# %%
# Function to handle the thousands like '28.1k'
def get_int(int_str):
    if 'k' in str(int_str):                  # Looks to see if there is a 'k' in the value. If not, we only need to make sure that it's an int
        num = int(float(int_str[:-1])*1000)  # Multiplies the decimal portion by 1000
    else:
        num = int(float(int_str))
    return num

# %%
# Apply my function for getting rid of the "k"s in the GDP values
melted_df['GDP'] = melted_df['GDP'].apply(get_int)
melted_df['Year'] = melted_df['Year'].apply(get_int)
# Rename the colunn to capitalize the variable name
melted_df = melted_df.rename(columns = {'country' : 'Country'})   
melted_df.head()

# %%
#Here is the line graph for GDP (y-axis) of Countries, with the years along the x-axis
fig_line_marker = px.line(melted_df,            
                          x = 'Year',
                          y = 'GDP',
                          color = 'Country',
                          )
fig_line_marker.update_layout(title_text='GDP of Countries From Years 1800 to 2100', title_x=0.5)   # Adding in the title and centering it
fig_line_marker.update_xaxes(dtick = 10)  # Changes the x axis tick increments to 10 instead of the deafult which was 6, this looks better.
fig_line_marker.show()

# %%
# Loading in the CSS stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] 

# Initialize the app
app = Dash(__name__, external_stylesheets=stylesheets)

# Connecting the server for Render purposes
server = app.server

# Define the layout
app.layout = html.Div([
    # Creating a Title for the app
    dcc.Markdown('''
    ## GDP Per Capita By Country (1800-2100) 
''',
    # Adding a stylesheet element to the title
style = {"color": "DarkBlue", 
         "textAlign": "center", 
         "backgroundColor": "LightBlue", 
         "fontSize": 10} 
), # Adding a description below the Title, including citation
    dcc.Markdown('''    
    This dashboard visually highlights the economic development of countries around the
    world from the years 1800 to projected 2100. According to the Gapminder authors, the GDP per capita is using the gold
                 standard. Most notably, Monaco has the highest GDP per capita, with its projected peak 244,000 in 2030. More information can be found in below:
    \n   [Citation](www.gapminder.org/sources/gdp-per-capita/)
                
''',
    # Adding style components to the description
style = {"color": "DarkBlue", 
         "textAlign": "center", 
         "backgroundColor": "LightBlue",
         "fontSize" : 13 
         }
    ),
    # Creating a new div for the two elements we want side by side
    html.Div([
        # Adding the Country Dropdown element
        html.Div(children = [
            html.Label('Country Dropdown'),
                dcc.Dropdown(
                    id = 'country_dropdown',
                    #options = country_names, # pulling the global variable defined in cell above
                    #options = [{'label': country, 'value': country} for country in melted_df['Country'].unique()], 
                    options = [country for country in melted_df['Country'].unique()],   # Options is a list of countries. 
                    placeholder = 'Select a Country or Countries',
                    value = [],    # Initializing the value to an empty list of countries. Doing this because options is a list.
                    multi = True,
                    maxHeight = 150,
                ), 
        ], style={'width': '48%', 'display': 'inline-block'}), # I found this on Stack overflow
        # Adding the Year Range slider element
        html.Div(
            dcc.RangeSlider(
                min = int(df.columns[1]),
                max = int(df.columns[-1]),
                step = 50,
                marks = {i: '{}'.format(i) for i in range(int(df.columns[1]), int(df.columns[-1]) + 50, 50)}, # I found this on Stack overflow
                updatemode='drag',
                value = [int(df.columns[151]), int(df.columns[201])], # Arbitrary dates
                id = 'year_slider',
                    tooltip= {"placement": "bottom",
                    "always_visible": True},
                    #verticalHeight=5,
            ), style={'width': '48%', 'float': 'right', 'display': 'inline-block'} # I found this on Stack overflow
        ) 
    ]),
        # Adding in the line graphs for countries' GDPs
    dcc.Graph(figure = fig_line_marker,
              
              id='country_fig'
    )
])
# Implementing the callback decorator, outputing the country figure when countries and years are inputted
@callback(
    Output('country_fig','figure'), 
    Input('country_dropdown', 'value'), 
    Input('year_slider', 'value')
    )
def update_graph(countrydropdown, yr_slider):
    # Making sure the years are integers
    yr_slider = [int(yr) for yr in yr_slider]
    # New df with only countries user selects in the dropdown
    dff = melted_df[(melted_df['Year'] >= yr_slider[0]) & (melted_df['Year'] <= yr_slider[1])] 
    dff = dff[dff['Country'].isin(countrydropdown)] 
    # Define the figure as a line plot    
    fig = px.line(dff,            
                          x = 'Year',
                          y = 'GDP', 
                          color = 'Country',
                           labels={
                     "GDP": "GDP Per Capita",},
                          )
    # Adding a title back and centering it
    fig.update_layout(title_text='GDP Per Capita of Selected Countries From Years ' + str(yr_slider[0]) + " to " + str(yr_slider[1]), title_x=0.5)
    # Initializing years on the x axis to the initial slider values
    fig.update_xaxes(range = [yr_slider[0], yr_slider[1]]) 
    # Initializing GDP values, this is arbitrary since no country/countries is/are selected yet. Importantly, making the lower bound zero.
    if len(countrydropdown) == 0:
        fig.update_yaxes(range = [0, 10])   
    # If countries are selected, make the GDP range from 0 to 1.2 times the max value for visual purposes.
    else: 
        fig.update_yaxes(range = [0, int(max(dff['GDP'])) * 1.2])   
                          
    return fig



# Run the app
# if __name__ == '__main__':
#     app.run(debug=True, port=8051)
if __name__ == '__main__':
    app.run_server(debug=True)



