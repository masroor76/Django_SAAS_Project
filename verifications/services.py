# verification/services.py
from .models import EmailOTP
from .utils import generate_otp
from .emails import send_otp_email

def send_verification_otp(user):
    if user.is_email_verified:
        return False  # Already verified

    otp = generate_otp()

    # Save OTP in DB
    EmailOTP.objects.create(user=user, otp=otp)

    # Send email
    send_otp_email(user.email, otp)

    return True
