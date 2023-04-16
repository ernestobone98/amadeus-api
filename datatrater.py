import datetime
import random
import time
import pandas as pd
from api_calls import get_cheapest_price

def get_airport_iata_code():
    '''
    Returns a list of airport iata codes
    '''

    df = pd.read_csv('airports.csv')
    df = df.dropna(subset=['iata_code'])
    return df['iata_code'].tolist()


def get_random_airport():
    '''
    Returns a random airport iata code
    '''
    airports_list = get_airport_iata_code()
    return random.choice(airports_list)

def get_random_date():
    '''
    Returns a random date between 2023-06-11 and 2023-12-30
    '''
    start_date = datetime.date(2023, 6, 11)
    end_date = datetime.date(2023, 12, 30)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")
    

def generate_random_request():
    '''
    Generates a random request
    '''
    origin = get_random_airport()
    destination = get_random_airport()
    departure_date = get_random_date()

    try:
        df = get_cheapest_price(origin, destination, departure_date)
        print("origin : ", origin)
        print("destination : ", destination)
        print("departure_date : ", departure_date)
        print("/n")
    except:
        return None
    else:
        return df
    
def generate_data_set():
    '''
    Generates a dataset of 500 random requests
    '''
    df = pd.DataFrame()
    for i in range(3):
        new = generate_random_request()
        if new is not None:
            df = pd.concat([df, new], ignore_index=True)
            # make pause of 100ms to avoid hitting the rate limit
            time.sleep(0.1)
        else:
            continue
    return df

print(len(generate_data_set()))

# Not working because not all airports support the API call