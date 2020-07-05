from django import forms
from django.contrib import admin
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label=_("password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("password confirmation"), widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "country")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            'using <a href="../password/">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "avatar",
            "first_name",
            "last_name",
            "country",
            "university",
            "academic_degree",
            "linkedin",
            "github",
            "active",
            "teacher",
            "staff",
            "admin",
            "groups",
            "user_permissions",
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar", False)
        if avatar:
            if len(avatar) > 1 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 1MB )")
            return avatar
            _, sub = avatar.content_type.split("/")
            if not sub in ["jpeg", "pjpeg", "png"]:
                raise forms.ValidationError(u"Please use a JPEG, or PNG image.")
        else:
            raise forms.ValidationError("Couldn't read uploaded image")


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        "email",
        "first_name",
        "last_name",
        "country",
        "admin",
        "teacher",
        "last_login",
    )
    list_filter = ("admin", "date_joined", "last_login", "country")
    fieldsets = (
        ("User info", {"fields": ("email", "password", "avatar", "date_joined")}),
        ("Personal info", {"fields": ("first_name", "last_name", "country")}),
        ("Profesional info", {"fields": ("university", "academic_degree")}),
        ("Social Media", {"fields": ("twitter", "linkedin", "github")}),
        ("Permissions", {"fields": ("active", "teacher", "staff", "admin")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "avatar",
                    "first_name",
                    "last_name",
                    "country",
                ),
            },
        ),
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "country",
        "university",
        "academic_degree",
        "twitter",
        "linkedin",
        "github",
        "date_joined",
        "last_login",
        "admin",
        "teacher",
        "active",
    )
    ordering = ("email", "first_name", "last_name", "country", "admin", "last_login")
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
