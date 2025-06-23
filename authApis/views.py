from django.shortcuts import render
from authApis.models import CreateProfileModel
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import *
from apis.utils import generate_otp, send_otp_email
from authApis.models import OTPVerification


@api_view(["POST"])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "status": {"code": 200, "success": True},
                "data": {"token": token.key},
                "error": None,
                "message": "Login successful.",
            },
            status=status.HTTP_200_OK,
        )
    error_messages = list(serializer.errors.values())
    message = (
        error_messages[0][0]
        if error_messages and isinstance(error_messages[0], list)
        else "Login failed."
    )

    return Response(
        {
            "status": {"code": 400, "success": False},
            "data": None,
            "error": None,
            "message": message,
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


STATIC_OTP = "0000"


# @api_view(["POST"])
# def signup(request):
#     serializer = SignupSerializer(data=request.data)

#     if serializer.is_valid():
#         user = serializer.save()
#         return Response(
#             {
#                 "status": {
#                     "code": 201,
#                     "success": True,
#                 },
#                 "data": {
#                     "username": user.username,
#                     "email": user.email,
#                     "otp": "00000",
#                 },
#                 "error": None,
#                 "message": "User registered successfully.",
#             },
#             status=status.HTTP_201_CREATED,
#         )

#     return Response(
#         {
#             "status": {
#                 "code": 400,
#                 "success": False,
#             },
#             "data": None,
#             "error": serializer.errors,
#             "message": "Signup failed.",
#         },
#         status=status.HTTP_400_BAD_REQUEST,
#     )


@api_view(["POST"])
def signup(request):
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Generate and save OTP
        otp = generate_otp()
        OTPVerification.objects.filter(user=user).delete()
        OTPVerification.objects.create(user=user, otp=otp)

        # Send OTP to email
        send_otp_email(user.email, otp)

        return Response(
            {
                "status": {
                    "code": 201,
                    "success": True,
                },
                "data": {
                    "username": user.username,
                    "email": user.email,
                },
                "error": None,
                "message": "User registered successfully. OTP sent to email.",
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
            "message": "Signup failed.",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
def verify_otp(request):
    serializer = OTPVerificationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "status": {
                    "code": 200,
                    "success": True,
                },
                "data": {
                    "email": user.email,
                    "token": token.key,
                },
                "error": None,
                "message": "OTP verified successfully.",
            },
            status=status.HTTP_200_OK,
        )

    all_errors = []
    for field_errors in serializer.errors.values():
        if isinstance(field_errors, list):
            all_errors.extend(field_errors)
        else:
            all_errors.append(str(field_errors))

    return Response(
        {
            "status": {"code": 400, "success": False},
            "data": None,
            "error": " ".join(all_errors),
            "message": "OTP verification failed.",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_profile(request):
    user = request.user

    if CreateProfileModel.objects.filter(user=user).exists():
        return Response(
            {
                "status": {"code": 400, "success": False},
                "data": {},
                "error": "Profile already exists.",
                "message": "You already have a profile.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = CreateProfileSerializer(data=request.data)
    if serializer.is_valid():
        CreateProfileModel.objects.create(
            user=request.user,
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            phone_number=serializer.validated_data["phone_number"],
            longitude=serializer.validated_data["longitude"],
            latitude=serializer.validated_data["latitude"],
            location=serializer.validated_data["location"],
            city=serializer.validated_data["city"],
            state=serializer.validated_data["state"],
        )

        return Response(
            {
                "status": {"code": 201, "success": True},
                "data": serializer.validated_data,
                "error": None,
                "message": "Profile created successfully.",
            },
            status=status.HTTP_201_CREATED,
        )

    all_errors = []
    for field_errors in serializer.errors.values():
        if isinstance(field_errors, list):
            all_errors.extend(field_errors)
        else:
            all_errors.append(str(field_errors))

    return Response(
        {
            "status": {"code": 400, "success": False},
            "data": None,
            "error": " ".join(all_errors),
            "message": "Profile creation failed.",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    user = request.user
    try:
        profile = CreateProfileModel.objects.get(user=user)
        serializer = CreateProfileSerializer(profile)
        return Response(
            {
                "status": {
                    "code": 200,
                    "success": True,
                },
                "data": serializer.data,
                "error": None,
                "message": "Profile fetched successfully.",
            },
            status=status.HTTP_200_OK,
        )
    except CreateProfileModel.DoesNotExist:
        return Response(
            {
                "status": {
                    "code": 404,
                    "success": False,
                },
                "data": None,
                "error": "Profile not found.",
                "message": "No profile exists for this user.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    try:
        profile = CreateProfileModel.objects.get(user=user)
    except CreateProfileModel.DoesNotExist:
        return Response(
            {
                "status": {
                    "code": 404,
                    "success": False,
                },
                "data": None,
                "error": "Profile not found.",
                "message": "No profile exists for this user.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = CreateProfileSerializer(profile, data=request.data, partial=True)
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
                "message": "Profile updated successfully.",
            },
            status=status.HTTP_200_OK,
        )

    all_errors = []
    for field_errors in serializer.errors.values():
        if isinstance(field_errors, list):
            all_errors.extend(field_errors)
        else:
            all_errors.append(str(field_errors))

    return Response(
        {
            "status": {"code": 400, "success": False},
            "data": None,
            "error": " ".join(all_errors),
            "message": "Profile update failed.",
        },
        status=status.HTTP_400_BAD_REQUEST,
    )
