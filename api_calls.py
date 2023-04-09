from amadeus import Client, ResponseError
import tokens as to

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
        response = amadeus.shopping.flight_dates.get(origin = ori, destination = dest, departureDate = '2023-04-09')
        print(response.data)
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

# get_flight_offers('MAD', 'ATH', '2022-11-01', 1)

# price_metrics_itinerary('CDG', 'BCN', '2023-11-13')

# cheapest_date('MAD', 'BCN')

# print(airport_routes('MAD'))
