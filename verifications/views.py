from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import EmailOTP
from .utils import generate_otp
from .emails import send_otp_email

# class SendEmailOTPView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user

#         if user.is_email_verified:
#             return Response({"detail": "Email already verified"}, status=400)

#         otp = generate_otp()

#         EmailOTP.objects.create(user=user, otp=otp)
#         send_otp_email(user.email, otp)

#         return Response({"detail": "OTP sent to email"})


class VerifyEmailOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        otp = request.data.get("otp")

        try:
            email_otp = EmailOTP.objects.filter(
                user=request.user,
                otp=otp,
                is_used=False
            ).latest("created_at")
        except EmailOTP.DoesNotExist:
            return Response({"detail": "Invalid OTP"}, status=400)

        if email_otp.is_expired():
            return Response({"detail": "OTP expired"}, status=400)

        email_otp.is_used = True
        email_otp.save()

        request.user.is_email_verified = True
        request.user.save()

        return Response({"detail": "Email verified successfully"})
