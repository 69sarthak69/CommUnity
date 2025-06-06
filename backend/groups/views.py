from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Group, GroupPost,GroupPostReaction, GroupActivity
from .serializers import GroupSerializer
from .serializers import GroupPostSerializer, GroupActivitySerializer
from .permissions import IsGroupAdmin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from chat.models import Room 

from rest_framework.parsers import MultiPartParser, FormParser



# List + Create Group (used on groups page)
class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        group = serializer.save(created_by=self.request.user)
        group.members.add(self.request.user)  # Add creator as member

        room_name = f"group_{group.id}"
        Room.objects.get_or_create(name=room_name)


# Join Group (POST /api/groups/<id>/join/)
class GroupJoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user in group.members.all():
            return Response({'detail': 'Already a member.'}, status=status.HTTP_200_OK)

        group.members.add(request.user)
        # Log activity
        GroupActivity.objects.create(
            group=group,
            user=request.user,
            activity_type='joined'
        )
        return Response({'detail': 'Joined successfully.'}, status=status.HTTP_200_OK)


# Get details of a single group (GET /api/groups/<id>/)
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def group_detail(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = GroupSerializer(group)
    return Response(serializer.data)


# Full CRUD for admins (used in admin panel or edit/delete logic)
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsGroupAdmin()]
        return [IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        group = serializer.save(created_by=self.request.user)
        group.members.add(self.request.user)

class GroupPostListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.request.query_params.get('group')
        return GroupPost.objects.filter(group_id=group_id).order_by('-created_at')

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        GroupActivity.objects.create(
        group=post.group,
        user=post.author,
        activity_type='post',
        post=post
    )


class GroupPostListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]   # <-- Add this!

    def get_queryset(self):
        group_id = self.request.query_params.get('group')
        return GroupPost.objects.filter(group_id=group_id).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_group_post(request, pk):
    post = GroupPost.objects.get(pk=pk)
    reaction, created = GroupPostReaction.objects.get_or_create(
        post=post, user=request.user, reaction_type='like'
    )
    if not created:
        reaction.delete()
        return Response({'liked': False}, status=status.HTTP_200_OK)
    return Response({'liked': True}, status=status.HTTP_200_OK)



class GroupActivityFeedView(generics.ListAPIView):
    serializer_class = GroupActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        group_id = self.request.query_params.get('group')
        return GroupActivity.objects.filter(group_id=group_id).order_by('-timestamp')[:20]
