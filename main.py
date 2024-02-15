import sys
import pandas as pd
import re

from results.print_results import print_the_first_movie_or_series_per_profile
from results.print_results import print_profiles_data_per_year_y


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

        # todo: check again the \d+
        # split_pattern = re.compile(r': Season \d+ :')  # identify the series
        # title = re.split(split_pattern, row['Title'])
        # category = 'Movie' if len(title) == 1 else 'TV Show'

        # the search method returns an object with two items;
        # a tuple object for the start and end index of the successful match
        # and an actual matching value that can be retrieved using the group() method
        match = re.search(r': Season ', row['Title'])
        category = 'TV Show' if match else 'Movie'

        modified_df.loc[index] = [row["Profile Name"], row['Title'], category, row['Start Time'].split(' ')[0]]

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

    array_of_dataframes_per_profile = []
    print('----------------------------------------------------------------------------------------')
    print('\n########### The very first watched movie/series for each user profile ###########\n')
    for profile in distinct_profile_names:
        print('-----> User ', profile)
        data_for_profile = data_per_profile_name(profile, modified_data)

        # ---- keep the dataframe for each 'profile' in an array
        array_of_dataframes_per_profile.append(data_for_profile)

        # Print the first watched movie/series
        print_the_first_movie_or_series_per_profile(data_for_profile, profile)

    print('\n########### All the watched movie/series for each user profile  per year ###########\n')
    idx = 0
    for profile in distinct_profile_names:
        # Get the dataframe for this profile based on the indexing
        df = array_of_dataframes_per_profile[idx]
        for y in years:
            print('------------------------------------------------------')
            # Get the data for this year
            data_for_year_y = data_per_profile_name_and_year(df, y)
            print('-----> User profile: ', profile, ' for Year: ', y)
            # Print all the data for this 'profile' for the year 'y'
            print_profiles_data_per_year_y(data_for_year_y)
            # print(data_for_year_y)
        idx += 1  # move to the next profile, so it can get the corresponding dataframe from array
        print('------------------------------------------------------')


if __name__ == '__main__':
    # args = sys.argv[1:]
    # filename = args[0]
    filename = 'ViewingActivity.csv'
    read_file(filename)
