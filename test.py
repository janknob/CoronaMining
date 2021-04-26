import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv ('kraj-okres-nakazeni-vyleceni-umrti (1).csv')
df.columns = ['date', 'state', 'district', 'infected', 'healed', 'deaths']
df.drop(df.index[(df["district"] != "CZ0411")],axis=0,inplace=True)
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
#df.drop(df[(df['date'].df.year == 2021 | df['date'].df.month > 2 )])

filtered_df = df.loc[(df['date'] >= '2020-03-01')
                     & (df['date'] < '2021-03-01')]
print(filtered_df.to_string())
df_cleaned = df.dropna()

"""fig = px.line(df, x = 'datum', y = 'kumulativni_pocet_vylecenych', title='Fallzahlen Tirschenreuth - Cheb')
fig.show()"""

df2 = pd.read_csv('https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv')
df2['time_iso8601'] = pd.to_datetime(df2['time_iso8601'])
#df2['time_iso8601'] = pd.to_datetime(df.time_iso8601)
df2['date_only'] = df2['time_iso8601'].dt.date
df2['date_only'] = pd.to_datetime(df2['date_only'], format='%Y-%m-%d')
filtered_df2 = df2.loc[(df2['date_only'] >= '2020-03-01')
                     & (df2['date_only'] < '2021-03-01')]
print(df2.to_string())

#fig = make_subplots(rows=1, cols = 2)
#fig = go.Figure()
#fig.add_trace(go.Scatter(x=filtered_df['date'],
#                         y=filtered_df['infected'].diff()),
#                         row=1, col=1)
#fig.add_trace(go.Scatter(x=filtered_df2['date_only'],
#                         y=filtered_df2['9377'].diff()),
#                         row=1, col=2
#                        )
#fig.update_layout(height=600, width=800, title_text="Cheb im Vergleich zu Tirscheinreuth")
#fig.show()

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = filtered_df['date'],
        y = filtered_df['infected'].diff(),
        name="Cheb"
    )
)
fig.add_trace(
    go.Scatter(
        x = filtered_df2['date_only'],
        y = filtered_df2['9377'].diff(),
        name="Tirschenreuth"
    )
)
fig.update_yaxes( dtick=10)

fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")
fig.update_layout(height=800, width=1500, title_text="Cheb im Vergleich zu Tirscheinreuth")
fig.show()
