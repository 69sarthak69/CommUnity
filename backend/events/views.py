from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Event
from .serializers import EventSerializer
from chat.models import Room 

# List + Create Events
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        event = serializer.save(created_by=self.request.user)
        event.attendees.add(self.request.user)  # Auto-join creator
        room_name = f"event_{event.id}"
        Room.objects.get_or_create(name=room_name)



# Get event detail
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EventSerializer(event)
    return Response(serializer.data)


# RSVP (Join) Event
class EventJoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=404)

        if request.user in event.attendees.all():  
            return Response({'message': 'Already joined'}, status=200)

        event.attendees.add(request.user)  
        return Response({'message': 'Joined event successfully'}, status=200)



# Cancel RSVP
class CancelRSVPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=404)

        if request.user in event.members.all():
            event.members.remove(request.user)
            return Response({'message': 'RSVP cancelled'}, status=200)

        return Response({'message': 'You were not attending'}, status=400)


# Update/Delete (Only by creator)
class EventUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        if event.created_by != request.user:
            return Response({'error': 'Not allowed'}, status=403)
        return super().delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        event = self.get_object()
        if event.created_by != request.user:
            return Response({'error': 'Not allowed'}, status=403)
        return super().put(request, *args, **kwargs)
