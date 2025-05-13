from rest_framework import serializers
from .models import Restaurant , SpinHistory


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"



class SpinHistorySerializer(serializers.ModelSerializer):
    selected_restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = SpinHistory
        fields = ["id", "selected_restaurant", "spin_time"]