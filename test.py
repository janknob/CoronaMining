import numpy as np
import pandas as pd
import plotly.graph_objs as go

# import Tscheschien
df = pd.read_csv('kraj-okres-nakazeni-vyleceni-umrti (1).csv')
df.columns = ['date', 'state', 'district', 'district_cz_infected_number', 'healed', 'deaths']
df['date_cz'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# import Germany
df2 = pd.read_csv('https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv')
df2['time_iso8601'] = pd.to_datetime(df2['time_iso8601'])
df2['date_de'] = df2['time_iso8601'].dt.date

# filter timeframe Tschechien
filtered_df = df.loc[(df['date_cz'] >= '2020-03-02')
                     & (df['date_cz'] < '2021-03-02')]

# filter timeframe Germany
df2['date_de'] = pd.to_datetime(df2['date_de'], format='%Y-%m-%d')
filtered_df2 = df2.loc[(df2['date_de'] >= '2020-03-02')
                       & (df2['date_de'] < '2021-03-02')]


def vergleicheTirschenreuthMitCheb():
    filtered_df.drop(filtered_df.index[(filtered_df["district"] != "CZ0411")], axis=0,
                     inplace=True)  # Funktion für Landrkeis Auswahl

    filtered_df.drop(filtered_df.columns.difference(['date_cz', 'district_cz_infected_number']), 1, inplace=True)
    print(filtered_df.to_string())
    df_cleaned = df.dropna()

    filtered_df2['district_de_infected_number'] = filtered_df2[
        '9377']  # Hier Landkreis Schlüssel ändern (Hier Tirschenreuth)
    filtered_df2.drop(filtered_df2.columns.difference(['date_de', 'district_de_infected_number']), 1, inplace=True)

    print(filtered_df.to_string())

    plot(filtered_df2['date_de'], filtered_df2['district_de_infected_number'].diff(), 'Tirschenreuth', filtered_df['date_cz'], filtered_df['district_cz_infected_number'].diff(), "Cheb", "Landkreis Tirschenreuth im Vergleich zu Landkreis Cheb")

    '''# Plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered_df2['date_de'],
            y=filtered_df2['district_de_infected_number'].diff(),
            name="Tirschenreuth"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=filtered_df['date_cz'],
            y=filtered_df['district_cz_infected_number'].diff(),
            name="Cheb"
        )
    )
    fig.update_yaxes(dtick=10)

    fig.update_xaxes(
        dtick="M1")
    fig.update_layout(height=800, width=1500, title_text="Landkreis Tirschenreuth im Vergleich zu Landkreis Cheb")
    fig.show()'''

    # Korrelation
    merged_df = filtered_df.merge(filtered_df2, how='inner', left_on=["date_cz"], right_on=["date_de"])

    x1 = merged_df["district_cz_infected_number"]
    x2 = merged_df["district_de_infected_number"]
    print(merged_df)

    print("KorrelationTest: ", x2.corr(x1))


'''Hier wird verglichen, ob die Durchschnittliche Infektionszahlen deutscher Randgebiete höher leigen als der Bundesweite Durschscnitt'''

def calAvg(dataframe):
    dataframe['daily_avg'] = dataframe.mean(axis=1)
    return dataframe




def plot(x1, y1, name_1, x2, y2, name_2, title):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x1,
            y=y1,
            name=name_1
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x2,
            y=y2,
            name=name_2
        )
    )
    fig.update_yaxes(dtick=10)

    fig.update_xaxes(
        dtick="M1")
    fig.update_layout(height=800, width=1500, title_text=title)
    fig.show()







# Funktionen hier aufrufen
vergleicheTirschenreuthMitCheb()


filtered_df2.drop(['sum_cases', 'time_iso8601'], axis=1, inplace=True)
print(filtered_df2)
calAvg(filtered_df2)
print(filtered_df2)