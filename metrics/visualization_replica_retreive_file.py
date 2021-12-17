
from os import name, stat
from numpy.core.fromnumeric import size
import pandas as pd
import plotly.express as px
from plotly.graph_objs.histogram import Marker
from plotly.graph_objs.histogram.marker import ColorBar, Pattern
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def read_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.sort_values(by=['time'])
    return df

def remove_outlier_mean(df):
    skip = 5
    acum = 0
    for i, entry in df.iterrows():
        if i >= skip and i<=(len(df)-skip):
            acum += float(entry['time'])

    return acum/len(df)

def process_strategy(stratA_file_list, sizes):
    means = []
    for index, csv_file in enumerate(stratA_file_list):
        df = read_csv(f"logs/{csv_file}")
        df = df.sort_values(by=['time'])
        mean = remove_outlier_mean(df)
        means.append(str(mean))
        print(f"{sizes[index]}: \t{mean}")
        
    return means


sizes = ['10KB', '100KB', '1MB', '10MB', '100MB']

retrieve = ["retrieve_10KB.csv","retrieve_100KB.csv","retrieve_1MB.csv","retrieve_10MB.csv","retrieve_100MB.csv"]

means_stratA_k2 = process_strategy(retrieve, sizes)     


trace0 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_k2, nbinsx=5)

fig = make_subplots(
    rows=1, cols=1,
    subplot_titles=["Retrieve file comparison"])
    
fig.update_yaxes(title_text="Seconds")
fig.update_xaxes(title_text="File Sizes")

fig.append_trace(trace0, 1, 1)

fig.update_layout(height=600, width=600)
fig.show()       




