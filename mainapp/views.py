from django.shortcuts import render
from django.http import HttpResponse
import json
from . import api_calls

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
    api = api_calls.FlightSearch()
    json_data =json.dumps(api.wget_prices(origin, destination, date))
    response = HttpResponse(json_data, content_type='application/json')
    response.status_code = 200
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
