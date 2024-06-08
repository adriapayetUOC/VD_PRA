import numpy as np
import pandas as pd


# Read csv
df = pd.read_csv("./data/astronauts.csv")

# Delete non-udeful columns
df.drop(columns=['id', 'nationwide_number', 'original_name', 'selection', 'occupation',
                 'ascend_shuttle', 'descend_shuttle', 'field21'], inplace=True)


# Radial chart dataframe

# Create decade column
df['decade_of_mission'] = df['year_of_mission'].apply(lambda x: int(x / 10) * 10)

df_radial = df[['name', 'mission_title', 'hours_mission', 'decade_of_mission', 'year_of_mission', 'sex',
                'year_of_birth', 'nationality', 'total_number_of_missions', 'total_hrs_sum']]
df_radial.to_csv('./data/df_radial.csv')


# Map chart
# Coordenates: https://github.com/albertyw/avenews/blob/master/old/data/average-latitude-longitude-countries.csv

# Rename astronauts typo countires
#  Hungry -> Hungary
#  Malysia -> Malaysia
df['nationality'] = df['nationality'].replace({
    'Hungry': 'Hungary',
    'Malysia': 'Malaysia'
})

astronaut_nationalities = df['nationality'].unique()
# print(astronaut_nationalities.size)
# print(np.sort(astronaut_nationalities))

# Read coordenates csv
country_coordenates = pd.read_csv("./data/average-latitude-longitude-countries.csv")

# Rername coordenates
#  Czech Republic -> Czechoslovakia
#  Korea, Republic of -> Korea
#  Netherlands -> Netherland
#  South Africa -> Republic of South Africa
#  Syrian Arab Republic -> Syria
#  United Kingdom -> U.K.
#  Ireland -> U.K./U.S.
#  United States -> U.S.
#  Russian Federation -> U.S.S.R/Russia
#  Ukraine -> U.S.S.R/Ukraine
#  United Arab Emirates -> UAE
country_coordenates['Country'] = country_coordenates['Country'].replace({
    'Czech Republic': 'Czechoslovakia',
    'Korea, Republic of': 'Korea',
    'Netherlands': 'Netherland',
    'South Africa': 'Republic of South Africa',
    'Syrian Arab Republic': 'Syria',
    'United Kingdom': 'U.K.',
    'Ireland': 'U.K./U.S.',
    'United States': 'U.S.',
    'Russian Federation': 'U.S.S.R/Russia',
    'Ukraine': 'U.S.S.R/Ukraine',
    'United Arab Emirates': 'UAE'
})

# Get coordenates of necessary countries
df_coordenates = country_coordenates[country_coordenates["Country"].isin(astronaut_nationalities)]
df_coordenates = df_coordenates.rename(columns={"Country": "nationality"})

# print(df_coordenates["Country"].unique().size)
# print(np.sort(df_coordenates["Country"].unique()))

df_map = pd.merge(df, df_coordenates, how="left", on="nationality")
# Add random variation to each point to set small diferent coordenates. Better for UX
df_map['Latitude'] = df_map['Latitude'] + np.random.uniform(low=-5, high=5, size=len(df_map))
df_map['Longitude'] = df_map['Longitude'] + np.random.uniform(low=-5, high=5, size=len(df_map))
# df_map['fake_mission_end'] = df_map['year_of_mission'] + 1  # Add

# Create output dataframe
df_map = df_map[['mission_title', 'hours_mission', 'year_of_mission', 'nationality', 'Latitude', 'Longitude']]

# Add small variations to
df_map.to_csv('./data/df_map.csv')


# Area chart

# Select necessary columns
df_tmp = df[['name', 'sex', 'year_of_selection']]  # Keep name to
df_tmp = df_tmp.drop_duplicates()
# print(df_tmp.head())
# Soret by date of selection
df_tmp = df_tmp.sort_values(by=['sex', 'year_of_selection'])
# print(df_tmp[['sex', 'year_of_selection']].tail())
# Obtain total count of astronauts as the position of each row (satring from 1). Differs between male and female
df_tmp['total_astronauts'] = 1
total_females = (df_tmp['sex'] == 'female').sum()
df_tmp = df_tmp.reset_index()
for row in range(1, total_females):
    df_tmp.loc[row, 'total_astronauts'] = df_tmp.loc[row - 1, 'total_astronauts'] + 1
for row in range(total_females + 1, len(df_tmp)):
    df_tmp.loc[row, 'total_astronauts'] = df_tmp.loc[row - 1, 'total_astronauts'] + 1

# Sort only by date, need to create a column for each sex
df_tmp = df_tmp.sort_values(by=['year_of_selection'])
max_year = (df_tmp['year_of_selection']).max()
min_year = (df_tmp['year_of_selection']).min()
print(f'{min_year} {max_year}')

# Create a column for each sex
years_range = range(min_year, max_year + 1)
df_area_chart = pd.DataFrame(years_range, columns=['Year'])
df_area_chart['male'] = 0
df_area_chart['female'] = 0
previous_male_count = 0
previous_female_count = 0
for year in years_range:
    # TODO: per cada any, afegir maxim de total_astronauts de cada sexe a la seva columna o be valor anterior. Actualitzar valor anterior tmb

df_area_chart.to_csv('./data/df_area_chart.csv')