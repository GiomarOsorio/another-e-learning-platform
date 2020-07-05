from django.contrib.auth.forms import AuthenticationForm
from .forms import CreationFrom


def SignIn_SignUp(request):
    context = {}
    if not request.user.is_authenticated:
        context["form_signin"] = AuthenticationForm()
        context["form_signup"] = CreationFrom()
    return context
