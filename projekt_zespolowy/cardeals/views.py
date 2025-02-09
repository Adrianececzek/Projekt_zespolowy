from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.db.models import Count, Avg
from django.db.models.functions import ExtractYear
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


class DashboardView(TemplateView):
    template_name = "cardeals/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deals = CarDeal.objects.all()
        cars = Car.objects.all()

        # Wykres 1: Kategorie cenowe
        context['cheap'] = deals.filter(price__lt=50000).count()
        context['mid'] = deals.filter(price__gte=50000, price__lte=150000).count()
        context['expensive'] = deals.filter(price__gt=150000).count()

        # Wykres 2: Ilość samochodów dla każdej liczby drzwi
        doors_count = cars.values('number_of_doors').annotate(count=Count('id')).order_by('number_of_doors')
        context['doors_labels'] = [str(item['number_of_doors']) for item in doors_count]
        context['doors_data'] = [item['count'] for item in doors_count]

        # Wykres 3: Średnia moc (power) dla każdego condition
        power_avg = cars.values('condition').annotate(avg_power=Avg('power')).order_by('condition')
        context['power_labels'] = [item['condition'] for item in power_avg]
        context['power_data'] = [round(item['avg_power'], 1) for item in power_avg]

        # Wykres 4: Liczba sprzedanych samochodów na rok
        sales_per_year = deals.values('car__year').annotate(count=Count('id')).order_by('car__year')
        context['sales_years'] = [item['car__year'] for item in sales_per_year]
        context['sales_counts'] = [item['count'] for item in sales_per_year]

        # Wyszukiwanie aut z najmniejszym przebiegiem
        manufacturer = self.request.GET.get('manufacturer', '')
        if manufacturer:
            cars_filtered = cars.filter(manufacturer__icontains=manufacturer).order_by('odometer')[:3]
            context['filtered_cars'] = cars_filtered
        else:
            context['filtered_cars'] = None





        return context

