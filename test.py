import pandas as pd
import plotly.graph_objs as go
pd.options.mode.chained_assignment = None  # default='warn'
#from sklearn import preprocessing

# import Tscheschien
czech_origin_data = pd.read_csv('kraj-okres-nakazeni-vyleceni-umrti (1).csv')
czech_origin_data.columns = ['date', 'state', 'district', 'district_cz_infected_number', 'healed', 'deaths']
czech_origin_data['date'] = pd.to_datetime(czech_origin_data['date'], format='%Y-%m-%d')

# import Germany
german_origin_data = pd.read_csv('https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv')
german_origin_data['time_iso8601'] = pd.to_datetime(german_origin_data['time_iso8601'])
german_origin_data['date'] = german_origin_data['time_iso8601'].dt.date
german_origin_data['date'] = pd.to_datetime(german_origin_data['date'], format='%Y-%m-%d')
german_origin_data.drop(['sum_cases', 'time_iso8601'], axis=1, inplace=True)

#filter timeframe Tschechien
filtered_czech_df = czech_origin_data.loc[(czech_origin_data['date'] >= '2020-03-02')
                                 & (czech_origin_data['date'] < '2021-03-02')]

# filter timeframe Germany
filtered_german_df = german_origin_data.loc[(german_origin_data['date'] >= '2020-03-02')
                                   & (german_origin_data['date'] < '2021-03-02')]

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


def compareCountries(germandf, german_what, czechdf, czech_what, title):
    czechdf.drop(czechdf.index[(czechdf["district"] != czech_what)], axis=0,
                 inplace=True)

    czechdf.drop(czechdf.columns.difference(['date', 'district_cz_infected_number']), 1,
                 inplace=True)

    germandf['district_de_infected_number'] = germandf[german_what]
    germandf.drop(germandf.columns.difference(['date', 'district_de_infected_number']), 1,
                  inplace=True)
    df_norm_de = min_max_scaling(germandf)
    df_norm_cz = min_max_scaling(czechdf)
    germandf_final_norm = join_date(germandf, df_norm_de)
    czechdf_final_norm = join_date(czechdf, df_norm_cz)

    print("1",czechdf_final_norm)
    print("2",germandf_final_norm)

    plot(germandf_final_norm['date'], germandf_final_norm['district_de_infected_number'].diff(), german_what,
         czechdf_final_norm['date'], czechdf_final_norm['district_cz_infected_number'].diff(), czech_what,
         title)


# Correlation
def correlation(df1, df2):
    merged_df = df1.merge(df2, how='inner', left_on=["date"], right_on=["date"])

    x1 = merged_df["district_cz_infected_number"]
    x2 = merged_df["district_de_infected_number"]
    print(merged_df)

    print("Korrelation: ", x2.corr(x1))


'''Hier wird verglichen, ob die Durchschnittliche Infektionszahlen deutscher Randgebiete 
höher leigen als der Bundesweite Durschscnitt'''

# Average
def calcAvg(df):
    df['daily_avg'] = round(df.mean(axis=1), 2)
    return df

#Normalisation

def min_max_scaling(df):
    # copy the dataframe
    df_norm = df.copy()
    # apply min-max scaling
    for column in df_norm.columns:
        df_norm[column] = (df_norm[column] - df_norm[column].min()) / (df_norm[column].max() - df_norm[column].min())
    df_norm.drop(['date'], axis=1, inplace=True)
    return df_norm

# Join Date

def join_date(df_date, df_norm):
    df_copy = df_date.copy(deep=False)
    df_copy.drop(df_copy.columns.difference(['date']), 1,
                  inplace=True)
    joined_df = df_copy.join(df_norm)
    return joined_df


# Functions

#filtered_german_df.drop(['sum_cases'], axis=1, inplace=True)
'''print(filtered_german_df)
calcAvg(filtered_german_df)
print(filtered_german_df)
'''
copy_german = filtered_german_df.copy(deep=False)
copy_cz = filtered_czech_df.copy(deep=False)
test = compareCountries(copy_german, Tirschenreuth, copy_cz, Eger, "Vergleiche Tirschenreuth mit Cheb")


