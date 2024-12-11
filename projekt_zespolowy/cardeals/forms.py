from django.contrib import messages
from django.forms import ModelForm, HiddenInput
from cardeals.models import Car, CarDeal
from projekt_zespolowy.users.models import User

class CarForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """Make sure car author is currently logged-in user."""
        self.request = kwargs.pop('request')
        super(CarForm, self).__init__(*args, **kwargs)
        self.fields['author'].queryset = User.objects.filter(id=self.request.user.id)
        self.fields['author'].initial = User.objects.get(id=self.request.user.id)
        self.fields['author'].widget = HiddenInput()
    class Meta:
        model = Car
        fields = '__all__'

class CarDealForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """Make sure car deal author is currently logged-in user."""
        self.request = kwargs.pop('request')
        super(CarDealForm, self).__init__(*args, **kwargs)

        """Check if the currently logged-in user has authored cars"""
        user_cars = Car.objects.filter(author=self.request.user.id)
        if not user_cars.exists():
            messages.info(self.request, 'You have not authored any cars! Create your car first.')
            #TO REDO, BLOCK THE BUTTON IF NONE CARS?

        self.fields['author'].queryset = User.objects.filter(id=self.request.user.id)
        self.fields['author'].initial = User.objects.get(id=self.request.user.id)
        self.fields['author'].widget = HiddenInput()

        """Make sure only cars made by the currently logged-in user are available."""
        self.fields['car'].queryset = user_cars
        """ Make sure only one car deal can be created per car"""
        #TO DO
    class Meta:
        model = CarDeal
        fields = '__all__'
