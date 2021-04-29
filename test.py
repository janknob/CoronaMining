import pandas as pd
import plotly.graph_objs as go


# Tschechische Landkreise
df = pd.read_csv ('kraj-okres-nakazeni-vyleceni-umrti (1).csv')
df.columns = ['date', 'state', 'district', 'district_cz_infected_number', 'healed', 'deaths']
df.drop(df.index[(df["district"] != "CZ0411")],axis=0,inplace=True) #Funktion für Landrkeis Auswahl
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

filtered_df = df.loc[(df['date'] >= '2020-03-02')
                     & (df['date'] < '2021-03-02')]
filtered_df.drop(filtered_df.columns.difference(['date', 'district_cz_infected_number']), 1, inplace=True)
print(filtered_df.to_string())
df_cleaned = df.dropna()

# Deutsche Landkreise
df2 = pd.read_csv('https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv')
df2['time_iso8601'] = pd.to_datetime(df2['time_iso8601'])
df2['date'] = df2['time_iso8601'].dt.date
df2['district_de_infected_number'] = df2['9377']
df2.drop(df2.columns.difference(['date', 'district_de_infected_number']), 1, inplace=True)


df2['date'] = pd.to_datetime(df2['date'], format='%Y-%m-%d')
filtered_df2 = df2.loc[(df2['date'] >= '2020-03-02')
                     & (df2['date'] < '2021-03-02')]
print(df2.to_string())

# Plot
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = filtered_df2['date'],
        y = filtered_df2['district_de_infected_number'].diff(),
        name="Tirschenreuth"
    )
)
fig.add_trace(
    go.Scatter(
        x = filtered_df['date'],
        y = filtered_df['district_cz_infected_number'].diff(),
        name="Cheb"
    )
)
fig.update_yaxes( dtick=10)

fig.update_xaxes(
    dtick="M1")
fig.update_layout(height=800, width=1500, title_text="Landkreis Tirschenreuth im Vergleich zu Landkreis Cheb")
fig.show()

# Korrelation
merged_df = filtered_df.merge(filtered_df2, how='inner', left_on=["date"], right_on=["date_only"])

s5 = merged_df["infected"]
s6 = merged_df["9377"]
print(merged_df)

print("KorrelationTest: ", s5.corr(s6))