from amadeus import Client, ResponseError
import tokens as to
import pandas as pd

amadeus = Client(
    client_id = to.client_id,
    client_secret = to.client_secret
)

def get_flight_offers(origin, destination, departure_date, ad):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode = origin,
            destinationLocationCode = destination,
            departureDate = departure_date,
            adults = ad)
        print(response.data)
    except ResponseError as error:
        print(error)



def price_metrics_itinerary(origin, destination, departure):
    try:
        '''
        Returns price metrics of a given itinerary
        '''
        response = amadeus.analytics.itinerary_price_metrics.get(originIataCode = origin,
                                                                destinationIataCode = destination,
                                                                departureDate = departure)
        print(response.data)
    except ResponseError as error:
        raise 


def cheapest_date(ori, dest):
    try:
        '''
        Find cheapest dates from Madrid to Munich
        '''
        response = amadeus.shopping.flight_dates.get(origin = ori, destination = dest, departureDate = '2023-11-11')
        print("cheapest date : ", pd.DataFrame(response.data))
    except ResponseError as error:
        raise error


def airport_routes(origin):
    try:
        '''
        What are the destinations served by BLR airport?
        '''
        response = amadeus.airport.direct_destinations.get(departureAirportCode=origin)
        airports_list = response.data
        airports_list = [airport['iataCode'] for airport in airports_list]
        return airports_list
    except ResponseError as error:
        raise error

def get_cheapest_price(origin, dest):
    try:
        '''
        Find the cheapest flights from SYD to BKK
        '''
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode = origin, destinationLocationCode = dest, departureDate='2023-11-11', adults=1)
        df = pd.DataFrame(response.data)
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
        df = df.drop(['lastTicketingDateTime'], axis=1)
        df = df.drop(['pricingOptions'], axis=1)
        df = df.drop(['fees'], axis=1)
        df = df.drop(['price'], axis=1)
        # convert itineraries list-like elements to columns
        df = pd.concat([df.drop(['itineraries'], axis=1), df['itineraries'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop([0], axis=1), df[0].apply(pd.Series)], axis=1)
        ############ to check what columns must be dropped ############
        # convert df to csv
        df.to_csv('cheapest_price_trainer_set.csv')
        print(df)
        print(df.columns.tolist()) 
    except ResponseError as error:
        raise error

# get_flight_offers('MAD', 'ATH', '2022-11-01', 1)

# price_metrics_itinerary('CDG', 'BCN', '2023-11-13')

# cheapest_date('SYD', 'BKK')
get_cheapest_price('CDG', 'MAD')

# print(airport_routes('MAD'))
