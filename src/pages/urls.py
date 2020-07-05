from django.urls import path, re_path
from .views import (
    HomeView,
    SearchView,
)
from django.conf import settings
from django.conf.urls.static import static
from users.views import (
    UserRegisterView,
    UserActivationEmailView,
    UserReSendActivationEmailView,
    UserLoginView,
    UserDetailView,
    UserLogoutView,
    UserChangePasswordView,
    UserForgotPasswordView,
    UserResetForgotPasswordView,
    UserUpdateView,
)

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home-page"),
    path("search", SearchView.as_view(), name="search-page"),
    path("login/", UserLoginView.as_view(), name="login-page"),
    path("register/", UserRegisterView.as_view(), name="register-page"),
    re_path(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        UserActivationEmailView.as_view(),
        name="activate-email-link",
    ),
    path(
        "re-send-activation-link/<str:username>",
        UserReSendActivationEmailView.as_view(),
        name="re-send-activate-email-link",
    ),
    path("profile/", UserDetailView.as_view(), name="profile-page"),
    path("update/", UserUpdateView.as_view(), name="update-page"),
    path("logout/", UserLogoutView.as_view(), name="logout-page"),
    path(
        "changepassword/", UserChangePasswordView.as_view(), name="changepassword-page"
    ),
    path(
        "reset_password/", UserForgotPasswordView.as_view(), name="send-reset-password-page",
    ),
    re_path(
        r"^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        UserResetForgotPasswordView.as_view(),
        name="reset-password-page",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

