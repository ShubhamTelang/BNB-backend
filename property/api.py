from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from .models import Property, Reservation
from .serializers import PropertiesListSerializer, propertiesDetailsSerializer, ReservationListSerializer
from .forms import PropertyForm
from useraccount.models import User

class PropertyList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
            token = AccessToken(token)
            user_id = token.payload['user_id']
            user = User.objects.get(pk=user_id)
        except Exception as e:
            user = None

        properties = Property.objects.all()
        filters = {
            'landlord_id': request.GET.get('landlord_id', ''),
            'country': request.GET.get('country', ''),
            'category': request.GET.get('category', ''),
            'bedrooms__gte': request.GET.get('bedrooms', ''),
            'guests__gte': request.GET.get('guests', ''),
            'bathrooms__gte': request.GET.get('bathrooms', ''),
        }

        # Remove empty filters
        filters = {k: v for k, v in filters.items() if v}

        properties = properties.filter(**filters)

        checkin_date = request.GET.get('checkin', '')
        checkout_date = request.GET.get('checkout', '')

        if checkin_date and checkout_date:
            exact_matches = Reservation.objects.filter(start_date=checkin_date) | Reservation.objects.filter(end_date=checkout_date)
            overlap_matches = Reservation.objects.filter(start_date__lte=checkout_date, end_date__gte=checkin_date)
            all_matches = exact_matches | overlap_matches
            properties = properties.exclude(id__in=[res.property_id for res in all_matches])

        if request.GET.get('is_favorites', '') and user:
            properties = properties.filter(favorite__in=[user])

        favorites = [prop.id for prop in properties if user and user in prop.favorite.all()]

        serializer = PropertiesListSerializer(properties, many=True)
        return JsonResponse({'data': serializer.data, 'fav': favorites})


class PropertyDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        property = get_object_or_404(Property, pk=pk)
        serializer = propertiesDetailsSerializer(property)
        return JsonResponse(serializer.data)


class CreateProperty(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.landlord = request.user
            property.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'errors': form.errors.as_json()}, status=400)


class BookProperty(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            number_of_nights = request.POST.get('number_of_nights', '')
            total_price = request.POST.get('total_price', '')
            guests = request.POST.get('guests', '')
            property = Property.objects.get(pk=pk)

            Reservation.objects.create(
                property=property,
                start_date=start_date,
                end_date=end_date,
                number_of_nights=number_of_nights,
                total_price=total_price,
                guests=guests,
                created_by=request.user
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


@permission_classes([IsAuthenticated])
class PropertyReservations(APIView):
    def get(self, request, pk):
        property = get_object_or_404(Property, pk=pk)
        reservations = property.reservations.all()
        serializer = ReservationListSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ToggleFavorite(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        property = get_object_or_404(Property, pk=pk)
        if request.user in property.favorite.all():
            property.favorite.remove(request.user)
            return Response({'is_favorite': False})
        else:
            property.favorite.add(request.user)
            return Response({'is_favorite': True})
