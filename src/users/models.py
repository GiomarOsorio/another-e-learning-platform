from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from django.db import models

# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Creates and saves a User with the given email, first_name,
        last_name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        if not first_name:
            raise ValueError("Users must have an first name")

        if not last_name:
            raise ValueError("Users must have an last name")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        print(user)
        return user

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("teacher", False)
        extra_fields.setdefault("admin", False)
        return self._create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )

    def create_teacheruser(
        self, email, first_name, last_name, password, **extra_fields
    ):
        extra_fields.setdefault("teacher", True)
        extra_fields.setdefault("staff", False)
        extra_fields.setdefault("admin", False)
        return self._create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )

    def create_staffuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("teacher", False)
        extra_fields.setdefault("staff", True)
        extra_fields.setdefault("admin", False)
        return self._create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("teacher", False)
        extra_fields.setdefault("staff", True)
        extra_fields.setdefault("admin", True)
        return self._create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    """
    An custom user class implementing a part of featured User model with 
    admin-compliant permissions.
    Email, password, first and las name are requiered. Other fields are optional.
    """

    COUNTRY_CHOICES = [
        ("AF", "Afghanistan"),
        ("AL", "Albania"),
        ("DZ", "Algeria"),
        ("AX", "Aland Islands"),
        ("AS", "American Samoa"),
        ("AI", "Anguilla"),
        ("AD", "Andorra"),
        ("AO", "Angola"),
        ("AN", "Antilles - Netherlands"),
        ("AG", "Antigua and Barbuda"),
        ("AQ", "Antarctica"),
        ("AR", "Argentina"),
        ("AM", "Armenia"),
        ("AU", "Australia"),
        ("AT", "Austria"),
        ("AW", "Aruba"),
        ("AZ", "Azerbaijan"),
        ("BA", "Bosnia and Herzegovina"),
        ("BB", "Barbados"),
        ("BD", "Bangladesh"),
        ("BE", "Belgium"),
        ("BF", "Burkina Faso"),
        ("BG", "Bulgaria"),
        ("BH", "Bahrain"),
        ("BI", "Burundi"),
        ("BJ", "Benin"),
        ("BM", "Bermuda"),
        ("BN", "Brunei Darussalam"),
        ("BO", "Bolivia"),
        ("BR", "Brazil"),
        ("BS", "Bahamas"),
        ("BT", "Bhutan"),
        ("BV", "Bouvet Island"),
        ("BW", "Botswana"),
        ("BV", "Belarus"),
        ("BZ", "Belize"),
        ("KH", "Cambodia"),
        ("CM", "Cameroon"),
        ("CA", "Canada"),
        ("CV", "Cape Verde"),
        ("CF", "Central African Republic"),
        ("TD", "Chad"),
        ("CL", "Chile"),
        ("CN", "China"),
        ("CX", "Christmas Island"),
        ("CC", "Cocos (Keeling) Islands"),
        ("CO", "Colombia"),
        ("CI", "Cote D'Ivoire (Ivory Coast)"),
        ("CK", "Cook Islands"),
        ("CR", "Costa Rica"),
        ("HR", "Croatia (Hrvatska)"),
        ("CU", "Cuba"),
        ("CY", "Cyprus"),
        ("CZ", "Czech Republic"),
        ("CD", "Democratic Republic of the Congo"),
        ("DJ", "Djibouti"),
        ("DK", "Denmark"),
        ("DM", "Dominica"),
        ("DO", "Dominican Republic"),
        ("EC", "Ecuador"),
        ("EG", "Egypt"),
        ("SV", "El Salvador"),
        ("TP", "East Timor"),
        ("EE", "Estonia"),
        ("GQ", "Equatorial Guinea"),
        ("ER", "Eritrea"),
        ("ET", "Ethiopia"),
        ("FI", "Finland"),
        ("FJ", "Fiji"),
        ("FK", "Falkland Islands (Malvinas)"),
        ("FM", "Federated States of Micronesia"),
        ("FO", "Faroe Islands"),
        ("FR", "France"),
        ("FX", "France, Metropolitan"),
        ("GF", "French Guiana"),
        ("PF", "French Polynesia"),
        ("GA", "Gabon"),
        ("GM", "Gambia"),
        ("DE", "Germany"),
        ("GH", "Ghana"),
        ("GI", "Gibraltar"),
        ("GB", "Great Britain (UK)"),
        ("GD", "Grenada"),
        ("GE", "Georgia"),
        ("GR", "Greece"),
        ("GL", "Greenland"),
        ("GN", "Guinea"),
        ("GP", "Guadeloupe"),
        ("GS", "S. Georgia and S. Sandwich Islands"),
        ("GT", "Guatemala"),
        ("GU", "Guam"),
        ("GW", "Guinea-Bissau"),
        ("GY", "Guyana"),
        ("HK", "Hong Kong"),
        ("HM", "Heard Island and McDonald Islands"),
        ("HN", "Honduras"),
        ("HT", "Haiti"),
        ("HU", "Hungary"),
        ("ID", "Indonesia"),
        ("IE", "Ireland"),
        ("IL", "Israel"),
        ("IN", "India"),
        ("IO", "British Indian Ocean Territory"),
        ("IQ", "Iraq"),
        ("IR", "Iran"),
        ("IT", "Italy"),
        ("JM", "Jamaica"),
        ("JO", "Jordan"),
        ("JP", "Japan"),
        ("KE", "Kenya"),
        ("KG", "Kyrgyzstan"),
        ("KI", "Kiribati"),
        ("KM", "Comoros"),
        ("KN", "Saint Kitts and Nevis"),
        ("KP", "Korea (North)"),
        ("KR", "Korea (South)"),
        ("KW", "Kuwait"),
        ("KY", "Cayman Islands"),
        ("KZ", "Kazakhstan"),
        ("LA", "Laos"),
        ("LB", "Lebanon"),
        ("LC", "Saint Lucia"),
        ("LI", "Liechtenstein"),
        ("LK", "Sri Lanka"),
        ("LR", "Liberia"),
        ("LS", "Lesotho"),
        ("LT", "Lithuania"),
        ("LU", "Luxembourg"),
        ("LV", "Latvia"),
        ("LY", "Libya"),
        ("MK", "Macedonia"),
        ("MO", "Macao"),
        ("MG", "Madagascar"),
        ("MY", "Malaysia"),
        ("ML", "Mali"),
        ("MW", "Malawi"),
        ("MR", "Mauritania"),
        ("MH", "Marshall Islands"),
        ("MQ", "Martinique"),
        ("MU", "Mauritius"),
        ("YT", "Mayotte"),
        ("MT", "Malta"),
        ("MX", "Mexico"),
        ("MA", "Morocco"),
        ("MC", "Monaco"),
        ("MD", "Moldova"),
        ("MN", "Mongolia"),
        ("MM", "Myanmar"),
        ("MP", "Northern Mariana Islands"),
        ("MS", "Montserrat"),
        ("MV", "Maldives"),
        ("MZ", "Mozambique"),
        ("NA", "Namibia"),
        ("NC", "New Caledonia"),
        ("NE", "Niger"),
        ("NF", "Norfolk Island"),
        ("NG", "Nigeria"),
        ("NI", "Nicaragua"),
        ("NL", "Netherlands"),
        ("NO", "Norway"),
        ("NP", "Nepal"),
        ("NR", "Nauru"),
        ("NU", "Niue"),
        ("NZ", "New Zealand (Aotearoa)"),
        ("OM", "Oman"),
        ("PA", "Panama"),
        ("PE", "Peru"),
        ("PG", "Papua New Guinea"),
        ("PH", "Philippines"),
        ("PK", "Pakistan"),
        ("PL", "Poland"),
        ("PM", "Saint Pierre and Miquelon"),
        ("CS", "Serbia and Montenegro"),
        ("PN", "Pitcairn"),
        ("PR", "Puerto Rico"),
        ("PS", "Palestinian Territory"),
        ("PT", "Portugal"),
        ("PW", "Palau"),
        ("PY", "Paraguay"),
        ("QA", "Qatar"),
        ("RE", "Reunion"),
        ("RO", "Romania"),
        ("RU", "Russian Federation"),
        ("RW", "Rwanda"),
        ("SA", "Saudi Arabia"),
        ("WS", "Samoa"),
        ("SH", "Saint Helena"),
        ("VC", "Saint Vincent and the Grenadines"),
        ("SM", "San Marino"),
        ("ST", "Sao Tome and Principe"),
        ("SN", "Senegal"),
        ("SC", "Seychelles"),
        ("SL", "Sierra Leone"),
        ("SG", "Singapore"),
        ("SK", "Slovakia"),
        ("SI", "Slovenia"),
        ("SB", "Solomon Islands"),
        ("SO", "Somalia"),
        ("ZA", "South Africa"),
        ("ES", "Spain"),
        ("SD", "Sudan"),
        ("SR", "Suriname"),
        ("SJ", "Svalbard and Jan Mayen"),
        ("SE", "Sweden"),
        ("CH", "Switzerland"),
        ("SY", "Syria"),
        ("SU", "USSR (former)"),
        ("SZ", "Swaziland"),
        ("TW", "Taiwan"),
        ("TZ", "Tanzania"),
        ("TJ", "Tajikistan"),
        ("TH", "Thailand"),
        ("TL", "Timor-Leste"),
        ("TG", "Togo"),
        ("TK", "Tokelau"),
        ("TO", "Tonga"),
        ("TT", "Trinidad and Tobago"),
        ("TN", "Tunisia"),
        ("TR", "Turkey"),
        ("TM", "Turkmenistan"),
        ("TC", "Turks and Caicos Islands"),
        ("TV", "Tuvalu"),
        ("UA", "Ukraine"),
        ("UG", "Uganda"),
        ("AE", "United Arab Emirates"),
        ("UK", "United Kingdom"),
        ("US", "United States"),
        ("UM", "United States Minor Outlying Islands"),
        ("UY", "Uruguay"),
        ("UZ", "Uzbekistan"),
        ("VU", "Vanuatu"),
        ("VA", "Vatican City State"),
        ("VE", "Venezuela"),
        ("VG", "Virgin Islands (British)"),
        ("VI", "Virgin Islands (U.S.)"),
        ("VN", "Viet Nam"),
        ("WF", "Wallis and Futuna"),
        ("EH", "Western Sahara"),
        ("YE", "Yemen"),
        ("YU", "Yugoslavia (former)"),
        ("ZM", "Zambia"),
        ("ZR", "Zaire (former)"),
        ("ZW", "Zimbabwe"),
    ]
    # session = models.OneToOneField(
    #     Session, on_delete=models.CASCADE, blank=True, null=False, default=None
    # )
    email = models.EmailField(
        ("email address"),
        max_length=60,
        unique=True,
        help_text=("Required. 60 characters or fewer."),
        error_messages={"unique": ("A user with that email already exists."),},
    )
    password = models.CharField(("password"), max_length=128)
    avatar = models.ImageField(
        ("Avatar image"),
        default="default.png",
        upload_to="avatar_pics/",
        help_text=("maxime zise of 1MB. JPG ó PNG."),
        blank=True,
    )
    first_name = models.CharField(
        ("first name"), max_length=150, blank=False, null=False
    )
    last_name = models.CharField(("last name"), max_length=150, blank=False, null=False)
    country = models.CharField(
        ("country"),
        max_length=2,
        choices=COUNTRY_CHOICES,
        help_text=("select your country."),
        blank=False,
        null=False,
        error_messages={
            "blank": ("you must select your country."),
            "null": ("you must select your country."),
        },
    )
    university = models.CharField(
        ("university"),
        max_length=70,
        blank=True,
        null=False,
        error_messages={"null": ("you must enter your University."),},
    )
    academic_degree = models.CharField(
        ("academic degree"),
        max_length=70,
        blank=True,
        null=False,
        error_messages={"null": ("you must enter your academic degree."),},
    )
    twitter = models.CharField(("twitter"), max_length=70, blank=True, null=True,)
    linkedin = models.CharField(("linkedin"), max_length=70, blank=True, null=True,)
    github = models.CharField(("github"), max_length=70, blank=True, null=True,)
    teacher = models.BooleanField(
        ("teacher"),
        default=False,
        help_text=("Designates if the user is a teacher of the platform."),
    )
    staff = models.BooleanField(
        ("staff"),
        default=False,
        help_text=("Designates whether the user is a platform staff."),
    )
    admin = models.BooleanField(
        ("admin"),
        default=False,
        help_text=("Designates whether the user is a platform administrator."),
    )
    active = models.BooleanField(
        ("active"),
        default=False,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "country"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_country(self):
        """
        Return the country for the user
        """
        for countryTuple in self.COUNTRY_CHOICES:
            if countryTuple[0] == self.country:
                return countryTuple[1]
        return self.country

    def get_password_help_text(self):
        """return password help text."""
        print(self._meta.password)
        for field in self._meta.fields:
            if field.name == field_name:
                return field.help_text


    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.first_name + "\n" + self.last_name

    def get_social_media(self):
        socialMedia = {}
        if self.twitter:
            socialMedia["twitter"] = self.twitter
        if self.linkedin:
            socialMedia["linkedin"] = self.linkedin
        if self.github:
            socialMedia["github"] = self.github
        socialMedia["exist"] = False if len(socialMedia) == 0 else True
        return socialMedia

    def get_detail_url(self):
        return reverse("user:user-detail", kwargs={"id": self.id})

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def has_permissions(self):
        return self.is_teacher or self.is_staff or self.is_admin

    @property
    def is_teacher(self):
        return self.teacher

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        User, related_name="logged_in_user", on_delete=models.CASCADE
    )
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
