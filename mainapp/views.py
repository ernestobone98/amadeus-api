from django.shortcuts import render
from django.http import HttpResponse
import json
import mainapp.api_calls

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
    HttpResponse(api.airport_routes(origin))

def prices(request, origin=None, destination=None, date=None):
    # create an object from the api_calls class
    api = api_calls.FlightSearch()
    api.get_prices(origin, destination, date)
