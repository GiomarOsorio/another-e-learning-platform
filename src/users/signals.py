# Signals that fires when a user logs in and logs out

from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import LoggedInUser


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    logged_in_user_instance, _ = LoggedInUser.objects.get_or_create(
        user=kwargs.get("user")
    )
    logged_in_user_instance.session_key = request.session.session_key
    logged_in_user_instance.save()


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get("user")).delete()

