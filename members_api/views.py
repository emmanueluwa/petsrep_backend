from django.urls import reverse
from rest_framework.response import Response, views, permissions
from rest_framework.decorators import api_view
from members_api.utils import Util
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status, response 
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from members.models import Profile
from members_api.serializers import EmailSerializer, ProfileSerializer, LoginSerializer, RegisterSerializer, ResetPasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your views here.
# @csrf_exempt


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(
                        data = self.request.data,
                        context = { 'request': self.request }
                        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = User.objects.filter(email=email).first()
        #not storing token in db, url only
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)

            reset_url = reverse(
                "members_api:resetting_password",
                kwargs = {"encoded_pk": encoded_pk, "token": token}
            )

            reset_link = f'http://127.0.0.1:8000{reset_url}'
            # reset_link = f'http://localhost:4200/password_reset{reset_url}'
            email_body = f'Greetings, use the link below to reset your password \n {reset_link}'
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset password'}
            Util.send_email(data)
            return response.Response({"message": 'A password reset link has been sent to your email.'})

            # return response.Response(
            #     {
            #         "message":
            #         f'Your password reset link: {reset_link}'
            #     },
            #     status = status.HTTP_200_OK,
            # )
        else:
            return response.Response(
                {"message": "User doesn't exist"},
                status = status.HTTP_400_BAD_REQUEST,
            )


class ResettingPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data = request.data,
            # the keyword args consist of the encoded pk and token 
            context = {"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)
        return response.Response(
            {"message": "Password reset complete"},
            status = status.HTTP_200_OK,
        )


# @api_view(["POST"])
# def email_view(request):
#     return send_email(request.data)
