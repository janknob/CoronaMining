from random import randrange

import pandas as pd
import plotly.graph_objs as go
import numpy as np
from matplotlib import pyplot as plt
from plotly.figure_factory._distplot import scipy
from scipy import stats
from varname import nameof

pd.options.mode.chained_assignment = None  # default='warn'

# import Tscheschien
czech_origin_data = pd.read_csv('kraj-okres-nakazeni-vyleceni-umrti (1).csv')
czech_origin_data.columns = ['date', 'state', 'district', 'infected_number', 'healed', 'deaths']
czech_origin_data['date'] = pd.to_datetime(czech_origin_data['date'], format='%Y-%m-%d')

# import Germany
german_origin_data = pd.read_csv(
    'https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv')
german_origin_data['time_iso8601'] = pd.to_datetime(german_origin_data['time_iso8601'])
german_origin_data['date'] = german_origin_data['time_iso8601'].dt.date
german_origin_data['date'] = pd.to_datetime(german_origin_data['date'], format='%Y-%m-%d')
german_origin_data.drop(['sum_cases', 'time_iso8601'], axis=1, inplace=True)

# import Germany-District-Keys

german_district_keys = pd.read_csv('de_districts_keys.csv')
print(german_district_keys)

temp = '16074'
#german_district_keys.drop(german_district_keys.index[(german_district_keys["keys"] != temp)], axis=0,
                          #inplace=True)
new_df = german_district_keys.query("keys == '1001'")
print("Datensatz Neu: ", new_df['name'])

# filter timeframe Tschechien
filtered_czech_df = czech_origin_data.loc[(czech_origin_data['date'] >= '2020-03-02')
                                          & (czech_origin_data['date'] < '2021-03-02')]

# shifted timeframe Deutsch
shifted_german_df = german_origin_data.loc[(german_origin_data['date'] >= '2020-03-16')
                                           & (german_origin_data['date'] < '2021-03-16')]

# filter timeframe Germany
filtered_german_df = german_origin_data.loc[(german_origin_data['date'] >= '2020-03-02')
                                            & (german_origin_data['date'] < '2021-03-02')]

# DE  border districts
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

# CZ districts Karlsbad (Karlovarsky kraj)
Eger = "CZ0411";
Karlsbad = "CZ0412";
Falkenau = "CZ0413"

# CZ districts Aussig (Ustecky kraj)
Tetschen = "CZ0421";
Komotau = "CZ0422";
Leitmeritz = "CZ0423";
Laun = "CZ0424";
Brux = "CZ0425";
Teplitz_Schoenau = "CZ0426";
Aussig = "CZ0427"

# CZ districts Reichenberg (Liberecky kraj)
Boehmisch_Leipa = "CZ0511";
Gablonz = "CZ0512";
Reichenberg = "CZ0513";
Semil = "CZ0514"

# CZ districts Königgrätz (Kralovehradecky kraj)
Koeniggraetz = "CZ0521";
Jitschin = "CZ0522";
Nachod = "CZ0523";
Reichenau_an_der_Knieschna = "CZ0524";
Trautenau = "CZ0525"

# CZ districts Pilsen (Plzensky kraj)
Taus = "CZ0321";
Klattau = "CZ0322";
Pilsen_Stadt = "CZ0323";
Pilsen_Sued = "CZ0324";
Pilsen_Nord = "CZ0325";
Rokitzan = "CZ0326";
Tachau = "CZ0327"

# CZ districts Mittelböhmen (Stredocesky kraj)
Beneschau = "CZ0201";
Beroun = "CZ0202";
Kladen = "CZ0203";
Kollin = "CZ0204";
Kuttenberg = "CZ0205";
Melnik = "CZ0206";
Jungbunzlau = "CZ0207";
Nimburg = "CZ0208";
Prag_Ost = "CZ0209";
Prag_West = "CZ020A";
Freiberg_in_Boehmen = "CZ020B";
Rakonitz = "CZ020C"

# CZ districts Prag (Praha)
Prag = "CZ0100"

# CZ districts Pardubitz (Pardubicky kraj)
Chrudim = "CZ0531";
Pardubitz = "CZ0532";
Zwittau = "CZ0533";
Wildenschwert = "CZ0534"

# CZ districts Olmütz (Olomoucky kraj)
Freiwaldau = "CZ0711";
Olmuetz = "CZ0712";
Prossnitz = "CZ0713";
Prerau = "CZ0714";
Maehrisch_Schoenberg = "CZ0715"

# CZ districts Mähren-Schlesien (Moravskoslezky kraj)
Freudenthal = "CZ0801";
Friedeck_Mistek = "CZ0802";
Karwin = "CZ0803";
Neu_Titschein = "CZ0804";
Troppau = "CZ0805";
Ostrau_Stadt = "CZ0806"

