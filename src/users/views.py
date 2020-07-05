from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView, RedirectView
from .forms import (
    CreationFrom,
    ChangeForm,
    LoginForm,
    SetPasswordForm,
    PasswordChangeForm,
)
from .models import User, LoggedInUser
from .tokens import account_activation_token

# from django.contrib.auth.forms import SetPasswordForm
from django.http.response import HttpResponse
import json


class UsersViewFunctions(object):
    def get_user_instance(self, email=None):
        user = None
        if email is None:
            id = self.kwargs.get("id")
            if id is not None:
                try:
                    user = User.objects.get(id=id)
                except User.DoesNotExist:
                    user = None
        else:
            try:
                user = user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
        return user

    def get_user_instance_or_404(self, email=None):
        user = None
        if email is None:
            id = self.kwargs.get("id")
            if id is not None:
                user = get_object_or_404(User, id=id)
        else:
            user = get_object_or_404(User, email=email)
        return user

    def get_user_session(self, user_instance):
        try:
            return LoggedInUser.objects.get(user=user_instance)
        except LoggedInUser.DoesNotExist:
            return None

    def send_registration_verification_email(self, user):
        mail_subject = "Activate your account."
        message = render_to_string(
            "email/user_activation_email.html",
            {
                "user": user,
                "domain": get_current_site(self.request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

    def send_reset_password_email(self, user):
        mail_subject = "Reset your password account."
        message = render_to_string(
            "email/user_reset_password_email.html",
            {
                "user": user,
                "domain": get_current_site(self.request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

    def user_validate_token(self, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user_instance = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user_instance = None
        if user_instance is not None and account_activation_token.check_token(
            user_instance, token
        ):
            return user_instance
        else:
            return None

    def user_activate_email(self, uidb64, token):
        user_instance = self.user_validate_token(uidb64, token)
        if user_instance is not None:
            user_instance.active = True
            user_instance.save()
            return True
        return False


class UserRegisterView(UsersViewFunctions, View):
    template_name = "users/userRegisterView.html"

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, {"user_creation_form": CreationFrom()}
        )

    def post(self, request, *args, **kwargs):
        data_type = request.POST.get("type")
        data = request.POST.get("data")
        if data_type is not None and data is not None:
            user_instance = self.get_user_instance(email=data)
            if user_instance is None:
                return HttpResponse(json.dumps({"valid": True,}))
            else:
                return HttpResponse(json.dumps({"valid": False,}))

        user_form = CreationFrom(request.POST)
        if user_form.is_valid():
            user_instance = user_form.save(commit=False)
            user_instance.save()
            self.send_registration_verification_email(user_instance)
            messages.success(
                request,
                "You have successfully registered. Please confirm your email address to complete the registration",
            )
            return redirect("pages:login-page")
        else:
            messages.error(request, "Please check one of the following fields")
            return render(
                request, self.template_name, {"user_creation_form": user_form}
            )


class UserActivationEmailView(UsersViewFunctions, View):
    template_name = "users/userRegisterView.html"

    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "You must logout before verifying the email")
            return redirect("pages:home-page")
        if uidb64 is None or token is None:
            messages.error(request, "Activation link is invalid!")
            return redirect("pages:home-page")
        if self.user_activate_email(uidb64, token):
            messages.success(
                request,
                "Thank you for your email confirmation. Now you can login your account.",
            )
        else:
            messages.error(request, "Activation link is invalid!")
        return redirect("pages:home-page")

    def post(self, request, *args, **kwargs):
        return redirect("pages:home-page")


class UserReSendActivationEmailView(UsersViewFunctions, View):
    def post(self, request, username=None, *args, **kwargs):

        if username is None:
            messages.error(request, "We need email to send validation link.")
            return redirect("pages:login-page")
        user_instance = self.get_user_instance_or_404(email=username)

        if user_instance is None:
            messages.error(request, "You must provide an email.")
            return redirect("pages:login-page")

        self.send_registration_verification_email(user_instance)
        messages.success(
            request,
            "Validation email successfully send. Please confirm your email address to complete the registration",
        )
        return redirect("pages:home-page")


class UserDetailView(View):
    template_name = "users/userDetailView.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        return render(request, self.template_name, {})


class UserUpdateView(UsersViewFunctions, View):
    template_name = "users/userUpdateView.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        user_instance = request.user
        if not user_instance is None:
            return render(
                request,
                self.template_name,
                {
                    "user_form": ChangeForm(instance=user_instance),
                    "change_password_form": PasswordChangeForm(user_instance),
                },
            )
        messages.error(request, "An error has occurred try again later.")
        return redirect("pages:home-page")

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:login-page")
        user_instance = request.user
        if user_instance is None:
            messages.error(request, "An error has occurred try again later.")
            return redirect("pages:home-page")
        user_form = ChangeForm(request.POST, request.FILES, instance=user_instance)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "You have successfully update your profile")
            return redirect("pages:profile-page")
        messages.error(request, "Please check one of the following fields")
        return render(request, self.template_name, {"user_form": user_form})


class UserChangePasswordView(View):
    template_name = "users/userChangePasswordView.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:home-page")
        return render(
            request,
            self.template_name,
            {"change_password_form": PasswordChangeForm(request.user)},
        )

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pages:home-page")
        change_password_form = PasswordChangeForm(request.user, request.POST)
        if change_password_form.is_valid():
            update_session_auth_hash(request, change_password_form.save())
            messages.success(request, "Your password was successfully updated!")
            return redirect("pages:update-page")
        else:
            messages.error(
                request, "The data entered has not been correct, please check"
            )
            return render(
                request,
                self.template_name,
                {"change_password_form": change_password_form},
            )


class UserForgotPasswordView(UsersViewFunctions, View):
    template_name = "users/userForgotPassword.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        user = self.get_user_instance(email=username)
        if user is not None:
            self.send_reset_password_email(user)
            messages.success(
                request,
                "We've emailed you instrctions for setting your password, if an account exists with the email you entered. You should receive them shortly.if you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder",
            )
            messages.success(
                request, "",
            )
            return redirect("pages:home-page")


class UserResetForgotPasswordView(UsersViewFunctions, View):
    template_name = "users/userResetPasswordView.html"

    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        if uidb64 is None or token is None:
            messages.error(request, "Activation link is invalid!")
            return redirect("pages:home-page")
        user_instance = self.user_validate_token(uidb64, token)
        if user_instance is None:
            messages.error(request, "Activation link is invalid!")
            return redirect("pages:home-page")
        return render(
            request,
            self.template_name,
            {
                "reset_password_form": SetPasswordForm(user=user_instance),
                "uidb64": uidb64,
                "token": token,
            },
        )

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "You must logout before using this link.")
            return redirect("pages:home-page")
        if uidb64 is None or token is None:
            messages.error(request, "Reset password link is invalid!")
            return redirect("pages:home-page")
        user_instance = self.user_validate_token(uidb64, token)
        if user_instance is not None:
            reset_password_form = SetPasswordForm(user_instance, request.POST)
            if reset_password_form.is_valid():
                update_session_auth_hash(request, reset_password_form.save())
                messages.success(
                    request, "Your password has been set!, now you can login.",
                )
                return redirect("pages:login-page")
            else:
                messages.error(
                    request, "The data entered has not been correct, please check"
                )
                return render(
                    request,
                    self.template_name,
                    {
                        "reset_password_form": reset_password_form,
                        "uidb64": uidb64,
                        "token": token,
                    },
                )
        messages.error(request, "Can't process this request.")
        return redirect("pages:home-page")


class UserLoginView(UsersViewFunctions, View):
    template_name = "users/userLoginView.html"
    template_account_not_activated_name = "users/userNoActiveEmail.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("pages:home-page")
        return render(request, self.template_name, {"user_login_form": LoginForm()})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("pages:home-page")
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user_instance = login_form.get_user()
            session = self.get_user_session(user_instance)
            if session is not None:
                messages.warning(request, "You already logged in.")
                return render(
                    request, self.template_name, {"user_login_form": LoginForm()}
                )
            login(request, user_instance)
            return redirect("pages:home-page")
        if login_form.is_inactive():
            return render(
                request,
                self.template_account_not_activated_name,
                {"username": request.POST["username"]},
            )
        messages.error(request, "The data entered is not correct, please try again.")
        return render(request, self.template_name, {"user_login_form": login_form})


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect("pages:home-page")

    def post(self, request, *args, **kwargs):
        return redirect("pages:home-page")

