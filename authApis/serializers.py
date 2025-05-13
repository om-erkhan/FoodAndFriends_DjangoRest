from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from .models import OTPVerification
from django.core.mail import send_mail
from rest_framework.exceptions import APIException
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import OTPVerification, CreateProfileModel
from rest_framework.exceptions import APIException


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username": "User not found."})

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({"password": "Invalid credentials."})

        data["user"] = user
        return data



class SignupSerializer(serializers.ModelSerializer):
    otp = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "otp"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "validators": [],
            },
        }

    def get_otp(self, obj):
        otp_record = OTPVerification.objects.filter(user=obj).first()
        return otp_record.otp if otp_record else None

    def validate_email(self, value):
        # Skip default unique validation – handle manually in create()
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]

        # Check if a user already exists
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            # If already verified, raise error
            if existing_user.is_otp_verified:
                raise serializers.ValidationError(
                    {"email": "Email already in use and verified."}
                )

            # If not verified, update or create OTP and return the existing user
            otp = "00000"
            OTPVerification.objects.update_or_create(
                user=existing_user, defaults={"otp": otp, "is_verified": False}
            )
            return existing_user

        # New user case
        user = User(username=email, email=email)
        user.set_password(password)
        user.save()

        otp = "00000"
        OTPVerification.objects.create(user=user, otp=otp, is_verified=False)

        return user


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate_otp(self, value):
        if not value.isdigit() or len(value) != 5:
            raise serializers.ValidationError("Invalid OTP format.")
        return value

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError(
                {"email": "User not found."},
            )

        try:
            otp_record = OTPVerification.objects.get(user=user, otp=otp)
        except OTPVerification.DoesNotExist:
            raise serializers.ValidationError(
                {"otp": "Invalid OTP."},
            )

        if otp_record.is_verified:
            raise serializers.ValidationError(
                {"otp": "OTP already verified."},
            )

        # Save references for use in .save()
        data["user"] = user
        data["otp_record"] = otp_record
        return data

    def save(self, **kwargs):
        user = self.validated_data["user"]
        otp_record = self.validated_data["otp_record"]

        otp_record.is_verified = True
        otp_record.save()

        user.is_otp_verified = True
        user.save()

        return user


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateProfileModel
        fields = [
            "first_name",
            "last_name",
            "longitude",
            "latitude",
            "location",
            "city",
            "state",
            "phone_number",
        ]

    def validate(self, data):
        for field, value in data.items():
            if value in [None, "", " "]:
                raise serializers.ValidationError(f"{field} cannot be empty.")
        return data


 