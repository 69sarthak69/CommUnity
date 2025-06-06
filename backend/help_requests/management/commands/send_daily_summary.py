# your_app/management/commands/send_daily_summary.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta

from help_requests.models import HelpRequest, CommunityPost

class Command(BaseCommand):
    help = "Send daily summary of new help requests and community posts to all users"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        now = timezone.now()
        yesterday = now - timedelta(days=1)

        users = User.objects.filter(email__isnull=False).exclude(email="")
        for user in users:
            # Fetch help requests and posts from last 24 hours
            new_help_requests = HelpRequest.objects.filter(created_at__gte=yesterday)
            new_posts = CommunityPost.objects.filter(created_at__gte=yesterday)

            # If nothing new, you can skip or still notify
            if not new_help_requests and not new_posts:
                continue

            help_request_lines = [
                f"- {req.title} ({req.get_category_display()}, {req.location})"
                for req in new_help_requests
            ]
            post_lines = [
                f"- {post.title} ({post.get_category_display()}, {post.location or 'N/A'})"
                for post in new_posts
            ]

            message = "Hello, here is your daily summary from CommunityHelp:\n\n"

            if help_request_lines:
                message += "New Help Requests:\n" + "\n".join(help_request_lines) + "\n\n"
            else:
                message += "No new help requests today.\n\n"

            if post_lines:
                message += "New Community Posts:\n" + "\n".join(post_lines) + "\n"
            else:
                message += "No new community posts today.\n"

            send_mail(
                "Your Daily CommunityHelp Summary",
                message,
                None,  # Uses DEFAULT_FROM_EMAIL
                [user.email],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS("Daily summary emails sent."))
