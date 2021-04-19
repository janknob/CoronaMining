import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv ('kraj-okres-nakazeni-vyleceni-umrti (1).csv')
df.drop(df.index[(df["okres_lau_kod"] != "CZ0411")],axis=0,inplace=True)
print(df.to_string())
df_cleaned = df.dropna()

"""fig = px.line(df, x = 'datum', y = 'kumulativni_pocet_vylecenych', title='Fallzahlen Tirschenreuth - Cheb')
fig.show()"""

df2 = pd.read_csv('https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv')
print(df2.to_string())

fig = make_subplots(rows=1, cols = 2)

fig.add_trace(go.Scatter(x=df['datum'],
                         y=df['kumulativni_pocet_vylecenych'].diff()),
                         row=1, col=1)
fig.add_trace(go.Scatter(x=df2['time_iso8601'],
                         y=df2['9377'].diff()),
                         row=1, col=2
                         )
fig.update_layout(height=600, width=800, title_text="Cheb im Vergleich zu Tirscheinreuth")
fig.show()
