## Begin necessary library imports
# Import file and data handling
import os
import pandas as pd
import numpy as np

# Import regex
import re

# Import Counter
from collections import Counter

# Import streamlit
import streamlit as st

# Import relevant dash libraries
from jupyter_dash import JupyterDash
from dash import dcc
from dash import dash_table
from dash import html
from dash.dependencies import Input, Output

# Import plotly visualization support
import plotly.express as px

# File path to access the data
filepath = "/Users/lesli/OneDrive/Desktop/Python Projects/Plotly Dashboard/Streamlit/data/ux-resops-test2021.csv"

##### DATAFRAME FOR DASHBOARD #####

## Cache the dataframe to improve web app performance - 
## Doesn't work here because manipulating columns after load
## Code example below for future reference
##@st.cache
##def get_excel_data():
    ## Gets the dataframe
    ##df= pd.read_csv(os.path.join(filepath, files[3]))
    ## returns the dataframe
    ##return df

##df = get_excel_data()

df= pd.read_csv(os.path.join(filepath))

## Begin cleaning the data
# Gather column names into a list and convert to lowercase
columns = [c for c in df.columns]

# Maps column names
column_map = {}

# Iterate through column list
for col in columns:
    # Set the dictionary key to the actual column name
    key = col
    # Get the column name from the actual column name to process as the dictionary value
    col_name = col
    # If there is a space in the column name
    if re.search(r"\s", col_name):
        # Replace space with underscore
        col_name = col_name.replace(" ", "_")
    # If there is a non-alphanumeric in the column name
    elif re.search(r"\W+", col_name):
        # Extract the first part of the string
        col_name = re.findall("[\dA-Za-z]*", col)[0]
    # If no space or alphanumeric
    else:
        # Nothing needed
        col_name = col
    # Add to mapping dictionary
    column_map[key] = col_name.lower()

# View new column names
print(column_map)
    
# Rename all columns
df.rename(columns = column_map, inplace = True)

##### PAGE CONFIGURATION #####

# Configuration initialization
st.set_page_config(page_title = "UX Research Ops Dashboard - Streamlit PoC",
                   page_icon = ":bar_chart:",
                   layout = "wide")

## Note: Create config.toml in a .streamlit folder to theme this web app

##### SIDEBAR #####
## Users will filter the dashboard from the sidebar ##

# Create a sidebar
st.sidebar.header("Dashboard Filters")

### INDIVIDUAL FILTERS ###
# Project Code - users should view multiple
project = st.sidebar.multiselect("Project Code:",
                                 options = df["project_code"].unique(),
                                 default = df["project_code"].unique())

# Type - users should view multiple
type = st.sidebar.multiselect("Participant Type:",
                              options = df["type"].unique(),
                              default = df["type"].unique())

# Year - users should view multiple
year = st.sidebar.multiselect("Year:",
                              options = df["year"].unique(),
                              default = df["year"].unique())

# Research Topic - users should view multiple
topic = st.sidebar.multiselect("Research Topic:",
                               options = df["product"].unique(),
                               default = df["product"].unique())

### LINK FILTERS TO DATAFRAME ###
# Link between multiselects defined above and the dataframe columns
# column @ multiselect variable
df_filtered = df.query("project_code == @project & type == @type & year == @year & product == @topic")

##### MAIN PAGE DASHBOARD #####
# Set dashboard title
st.title("UX ResearchOps Dashboard")

# Markdown
st.markdown("##")

### KPI CARD DEFINITION ###
# Total number of participants across all studies - allows for repeat participants
total_participants = int(df_filtered["type"].count())

# Total number of projects - count only the number of unique projects
total_projects = df_filtered["project_code"].nunique()

# Total number of topics researched - count only the number of unique topics
total_topics = df_filtered["product"].nunique()

### KPI CARD DISPLAY ###
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Participants for All Projects")
    st.subheader(total_participants)
with middle_column:
    st.subheader("Total Projects Run")
    st.subheader(total_projects)
with right_column:
    st.subheader("Total Topics Researched")
    st.subheader(total_topics)
    
# Markdown for separation
st.markdown("-----")

##### GRAPHS #####
## Note: Make calculations in a Jupyter notebook to ensure correctness of results, then copy results and paste into here
## Graphs will rely upon plotly express library

# Set the color scheme
wheels = ['#56A0D3','#679146', '#EC881D', '#ABB518', '#7C2B83', '#FEC057', '#85CDDB']                         

# PARTICIPANT TYPE: PIE CHART
# Counter object
participant_counter = Counter(df_filtered["type"])

# Create pie chart object
fig_participant_type = px.pie(df_filtered,
                              values = participant_counter.values(),
                              names = participant_counter.keys(),
                              title = "Participant Types",
                              color_discrete_sequence = wheels,
                              template = "simple_white")

# Make the chart plot
st.plotly_chart(fig_participant_type)

### PROJECT CODES: PIE CHART
# Counter object
project_counter = Counter(df_filtered["project_code"])

# Sorted object
sorted_project_codes = {}

# Sort in alphabetical order of keys
for k,v in sorted(project_counter.items()):
    # Add to 
    sorted_project_codes.update({k:v})

# Create pie chart object
fig_project_codes = px.pie(df_filtered, 
                           values = sorted_project_codes.values(), 
                           names = sorted_project_codes.keys(), 
                           title = "Project Codes",
                           color_discrete_sequence = wheels,
                           template = "simple_white")

## Note: To make further visual changes, either use inline styling in the px.pie style = {} or .update_layout()
## before allowing the chart to display

# Make the chart plot
st.plotly_chart(fig_project_codes)

### RESEARCH TOPICS: PIE CHART
# Counter object
topic_counter = Counter(df_filtered["product"])

# Sorted object
sorted_topics = {}

# Sort in alphabetical order of keys
for k,v in sorted(topic_counter.items()):
    # Add
    sorted_topics.update({k:v})
    
# Create pie chart object
fig_topics = px.pie(df_filtered,
                    values = sorted_topics.values(),
                    names = sorted_topics.keys(),
                    title = "Research Topics",
                    color_discrete_sequence = wheels,
                    template = "simple_white")

# Display the pie chart
st.plotly_chart(fig_topics)