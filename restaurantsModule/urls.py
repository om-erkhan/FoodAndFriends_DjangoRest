from django.urls import path, include
from .views import (
    get_restaurants,
    create_restaurant,
    update_or_delete_restaurant,
    get_questionaire_result,
    save_spin_result,
    get_spin_history,
)


urlpatterns = [
    path("restaurants/", get_restaurants),
    path("filter_restaurants/", get_questionaire_result),
    path("createrestaurants/", create_restaurant),
    path("get_spin_history/", get_spin_history),
    path(
        "update_or_delete_restaurant/<int:restaurant_id>/", update_or_delete_restaurant
    ),
    path("save_spin_result/<int:restaurant_id>/", save_spin_result),
]
