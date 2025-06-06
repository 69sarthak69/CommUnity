
import math
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import HelpRequest, HelpResponse, Comment, HelpApplication
from .serializers import HelpRequestSerializer, HelpResponseSerializer, CommentSerializer, HelpApplicationSerializer
# , NotificationSerializer
import logging
from django.http import JsonResponse
from .models import CommunityPost
from .serializers import CommunityPostSerializer
from rest_framework.permissions import IsAuthenticated
from notifications.utils import create_notification
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from rest_framework import serializers
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .realtime import broadcast_new_help_request
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


from .realtime import broadcast_new_community_post  

logger = logging.getLogger(__name__)




def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points 
    on the Earth surface specified in decimal degrees of latitude and longitude.
    """
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def help_requests(request):
    try:
        user_lat = float(request.GET.get('lat'))
        user_lng = float(request.GET.get('lng'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid or missing lat/lng'}, status=400)

    radius_km = 5
    requests = HelpRequest.objects.all()
    results = []

    for req in requests:
        if req.latitude is not None and req.longitude is not None:
            distance = haversine(user_lat, user_lng, req.latitude, req.longitude)
            if distance <= radius_km:
                # Convert applicants to list of ids for frontend
                applicants = list(req.applicants.values_list('id', flat=True)) if hasattr(req, 'applicants') else []
                results.append({
                    "id": req.id,
                    "title": req.title,
                    "description": req.description,
                    "category": getattr(req, 'category', ''),
                    "location": getattr(req, 'location', ''),
                    "status": getattr(req, 'status', ''),
                    "is_emergency": getattr(req, 'is_emergency', False),
                    "created_at": req.created_at.isoformat() if hasattr(req, 'created_at') else "",
                    "created_by": req.created_by.id if hasattr(req, 'created_by') else None,
                    "applicants": applicants,
                    "latitude": req.latitude,
                    "longitude": req.longitude,
                    "distance": round(distance, 2)
                })

    return JsonResponse(results, safe=False)




# Help Request Views
class HelpRequestListCreateView(generics.ListCreateAPIView):
    """List all help requests or create a new one, with nearby requests first"""
    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius_km = 50  # Set your "nearby" radius

        help_requests_with_distance = []
        if lat and lng:
            try:
                user_lat = float(lat)
                user_lng = float(lng)
                for req in queryset:
                    # Only calculate if req has lat/lng
                    if req.latitude is not None and req.longitude is not None:
                        distance = haversine(user_lat, user_lng, req.latitude, req.longitude)
                    else:
                        distance = None
                    help_requests_with_distance.append((req, distance))
            except ValueError:
                # If invalid lat/lng, just return without distances
                for req in queryset:
                    help_requests_with_distance.append((req, None))
        else:
            for req in queryset:
                help_requests_with_distance.append((req, None))

        # Sort: nearby first, then the rest
        # Sorts by: (in-range first, then by distance, then by is_emergency, then by date)
        help_requests_with_distance.sort(
            key=lambda x: (
                0 if (x[1] is not None and x[1] <= radius_km) else 1,
                x[1] if x[1] is not None else float('inf'),
                -int(getattr(x[0], 'is_emergency', False)),
                -x[0].created_at.timestamp() if x[0].created_at else 0,
            )
        )

        # Serialize with distance
        serializer = self.get_serializer(
            [x[0] for x in help_requests_with_distance], many=True
        )
        data = serializer.data

        # Add "distance" to each response
        for i, (req, distance) in enumerate(help_requests_with_distance):
            data[i]['distance'] = round(distance, 2) if distance is not None else None
            data[i]['is_nearby'] = bool(distance is not None and distance <= radius_km)

        return Response(data)

    def perform_create(self, serializer):
        help_request = serializer.save(created_by=self.request.user)
        from .realtime import broadcast_new_help_request
        from notifications.utils import create_notification
        from django.contrib.auth import get_user_model
        print("✅ Task created. Emergency status:", help_request.is_emergency)
        if help_request.is_emergency:
            print("🚨 Creating emergency notifications...")
            User = get_user_model()
            for user in User.objects.exclude(id=self.request.user.id):
                create_notification(
                    user=user,
                    message=f"🚨 Emergency Help Needed: '{help_request.title}'",
                    notif_type="emergency",
                    related_object_id=str(help_request.id)
                )
        broadcast_new_help_request(help_request)



class HelpRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific help request"""
    queryset = HelpRequest.objects.all()
    serializer_class = HelpRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Limit access to only requests created by the user"""
        return HelpRequest.objects.filter(created_by=self.request.user)
    

from .models import HelpRequest, HelpApplication

class ApplyToHelpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            help_request = HelpRequest.objects.get(pk=pk)
        except HelpRequest.DoesNotExist:
            return Response({'error': 'Help request not found'}, status=404)

        # Check if already applied
        if HelpApplication.objects.filter(user=request.user, help_request=help_request).exists():
            return Response({'message': 'Already applied'}, status=200)

        # Get the letter from frontend
        letter = request.data.get("letter", "")

        # Save the letter in HelpApplication model
        HelpApplication.objects.create(
            user=request.user,
            help_request=help_request,
            letter=letter
        )

        # Still add to applicants list for legacy logic
        help_request.applicants.add(request.user)

        # Notify the creator
        if help_request.created_by and help_request.created_by != request.user:
            applicant_name = request.user.first_name or request.user.email
            create_notification(
                user=help_request.created_by,
                message=f"{applicant_name} applied to your help request: '{help_request.title}'",
                notif_type="application",
                related_object_id=str(help_request.id)
            )

        return Response({'message': 'Successfully applied with letter'}, status=200)


# Help Response Views
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

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)
        # Real-time broadcast:
        broadcast_new_community_post(post)


class CommunityPostListView(generics.ListAPIView):
    queryset = CommunityPost.objects.all().order_by('-created_at')  # newest first
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class HelpApplicationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        help_request = HelpRequest.objects.get(pk=pk)
        if help_request.created_by != request.user:
            return Response({'detail': 'Unauthorized'}, status=403)

        applications = HelpApplication.objects.filter(help_request=help_request).order_by('-created_at')
        data = HelpApplicationSerializer(applications, many=True).data
        return Response(data)

class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        if post_id:
            # Only root comments (parent=None) for the post
            return Comment.objects.filter(post_id=post_id, parent__isnull=True).order_by('created_at')
        return Comment.objects.none()  # Or all comments if you want

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_applicant(request, application_id):
    try:
        application = HelpApplication.objects.get(id=application_id)
    except HelpApplication.DoesNotExist:
        return Response({'detail': 'Application not found'}, status=HTTP_404_NOT_FOUND)

    if application.help_request.created_by != request.user:
        return Response({'detail': 'Unauthorized'}, status=403)
    

    if application.status != 'pending':
        return Response({'detail': 'This application was already processed.'}, status=400)

    application.status = 'approved'
    application.save()
    print("Approving application, preparing to send email...")  
    # Prepare and send approval email
    subject = f"🎉 Your Application for '{application.help_request.title}' Was Approved!"
    to_email = application.user.email
    context = {
        'user': application.user,
        'help_request': application.help_request,
    }
    text_content = f"Congratulations {application.user.username}, your application for '{application.help_request.title}' was approved!"
    html_content = render_to_string('emails/application_approved.html', context)
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [to_email])
    email.attach_alternative(html_content, "text/html")
    print("SENDING EMAIL NOW to", to_email)
    email.send()
    print("EMAIL SENT SUCCESSFULLY") 

    # Notify the applicant
    create_notification(
        user=application.user,
        message=f"🎉 Your application for '{application.help_request.title}' was approved!",
        notif_type="application_result",
        related_object_id=str(application.help_request.id)
    )

    return Response({'message': 'Applicant approved'}, status=HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_applicant(request, application_id):
    try:
        application = HelpApplication.objects.get(id=application_id)
    except HelpApplication.DoesNotExist:
        return Response({'detail': 'Application not found'}, status=HTTP_404_NOT_FOUND)

    if application.help_request.created_by != request.user:
        return Response({'detail': 'Unauthorized'}, status=403)
    
    if application.status != 'pending':
        return Response({'detail': 'This application was already processed.'}, status=400)

    application.status = 'rejected'
    application.save()
    print("Rejjecting application, preparing to send email...") 
    # Prepare and send rejection email
    subject = f"❌ Your Application for '{application.help_request.title}' Was Rejected"
    to_email = application.user.email
    context = {
        'user': application.user,
        'help_request': application.help_request,
    }
    text_content = f"Hello {application.user.username}, your application for '{application.help_request.title}' was rejected. Thank you for volunteering!"
    html_content = render_to_string('emails/application_rejected.html', context)
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [to_email])
    email.attach_alternative(html_content, "text/html")
    print("SENDING EMAIL NOW to", to_email)
    email.send()
    print("EMAIL SENT SUCCESSFULLY") 

    # Notify the applicant
    create_notification(
        user=application.user,
        message=f"❌ Your application for '{application.help_request.title}' was rejected.",
        notif_type="application_result",
        related_object_id=str(application.help_request.id)
    )

    return Response({'message': 'Applicant rejected'}, status=HTTP_200_OK)



class HelpApplicationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        help_request = HelpRequest.objects.get(pk=pk)
        if help_request.created_by != request.user:
            return Response({'detail': 'Unauthorized'}, status=403)

        applications = HelpApplication.objects.filter(help_request=help_request).order_by('-created_at')
        data = HelpApplicationSerializer(applications, many=True).data
        return Response(data)

class MyHelpApplicationsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        apps = HelpApplication.objects.filter(user=request.user).select_related('help_request').order_by('-created_at')
        serializer = HelpApplicationSerializer(apps, many=True)
        return Response(serializer.data)


def broadcast_help_request_update(help_request_id, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"help_request_{help_request_id}",
        {
            "type": "send_update",
            "data": data,
        }
    )