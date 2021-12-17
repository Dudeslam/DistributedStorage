
import pandas as pd
import plotly.express as px
from plotly.graph_objs.histogram import Marker
from plotly.graph_objs.histogram.marker import ColorBar, Pattern
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def read_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.sort_values(by=['time'])



fig = make_subplots(
    rows=5,
    cols=2,
    subplot_titles=("size=10KB,     k=2",   "size=10KB,     k=3",
                    "size=100KB,    k=2",   "size=100KB,    k=3",
                    "size=1MB,      k=2",   "size=1MB,      k=3",
                    "size=10MB,     k=2",   "size=10MB,     k=3",
                    "size=100MB,    k=2",   "size=100MB,    k=3"),
    x_title='seconds',
    y_title='counts')

fig.show()       