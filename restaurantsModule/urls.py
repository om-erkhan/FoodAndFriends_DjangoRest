from django.urls import path, include
from .views import get_restaurants, create_restaurant, update_or_delete_restaurant


urlpatterns = [
    path("restaurants/", get_restaurants),
    path("createrestaurants/", create_restaurant),
    path(
        "update_or_delete_restaurant/<int:restaurant_id>/", update_or_delete_restaurant
    ),
]
