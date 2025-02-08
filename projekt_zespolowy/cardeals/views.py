from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView

from cardeals.models import Car, CarDeal
from cardeals.forms import CarForm, CarDealForm
from cardeals.filters import CarDealFilter

class CarDealListView(ListView):
    model = CarDeal
    paginate_by = 100

    context_object_name = 'deals'

    def get_queryset(self):
        return CarDealFilter(self.request.GET, queryset=super().get_queryset()).qs

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

class CarDealDeleteView(LoginRequiredMixin, DeleteView):
    model = CarDeal
    success_url = reverse_lazy("cardeals:list")

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "cardeals/dashboard.html"
