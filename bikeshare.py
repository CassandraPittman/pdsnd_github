import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = ''
    while True:
        city = input('Select a city: Chicago, New York City, or Washington\n').lower() 
        if city in CITY_DATA.keys():
            break

    # get user input for month (all, january, february, ... , june)
    month = ''
    while True:
        month = input('Which month? All, January, February, March, April, May, or June?\n').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while True:
        day = input('Which day? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break

    print('-'*40)
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['weekday_number'] = df['Start Time'].dt.weekday
    df['start_hour'] = df['Start Time'].dt.hour

    if month != 'all':
        # filter by month to create the new dataframe
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most Common Month:', months[int(df['month'].median()-1)].title())

    # display the most common day of week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print('Most Common Day of the Week:', days[int(df['weekday_number'].median())])

    # display the most common start hour
    print('Most Common Start Hour:', int(df['start_hour'].median()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Common Start Station:', get_most_common(df, 'Start Station'))

    #  display most commonly used end station
    print('Most Common End Station:', get_most_common(df, 'End Station'))

    # display most frequent combination of start station and end station trip
    start_list = list(df['Start Station'])
    end_list = list(df['End Station'])
    trip_dict = {}
    for index in range(0,len(start_list)-1):
        trip_concat = start_list[index] + ' to ' + end_list[index]
        if trip_concat not in trip_dict.keys():
            trip_dict[trip_concat]=1
        else:
            trip_dict[trip_concat]+=1
    trip_keys = list(trip_dict)
    trip_values = list(trip_dict.values())
    largest_trip_value = max(trip_dict.values())
    largest_trip_index = trip_values.index(largest_trip_value)
    print('Most Common Trip:', trip_keys[largest_trip_index])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    start_list = list((df['Start Time']))
    end_list = list((df['End Time']))
    
    trip_time = []
    for index in range(0,len(start_list)-1):
        trip_time.append(np.subtract(pd.Timestamp(end_list[index]), pd.Timestamp(start_list[index])).total_seconds())

        
    # display total travel time
    trip_total = sum(trip_time)
    print('Total Travel Time:', (pd.to_timedelta(trip_total, 's')))

    # display mean travel timeyers
    trip_mean = np.mean(trip_time)
    print('Mean Travel Time:', (pd.to_timedelta(trip_mean, 's')))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_dict = {}
    for user in df['User Type']:
        if user not in user_dict.keys():
            user_dict[user]=1
        else:
            user_dict[user]+=1
    
    # Display counts of user types
    print('Number of Subscribers:', user_dict['Subscriber'])
    print('Number of Customers:', user_dict['Customer'])
    print('')
    # Display counts of gender
    gender_dict = {}
    if 'Gender' in df.keys():
        for gender in df['Gender']:
            if gender!=gender:
                gender = 'Unspecified'
            if gender not in gender_dict.keys():
                gender_dict[gender]=1
            else:
                gender_dict[gender]+=1
        for gender in gender_dict.keys():
            print('Number of', gender, 'Users:', gender_dict[gender])
    else:
        print('No Gender Info Available For This Selection')
    print('')

    # Display earliest, most recent, and most common year of birth
    birth_year_list = []
    if 'Birth Year' in df.keys():
        for year in df['Birth Year']:
            if year==year:
                birth_year_list.append(year)
        print('Earliest Year of Birth:', int(min(birth_year_list)))
        print('Most Recent Year of Birth:', int(max(birth_year_list)))
        print('Most Common Year of Birth:', int(np.median(birth_year_list)))
    else:
        print('Year of Birth Not Available for this Selection')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_most_common(df, column_name):
    station_dict = {}
    for station in df[column_name]:
        if station not in station_dict.keys():
            station_dict[station]=1
        else:
            station_dict[station]+=1
    station_keys = list(station_dict)
    station_values = list(station_dict.values())
    largest_value = max(station_dict.values())
    largest_index = station_values.index(largest_value)
    return station_keys[largest_index]

def raw_data(df):
    while True:
        data_prompt=input('Display 5 Lines of Raw Data? (Yes or No)\n').lower()
        if data_prompt=='yes':
            start_loc=0
            print(df.iloc[start_loc:(start_loc+5)])
            while True:
                more_data_prompt=input('Display Next 5 Lines of Raw Data? (Yes or No)\n').lower()
                if more_data_prompt=='yes':
                    start_loc+=5
                    print(df.iloc[start_loc:(start_loc+5)])
                else:
                    break
            break
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

