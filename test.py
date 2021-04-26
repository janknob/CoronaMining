import pandas as pd
import plotly.graph_objs as go


# Tschechische Landkreise
df = pd.read_csv ('kraj-okres-nakazeni-vyleceni-umrti (1).csv')
df.columns = ['date', 'state', 'district', 'infected', 'healed', 'deaths']
df.drop(df.index[(df["district"] != "CZ0411")],axis=0,inplace=True) #Funktion für Landrkeis Auswahl
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
#df.drop(df[(df['date'].df.year == 2021 | df['date'].df.month > 2 )])

filtered_df = df.loc[(df['date'] >= '2020-03-02')
                     & (df['date'] < '2021-03-02')]
filtered_df.drop(filtered_df.columns.difference(['date', 'infected']), 1, inplace=True)
print(filtered_df.to_string())
df_cleaned = df.dropna()

# Deutsche Landkreise
df2 = pd.read_csv('https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv')
df2['time_iso8601'] = pd.to_datetime(df2['time_iso8601'])
df2.drop(df2.columns.difference(['time_iso8601','9377']), 1, inplace=True)
df2['date_only'] = df2['time_iso8601'].dt.date

df2['date_only'] = pd.to_datetime(df2['date_only'], format='%Y-%m-%d')
filtered_df2 = df2.loc[(df2['date_only'] >= '2020-03-02')
                     & (df2['date_only'] < '2021-03-02')]
filtered_df2.drop(filtered_df2.columns.difference(['date_only','9377']), 1, inplace=True)
print(df2.to_string())

# Plot
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
    dtick="M1")
fig.update_layout(height=800, width=1500, title_text="Cheb im Vergleich zu Tirscheinreuth")
#fig.show()

# Korrelation
merged_df = filtered_df.merge(filtered_df2, how='inner', left_on=["date"], right_on=["date_only"])

s5 = merged_df["infected"]
s6 = merged_df["9377"]
print(merged_df)

print("KorrelationTest: ", s5.corr(s6))