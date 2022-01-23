import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city?, please choose from (chicago, new york city, washington)')
    city = city.lower()
    while city not in CITY_DATA:
        print('No way, this {} city is not found, check spelling!'.format(city))
        city = input('Which city?, please choose from (chicago, new york city, washington)')
        city = city.lower()
    print('okay, we will start exploring {}'.format(city))

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('which month?, please choose from (january, february, march, april, may, june) or all!')
    month = month.lower()
    while month not in months:
        print('Ugh, this {} isn´t right, check the options again!'.format(month))
        month = input('which months?, please choose from (january, february, march, april, may, june) or all!')
        month = month.lower()
    print('well, let´s see what {} got for us!'.format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('which day?, please choose from (monday, tuesday, wednesday, thursday, friday, saturday, sunday)')
    day = day.lower()
    while day not in day_of_week:
        print('Mmm, this {} not even a day of the earth´s weekdays, so check it!'.format(day))
        day = input('which day?, please choose from (monday, tuesday, wednesday, thursday, friday, saturday, sunday)')
        day = day.lower()
    print('Good, it´s {}'.format(day))

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    # print('month df', df['month'])
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # when user choose a month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # when user choose a day
    if day != 'all':
        day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = day_of_week.index(day) + 1
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().idxmax()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('common month:', months[common_month - 1])

    # display the most common day of week
    common_day = df['day_of_week'].value_counts().idxmax()
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print('common day:', days[common_day - 1])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].value_counts().idxmax()
    print('common hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_st_station = df['Start Station'].mode()[0]
    print('Common starting station is:', common_st_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Common ending station is:', common_end_station)

    # display most frequent combination of start station and end station trip
    common_combined_sations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('common combined:', common_combined_sations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('mean of travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('user types counts: ', user_types_counts)

    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print('gender count:', gender_count)
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year_of_birth = df['Birth Year'].min()
        recent_year_of_birth = df['Birth Year'].max()
        common_year_of_birth = df['Birth Year'].mode()[0]
        print('the earliest year of birth :', earliest_year_of_birth)
        print('the recent year of birth :', recent_year_of_birth)
        print('the most common year of birth :', common_year_of_birth)
    else:
        print('Birth year stats cannot be calculated because it does not appear in the dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """Displays a review af five rows on bikeshare data that is filtered."""
    start_time = time.time()
    # display the rows of the data
    view_display = input('Do you want to see the first five rows? Yes or No')
    view_display.lower()
    start_loc = 0
    # to keep on viewing five rows by five rows to the use whenever wanted.
    while view_display == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_display = input(' Do you want to see the next 5 rows of data? Yes or No')
        view_display.lower()

    print("\nThis took %s seconds." % (time.time() - start_time))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
