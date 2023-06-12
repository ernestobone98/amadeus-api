from django.urls import path
from . import views

urlpatterns = [
    path('price/<str:origin>&<str:destination>&<str:date>/', views.prices, name='prices'),
    path('reco/<str:like>&<str:ori>/', views.recommendations, name='recommendations'),
    path('routes/<str:origin>/', views.routes, name='routes'),
    path('ai/<str:origin>&<str:destination>&<str:depart_date>&<str:depart_time>&<str:arrival_date>&<str:arrival_time>&<str:aircraftCode>'
         '&<str:carrierCode>&<str:flight_number>&<str:drt>/', views.predictions, name='predictions'),
    path('delimitation/<str:lat>&<str:lon>&<str:country>&<str:dest>&<str:date>&<str:ratio>/', views.airports, name='airports'),
    path('hello/', views.say_hello, name='say_hello')
]