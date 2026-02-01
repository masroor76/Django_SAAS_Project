from django.urls import path
from .views import VerifyEmailOTPView

urlpatterns = [
    path("verify-otp/", VerifyEmailOTPView.as_view()),
]
