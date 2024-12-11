from django.shortcuts import render
from django.views.generic.list import ListView

from cardeals.models import CarDeal

class CarDealListView(ListView):
    model = CarDeal
    paginate_by = 100

    context_object_name = 'deals'
