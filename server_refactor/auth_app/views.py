from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework.permissions import AllowAny,IsAuthenticated
import os
import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data)
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.is_verified=True
                user.save()
                # token = PasswordResetTokenGenerator().make_token(user)
                # verification_link = f"{request.data.get('base_url', 'http://localhost:3000/verify-email')}?uid={encrypt_uuid(str(user.id))}&token={token}"
                
                # send_mail(
                #     'Verify Your Email',
                #     f'Click the link to verify your email: {verification_link}',
                #     settings.EMAIL_HOST_USER,
                #     [user.email],
                #     fail_silently=False,
                # )
                return Response({"success":True,"message": "User registration is completed successfully."}, status=status.HTTP_201_CREATED)
            raise Exception(serializer.errors)
        except Exception as e:
            print(str(e))
            return Response({"error": f"Error while registering user. This Username or Email is already taken!"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            uid = request.data.get('uid')
            token = request.data.get('token')
            user_id = decrypt_uuid(uid)
            user = get_object_or_404(User, id=user_id)

            if PasswordResetTokenGenerator().check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({"message": "Email verified successfully.","success":True}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: 
            return Response({"error":f"error while varifying email. {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            if not user.is_verified:
                return Response({"error": "Email not verified.","success":True}, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'success':True,
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username
            }, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response({'error':serializer.errors,'success':False}, status=status.HTTP_400_BAD_REQUEST)




class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True ,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        old_profile_picture = (
            user.profile_picture.path
            if user.profile_picture and os.path.exists(user.profile_picture.path)
            else None
        )

        user.delete()

        if old_profile_picture:
            try:
                os.remove(old_profile_picture)
            except Exception as e:
                return Response(
                    {"error": f"Failed to delete profile picture: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response({"message": "User deleted successfully.","success":True}, status=status.HTTP_204_NO_CONTENT)

from .utils import encrypt_uuid
class PasswordResetRequestView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            base_url = request.data.get('base_url',f'http://localhost:3000/reset-password') #http://localhost:3000/reset-password?token=
            user = get_object_or_404(User, email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = f"{base_url}?uid={encrypt_uuid(str(user.id))}&token={token}"
            send_mail(
                'Password Reset',
                f'Click the link to reset your password: {reset_link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset email sent. Please check your email and follow the instructions.',"success":True})
        except Exception as e:
            return Response({'error': f'Error sending password reset email: {str(e)}',"success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from rest_framework.decorators import api_view
from .utils import decrypt_uuid

@api_view(['POST'])
def verify_token(request):
    token = request.data.get('token', None)
    if not token:
        return Response({'detail': 'Token is required',"success":False}, status=status.HTTP_400_BAD_REQUEST)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return Response({'detail': 'Token is valid', 'payload': payload,"success":False}, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError:
        return Response({'detail': 'Token has expired',"success":False}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({'detail': 'Invalid token',"success":False}, status=status.HTTP_401_UNAUTHORIZED)
    
class PasswordResetConfirmView(APIView):
    def post(self, request):
        try:    
            token = request.data.get('token')
            new_password = request.data.get('new_password')
            uuid = request.data.get('uid')
            user_id = decrypt_uuid(uuid)
            user = get_object_or_404(User, id=user_id)
            
            if PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successfully.',"success":False})
            return Response({'error': 'Invalid token or user.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Error resetting password: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework_simplejwt.tokens import RefreshToken

class LogoutView(APIView):
    permission_classes = [AllowAny]  # Allow any user to call this endpoint

    def post(self, request):
        try:
            print(request.data)
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate and blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error during logout: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
