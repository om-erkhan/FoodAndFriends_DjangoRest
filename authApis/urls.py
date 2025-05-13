from django.urls import path
from .views import (
    login,
    signup,
    update_profile,
    verify_otp,
    create_profile,
    get_my_profile,
)


urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("verifyOtp/", verify_otp, name="verify_otp"),
    path("createProfile/", create_profile, name="create_profile"),
    path("getProfile/", get_my_profile, name="get_my_profile"),
    path("updateProfile/", update_profile, name="update_profile"),
]
