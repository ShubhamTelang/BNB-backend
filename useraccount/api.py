from .serializers import *
from property.serializers import *
from .models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class landlord_detail(APIView):
    def get(self,request,pk):
        user = User.objects.get(pk=pk)
        serializers = UserDetailSerializer(user)
        return Response({"response":serializers.data})
    
class reservations_list(APIView):
    def get(self,request):
        reservations = request.user.reservations.all()
        serializer = ReservationListSerializer(reservations,many=True)
        return Response(serializer.data)