
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


plot_names = ["StrategyA: k=2", "StrategyA: k=3", "StrategyB: k=2", "StrategyB: k=3"]
sizes = ['10KB', '100KB', '1MB', '10MB', '100MB']

stratA_k2 = ["replica_k2strategyA10KB.csv","replica_k2strategyA100KB.csv","replica_k2strategyA1MB.csv",
            "replica_k2strategyA10MB.csv", "replica_k2strategyA100MB.csv"]
stratA_k3 = ["replica_k3strategyA10KB.csv","replica_k3strategyA100KB.csv","replica_k3strategyA1MB.csv",
            "replica_k3strategyA10MB.csv", "replica_k3strategyA100MB.csv"]
stratB_k2 = ["replica_k2strategyB10KB.csv","replica_k2strategyB100KB.csv","replica_k2strategyB1MB.csv",
            "replica_k2strategyB10MB.csv", "replica_k2strategyB100MB.csv"]
stratB_k3 = ["replica_k3strategyB10KB.csv","replica_k3strategyB100KB.csv","replica_k3strategyB1MB.csv",
            "replica_k3strategyB10MB.csv", "replica_k3strategyB100MB.csv"]



means_stratA_k2 = process_strategy(stratA_k2, sizes)     
means_stratA_k3 = process_strategy(stratA_k3, sizes)
means_stratB_k2 = process_strategy(stratB_k2, sizes)       
means_stratB_k3 = process_strategy(stratB_k3, sizes)

trace0 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_k2, name=plot_names[0], nbinsx=5)
trace1 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_k3, name=plot_names[1], nbinsx=5)
trace2 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_k2, name=plot_names[2], nbinsx=5)
trace3 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_k3, name=plot_names[3], nbinsx=5)

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=["Strategy A vs Strategy B with k = 2", "Strategy A vs Strategy B with k = 3"])
    
fig.update_yaxes(title_text="Seconds", range = [0,26])
fig.update_xaxes(title_text="File Sizes")

fig.append_trace(trace2, 1, 1)
fig.append_trace(trace0, 1, 1)
fig.append_trace(trace3, 1, 2)
fig.append_trace(trace1, 1, 2)

fig.update_layout(height=600, width=1600, title_text="Store file comparison")
fig.show()       




