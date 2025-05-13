import random
from restaurantsModule.models import Restaurant

def create_restaurants():
    names = [
        "Tasty Bites", "Food Haven", "Flavor Town", "Spicy Spoon", "Urban Dine",
        "The Grub Spot", "Bistro Bliss", "Golden Plate", "Feast House", "Yummy Yard"
    ]
    
    ambiences = [choice[0] for choice in Restaurant.Ambience.choices]
    deliveries = [choice[0] for choice in Restaurant.Delivery.choices]
    preferences = [choice[0] for choice in Restaurant.CuisinePreferences.choices]

    for i in range(50):
        name = f"{random.choice(names)} #{i+1}"
        address = f"{random.randint(1, 999)} Main Street, Cityville"
        phone_number = f"0300{random.randint(1000000, 9999999)}"
        email = f"contact{i}@restaurant.com"
        business_name = f"Business {i+1}"

        Restaurant.objects.create(
            name=name,
            address=address,
            phone_number=phone_number,
            web_url=email,
            bussiness_name=business_name,
            longitude=random.uniform(-180, 180),
            latitude=random.uniform(-90, 90),
            profile_image=f"https://example.com/images/{i}.jpg",
            ambience=random.choice(ambiences),
            delivery=random.choice(deliveries),
            preferences=random.choice(preferences),
        )

    print("✅ Successfully created 50 random restaurants!")
