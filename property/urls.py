from .api import *
from django.urls import path

urlpatterns = [
    path('', PropertyList.as_view(),name='property list api'),
    path('<uuid:pk>/toggle_favorite/', ToggleFavorite.as_view(),name='toggle favorite'),
    path('create/',CreateProperty.as_view(),name='create_property_api'),
    path('<uuid:pk>/',PropertyDetail.as_view(),name='property_detail_api'),
    path('<pk>/book/',BookProperty.as_view(),name='property_book_api'),
    path('<uuid:pk>/reservations/',PropertyReservations.as_view(),name='property_reservations')
]