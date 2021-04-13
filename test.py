import pandas as pd
import plotly.express as px

df = pd.read_csv ('https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-state.csv')
print(df.to_string())

fig = px.line(df, x = 'time_iso8601', y = 'DE-BY', title='Fallzahlen Bayern')
fig.show()