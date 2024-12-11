from django.urls import path
from cardeals.views import (
    CarDealListView,
    CarCreateView,
    CarDealCreateView,
    CarDealDetailView
)

app_name = 'cardeals'
urlpatterns = [
    path('', CarDealListView.as_view(), name='list'),
    path("createcar/", CarCreateView.as_view(), name='createcar'),
    path("createcardeal/", CarDealCreateView.as_view(), name='createcardeal'),
    path("<str:slug>/", CarDealDetailView.as_view(), name='detail'),
]
