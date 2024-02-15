# ------ The following method will print the very first watched movie/series for each profile
def print_the_first_movie_or_series_per_profile(dataframe_for_profile, profile_name):
    # tail() method by default returns the 5 last rows of a dataframe
    first_movie_name = dataframe_for_profile['Title'].tail(1).to_string().split('    ')[1]
    date_of_first_watch = dataframe_for_profile['Datetime'].tail(1).to_string().split('    ')[1]
    print('     The very first movie/series for user', profile_name, ':')
    print('         Title: ', first_movie_name)
    print('         Date: ', date_of_first_watch)


# ------ The following method will print all the data for a certain profile and year
#       It prints the title, the category and the date of the watched movie/series
def print_profiles_data_per_year_y(dataframe_for_profile_and_year):
    # Iterate through rows
    for row_idx in range(len(dataframe_for_profile_and_year)):
        title = dataframe_for_profile_and_year.iloc[row_idx, 0]   # 0 ==> 'Title'
        category = dataframe_for_profile_and_year.iloc[row_idx, 1]    # 1 ==> 'Category'
        date = dataframe_for_profile_and_year.iloc[row_idx, 2]    # 2 ==> 'Datetime'
        print('    Details for movie/category #', row_idx + 1)
        print('             Title: ', title)
        print('          Category: ', category)
        print('              Date: ', date)
