from amadeus import Client, ResponseError
import tokens as to

amadeus = Client(
    client_id = to.client_id,
    client_secret = to.client_secret
)

try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='MAD',
        destinationLocationCode='ATH',
        departureDate='2022-11-01',
        adults=1)
    print(response.data)
except ResponseError as error:
    print(error)