# CZ districts Mähren-Schlesien (Moravskoslezky kraj)
Budweis = "CZ0311";
Krumau = "CZ0312";
Neuhaus = "CZ0313";
Pisek = "CZ0314";
Prachatiz = "CZ0315";
Strakonitz = "CZ0316";
Tabor = "CZ0317"

# CZ districts Hochland (Kraj Vysocina)
Deutschbrod = "CZ0631";
Iglau = "CZ0632";
Pilgrams = "CZ0633";
Trebic = "CZ0634";
Saar = "CZ0635"

# CZ districts Südmähren (Jihomoravsky kraj)
Blanz = "CZ0641";
Bruenn_Stadt = "CZ0642";
Bruenn_Land = "CZ0643";
Lundenburg = "CZ0644";
Goeding = "CZ0645";
Wischau = "CZ0646";
Znaim = "CZ0647"

# CZ districts MZlin (Zlinsky kraj)
Kremsier = "CZ0721";
Ungarisch_Hradisch = "CZ0722";
Wsetin = "CZ0723";
Zlin = "CZ0724"

# Array of CZ districts
districtsCZArray = np.array([Eger, Karlsbad, Falkenau,
                             Tetschen, Komotau, Leitmeritz, Laun, Brux, Teplitz_Schoenau, Aussig,
                             Boehmisch_Leipa, Gablonz, Reichenberg, Semil,
                             Koeniggraetz, Jitschin, Nachod, Reichenau_an_der_Knieschna, Trautenau,
                             Taus, Klattau, Pilsen_Stadt, Pilsen_Sued, Pilsen_Nord, Rokitzan, Tachau,
                             Beneschau, Beroun, Kladen, Kollin, Kuttenberg, Melnik, Jungbunzlau, Nimburg, Prag_Ost,
                             Prag_West, Freiberg_in_Boehmen, Rakonitz,
                             Prag,
                             Chrudim, Pardubitz, Zwittau, Wildenschwert,
                             Freiwaldau, Olmuetz, Prossnitz, Prerau, Maehrisch_Schoenberg,
                             Freudenthal, Friedeck_Mistek, Karwin, Neu_Titschein, Troppau, Ostrau_Stadt,
                             Budweis, Krumau, Neuhaus, Pisek, Prachatiz, Strakonitz, Tabor,
                             Deutschbrod, Iglau, Pilgrams, Trebic, Saar,
                             Blanz, Bruenn_Stadt, Bruenn_Land, Lundenburg, Goeding, Wischau, Znaim,
                             Kremsier, Ungarisch_Hradisch, Wsetin, Zlin])

# Array of DE districts
german_array = []
german_district_list = german_origin_data.columns.tolist()
# print("District List: ", german_district_list)
german_district_list.pop(len(german_district_list) - 1)
german_array = np.array(german_district_list)


# print(german_array)

def compareAllDistricts():
    for i in districtsCZArray:
        temp = getGermanDistrict()
        # print(german_district_keys)
        copy_german_district_keys = german_district_keys.copy(deep=False)
        copy_german_district_keys.drop(copy_german_district_keys.index[(copy_german_district_keys["keys"] != temp)],
                                       axis=0,
                                       inplace=True)
        # new_df = copy_german_district_keys[copy_german_district_keys[] == temp]
        print("Datensatz: ", copy_german_district_keys)
        # print(temp ," (DE) und ", i,"(CZ):")
        # compareCountries(filtered_german_df, temp, filtered_czech_df, i, (temp, " im Vergleich zu ", i), temp, i)


def getGermanDistrict():
    # print('Länge:', len(german_array))
    x = randrange(0, int(len(german_array) - 2), 1)
    return german_array[x]


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
    fig.update_layout(height=800, width=2000, title_text=title)
    fig.show()


def compareCountries(germandf, german_what, czechdf, czech_what, title, name_de, name_cz):
    # copy cause python wants this
    copy_german = germandf.copy(deep=False)

    copy_cz = czechdf.copy(deep=False)
    copy_cz.drop(copy_cz.index[(copy_cz["district"] != czech_what)], axis=0,
                 inplace=True)
    copy_cz.drop(copy_cz.columns.difference(['date', 'infected_number']), 1,
                 inplace=True)

    copy_german['infected_number_de'] = copy_german[german_what]
    copy_german.drop(copy_german.columns.difference(['date', 'infected_number_de']), 1,
                     inplace=True)

    shifted_merge_df = copy_german.merge(copy_cz)

    print()
    print("----------------------------------------------------------------------")
    print()
    print("##### ", name_de, " vergleich zu ", name_cz, " (Normal) #####")

    norm_test(shifted_merge_df)

    ## Normalization ##
    # inf_difference(czechdf)
    # inf_difference(germandf)
    ##f_norm_de = min_max_scaling(germandf)
    # df_norm_cz = min_max_scaling(czechdf)
    # germandf_final_norm = join_date(germandf, df_norm_de)
    # czechdf_final_norm = join_date(czechdf, df_norm_cz)
    # print(germandf_final_norm)

    # plot(copy_german['date'], copy_german['infected_number_de'].diff(), name_de, copy_cz['date'], copy_cz['infected_number'].diff(), name_cz, title)


