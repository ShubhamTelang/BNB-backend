from .views import *
from django.urls import path

urlpatterns = [
    path('',conversation_list.as_view(),name='api_conversation_list'),
    path('start/<uuid:user_id>/',Conversation_start.as_view(),name='conversation start'),
    path('<uuid:pk>/',ConversationDetail.as_view(),name='conversation detail')
]
