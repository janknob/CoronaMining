import pandas as pd
import plotly.graph_objs as go
from sklearn import preprocessing

# import Tscheschien
czech_df = pd.read_csv('kraj-okres-nakazeni-vyleceni-umrti (1).csv')
'''czech_df.columns = ['date', 'state', 'district', 'district_cz_infected_number', 'healed', 'deaths']
czech_df['date_cz'] = pd.to_datetime(czech_df['date'], format='%Y-%m-%d')
czech_df.drop(['date'], axis=1, inplace=True)'''

# import Germany
german1 = pd.read_csv('https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv')
#german_df['time_iso8601'] = pd.to_datetime(german_df['time_iso8601'])
#german_df['date_de'] = german_df['time_iso8601'].dt.date
#german_df.drop(['sum_cases', 'time_iso8601'], axis=1, inplace=True)

# filter timeframe Tschechien
#filtered_czech_df = czech_df.loc[(czech_df['date_cz'] >= '2020-03-02')
                                 #& (czech_df['date_cz'] < '2021-03-02')]

# filter timeframe Germany
#german_df['date_de'] = pd.to_datetime(german_df['date_de'], format='%Y-%m-%d')
#filtered_german_df = german_df.loc[(german_df['date_de'] >= '2020-03-02')
                                   #& (german_df['date_de'] < '2021-03-02')]


# normalisation
#filtered_german_df.drop(['date_de'], axis=1, inplace=True)
#x = filtered_german_df.values #returns a numpy array
#min_max_scaler = preprocessing.MinMaxScaler()
#x_scaled = min_max_scaler.fit_transform(x)
#norm_german_df = pd.DataFrame(x_scaled)
#print('German: ', norm_german_df)

# normalisation
'''filtered_czech_df.drop(['date_cz', 'state', 'district'], axis=1, inplace=True)
#print('filterd cz: ', filtered_czech_df)
x = filtered_czech_df.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
norm_czech_df = pd.DataFrame(x_scaled)
#print('normalisiert cz:', norm_czech_df)'''


# DE districts
Freyung_Grafenau = "9272"
Regen = "9276"
Cham = "9372"
Schwandorf = "9376"
Neudstadt_Waldnaab = "9374"
Tirschenreuth = "9377"
Wunsiedel = "9479"
Hof = "9475"
Vogtlandkreis = "14523"
Erzgebirgskreis = "14521"
Mittelsachsen = "14522"
Sächsische_Schweiz = "14628"
Bautzen = "14625"
Görlitz = "14626"

# CZ districts
Prachatitz = "CZ0315"  # Prachatitz (Prachatice)
Klattau = "CZ0315"  # Klattau (Klatovy)
Taus = "CZ0321"  # Taus (Domažlice)
Tachau = "CZ0327"  # Tachau (Tachov)
Eger = "CZ0411"  # Eger (Cheb)
Falkenau = "CZ0413"  # Falkenau (Sokolov)
Karlsbad = "CZ0412"  # Karlsbad (Karlovy Vary)
Komotau = "CZ0422"  # Komotau (Chomutov)
Brux = "CZ0425"  # Brux (Most)
Teplitz_Schönau = "CZ0426"  # Teplitz-Schönau (Teplice)
Aussig = "CZ0427"  # Aussig (Ústí nad Labem)
Tetschen = "CZ0421"  # Tetschen (Děčín)
Böhmisch_Leipa = "CZ0511"  # Böhmisch Leipa (Česká Lípa)


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


def vergleicheTirschenreuthMitCheb(germandf, czechdf):
    czechdf.drop(czechdf.index[(czechdf["district"] != Eger)], axis=0,
                 inplace=True)  # Hier Landkreis Schlüssel ändern (Hier Cheb)

    czechdf.drop(czechdf.columns.difference(['date_cz', 'district_cz_infected_number']), 1,
                 inplace=True)
    # print(czechdf.to_string())
    df_cleaned = czech_df.dropna()

    germandf['district_de_infected_number'] = germandf[
        Tirschenreuth]  # Hier Landkreis Schlüssel ändern (Hier Tirschenreuth)
    germandf.drop(germandf.columns.difference(['date_de', 'district_de_infected_number']), 1,
                  inplace=True)

    # print(czechdf.to_string())

    plot(germandf['date_de'], germandf['district_de_infected_number'].diff(), 'Tirschenreuth',
         czechdf['date_cz'], czechdf['district_cz_infected_number'].diff(), "Cheb",
         "Landkreis Tirschenreuth im Vergleich zu Landkreis Cheb")


# Correlation
def correlation(df1, df2):
    merged_df = df1.merge(df2, how='inner', left_on=["date_cz"], right_on=["date_de"])

    x1 = merged_df["district_cz_infected_number"]
    x2 = merged_df["district_de_infected_number"]
    print(merged_df)

    print("Korrelation: ", x2.corr(x1))


'''Hier wird verglichen, ob die Durchschnittliche Infektionszahlen deutscher Randgebiete 
höher leigen als der Bundesweite Durschscnitt'''


def calcAvg(df):
    df['daily_avg'] = round(df.mean(axis=1), 2)
    return df


# Functions

#filtered_german_df.drop(['sum_cases'], axis=1, inplace=True)
'''print(filtered_german_df)
calcAvg(filtered_german_df)
print(filtered_german_df)
'''

german1 = german1.copy(deep=True)
#czech_df = filtered_czech_df.copy(deep=True)
print('Testprint:', german1)
#vergleicheTirschenreuthMitCheb(german_df, czech_df)
#correlation(filtered_czech_df, filtered_german_df)


