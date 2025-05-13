# import uuid
# from django.db import models


# class Restaurant(models.Model):
#     name = models.CharField(max_length=250)
#     address = models.CharField(max_length=250)
#     phone_number = models.CharField(max_length=15)
#     web_url = models.EmailField()
#     bussiness_name = models.CharField(max_length=250)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
#     profile_image = models.CharField(max_length=400, null=True, blank=True)


from django.db import models


class Restaurant(models.Model):
    class Ambience(models.TextChoices):
        CASUAL = "casual", "Casual"
        FAMILY = "family", "Family"
        FINE_DINING = "fine_dining", "Fine Dining"
        OUTDOOR = "outdoor", "Outdoor"
        ROMANTIC = "romantic", "Romantic"

    class Delivery(models.TextChoices):
        NONE = "none", "No Delivery"
        IN_HOUSE = "in_house", "In-House Delivery"

    class CuisinePreferences(models.TextChoices):
        JAPENESE = "Japenese", "japenese"
        CHINESE = "Chinese", "chinese"
        DESI = "Desi", "desi"

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
