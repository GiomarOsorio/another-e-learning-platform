# users/forms.py
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
    SetPasswordForm,
    PasswordChangeForm,
)
from django.db.models import ImageField
from django.core.files.images import get_image_dimensions
from django.contrib.auth import password_validation
from .models import User
from django import forms
from PIL import Image

from django.contrib.auth import authenticate


class CreationFrom(UserCreationForm):
    password1 = forms.CharField(
        label=("password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_texts(),
    )
    password2 = forms.CharField(
        label=("password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "country",
        ]

    field_order = [
        "email",
        "password1",
        "password2",
        "first_name",
        "last_name",
        "country",
    ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                ("Passwords don't match"), code="password_mismatch",
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_texts(),
    )


class PasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_texts(),
    )


class ChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "avatar",
            "first_name",
            "last_name",
            "country",
            "university",
            "academic_degree",
            "linkedin",
            "github",
            "twitter",
        ]

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar", False)

        if type(avatar).__name__ == "ImageFieldFile":
            return avatar
        elif avatar and type(avatar).__name__ == "InMemoryUploadedFile":
            if avatar.size > 1 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 1MB )")
            _, sub = avatar.content_type.split("/")
            if not sub in ["jpeg", "pjpeg", "png"]:
                raise forms.ValidationError(u"Please use a JPEG, or PNG image.")
            return avatar
        else:
            raise forms.ValidationError("Couldn't read uploaded image")

    def save(self):
        user = super(ChangeForm, self).save()

        avatar = Image.open(user.avatar)

        width, height = avatar.size
        cropped_avatar = avatar
        if height < width:
            cropped_avatar = avatar.crop(
                (0.5 * (width - height), 0, 0.5 * (width + height), height)
            )
        elif height > width:
            cropped_avatar = avatar.crop(
                (0, 0.5 * (height - width), width, 0.5 * (height + width))
            )

        resized_image = cropped_avatar.resize((300, 300), Image.ANTIALIAS)
        resized_image.save(user.avatar.path)

        return user


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(request, *args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(email=username)
                except:
                    user_temp = None
                if user_temp is not None and user_temp.check_password(password):
                    self.confirm_login_allowed(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages["invalid_login"],
                        code="invalid_login",
                        params={"username": self.username_field.verbose_name},
                    )

        return self.cleaned_data

    def is_inactive(self):
        if self.user_cache is not None:
            user_temp = self.user_cache
        else:
            username = self.cleaned_data.get("username")
            try:
                user_temp = User.objects.get(email=username)
            except:
                user_temp = None
        return not user_temp.is_active if user_temp is not None else None
