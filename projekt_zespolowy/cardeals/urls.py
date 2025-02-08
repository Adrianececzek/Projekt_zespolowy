from django.urls import path
from cardeals.views import (
    CarDealListView,
    CarCreateView,
    CarDealCreateView,
    CarDealDetailView,
    CarDealUpdateView,
    CarDealDeleteView,
    DashboardView,
)

app_name = 'cardeals'
urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path('', CarDealListView.as_view(), name='list'),
    path("createcar/", CarCreateView.as_view(), name='createcar'),
    path("createcardeal/", CarDealCreateView.as_view(), name='createcardeal'),
    path("<str:slug>/", CarDealDetailView.as_view(), name='detail'),
    path("<str:slug>/edit/", CarDealUpdateView.as_view(), name='editcardeal'),
    path("<str:slug>/delete/", CarDealDeleteView.as_view(), name='deletecardeal'),
]
