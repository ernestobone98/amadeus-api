from django.urls import path
from . import views

urlpatterns = [
    # path('/', views.api, name='api'),
    # path('<str:city>/', views.api, name='api'),
    # # create a path with origin, destination and date ie. api/origin&destination&date
    path('<str:origin>&<str:destination>&<str:date>/', views.prices, name='prices'),
    path('<str:origin>/', views.routes, name='routes'),
    path('hello/', views.say_hello, name='say_hello')
]