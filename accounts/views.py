from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from verifications import services

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            services.send_verification_otp(user)

            return Response({"message": "User registered successfully", "user_id": user.id},status=201)
        return Response(serializer.errors, status=400)