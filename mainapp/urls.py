from django.urls import path
from . import views

urlpatterns = [
    path('<str:origin>&<str:destination>&<str:date>/', views.prices, name='prices'),
    path('<str:like>&<str:ori>/', views.recommendations, name='recommendations'),
    path('<str:origin>/', views.routes, name='routes'),
    path('ai/<str:origin>&<str:destination>&<str:depart_date>&<str:depart_time>&<str:arrival_date>&<str:arrival_time>&<str:aircraftCode>'
         '&<str:carrierCode>&<str:flight_number>&<str:drt>/', views.predictions, name='predictions'),
    path('hello/', views.say_hello, name='say_hello')
]