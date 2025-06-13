 

from django.db import models

from django.conf import settings


class Restaurant(models.Model):
    class Ambience(models.TextChoices):
        CASUAL = "CASUAL"
        FAMILY = "FAMILY"
        OUTDOOR = "OUTDOOR"
        ROMANTIC = "ROMANTIC"

    class Delivery(models.TextChoices):
        NONE = "NONE"
        IN_HOUSE = "IN_HOUSE"

    class CuisinePreferences(models.TextChoices):
        JAPENESE = "JAPENESE"
        CHINESE = "CHINESE"
        DESI = "DESI"

    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15)
    web_url = models.EmailField()
    bussiness_name = models.CharField(max_length=250)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    profile_image = models.CharField(max_length=400, null=True, blank=True)
    ambience = models.CharField(
        max_length=20,
        choices=Ambience.choices,
        default=Ambience.CASUAL,
    )
    delivery = models.CharField(
        max_length=20,
        choices=Delivery.choices,
        default=Delivery.NONE,
    )
    preferences = models.CharField(
        max_length=20,
        choices=CuisinePreferences.choices,
        default=CuisinePreferences.JAPENESE,
    )


class SpinHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    selected_restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    spin_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} spun and got {self.selected_restaurant.name}"
    
    
    

 