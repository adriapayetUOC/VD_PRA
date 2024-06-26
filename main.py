import math

import pandas as pd


# Data source astronauts: https://www.kaggle.com/datasets/jessemostipak/astronaut-database/data
# Read csv
df = pd.read_csv("./data/astronauts.csv")
# Delete non-udeful columns
df.drop(columns=['id', 'nationwide_number', 'original_name', 'selection', 'occupation',
                 'ascend_shuttle', 'descend_shuttle', 'field21'], inplace=True)

# Radial chart dataframe

# Create decade column
df['decade_of_mission'] = df['year_of_mission'].apply(lambda x: int(x / 10) * 10)

# Export data
df_radial = df[['name', 'mission_title', 'hours_mission', 'decade_of_mission', 'year_of_mission', 'sex',
                'year_of_birth', 'nationality', 'total_number_of_missions', 'total_hrs_sum']]
df_radial.to_csv('./data/df_radial.csv')


# Map chart

# Coordenates: https://github.com/albertyw/avenews/blob/master/old/data/average-latitude-longitude-countries.csv

# Read coordenates csv
country_coordenates = pd.read_csv("./data/average-latitude-longitude-countries.csv")

# Rename astronauts typo countires
#  Hungry -> Hungary
#  Malysia -> Malaysia
df['nationality'] = df['nationality'].replace({
    'Hungry': 'Hungary',
    'Malysia': 'Malaysia'
})
astronaut_nationalities = df['nationality'].unique()

# Rename coordenates
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

# Get coordenates of necessary countries and mix dataframes
df_coordenates = country_coordenates[country_coordenates["Country"].isin(astronaut_nationalities)]
df_coordenates = df_coordenates.rename(columns={"Country": "nationality"})
df_map = pd.merge(df, df_coordenates, how="left", on="nationality")

# Create output dataframe. Only one row for each astronaut
df_map = df_map[['name', 'year_of_selection', 'nationality', 'Latitude', 'Longitude']]
df_map = df_map.drop_duplicates()

# Circle size. Increment at each astronaut from same country
df_map = df_map.sort_values(by=['year_of_selection', 'nationality'])
df_map["total_astronauts"] = 1
dict_total_astronauts = {country: 0 for country in astronaut_nationalities}
for index, row in df_map.iterrows():
    dict_total_astronauts[row['nationality']] += 1
    df_map.loc[index, 'total_astronauts'] = dict_total_astronauts[row['nationality']]

# Add an end date for animation purposes
df_map['end_date'] = (df['year_of_mission']).max()


# Export data
df_map.to_csv('./data/df_map.csv')

# Area chart

# Select necessary columns
df_tmp = df[['name', 'sex', 'year_of_selection']]  # Keep name to keep all astronauts
df_tmp = df_tmp.drop_duplicates()
# Sort by date of selection
df_tmp = df_tmp.sort_values(by=['sex', 'year_of_selection'])

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

# Create a column for each sex
years_range = range(min_year, max_year + 1)
df_area_chart = pd.DataFrame(years_range, columns=['Year'])
df_area_chart['male'] = 0
df_area_chart['female'] = 0
previous_male_count = 0
previous_female_count = 0
for year in years_range:
    # Get max value of total astronauts per year (nan if not found)
    year_df = df_tmp[df_tmp['year_of_selection'] == year]
    male_year_df = year_df[year_df['sex'] == 'male']
    female_year_df = year_df[year_df['sex'] == 'female']
    max_value_male = male_year_df['total_astronauts'].max()
    max_value_female = female_year_df['total_astronauts'].max()
    # Max value for current year is foun vale or previous value if nan. update previous value
    max_value_male = previous_male_count if math.isnan(max_value_male) else max_value_male
    max_value_female = previous_female_count if math.isnan(max_value_female) else max_value_female
    previous_male_count = max_value_male
    previous_female_count = max_value_female
    # Assign new values
    df_area_chart.loc[df_area_chart['Year'] == year, 'male'] = max_value_male
    df_area_chart.loc[df_area_chart['Year'] == year, 'female'] = max_value_female

# Export data
df_area_chart.to_csv('./data/df_area_chart.csv')


























