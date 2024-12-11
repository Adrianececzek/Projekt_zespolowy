from django.urls import path
from cardeals.views import (
    CarDealListView
)

app_name = 'cardeals'
urlpatterns = [
    path('', CarDealListView.as_view(), name='list'),
]
