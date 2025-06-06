from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from help_requests.models import HelpRequest, CommunityPost

import math

# Haversine formula for distance (copy from your views)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class Command(BaseCommand):
    help = "Send daily digest of new help requests and community posts"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        radius_km = 50  # Only show requests within 30km

        users = User.objects.filter(is_active=True)
        for user in users:
            if not user.email:
                continue

            # If user has lat/lng (optional: check profile model, adapt as needed)
            user_lat = getattr(user, 'latitude', None)
            user_lng = getattr(user, 'longitude', None)

            # Filter new requests
            help_qs = HelpRequest.objects.filter(created_at__gte=yesterday)
            if user_lat is not None and user_lng is not None:
                help_qs = [
                    r for r in help_qs
                    if r.latitude and r.longitude and haversine(user_lat, user_lng, r.latitude, r.longitude) <= radius_km
                ]
            else:
                help_qs = list(help_qs)

            # Filter new posts (no location filter here, but you can add it)
            post_qs = CommunityPost.objects.filter(created_at__gte=yesterday)

            # Build email content
            msg = f"Hello {user.get_full_name() or user.username},\n\n"
            msg += "Here are new help requests near you:\n"
            if help_qs:
                for req in help_qs:
                    msg += f"- {req.title} ({req.location})\n"
            else:
                msg += "No new help requests near you today.\n"

            msg += "\nCommunity Posts:\n"
            if post_qs:
                for post in post_qs:
                    msg += f"- {post.title}\n"
            else:
                msg += "No new posts today.\n"

            msg += "\nSee more on your community app!"

            # Send mail
            send_mail(
                subject="Your Daily Community Digest",
                message=msg,
                from_email="noreply@yourcommunity.com",
                recipient_list=[user.email],
                fail_silently=False,
            )
            print(f"Sent digest to {user.email}")

        self.stdout.write(self.style.SUCCESS("All daily digests sent!"))
