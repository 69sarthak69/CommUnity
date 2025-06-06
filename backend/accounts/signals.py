# accounts/signals.py
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings

def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = f"Your password reset token is: {reset_password_token.key}\n" \
                              f"Or use this link: http://localhost:5173/reset-password/{reset_password_token.user.pk}/{reset_password_token.key}/"

    send_mail(
        # title:
        "Password Reset for CommunityHelp",
        # message:
        email_plaintext_message,
        # from:
        settings.DEFAULT_FROM_EMAIL,
        # to:
        [reset_password_token.user.email]
    )

reset_password_token_created.connect(password_reset_token_created)
