import pandas as pd
import plotly.graph_objs as go
import numpy as np
from random import randrange
from matplotlib import pyplot as plt
from plotly.figure_factory._distplot import scipy
from scipy import stats
from varname import nameof

pd.options.mode.chained_assignment = None  # default='warn'

# read czech data from a csv file (all districts with daily infections)
czech_origin_data = pd.read_csv('kraj-okres-nakazeni-vyleceni-umrti.csv')
czech_origin_data.columns = ['date', 'state', 'district', 'infected_number', 'healed', 'deaths']
czech_origin_data['date'] = pd.to_datetime(czech_origin_data['date'], format='%Y-%m-%d')

# read german data from github repository (all districts with daily infections)
german_origin_data = pd.read_csv(
    'https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv')
german_origin_data['time_iso8601'] = pd.to_datetime(german_origin_data['time_iso8601'])
german_origin_data['date'] = german_origin_data['time_iso8601'].dt.date
german_origin_data['date'] = pd.to_datetime(german_origin_data['date'], format='%Y-%m-%d')
german_origin_data.drop(['sum_cases', 'time_iso8601'], axis=1, inplace=True)

# read help csv file to be able to assign the district name to the district key
german_district_keys = pd.read_csv('de_districts_keys.csv')

# read help csv file to be able to assign the district name to the NUT codes
czech_district_keys = pd.read_csv('cz_districts_keys.csv')

# selected time period Czech Republic (exactly 365 days)
filtered_czech_df = czech_origin_data.loc[(czech_origin_data['date'] >= '2020-03-02')
                                          & (czech_origin_data['date'] < '2021-03-02')]

# selected time period Germany (exactly 365 days)
filtered_german_df = german_origin_data.loc[(german_origin_data['date'] >= '2020-03-02')
                                            & (german_origin_data['date'] < '2021-03-02')]

# shifted time period Germany (exactly 365 days, but 2 Weeks later)
shifted_german_df = german_origin_data.loc[(german_origin_data['date'] >= '2020-03-16')
                                           & (german_origin_data['date'] < '2021-03-16')]

# Array of all CZ districts from the help csv file "czech_district_keys"
czech_array = []
czech_district_list = czech_district_keys.columns.tolist()
czech_array = np.array(czech_district_keys['CZ_LKR_Schlüssel'])

# Array of all DE districts from the help csv file "german_district_keys"
german_array = []
german_district_list = german_origin_data.columns.tolist()
german_district_list.pop(len(german_district_list) - 1)
german_array = np.array(german_district_list)

# Array of all CZ border districts
germanBorderDistricts_array = ["Freyung-Grafenau", "Regen", "Cham", "Schwandorf", "Neustadt a.d.Waldnaab",
                                  "Tirschenreuth", "Wunsiedel i.Fichtelgebirge", "Hof", "Vogtlandkreis",
                                  "Erzgebirgskreis", "Mittelsachsen", "Sächsische Schweiz-Osterzgebirge", "Bautzen",
                                  "Görlitz"]

# Array of all DE border districts
czechBorderDistricts_array = ["Prachatiz (Prachatice)", "Klattau (Klatovy)", "Taus (Domažlice)", "Tachau (Tachov)",
                              "Eger (Cheb)", "Falkenau (Sokolov)", "Karlsbad (Karlovy Vary)", "Komotau (Chomutov)",
                              "Brux (Most)", "Teplitz-Schönau (Teplice)", "Aussig (Ústí nad Labem)", "Tetschen (Děčín)",
                              "Böhmisch Leipa (Česká Lípa)"]

#  Method comparing all Czech districts with random German districts,
#  and outputting the Shapiro test, Pearson test, and Whitney U test for each comparison.
def compareAllDistricts():
    for i in czech_array:
        temp = getGermanDistrict()
        new_df = german_district_keys.query("keys == @temp")
        name = new_df.iloc[0]['name']
        new_df2 = czech_district_keys.query("CZ_LKR_Schlüssel == @temp2")
        name2 = new_df2.iloc[0]['CZ_LKR_Name']

        compareCountriesDistricts(filtered_german_df, temp, filtered_czech_df, i, (name, " im Vergleich zu ", name2), name,
                         name2)

# Method that compares all German border districts with random German districts,
# and outputting the Shapiro test, Pearson test, and Whitney U test for each comparison.
def compareRandomGermanDistricts(array):
    for i in germanBorderDistricts_array:
        temp = getGermanDistrict()
        new_df = german_district_keys.query("keys == @temp")
        name = new_df.iloc[0]['name']

        compareGermanDistricts(filtered_german_df, temp, filtered_german_df, searchLKS(i), (name, " im Vergleich zu ", i), name,
                         i)

# help method fo compareRandomGermanDistricts() that creates a merged dataframe with two districts
def compareGermanDistricts(germandf, german_what, germandf2, german_what2, title, name_de, name_de2):

    copy_german = germandf.copy(deep=False)
    copy_german2 = germandf2.copy(deep=False)

    copy_german['infected_number_de'] = copy_german[german_what]
    copy_german.drop(copy_german.columns.difference(['date', 'infected_number_de']), 1,
                     inplace=True)
    copy_german2['infected_number'] = copy_german2[german_what2]
    copy_german2.drop(copy_german2.columns.difference(['date', 'infected_number']), 1,
                     inplace=True)

    shifted_merge_df = copy_german.merge(copy_german2)
    print()
    print("----------------------------------------------------------------------")
    print()
    print("##### ", name_de, " vergleich zu ", name_de2, " (Normal) #####")

    test(shifted_merge_df)

