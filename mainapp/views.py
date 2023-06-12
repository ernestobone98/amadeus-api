from django.shortcuts import render
from django.http import HttpResponse
import json
from . import api_calls
import geopy.distance
from geopy.geocoders import Nominatim
import time

def say_hello(request):
    # create a blank json object
    json_object = {
        'name': 'John Doe',
        'age': 30,
        'address': '123 Main St'
    }
    json_data = json.dumps(json_object)
    response = HttpResponse(json_data, content_type='application/json')
    response.status_code = 200
    return response

def routes(request, origin=None):
    # create an object from the api_calls class
    api = api_calls.FlightSearch()
    json_data = json.dumps(api.airport_routes(origin))
    response = HttpResponse(json_data, content_type='application/json')
    response.status_code = 200
    return response

def prices(request, origin=None, destination=None, date=None):
    print("entering prices")
    api = api_calls.FlightSearch()
    json_data =json.dumps(api.wget_prices(origin, destination, date))
    response = HttpResponse(json_data, content_type='application/json')
    response.status_code = 200
    print(json_data)
    return response

def recommendations(request, like=None, ori=None):
    api = api_calls.FlightSearch()
    json_data = json.dumps(api.wget_recommendations(like, ori))
    response = HttpResponse(json_data, content_type='application/json')
    response.status_code = 200
    return response

def predictions(request, origin=None, destination=None, depart_date=None, depart_time=None, arrival_date=None, 
                arrival_time=None, aircraftCode=None, carrierCode=None, flight_number=None, drt=None):
    
    api = api_calls.FlightSearch()
    json_data = json.dumps(api.wget_delay_prediction(origin, destination, depart_date, depart_time, arrival_date, 
                                                     arrival_time, aircraftCode, carrierCode, flight_number, drt))
    response = HttpResponse(json_data, content_type='application/json')
    response.status_code = 200
    return response


def airports(request, lat=None, lon=None, country='France', dest=None, date=None, ratio=None):
    coord1 = (float(lat), float(lon))
    # open the json file airports.json
    with open('/home/ernestobone/Documents/M1/TERD2/amadeus-api/mainapp/airports.json', 'r') as f:
        data = json.load(f)
    
    # if country from a item in the json file is equal to the country from the request
    # then calculate the distance between the two coordinates
    # if the distance is less than the ratio, then add the airport to the list
    airports = []
    for item in data:
        if item['country'] == country:
            coord2 = (float(item['geo_point_2d']['lat']), float(item['geo_point_2d']['lon']))
            distance = geopy.distance.distance(coord1, coord2).km
            if distance < float(ratio):
                item['distance'] = distance
                airports.append(item)

    # now from airports, sort the list by distance and then convert the list to json
    airports = sorted(airports, key=lambda k: k['distance'])
    # get prices for each airport
    api = api_calls.FlightSearch()
    result = {}
    # try execept to block the error when the api call returns an error
    try:
        for airport in airports:
            # the result dict will concatenate all api calls
            result[airport['iata']] = api.wget_prices(airport['iata'], dest, date)
            # 100 ms pause between each api call
            # time.sleep(0.1)
            # add date to the result dict
            result[airport['iata']]['date'] = date
            # add distance to the result dict
            result[airport['iata']]['distance'] = airport['distance']
    except:
        pass
    # convert the result dict to a valid json format
    json_data = json.dumps(result)
    response = HttpResponse(json_data, content_type='application/json')
    response.status_code = 200
    return response
    
        






