import pandas as pd
import plotly.express as px
from plotly.graph_objs.histogram import Marker
from plotly.graph_objs.histogram.marker import ColorBar, Pattern
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def calculateMean(df, column, outliers_remove):
    df = df.sort_values(by=[column])
    df = df.iloc[outliers_remove:].iloc[:-outliers_remove]
    acum = 0

    for i, entry in df.iterrows():
        acum += float(entry[column])

    return acum/len(df)

def retrieveMeans(df, column, storage_mode, max_erasures, sizes, outliers_remove=5):
    means = []

    for size in sizes:
        data = df[(df.storage_mode == storage_mode) &
                  (df.max_erasures == max_erasures) &
                  (df.file_size == size)]

        if size == '100MB' or size == '104857600':
            outliers_remove = 1

        means.append(calculateMean(data, column, outliers_remove))
    return means

plot_names = ["StrategyA: l=1", "StrategyA: l=2", "StrategyB: l=1", "StrategyB: l=2"]
sizes = ['10KB', '100KB', '1MB', '10MB', '100MB']
# END TO END
df = pd.read_csv('logs/client_results_1.csv')

#region write_time
col = 'write_time'
df = df.sort_values(by=[col])


means_stratA_l1 = retrieveMeans(df, col, 'erasure_coding_rs', '1', sizes)
means_stratA_l2 = retrieveMeans(df, col, 'erasure_coding_rs', '2', sizes)
means_stratB_l1 = retrieveMeans(df, col, 'erasure_coding_rs_random_worker', '1', sizes)
means_stratB_l2 = retrieveMeans(df, col, 'erasure_coding_rs_random_worker', '2', sizes)

traces = []

trace0 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_l1, name=plot_names[0], nbinsx=5)
trace1 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_l2, name=plot_names[1], nbinsx=5)
trace2 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_l1, name=plot_names[2], nbinsx=5)
trace3 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_l2, name=plot_names[3], nbinsx=5)

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["Strategy A vs Strategy B with l = 1",
                    "Strategy A vs Strategy B with l = 2"],
    x_title='File Size',
    y_title='Seconds')

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace2, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace3, 1, 2)

fig.update_layout(height=600, width=1600, title_text="Store file comparison", title_x=0.5)
fig.show()

#endregion

#region read_time
col = 'read_time'
df = df.sort_values(by=[col])


means_stratA_l1 = retrieveMeans(df, col, 'erasure_coding_rs', '1', sizes)
means_stratA_l2 = retrieveMeans(df, col, 'erasure_coding_rs', '2', sizes)
means_stratB_l1 = retrieveMeans(df, col, 'erasure_coding_rs_random_worker', '1', sizes)
means_stratB_l2 = retrieveMeans(df, col, 'erasure_coding_rs_random_worker', '2', sizes)

traces = []

trace0 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_l1, name=plot_names[0], nbinsx=5)
trace1 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_l2, name=plot_names[1], nbinsx=5)
trace2 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_l1, name=plot_names[2], nbinsx=5)
trace3 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_l2, name=plot_names[3], nbinsx=5)

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["Strategy A vs Strategy B with l = 1",
                    "Strategy A vs Strategy B with l = 2"],
    x_title='File Size',
    y_title='Seconds')

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace2, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace3, 1, 2)

fig.update_layout(height=600, width=1600, title_text="Read file comparison", title_x=0.5)
fig.show()

#endregion

sizes_int = ['10240', '102400', '1048576', '10485760', '104857600']

# Lead Node internal timings
df = pd.read_csv('logs/erasure_server_results_1.csv')

#region encoding
col = 'time'
filtered_df_stratA = df[(df.event == 'erasure_write') & (df.storage_mode == 'erasure_coding_rs')]
filtered_df_stratA = filtered_df_stratA.sort_values(by=['time'])

filtered_df_stratB = df[(df.event == 'erasure_write_worker_response') & (df.storage_mode == 'erasure_coding_rs_random_worker')]
filtered_df_stratB = filtered_df_stratB.sort_values(by=['time'])

