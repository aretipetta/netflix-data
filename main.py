import sys
import pandas as pd
import re

from results.print_results import print_results


# ------ The following method returns the data from a dataframe of a specified profile for a certain year
#       ---- param 'dataframe': the dataframe of a specified profile (not the whole data)
#       ---- param: 'year': the year for which the data of the dataframe are going to be returned
def data_per_profile_name_and_year(dataframe, year):
    return dataframe.loc[dataframe['Datetime'].str.split('-', expand=True)[0] == year]


# ------ The following method returns the data for a specified profile name from the dataframe
def data_per_profile_name(profile_name, dataframe):
    return dataframe.loc[dataframe['Profile Name'] == profile_name].loc[:, dataframe.columns != 'Profile Name']


# ------ The following method modifies the dataframe so only the needed columns will appear
def modify_dataframe(dataframe):
    modified_df = pd.DataFrame(columns=['Profile Name', 'Title', 'Category', 'Datetime'])
    for index, row in dataframe.iterrows():
        # Group movies/series
        split_pattern = re.compile(r': Season \d+ :')   # identify the series
        title = re.split(split_pattern, row['Title'])
        category = 'Movie' if len(title) == 1 else 'TV Show'

        modified_df.loc[index] = [row["Profile Name"], title[0], category, row['Start Time'].split(' ')[0]]

    return modified_df


def read_file(filename):
    df = pd.read_csv(filename)

    # Get the distinct profile names
    distinct_profile_names = df['Profile Name'].unique()

    # Get the distinct years of the viewing shows
    years = df['Start Time'].str.split('-', expand=True)[0].unique()
    years.sort()
    per_year_df = pd.DataFrame(years)

    modified_data = modify_dataframe(df)

    for profile in distinct_profile_names:
        print('---------------------------------------------------------------------')
        print('-----> User ', profile)
        data = data_per_profile_name(profile, modified_data)
        temp_df = pd.DataFrame(columns=years)
        for y in years:
            dt = data_per_profile_name_and_year(data, y)
            # temp_df[y] = dt
            print('--- year: ', y)
            print(dt)
        # print(temp_df)

if __name__ == '__main__':
    # args = sys.argv[1:]
    # filename = args[0]
    filename = 'ViewingActivity.csv'
    read_file(filename)
