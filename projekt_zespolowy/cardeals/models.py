from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext as _

from datetime import datetime

from projekt_zespolowy.users.models import User
from cardeals.utils import generate_slug

class Car(models.Model):
    """User car model class"""
    class ConditionChoice(models.TextChoices):
        NEW = "N", _("New")
        USED = "U", _("Used")
        CERTIFIED = "C", _("Certified Pre-Owned")
        TOTALED = "T", _("Totaled")
    class FuelChoice(models.TextChoices):
        PETROL = "P", _("Petrol")
        DIESEL = "D", _("Diesel")
        ELECTRIC = "E", _("Electric")
        HYBRID = "H", _("Hybrid")
        PLUG_IN_HYBRID = "PL", _("Plug-In Hybrid")
        CNG = "C", _("CNG")
        LPG = "L", _("LPG")
        HYDROGEN = "HY", _("Hydrogen")
        ETHANOL = "ET", _("Ethanol")
    class TransmissionChoice(models.TextChoices):
        MANUAL = "M", _("Manual")
        AUTOMATIC = "A", _("Automatic")
        CVT = "C", _("CVT")
        DUAL_CLUTCH = "D", _("Dual Clutch")
        SEMI_AUTOMATIC = "S", _("Semi-Automatic")
    class DriveTypeChoice(models.TextChoices):
        FRONT = "FR", _("Front (FWD)")
        REAR = "R", _("Rear (RWD)")
        ALL = "A", _("All (AWD)")
        FOUR = "F", _("Four (FWD)")
    manufacturer = models.CharField(max_length=50, verbose_name='Car Manufacturer')
    model = models.CharField(max_length=50, verbose_name='Car Model')
    version = models.CharField(max_length=50, verbose_name='Car Version')
    odometer = models.PositiveIntegerField(default=0, help_text="Mileage", verbose_name='Car Odometer')
    colour = models.CharField(max_length=20, verbose_name='Car Colour')
    number_of_doors = models.PositiveSmallIntegerField(default=5, verbose_name='Car Number of Doors')
    number_of_seats = models.PositiveSmallIntegerField(default=5, verbose_name='Car Number of Seats')
    engine_displacement = models.PositiveIntegerField(help_text="Engine displacement in cubic centimeters (cc)", verbose_name='Car Engine Displacement')
    power = models.PositiveIntegerField(help_text="Engine power in horsepower (hp)", verbose_name='Car Power')
    year = models.PositiveSmallIntegerField(verbose_name='Car Year',
                                                validators=[MinValueValidator(1886), MaxValueValidator(datetime.now().year)])
    condition = models.CharField(max_length=20, choices=ConditionChoice, default=ConditionChoice.USED, verbose_name='Car Condition')
    fuel_type = models.CharField(max_length=20, choices=FuelChoice, default=FuelChoice.PETROL, verbose_name='Car Fuel Type')
    transmission_type = models.CharField(max_length=20, choices=TransmissionChoice, default=TransmissionChoice.MANUAL, verbose_name='Car Transmission Type')
    drive_type = models.CharField(max_length=20, choices=DriveTypeChoice, default=DriveTypeChoice.FRONT, verbose_name='Car Drive Type')

class CarDeal(models.Model):
    """User car deal model class"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, blank=False, verbose_name='Car', related_name='deals')
    title = models.CharField(max_length=150, verbose_name=_('Title'))
    slug = models.SlugField(max_length=256, unique=True, editable=False)
    description = models.TextField(default=_("No description available."), blank=True, verbose_name=_("Description"))
    main_photo = models.URLField(verbose_name="Photo", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, verbose_name='Author')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Price')
    contact = models.CharField(max_length=15, verbose_name=_('Contact'),
                               validators=[RegexValidator(regex=r'^\+?\d{1,4}?[-.\s]??\(?\d{1,3}?\)?[-.\s]??\d{1,4}[-.\s]??\d{1,4}[-.\s]??\d{1,9}$',
                                                          message="Enter a valid phone number.")])

    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.title.strip()
            for candidate in generate_slug(base):
                if not CarDeal.objects.filter(slug=candidate).exists():
                    self.slug = candidate
                    break
            else:
                raise Exception("Can't create new CarDeal object")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

