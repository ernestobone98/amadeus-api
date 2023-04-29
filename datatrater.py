import datetime
import random
import time
import pandas as pd
from api_calls import FlightSearch


class FlightGenerator:
    
    def __init__(self):
        self.airports = pd.read_csv('airports.csv').dropna(subset=['iata_code'])['iata_code'].tolist()
        self.api = FlightSearch()
    
    def get_random_airport(self):
        return random.choice(self.airports)
    
    def get_random_date(self):
        start_date = datetime.date(2023, 6, 11)
        end_date = datetime.date(2023, 12, 30)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        return random_date.strftime("%Y-%m-%d")
    
    def generate_random_request(self):
        origin = self.get_random_airport()
        destination = self.get_random_airport()
        departure_date = self.get_random_date()
        try:
            df = self.api.get_cheapest_price(origin, destination, departure_date)
            print("origin : ", origin)
            print("destination : ", destination)
            print("departure_date : ", departure_date)
            print("/n")
        except:
            return None
        else:
            return df
    
    def generate_data_set(self, n=500):
        df = pd.DataFrame()
        for i in range(n):
            new = self.generate_random_request()
            if new is not None:
                df = pd.concat([df, new], ignore_index=True)
                time.sleep(0.1)  # pause to avoid hitting the rate limit
            else:
                continue
        return df


if __name__ == "__main__":
    flight_gen = FlightGenerator()
    data = flight_gen.generate_data_set(n=3)
    print(len(data))
