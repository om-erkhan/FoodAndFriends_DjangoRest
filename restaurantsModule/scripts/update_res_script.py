import random
from restaurantsModule.models import Restaurant

def update_restaurant_enums():
    ambience_choices = [choice[0] for choice in Restaurant.Ambience.choices]
    delivery_choices = [choice[0] for choice in Restaurant.Delivery.choices]
    preference_choices = [choice[0] for choice in Restaurant.CuisinePreferences.choices]

    restaurants = Restaurant.objects.all()
    for restaurant in restaurants:
        restaurant.ambience = random.choice(ambience_choices)
        restaurant.delivery = random.choice(delivery_choices)
        restaurant.preferences = random.choice(preference_choices)
        restaurant.save()

    print(f"✅ Updated {restaurants.count()} restaurants with random ambience, delivery, and preferences!")

# Run this script in Django shell or as a management command
# Example from shell:
# python manage.py shell
# >>> from path.to.script import update_restaurant_enums
# >>> update_restaurant_enums()