#   plot(copy_german['date'], copy_german['infected_number_de'].diff(), name_de, copy_cz['date'],
#        copy_cz['infected_number'].diff(), name_cz, title)

# method that returns a random german district
def getGermanDistrict():
    x = randrange(0, int(len(german_array) - 2), 1)
    return german_array[x]

# method for plotting a line graph with two districts an their infection numbers and dates
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

# method that is given a district name and returns the district NUT-Code
def searchNutCode(name):
    czData = czech_district_keys.copy(deep=False)

    czData.drop(czData.index[(czData["CZ_LKR_Name"] != name)], axis=0,
                inplace=True)

    key = czData.iloc[0]['CZ_LKR_Schlüssel']
    return key

# method that is given a district name and returns the district key
def searchLKS(name):
    germanData = german_district_keys.copy(deep=False)

    germanData.drop(germanData.index[(germanData["name"] != name)], axis=0,
                    inplace=True)

    key = germanData.iloc[0]['keys']
    return str(key)

# method that compares a german and czech district
def compareCountriesDistricts(germandf, german_what, czechdf, czech_what, title, name_de, name_cz):
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

    test(shifted_merge_df)

# !!! Comment out this method, otherwise a plot will be created every time !!!
#    plot(copy_german['date'], copy_german['infected_number_de'].diff(), name_de, copy_cz['date'],
#        copy_cz['infected_number'].diff(), name_cz, title)


# method that compares a german district which dates are 2 weeks shifted and a czech district
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

    test(shifted_merge_df)
    # !!! Comment out this method, otherwise a plot will be created every time !!!a
#    plot(shifted_merge_df['date'], shifted_merge_df['infected_number_de'].diff(), name_de, shifted_merge_df['date'],
#        shifted_merge_df['infected_number'].diff(), name_cz, title)


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

# method that creates a dataframe from a df with a date and a df with data
def join_date(df_date, df_norm):
    df_copy = df_date.copy(deep=False)
    df_copy.drop(df_copy.columns.difference(['date']), 1,
                 inplace=True)
    joined_df = df_copy.join(df_norm)
    return joined_df

# Difference
def inf_difference(df):
    df['inf_dif'] = df['infected_number'].diff()

# method that performs all the different important tests
def test(df):
    copy_df = df.copy(deep=False)
    print()
    print("Shapiro Test: ")
    shapiro_test = stats.shapiro(np.array(copy_df['infected_number_de']))
    print(shapiro_test)

    plt.hist(copy_df['infected_number_de'].diff())
    plt.title('Verteilung der Neuinfektionen pro Tag von Hof')
    plt.xlabel('Infektionen pro Tag')
    plt.ylabel('Häufigkeit')
    plt.show()

    print()
    print("Mann-Whitney-U Test (Infektionen/Tag): ")
    u = scipy.stats.mannwhitneyu(copy_df['infected_number_de'].diff(), copy_df['infected_number'].diff())
    print(u)

    print()
    print("Mann-Whitney-U Test (Absolut): ")
    v = scipy.stats.mannwhitneyu(copy_df['infected_number_de'], copy_df['infected_number'])
    print(v)

    print()
    print("Mann-Whitney-U Test (Relativ): ")
    v2 = scipy.stats.mannwhitneyu(copy_df['infected_number_de'] / 94522, copy_df['infected_number'] / 32071)
    print(v2)
    print(copy_df['infected_number_de'] / 94522, copy_df['infected_number'] / 32071)

    print()
    print("Spearman: ")
    sp = scipy.stats.spearmanr(copy_df['infected_number_de'], copy_df['infected_number'])
    print(sp)

    print()
    print("Pearson: ")
    pearson = scipy.stats.pearsonr(copy_df['infected_number_de'], copy_df['infected_number'])
    print(pearson)


'''Funktionen'''

# Hier deutsche Landkreise austauschen

cz_district = "Böhmisch Leipa (Česká Lípa)"

de_district = "Görlitz"

de_district2 = "Gießen" #Für innerdeutschen Vergleich

'''Funktisaufrufe'''

#Method that compares one specific german and czech district

#compareCountriesDistricts(filtered_german_df, searchLKS(de_district), filtered_czech_df, searchNutCode(cz_district),
#                 (de_district + " zu " + cz_district + " (Normal)"), de_district, cz_district)
#-----------------------------------------------------------------------------------------------------------------------
#Method that compares one shifted german district and czech district

# compareShiftedCountries(shifted_german_df, de_district, filtered_czech_df, cz_district, (de_name + " zu " + cz_name + " (Verschoben)"), de_name, cz_name)
#-----------------------------------------------------------------------------------------------------------------------
#Method that compares two specific german districts

#compareGermanDistricts(filtered_german_df, searchLKS(de_district), filtered_german_df, searchLKS(de_district2),
                       #(de_district + " zu " + de_district2 + " (Normal)"), de_district, de_district2)
#-----------------------------------------------------------------------------------------------------------------------
#Method that compares all german border Districts with random german inner districts

compareRandomGermanDistricts(germanBorderDistricts_array)
#-----------------------------------------------------------------------------------------------------------------------
# Method for Comparing all Czech Districts with random German districts

#compareAllDistricts()