# Shifted Compare Plot

def compareShiftedCountries(germandf, german_what, czechdf, czech_what, title, name_de, name_cz):
    # copy cause python wants this
    copy_german = germandf.copy(deep=False)
    copy_cz = czechdf.copy(deep=False)

    copy_cz.drop(copy_cz.index[(copy_cz["district"] != czech_what)], axis=0,
                 inplace=True)

    copy_cz.drop(copy_cz.columns.difference(['date', 'infected_number']), 1,
                 inplace=True)

    copy_german['infected_number_de'] = copy_german[german_what]
    copy_german.drop(copy_german.columns.difference(['date', 'infected_number_de']), 1,
                     inplace=True)

    copy_cz.reset_index(drop=True, inplace=True)
    copy_german.reset_index(drop=True, inplace=True)

    temp = copy_cz['infected_number']
    copy_cz['date_cz'] = copy_cz['date']

    temp2 = copy_cz['date_cz']
    shifted_merge_df = copy_german.join(temp)
    shifted_merge_df = shifted_merge_df.join(temp2)

    print()
    print("----------------------------------------------------------------------")
    print()
    print("##### ", name_de, " vergleich zu ", name_cz, " (Verschoben um 2 Wochen) #####")

    norm_test(shifted_merge_df)

    plot(shifted_merge_df['date'], shifted_merge_df['infected_number_de'].diff(), name_de, shifted_merge_df['date'],
         shifted_merge_df['infected_number'].diff(), name_cz, title)


# Correlation

def correlation(germandf, german_what, czechdf, czech_what):
    # copy cause python wants this
    copy_german = germandf.copy(deep=False)
    copy_cz = czechdf.copy(deep=False)

    copy_cz.drop(czechdf.index[(copy_cz["district"] != czech_what)], axis=0,
                 inplace=True)
    # copy_german.drop(copy_german.columns(copy_german.columns != german_what))
    copy_german['infected_number_de'] = copy_german[german_what]
    merged_df = copy_german.merge(copy_cz, how='inner', left_on=["date"], right_on=["date"])

    x1 = merged_df["infected_number"]
    x2 = merged_df["infected_number_de"]
    # print('Merged DF: \n', merged_df)

    print("Korrelation: ", x2.corr(x1))


'''Hier wird verglichen, ob die Durchschnittliche Infektionszahlen deutscher Randgebiete 
höher leigen als der Bundesweite Durschscnitt'''


# Average
def calcAvg(df):
    df['daily_avg'] = round(df.mean(axis=1), 2)
    return df


# Normalisation

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


def inf_difference(df):
    df['inf_dif'] = df['infected_number'].diff()


# Normalization Tests

def norm_test(df):
    copy_df = df.copy(deep=False)
    print()
    print("Shapiro Test: ")
    shapiro_test = stats.shapiro(np.array(copy_df['infected_number_de']))
    print(shapiro_test)

    plt.hist(copy_df['infected_number_de'])
    plt.show()

    print()
    print("Mann-Whitney-U Test (Infektionen/Tag): ")
    u = scipy.stats.mannwhitneyu(copy_df['infected_number_de'].diff(), copy_df['infected_number'].diff())
    print(u)

    print()
    print("Mann-Whitney-U Test (Summe): ")
    v = scipy.stats.mannwhitneyu(copy_df['infected_number_de'], copy_df['infected_number'])
    print(v)

    print()
    print("Spearman: ")
    sp = scipy.stats.spearmanr(copy_df['infected_number_de'], copy_df['infected_number'])
    print(sp)

    print()
    print("Pearson: ")
    pearson = scipy.stats.pearsonr(copy_df['infected_number_de'], copy_df['infected_number'])
    print(pearson)


# Functions


'''Funktionen00'''

# Hier Landkreise austauschen (rechte Seite)
cz_district = Eger
cz_name = nameof(Eger)

de_district = Hof
de_name = nameof(Hof)

# Funktionsaufrufe
# compareCountries(filtered_german_df, de_district, filtered_czech_df, cz_district, (de_name + " zu " + cz_name + " (Normal)"), de_name, cz_name)
# compareShiftedCountries(shifted_german_df, de_district, filtered_czech_df, cz_district, (de_name + " zu " + cz_name + " (Verschoben)"), de_name, cz_name)

# compareAllDistricts()
