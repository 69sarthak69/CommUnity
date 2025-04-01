from django.urls import path
from .views import RoomMessageListView

urlpatterns = [
    path('messages/<str:room_name>/', RoomMessageListView.as_view(), name='room-messages'),
]
