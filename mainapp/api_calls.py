import sys
sys.path.append('/home/menez/EnseignementsCurrent/Projets/amadeus-api/')
print("Mon python path : ", sys.path)

from amadeus import Client, ResponseError
# import tokens as to    
import tokens as to
# from ..tokens import client_id, client_secret
import pandas as pd
import mainapp.encoder as encoder

class FlightSearch:
    def __init__(self):
        self.label_encoder = encoder.Encoder()
        self.amadeus = Client(
            client_id = to.client_id,
            client_secret = to.client_secret
        )

    def get_flight_offers(self, origin, destination, departure_date, ad):
        try:
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode = origin,
                destinationLocationCode = destination,
                departureDate = departure_date,
                adults = ad)
            print(response.data)
        except ResponseError as error:
            print(error)

    def price_metrics_itinerary(self, origin, destination, departure):
        try:
            '''
            Returns price metrics of a given itinerary
            '''
            response = self.amadeus.analytics.itinerary_price_metrics.get(originIataCode = origin,
                                                                    destinationIataCode = destination,
                                                                    departureDate = departure)
            print(response.data)
        except ResponseError as error:
            raise 

    def cheapest_date(self, ori, dest):
        try:
            '''
            Find cheapest dates from Madrid to Munich
            '''
            response = self.amadeus.shopping.flight_dates.get(origin = ori, destination = dest, departureDate = '2023-11-11')
            print("cheapest date : ", pd.DataFrame(response.data))
        except ResponseError as error:
            raise error

    def airport_routes(self, origin):
        try:
            '''
            What are the destinations served by BLR airport?
            '''
            response = self.amadeus.airport.direct_destinations.get(departureAirportCode=origin)
            airports_list = response.data
            airports_list = [airport['iataCode'] for airport in airports_list]
            return airports_list
        except ResponseError as error:
            raise error

    def get_prices(self, origin, dest, dep_date, encode = True):
        try:
            '''
            Find the cheapest flights from SYD to BKK
            '''
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode = origin, destinationLocationCode = dest, departureDate = dep_date, adults=1)
            df = pd.DataFrame(response.data)

        except ResponseError as error:
            raise error
        
        else:
            # from df convert all list-like elements to columns
            df = pd.concat([df.drop(['price'], axis=1), df['price'].apply(pd.Series)], axis=1)
            # drop type, id and source
            df = df.drop(['type', 'id', 'source'], axis=1)
            # drop currency (assuming all prices are in the same currency)
            df = df.drop(['currency'], axis=1)
            # convert travelerPricings list-like elements to columns (travelerId, fareOption, travelerType, price)
            df = pd.concat([df.drop(['travelerPricings'], axis=1), df['travelerPricings'].apply(pd.Series)], axis=1)
            df = pd.concat([df.drop([0], axis=1), df[0].apply(pd.Series)], axis=1)
            # delete repeated or useless columns
            df = df.drop(['lastTicketingDateTime', 'pricingOptions', 'fees', 'price'], axis=1)
            # convert itineraries list-like elements to columns
            df = pd.concat([df.drop(['itineraries'], axis=1), df['itineraries'].apply(pd.Series)], axis=1)
            df = pd.concat([df.drop([0], axis=1), df[0].apply(pd.Series)], axis=1)
            ############ to check what columns must be dropped ############
            df = df.drop(['additionalServices'], axis=1)

            df = pd.concat([df.drop(['fareDetailsBySegment'], axis=1), df['fareDetailsBySegment'].apply(pd.Series)], axis=1)
            df = pd.concat([df.drop([0], axis=1), df[0].apply(pd.Series)], axis=1)
            df = df.drop([1], axis=1)

            df = pd.concat([df.drop(['segments'], axis=1), df['segments'].apply(pd.Series)], axis=1)
            df = pd.concat([df.drop([0], axis=1), df[0].apply(pd.Series)], axis=1)
            df = df.drop([1], axis=1)
            
            df = pd.concat([df.drop(['departure'], axis=1), df['departure'].apply(pd.Series)], axis=1)
            
            df = df.drop(['operating', 'blacklistedInEU', 'id', 'duration'], axis=1)
            # change the column named 'at' to 'departureAt'
            df = df.rename(columns={'at': 'departureAt'})

            print(df['aircraft'])
            df = pd.concat([df.drop(['aircraft'], axis=1), df['aircraft'].apply(pd.Series)], axis=1)
            df = pd.concat([df.drop(['includedCheckedBags'], axis=1), df['includedCheckedBags'].apply(pd.Series)], axis=1)

            df = df.drop(['weight', 'weightUnit'], axis=1)
            
            df = pd.concat([df.drop(['arrival'], axis=1), df['arrival'].apply(pd.Series)], axis=1)
            df = df.drop(['terminal', 'grandTotal', 'travelerId', 'segmentId', 'validatingAirlineCodes'], axis=1)
            df = df.rename(columns={'at': 'arrivalAt'})
            

            # divinding lastTicketingDate into ltd_year, ltd_month and ltd_day
            df['ltd_year'] = df['lastTicketingDate'].apply(lambda x: x[:4])
            df['ltd_month'] = df['lastTicketingDate'].apply(lambda x: x[5:7])
            df['ltd_day'] = df['lastTicketingDate'].apply(lambda x: x[8:10])
            df = df.drop(['lastTicketingDate'], axis=1)
            # add the new columns to the dataframe
            df = pd.concat([df, df['ltd_year'].apply(pd.Series)], axis=1)
            df = pd.concat([df, df['ltd_month'].apply(pd.Series)], axis=1)
            df = pd.concat([df, df['ltd_day'].apply(pd.Series)], axis=1)

            #print column names
            

            # do the same for departureAt and arrivalAt knowing that they are in the format '2023-11-11T07:00:00'
            df['departure_year'] = df['departureAt'].apply(lambda x: x[:4])
            df['departure_month'] = df['departureAt'].apply(lambda x: x[5:7])
            df['departure_day'] = df['departureAt'].apply(lambda x: x[8:10])
            df['departure_hour'] = df['departureAt'].apply(lambda x: x[11:13])
            df['departure_minute'] = df['departureAt'].apply(lambda x: x[14:16])
            df = df.drop(['departureAt'], axis=1)
            # add the new columns to the dataframe
            df = pd.concat([df, df['departure_year'].apply(pd.Series)], axis=1)
            df = pd.concat([df, df['departure_month'].apply(pd.Series)], axis=1)
            df = pd.concat([df, df['departure_day'].apply(pd.Series)], axis=1)
            df = pd.concat([df, df['departure_hour'].apply(pd.Series)], axis=1)
            df = pd.concat([df, df['departure_minute'].apply(pd.Series)], axis=1)

            df['arrival_year'] = df['arrivalAt'].apply(lambda x: x[:4])
            df['arrival_month'] = df['arrivalAt'].apply(lambda x: x[5:7])
            df['arrival_day'] = df['arrivalAt'].apply(lambda x: x[8:10])
            df['arrival_hour'] = df['arrivalAt'].apply(lambda x: x[11:13])
            df['arrival_minute'] = df['arrivalAt'].apply(lambda x: x[14:16])
            df = df.drop(['arrivalAt'], axis=1)
            # add the new columns to the dataframe
            df = pd.concat([df, df['arrival_year'].apply(pd.Series)], axis=1)
            df = pd.concat([df, df['arrival_month'].apply(pd.Series)], axis=1)
            df = pd.concat([df, df['arrival_day'].apply(pd.Series)], axis=1)
            df = pd.concat([df, df['arrival_hour'].apply(pd.Series)], axis=1)
            df = pd.concat([df, df['arrival_minute'].apply(pd.Series)], axis=1)
            
            # drop all columns named '0'
            df = df.drop([0], axis=1)

            df.columns = ['instantTicketingRequired', 'nonHomogeneous', 'oneWay', 'numberOfBookableSeats', 
                        'total', 'base', 'fareOption', 'travelerType', 'cabin', 'fareBasis', 'brandedFare',
                            'class', 'carrierCode', 'number', 'numberOfStops', 'departureIataCode',
                        'aircraftCode', 'bagageQuantity', 'arrivalIataCode', 'ltd_year', 'ltd_month', 
                        'ltd_day', 'departure_year', 'departure_month', 'departure_day', 'departure_hour',
                        'departure_minute', 'arrival_year', 'arrival_month', 'arrival_day', 'arrival_hour', 'arrival_minute']

            df = df.dropna()

            # Encoding labels in all non-numeric columns
            if encode == True:
                for col in df.columns:
                    if df[col].dtype == 'object' or df[col].dtype == bool:
                        df[col] = self.label_encoder.fit_transform(df[col])

            return df

    def get_cheapest_price(self, origin, dest, depart):
        '''
        This function returns the cheapest price for a given origin, destination and departure date.
        '''
        # get the flight offers
        df = self.get_prices(origin, dest, depart, encode=False)
        # get the cheapest price
        cheapest_price = df['total'].min()
        return cheapest_price

def main():
    # create an instance of the class
    flight_search = FlightSearch()
    # get the cheapest price for a flight
    cheapest_price = flight_search.get_cheapest_price('CDG', 'BCN', '2023-11-13')
    # print the result
    print(f'The cheapest price for a flight from CDG to BCN on 2023-11-13 is {cheapest_price} euros.')


# create un main
if __name__ == '__main__':
    
    main()
# df =pd.concat([get_prices('CDG', 'MAD', '2023-11-11'), get_prices('MAD', 'CDG', '2023-11-21')], ignore_index=True)
# df =pd.concat([df, get_prices('MAD', 'BCN', '2023-12-21')], ignore_index=True)
# df =pd.concat([df, get_prices('CDG', 'BCN', '2023-10-02')], ignore_index=True)
# # convert df to csv
# df.to_csv('flight_offers.csv', index=False)

# get_flight_offers('MAD', 'ATH', '2022-11-01', 1)

# price_metrics_itinerary('CDG', 'BCN', '2023-11-13')

# cheapest_date('SYD', 'BKK')

# print(airport_routes('MAD'))
