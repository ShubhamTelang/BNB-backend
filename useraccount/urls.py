from django.urls import path,include
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.urls import path
from .views import *
from .api import *


urlpatterns = [ 
    path('myreservations/',reservations_list.as_view(),name='myreservations'),
    path('<uuid:pk>/',landlord_detail.as_view(),name='landlord details'),
    path('register/',UserRegisterationView.as_view(),name="registeration"),
    path('login/',USerLOginView.as_view(),name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]