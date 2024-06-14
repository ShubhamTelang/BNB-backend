from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from useraccount.models import *

class conversation_list(APIView):
    def get(self,request):
        conversations = request.user.conversations.all()
        serializer = ConversationListSerializer(conversations,many=True)
        return Response(serializer.data)


class ConversationDetail(APIView):
    def get(self, request, pk):
        conversation = get_object_or_404(request.user.conversations, pk=pk)
        convoSerializer = ConversationDetailSerializer(conversation)
        message_serializer = ConversationMessageSerializer(conversation.messages.all(),many=True)
        return Response({"conversation":convoSerializer.data,'messages':message_serializer.data}, status=status.HTTP_200_OK)
    
class Conversation_start(APIView):
    def get(self,request,user_id):
        conversations = Conversation.objects.filter(users__in=[user_id]).filter(users__in=[request.user.id])

        if conversations.count() > 0:
            conversation = conversations.first()
            return Response({'success':True,'conversation':conversation.id})
        else:
            user = User.objects.get(pk=user_id)
            conversation = Conversation.objects.create()
            conversation.users.add(request.user)
            conversation.users.add(user)
            return Response({'success':True,'conversation':conversation.id})