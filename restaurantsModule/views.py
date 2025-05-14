from django.shortcuts import render
from .models import Restaurant, SpinHistory
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RestaurantSerializer, SpinHistorySerializer
import math

from authApis.models import CreateProfileModel


# Create your views here.


def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_restaurants(request):
    user = request.user

    if not user.is_authenticated:
        return Response(
            {
                "status": {"code": 401, "success": False},
                "data": None,
                "error": {"location": "User not authenticated."},
                "message": "User is not authenticated.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        profile = CreateProfileModel.objects.get(user=user)
        user_lat = float(profile.latitude)
        user_lng = float(profile.longitude)
    except (CreateProfileModel.DoesNotExist, TypeError, ValueError):
        return Response(
            {
                "status": {"code": 400, "success": False},
                "data": None,
                "error": {"location": "User location not set."},
                "message": "User's latitude and longitude are required in profile.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    restaurants = Restaurant.objects.all()
    serialized = RestaurantSerializer(restaurants, many=True).data

    for restaurant in serialized:
        rest_lat = restaurant.get("latitude")
        rest_lng = restaurant.get("longitude")
        if rest_lat is not None and rest_lng is not None:
            restaurant["distance_km"] = calculate_distance(
                user_lat, user_lng, float(rest_lat), float(rest_lng)
            )
        else:
            restaurant["distance_km"] = None

    return Response(
        {
            "status": {"code": 200, "success": True},
            "data": serialized,
            "error": None,
            "message": "All restaurants fetched successfully.",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def create_restaurant(request):
    serializer = RestaurantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "status": {
                    "code": 201,
                    "success": True,
                },
                "data": serializer.data,
                "error": None,
                "message": "Restaurant created successfully.",
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {
            "status": {
                "code": 400,
                "success": False,
            },
            "data": None,
            "error": serializer.errors,
            "message": "Failed to create restaurant.",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["PUT", "DELETE"])
def update_or_delete_restaurant(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {
                "status": {
                    "code": 404,
                    "success": False,
                },
                "data": None,
                "error": {"restaurant": "Restaurant not found."},
                "message": "Failed to find restaurant.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "PUT":
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": {
                        "code": 200,
                        "success": True,
                    },
                    "data": serializer.data,
                    "error": None,
                    "message": "Restaurant updated successfully.",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": {
                    "code": 400,
                    "success": False,
                },
                "data": None,
                "error": serializer.errors,
                "message": "Failed to update restaurant.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    elif request.method == "DELETE":
        restaurant.delete()
        return Response(
            {
                "status": {
                    "code": 204,
                    "success": True,
                },
                "data": None,
                "error": None,
                "message": "Restaurant deleted successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_questionaire_result(request):
    user = request.user

    if not user.is_authenticated:
        return Response(
            {
                "status": {"code": 401, "success": False},
                "data": None,
                "error": {"location": "User not authenticated."},
                "message": "User is not authenticated.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    preferences = request.data.get("preferences")
    delivery = request.data.get("delivery")
    ambience = request.data.get("ambience")

    filter_kwargs = {}
    if preferences:
        filter_kwargs["preferences"] = preferences.upper()
    if delivery:
        filter_kwargs["delivery"] = delivery.upper()
    if ambience:
        filter_kwargs["ambience"] = ambience.upper()

    restaurants = Restaurant.objects.filter(**filter_kwargs)

    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(
        {
            "status": {"code": 200, "success": True},
            "data": serializer.data,
            "error": None,
            "message": "Restaurants fetched successfully.",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_spin_result(request, restaurant_id):
    user = request.user

    if not restaurant_id:
        return Response(
            {
                "status": {"code": 400, "success": False},
                "data": None,
                "error": {"location": "restaurant_id is required."},
                "message": "Restaurant ID is missing.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {
                "status": {"code": 404, "success": False},
                "data": None,
                "error": {"location": "restaurant_id"},
                "message": "Restaurant not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    spin = SpinHistory.objects.create(user=user, selected_restaurant=restaurant)

    return Response(
        {
            "status": {"code": 201, "success": True},
            "data": {
                "spin_id": spin.id,
                "restaurant": restaurant.name,
                "spin_time": spin.spin_time,
            },
            "error": None,
            "message": "Spin result saved successfully.",
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_spin_history_records(request):
    user = request.user

    if not user.is_authenticated:
        return Response(
            {
                "status": {"code": 401, "success": False},
                "data": None,
                "error": {"location": "User not authenticated."},
                "message": "User is not authenticated.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    spins = SpinHistory.objects.filter(user=user).order_by("-spin_time")

    serializer = SpinHistorySerializer(spins, many=True)
    return Response(
        {
            "status": {"code": 200, "success": True},
            "data": serializer.data,
            "error": None,
            "message": "Spin history fetched successfully.",
        },
        status=status.HTTP_200_OK,
    )
