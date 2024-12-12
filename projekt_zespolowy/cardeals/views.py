from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from cardeals.models import Car, CarDeal
from cardeals.forms import CarForm, CarDealForm

class CarDealListView(ListView):
    model = CarDeal
    paginate_by = 100

    context_object_name = 'deals'

class CarDealDetailView(DetailView):
    model = CarDeal

class CarCreateView(LoginRequiredMixin ,CreateView):
    model = Car
    form_class = CarForm

    def get_form_kwargs(self):
        kw = super(CarCreateView, self).get_form_kwargs()
        kw['request'] = self.request
        return kw

class CarDealCreateView(LoginRequiredMixin ,CreateView):
    model = CarDeal
    form_class = CarDealForm

    def get_form_kwargs(self):
        kw = super(CarDealCreateView, self).get_form_kwargs()
        kw['request'] = self.request
        return kw

class CarDealUpdateView(LoginRequiredMixin, UpdateView):
    model = CarDeal
    form_class = CarDealForm
    template_name = 'cardeals/cardeal_form.html'  # Używamy istniejącego szablonu formularza

    def get_form_kwargs(self):
        kw = super(CarDealUpdateView, self).get_form_kwargs()
        kw['request'] = self.request
        return kw

    def get_success_url(self):
        # Po zapisaniu użytkownik wraca do szczegółów oferty
        return self.object.get_absolute_url()
