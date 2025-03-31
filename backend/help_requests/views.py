from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import HelpRequest, HelpResponse
from .serializers import HelpRequestSerializer, HelpResponseSerializer
# , NotificationSerializer
import logging
from django.http import JsonResponse
from .models import CommunityPost
from .serializers import CommunityPostSerializer
from rest_framework.permissions import IsAuthenticated
from notifications.utils import create_notification
from django.contrib.auth import get_user_model
from accounts.models import CustomUser



logger = logging.getLogger(__name__)

# 🚀 Help Request Views
class HelpRequestListCreateView(generics.ListCreateAPIView):
    """List all help requests or create a new one"""
    queryset = HelpRequest.objects.all().order_by('-is_emergency', '-created_at')  # Emergency requests come first
    serializer_class = HelpRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        help_request = serializer.save(created_by=self.request.user)

        # ✅ Create notification for emergency
        if help_request.is_emergency:
            all_users = CustomUser.objects.exclude(id=self.request.user.id)
            for user in all_users:
                create_notification(
                    user=user,
                    message=f"🚨 Emergency help requested: {help_request.title}",
                    notif_type="emergency",
                    related_object_id=str(help_request.id)
                )

class HelpRequestCreateView(generics.ListCreateAPIView):
    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
         help_request = serializer.save(created_by=self.request.user)

         print("✅ Task created. Emergency status:", help_request.is_emergency)

         # ✅ Create emergency notifications
         if help_request.is_emergency:
            print("🚨 Creating emergency notifications...")
            for user in User.objects.exclude(id=self.request.user.id):
                create_notification(
                    user=user,
                    message=f"🚨 Emergency Help Needed: '{help_request.title}'",
                    notif_type="emergency",
                    related_object_id=str(help_request.id)
                )


class HelpRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific help request"""
    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Limit access to only requests created by the user"""
        return HelpRequest.objects.filter(created_by=self.request.user)
    

class ApplyToHelpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            help_request = HelpRequest.objects.get(pk=pk)
        except HelpRequest.DoesNotExist:
            return Response({'error': 'Help request not found'}, status=404)

        if request.user in help_request.applicants.all():
            return Response({'message': 'You have already applied'}, status=200)

        help_request.applicants.add(request.user)

        # ✅ Notify the creator of the task
        if help_request.created_by and help_request.created_by != request.user:
            applicant_name = request.user.first_name or request.user.email
            create_notification(
                user=help_request.created_by,
                message=f"{applicant_name} applied to your help request: '{help_request.title}'",
                notif_type="application",
                related_object_id=str(help_request.id)
            )

        return Response({'message': 'Successfully applied to help'}, status=200)


# 🚀 Help Response Views
class HelpResponseCreateView(generics.CreateAPIView):
    """Create a response to a help request"""
    serializer_class = HelpResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Ensure helper is set to the current user"""
        serializer.save(helper=self.request.user)

class HelpResponseListView(generics.ListAPIView):
    """List all responses for a given help request"""
    serializer_class = HelpResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter responses by the request ID"""
        request_id = self.kwargs['request_id']
        return HelpResponse.objects.filter(request=request_id)

class CommunityPostCreateView(generics.CreateAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommunityPostListView(generics.ListAPIView):
    queryset = CommunityPost.objects.all().order_by('-created_at')  # newest first
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# class NotificationListView(generics.ListAPIView):
#     """List all notifications for the logged-in user"""
#     serializer_class = NotificationSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         """Fetch notifications for the logged-in user"""
#         user = self.request.user
#         queryset = Notification.objects.filter(user=user).order_by('-created_at')

#         # ✅ Print Debugging Info
#         logger.debug(f"User {user} requested notifications: {queryset.values()}")

#         return queryset


# class MarkNotificationAsReadView(APIView):
#     """Mark a notification as read"""
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, notification_id):
#         """Mark notification as read"""
#         try:
#             notification = Notification.objects.get(id=notification_id, user=request.user)
#             notification.is_read = True
#             notification.save()
#             return Response({"message": "Notification marked as read"})
#         except Notification.DoesNotExist:
#             return Response({"error": "Notification not found"}, status=404)




# class MarkAllNotificationsAsReadView(APIView):
#     """Mark all notifications as read for the logged-in user"""
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         """Mark all notifications as read"""
#         notifications = Notification.objects.filter(user=request.user, is_read=False)
#         count = notifications.update(is_read=True)
#         return Response({"message": f"{count} notifications marked as read."})