means_stratA_l1 = retrieveMeans(filtered_df_stratA, col, 'erasure_coding_rs', '1', sizes_int)
means_stratA_l2 = retrieveMeans(filtered_df_stratA, col, 'erasure_coding_rs', '2', sizes_int)
means_stratB_l1 = retrieveMeans(filtered_df_stratB, col, 'erasure_coding_rs_random_worker', '1', sizes_int)
means_stratB_l2 = retrieveMeans(filtered_df_stratB, col, 'erasure_coding_rs_random_worker', '2', sizes_int)

traces = []

trace0 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_l1, name=plot_names[0], nbinsx=5)
trace1 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_l2, name=plot_names[1], nbinsx=5)
trace2 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_l1, name=plot_names[2], nbinsx=5)
trace3 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_l2, name=plot_names[3], nbinsx=5)

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["Strategy A vs Strategy B with l = 1",
                    "Strategy A vs Strategy B with l = 2"],
    x_title='File Size',
    y_title='Seconds')

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace2, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace3, 1, 2)

fig.update_layout(height=600, width=1600, title_text="Encoding comparison", title_x=0.5)
fig.show()

#endregion

#region decoding
col = 'time'

filtered_df_stratA = df[(df.event == 'erasure_get_response') & (df.storage_mode == 'erasure_coding_rs')]
filtered_df_stratA = filtered_df_stratA.sort_values(by=['time'])

filtered_df_stratB = df[(df.event == 'erasure_get_random_worker_response') & (df.storage_mode == 'erasure_coding_rs_random_worker')]
filtered_df_stratB = filtered_df_stratB.sort_values(by=['time'])

means_stratA_l1 = retrieveMeans(filtered_df_stratA, col, 'erasure_coding_rs', '1', sizes_int)
means_stratA_l2 = retrieveMeans(filtered_df_stratA, col, 'erasure_coding_rs', '2', sizes_int)
means_stratB_l1 = retrieveMeans(filtered_df_stratB, col, 'erasure_coding_rs_random_worker', '1', sizes_int)
means_stratB_l2 = retrieveMeans(filtered_df_stratB, col, 'erasure_coding_rs_random_worker', '2', sizes_int)

traces = []

trace0 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_l1, name=plot_names[0], nbinsx=5)
trace1 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_l2, name=plot_names[1], nbinsx=5)
trace2 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_l1, name=plot_names[2], nbinsx=5)
trace3 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_l2, name=plot_names[3], nbinsx=5)

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["Strategy A vs Strategy B with l = 1",
                    "Strategy A vs Strategy B with l = 2"],
    x_title='File Size',
    y_title='Seconds')

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace2, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace3, 1, 2)

fig.update_layout(height=600, width=1600, title_text="Decoding comparison", title_x=0.5)
fig.show()


#endregion

#region Lead node complete it task when writing
col = 'time'
filtered_df = df[(df.event == 'erasure_write')]
filtered_df = filtered_df.sort_values(by=['time'])

means_stratA_l1 = retrieveMeans(filtered_df, col, 'erasure_coding_rs', '1', sizes_int)
means_stratA_l2 = retrieveMeans(filtered_df, col, 'erasure_coding_rs', '2', sizes_int)
means_stratB_l1 = retrieveMeans(filtered_df, col, 'erasure_coding_rs_random_worker', '1', sizes_int)
means_stratB_l2 = retrieveMeans(filtered_df, col, 'erasure_coding_rs_random_worker', '2', sizes_int)

traces = []

trace0 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_l1, name=plot_names[0], nbinsx=5)
trace1 = go.Histogram(histfunc="sum", x=sizes, y=means_stratA_l2, name=plot_names[1], nbinsx=5)
trace2 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_l1, name=plot_names[2], nbinsx=5)
trace3 = go.Histogram(histfunc="sum", x=sizes, y=means_stratB_l2, name=plot_names[3], nbinsx=5)

fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=["Strategy A vs Strategy B with l = 1",
                    "Strategy A vs Strategy B with l = 2"],
    x_title='File Size',
    y_title='Seconds')

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace2, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace3, 1, 2)

fig.update_layout(height=600, width=1600, title_text="Lead node complete with its task when writing", title_x=0.5)
fig.show()
#endregion
