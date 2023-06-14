from amadeus import Client, ResponseError
from . import tokens as to
# import tokens as to
import pandas as pd
from .encoder import Encoder
# from encoder import Encoder
import http.client
import json

class FlightSearch:
    def __init__(self):
        self.label_encoder = Encoder()
        self.amadeus = Client(
            client_id = to.client_id,
            client_secret = to.client_secret
        )

    def get_flight_offers(self, origin, destination, departure_date, ad):
        '''
        Returns flight offers from Madrid to Paris on 2021-12-01
        '''
        try:
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode = origin,
                destinationLocationCode = destination,
                departureDate = departure_date,
                adults = ad)
            result = {}; origin = []; destination = []; departure_date = []; departure_time = []; arrival_date = []; arrival_time = []
            aircraftCode = []; carrierCode = []; number = []; duration = []

            for i in range(len(response.data)):
                origin.append(response.data[i]['itineraries'][0]['segments'][0]['departure']['iataCode'])
                destination.append(response.data[i]['itineraries'][0]['segments'][0]['arrival']['iataCode'])
                departure_date.append(response.data[i]['itineraries'][0]['segments'][0]['departure']['at'][0:10])
                departure_time.append(response.data[i]['itineraries'][0]['segments'][0]['departure']['at'][11:16])
                arrival_date.append(response.data[i]['itineraries'][0]['segments'][0]['arrival']['at'][0:10])
                arrival_time.append(response.data[i]['itineraries'][0]['segments'][0]['arrival']['at'][11:16])
                aircraftCode.append(response.data[i]['itineraries'][0]['segments'][0]['aircraft']['code'])
                carrierCode.append(response.data[i]['itineraries'][0]['segments'][0]['carrierCode'])
                number.append(response.data[i]['itineraries'][0]['segments'][0]['number'])
                duration.append(response.data[i]['itineraries'][0]['duration'][2:])

            for i in range(len(response.data)):
                result[i] = {'origin': origin[i], 'destination': destination[i], 'departure_date': departure_date[i], 
                             'departure_time': departure_time[i], 'arrival_date': arrival_date[i], 'arrival_time': arrival_time[i], 
                             'aircraftCode': aircraftCode[i], 'carrierCode': carrierCode[i], 'number': number[i], 'duration': duration[i]}
            print(result)
        except ResponseError as error:
            print(error)

    # NOTE: request not working
    def cheapest_date(self, ori, dest):
        try:
            '''
            Find cheapest dates from Madrid to Munich
            '''
            response = self.amadeus.shopping.flight_dates.get(origin=ori, destination=dest)
            print(response.data)
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

    def get_prices(self, origin, dest, dep_date, encode = False):
        try:
            '''
            Find the cheapest flights from SYD to BKK
            '''
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode = origin, destinationLocationCode = dest, departureDate = dep_date, adults=1)
            df = pd.DataFrame(response.data)

        except ResponseError as error:
            raise error
        
        
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

        
        return df.to_json()

    def get_cheapest_price(self, origin, dest, depart):
        '''
        This function returns the cheapest price for a given origin, destination and departure date.
        '''
        # get the flight offers
        df = self.get_prices(origin, dest, depart, encode=False)
        # get the cheapest price
        cheapest_price = df['total'].min()
        return cheapest_price
    

    def wget_prices(self, origin, dest, depart):
        try:
            '''
            Returns a orderd list of flight offers from the origin to the destination on the departure date.
            '''
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode = origin, destinationLocationCode = dest, departureDate = depart, adults=1)
            response = response.data
            result = {}; price = {}; cureency = {}; carrierCode = {}; duration = {}; date = {}
            for i in range(len(response)):
                price[i] = response[i]['price']['total']
                cureency[i] = response[i]['price']['currency']
                carrierCode[i] = response[i]['validatingAirlineCodes'][0]
                duration[i] = response[i]['itineraries'][0]['duration']
                date[i] = response[i]['itineraries'][0]['segments'][0]['departure']['at']
            # the dict result is composed of a key called 'flight n' and a value which is a dict with the keys 'price',
            #   'currency' and 'carrierCode'
            for i in range(len(response)):
                result[f'flight {i}'] = {'price': price[i], 'currency': cureency[i],
                                         'carrierCode': carrierCode[i], 'duration': duration[i], 'date': date[i]}
            
            return result
        except ResponseError as error:
            raise error
        

    def wget_prices2(self, origin, dest, depart, ret, adu):
        try:
            # Access token
            conn = http.client.HTTPSConnection("test.api.amadeus.com")
            payload = "client_id=nzRfRZWzv8XjvR7byTGwTqf58Z50NOil&client_secret=lN9yTIWfxB0VQtbx&grant_type=client_credentials"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            conn.request("POST", "/v1/security/oauth2/token", body=payload, headers=headers)
            response = conn.getresponse()
            data = response.read().decode("utf-8")
            access_token = json.loads(data)['access_token']

            # Realizar solicitud GET para obtener precios de vuelos
            headers = {'Authorization': f'Bearer {access_token}'}
            conn.request("GET", f"/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={depart}&returnDate={ret}&adults={adu}&max=5", headers=headers)
            response = conn.getresponse()
            data = response.read().decode("utf-8")
            print(data)

        except Exception as e:
            print(f"Error en la solicitud: {str(e)}")

    def wget_recommendations(self, like, ori):
        try:
            '''
            Recommends travel destinations similar to Paris for travelers in France
            '''
            response = self.amadeus.reference_data.recommended_locations.get(cityCodes=like , travelerCountryCode=ori)
            result = {}; name = {}; relevance = {}
            for i in range(len(response.data)):
                name[i] = response.data[i]['name']
                relevance[i] = response.data[i]['relevance']
            for i in range(len(response.data)):
                result[f'recommendation{i}'] = {'name': name[i], 'relevance': relevance[i]}
            return result
        except ResponseError as error:
            raise error
        
    def wget_delay_prediction(self, origin, dest, depart_date, depart_time, arrival_date, arrival_time, aircraftCode, carrierCode, 
                              flight_number, drt):
        try:
            response = self.amadeus.travel.predictions.flight_delay.get(originLocationCode=origin, destinationLocationCode=dest,
                                                           departureDate=depart_date, departureTime=depart_time,
                                                           arrivalDate=arrival_date, arrivalTime=arrival_time,
                                                           aircraftCode=aircraftCode, carrierCode=carrierCode,
                                                           flightNumber=flight_number, duration=drt)
            result = {}; probability = {}; delay = {}; sub_type = {}
            for i in range(len(response.data)):
                probability[i] = response.data[i]['probability']
                delay[i] = response.data[i]['result']
                sub_type[i] = response.data[i]['subType']
            for i in range(len(response.data)):
                result[f'prediction{i}'] = {'probability': probability[i], 'delay': delay[i], 'sub_type': sub_type[i]}
            return result
        except ResponseError as error:
            raise error
        

# def main():
#     # create an instance of the class
#     flight_search = FlightSearch()
#     print(flight_search.wget_prices('CDG', 'BCN', '2023-11-11'))
#     # flight_search.wget_prices2('CDG', 'BCN', '2023-11-11', '2023-11-13', 1)
#     # flight_search.wget_recommendations('PAR', 'FR')
#     # flight_search.get_flight_offers('CDG', 'BCN', '2023-11-13', 1)
#     # flight_search.wget_delay_prediction('CDG', 'BCN', '2023-11-13', '18:20:00', '2023-11-13', '20:45:00', '321', 'VY', '1001', 'PT2H25M')

# if __name__ == '__main__':
#     main()
