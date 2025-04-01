from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room, Message
from .serializers import MessageSerializer

class RoomMessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_name):
        try:
            room = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return Response({"error": "Room not found"}, status=404)

        # ✅ STEP 6: Restrict based on room type
        if room_name.startswith("group_"):
            group_id = room_name.split("_")[1]
            if not request.user.joined_groups.filter(id=group_id).exists():
                return Response({"error": "You are not a member of this group"}, status=403)

        elif room_name.startswith("event_"):
            event_id = room_name.split("_")[1]
            if not request.user.attending_events.filter(id=event_id).exists():
                return Response({"error": "You are not attending this event"}, status=403)

        # ✅ If passed, fetch messages
        messages = Message.objects.filter(room=room).order_by("timestamp")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    room_name = request.data.get('room')
    message = request.data.get('message')

    if not room_name or not message:
        return Response({'error': 'Room and message are required.'}, status=400)

    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found.'}, status=404)

    # Optional: access control like RoomMessageListView (reuse logic)
    if room_name.startswith("group_"):
        group_id = room_name.split("_")[1]
        if not request.user.joined_groups.filter(id=group_id).exists():
            return Response({'error': 'You are not a member of this group'}, status=403)

    elif room_name.startswith("event_"):
        event_id = room_name.split("_")[1]
        if not request.user.attending_events.filter(id=event_id).exists():
            return Response({'error': 'You are not attending this event'}, status=403)

    msg = Message.objects.create(room=room, sender=request.user, content=message)
    serializer = MessageSerializer(msg)
    return Response(serializer.data, status=201)
