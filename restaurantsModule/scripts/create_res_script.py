from restaurantsModule.models import Restaurant

import random


def create_restaurants():
    names = [
        "Tasty Bites",
        "Food Haven",
        "Flavor Town",
        "Spicy Spoon",
        "Urban Dine",
        "The Grub Spot",
        "Bistro Bliss",
        "Golden Plate",
        "Feast House",
        "Yummy Yard",
    ]

    addresses = [f"{i} Main Street, Cityville" for i in range(1, 11)]
    phone_numbers = [f"12345678{i:02}" for i in range(10)]
    emails = [f"contact{i}@restaurant.com" for i in range(10)]
    bussiness_names = [f"Business {i}" for i in range(10)]

    for i in range(10):
        Restaurant.objects.create(
            name=names[i],
            address=addresses[i],
            phone_number=phone_numbers[i],
            web_url=emails[i],
            bussiness_name=bussiness_names[i],
            longitude=random.uniform(-180, 180),
            latitude=random.uniform(-90, 90),
            profile_image=f"https://example.com/images/{i}.jpg",
        )

    print("✅ 10 Restaurants created successfully!")
