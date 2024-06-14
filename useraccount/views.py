from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate



from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegisterationView(APIView):
    def post(self,request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user= serializer.save()
            token = get_tokens_for_user(user)
            return Response({"response":"Created successfully","token":token,"user":user.id},status=status.HTTP_201_CREATED)
        return Response({"Response":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

class USerLOginView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            token = get_tokens_for_user(user)
            if user is not None:
                return Response({"Response":"Logged in","token":token,"user":user.id},status=status.HTTP_202_ACCEPTED)
            return Response({"Response":{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_400_BAD_REQUEST)
        return Response({"Response":{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_400_BAD_REQUEST)
        