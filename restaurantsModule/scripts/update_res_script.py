import random
from restaurantsModule.models import Restaurant

# def update_restaurant_enums():
#     ambience_choices = [choice[0] for choice in Restaurant.Ambience.choices]
#     delivery_choices = [choice[0] for choice in Restaurant.Delivery.choices]
#     preference_choices = [choice[0] for choice in Restaurant.CuisinePreferences.choices]

#     restaurants = Restaurant.objects.all()
#     for restaurant in restaurants:
#         restaurant.ambience = random.choice(ambience_choices)
#         restaurant.delivery = random.choice(delivery_choices)
#         restaurant.preferences = random.choice(preference_choices)
#         restaurant.save()

#     print(f"✅ Updated {restaurants.count()} restaurants with random ambience, delivery, and preferences!")


# # python manage.py shell
# # >>> from path.to.script import update_restaurant_enums
# # >>> update_restaurant_enums()

image_urls = [
    "https://images.unsplash.com/photo-1555992336-03a23c2a8613",
    "https://images.unsplash.com/photo-1550966871-3ed90a6fbc9c",
    "https://images.unsplash.com/photo-1556761175-4b46a572b786",
    "https://images.unsplash.com/photo-1582452972060-4cd94a2b3a53",
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
    "https://images.unsplash.com/photo-1528605248644-14dd04022da1",
    "https://images.unsplash.com/photo-1498654896293-37aacf113fd9",
    "https://images.unsplash.com/photo-1504674900239-24159a89200e",
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
    "https://images.unsplash.com/photo-1504674900247-1e8bfeaa6813",
    "https://images.unsplash.com/photo-1553621042-f6e147245754",
    "https://images.unsplash.com/photo-1576618148400-f54bed99fcfd",
    "https://images.unsplash.com/photo-1504674900239-24159a89200e",
    "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38",
    "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
    "https://images.unsplash.com/photo-1598514982780-3c0fdf64aebd",
    "https://images.unsplash.com/photo-1606787366850-de6330128bfc",
    "https://images.unsplash.com/photo-1588854337118-3e846deef4f2",
    "https://images.unsplash.com/photo-1572569729334-9e5a4a6fefb3",
    "https://images.unsplash.com/photo-1621961459609-d75b94d44e1c",
    "https://images.unsplash.com/photo-1620841222285-3382f71c9a3c",
    "https://images.unsplash.com/photo-1533777324565-a040eb52fac1",
    "https://images.unsplash.com/photo-1533777419517-35ef2b63e0b3",
    "https://images.unsplash.com/photo-1579202673506-ca3ce28943ef",
    "https://images.unsplash.com/photo-1600047509124-3e4e09dfe28e",
    "https://images.unsplash.com/photo-1603066692371-f4fe055007c8",
    "https://images.unsplash.com/photo-1601780483449-7a18212aabf2",
    "https://images.unsplash.com/photo-1613145993486-b2de572cfdd9",
    "https://images.unsplash.com/photo-1600891964325-b1e6f6779db5",
    "https://images.unsplash.com/photo-1600891964096-d4fe75b284f4",
    "https://images.unsplash.com/photo-1551218808-94e220e084d2",
    "https://images.unsplash.com/photo-1581276879432-15a43c01b0f2",
    "https://images.unsplash.com/photo-1598511721390-8d1512b7b2be",
    "https://images.unsplash.com/photo-1600789541125-100a02ff9eb8",
    "https://images.unsplash.com/photo-1600891964224-dc69e073f579",
    "https://images.unsplash.com/photo-1581547842009-364d387aecb1",
    "https://images.unsplash.com/photo-1608219959300-8d4d9a7d961d",
    "https://images.unsplash.com/photo-1581547841980-99771f0c3d9e",
    "https://images.unsplash.com/photo-1600891964162-f3835d552c4b",
    "https://images.unsplash.com/photo-1556905055-8f358a7a47b2",
    "https://images.unsplash.com/photo-1581547841985-9e229d391d96",
    "https://images.unsplash.com/photo-1581291518830-4c27fd1d7b3d",
    "https://images.unsplash.com/photo-1581547842005-3bdfb46008c7",
    "https://images.unsplash.com/photo-1581547841996-74978d5b8a4b",
    "https://images.unsplash.com/photo-1581547841986-d9df7c7a9572",
    "https://images.unsplash.com/photo-1581547841991-997db6747c12",
    "https://images.unsplash.com/photo-1523978591478-c753949ff840",
    "https://images.unsplash.com/photo-1581547841992-5eabc6a130b6",
    "https://images.unsplash.com/photo-1572373676727-9a8b2c2a7a07",
    "https://images.unsplash.com/photo-1578926283824-5737c7b4f21e",
]
extra_image_urls = [
    "https://images.unsplash.com/photo-1556740738-b6a63e27c4df",
    "https://images.unsplash.com/photo-1600891964849-594b6b3d0802",
    "https://images.unsplash.com/photo-1565895405139-628b6c094a3c",
    "https://images.unsplash.com/photo-1598515213701-211f01c17c5d",
    "https://images.unsplash.com/photo-1579583763976-51c32dc43a3f",
    "https://images.unsplash.com/photo-1544148105-e9c2edb8f9a5",
    "https://images.unsplash.com/photo-1514514783821-f3515e9147f4",
    "https://images.unsplash.com/photo-1551782450-a2132b4ba21d",
    "https://images.unsplash.com/photo-1586190848861-99aa4a171e90",
    "https://images.unsplash.com/photo-1581551066271-c9c5af8d55b8",
    "https://images.unsplash.com/photo-1617191518000-d534bdf7e7e0",
]

image_urls.extend(extra_image_urls)


def update_restaurant_urls():
    restaurants = Restaurant.objects.all()[:61]
    print(f"Total restaurants fetched: {len(restaurants)}")
    print(f"Total images available: {len(image_urls)}")
    for i, restaurant in enumerate(restaurants):
        restaurant.profile_image = image_urls[i]
        restaurant.save()
        print(f"Updated {restaurant.name} with image {image_urls[i]}")
