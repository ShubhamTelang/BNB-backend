from rest_framework import serializers
from .models import *
from useraccount.serializers import UserDetailSerializer

class PropertiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id','title','price_per_night','Image_url')


class propertiesDetailsSerializer(serializers.ModelSerializer):
    landlord = UserDetailSerializer(read_only=True,many=False)
    class Meta:
        model =Property
        fields = (
            'id','title',
            'description',
            'price_per_night',
            'bedrooms',
            'bathrooms',
            'guests',
            'country',
            'country_code',
            'category',
            'Image_url',
            'landlord'
        )


class ReservationListSerializer(serializers.ModelSerializer):
    property =PropertiesListSerializer(read_only=True,many=False)
    class Meta:
        model = Reservation
        fields = (
            'id','start_date','end_date','number_of_nights','total_price','property'
        )