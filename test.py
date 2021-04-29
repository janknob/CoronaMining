import pandas as pd
import plotly.graph_objs as go


# Tschechische Landkreise
df = pd.read_csv ('kraj-okres-nakazeni-vyleceni-umrti (1).csv')
df.columns = ['date', 'state', 'district', 'district_cz_infected_number', 'healed', 'deaths']
df.drop(df.index[(df["district"] != "CZ0411")],axis=0,inplace=True) #Funktion für Landrkeis Auswahl
df['date_cz'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

filtered_df = df.loc[(df['date_cz'] >= '2020-03-02')
                     & (df['date_cz'] < '2021-03-02')]
filtered_df.drop(filtered_df.columns.difference(['date_cz', 'district_cz_infected_number']), 1, inplace=True)
print(filtered_df.to_string())
df_cleaned = df.dropna()

# Deutsche Landkreise
df2 = pd.read_csv('https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv')
df2['time_iso8601'] = pd.to_datetime(df2['time_iso8601'])
df2['date_de'] = df2['time_iso8601'].dt.date
df2['district_de_infected_number'] = df2['9377'] #Hier Landkreis Schlüssel ändern
df2.drop(df2.columns.difference(['date_de', 'district_de_infected_number']), 1, inplace=True)


df2['date_de'] = pd.to_datetime(df2['date_de'], format='%Y-%m-%d')
filtered_df2 = df2.loc[(df2['date_de'] >= '2020-03-02')
                     & (df2['date_de'] < '2021-03-02')]
print(df2.to_string())

# Plot
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x = filtered_df2['date_de'],
        y = filtered_df2['district_de_infected_number'].diff(),
        name="Tirschenreuth"
    )
)
fig.add_trace(
    go.Scatter(
        x = filtered_df['date_cz'],
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
merged_df = filtered_df.merge(filtered_df2, how='inner', left_on=["date_cz"], right_on=["date_de"])

s5 = merged_df["district_cz_infected_number"]
s6 = merged_df["district_de_infected_number"]
print(merged_df)

print("KorrelationTest: ", s5.corr(s6))