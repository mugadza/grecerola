from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)

from versatileimagefield.fields import VersatileImageField
from phonenumber_field.modelfields import PhoneNumberField

from ..core.permissions import AccountPermissions, BasePermissionEnum
from ..core.models import Address
from .validators import validate_possible_number

class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_number]


class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )

    def investors(self):
        return self.get_queryset().filter(
            Q(is_staff=False) | (Q(is_staff=True) & Q(campaigns__isnull=False))
        )

    def staff(self):
        return self.get_queryset().filter(is_staff=True)


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    address = models.OneToOneField(
        Address, related_name="address", on_delete=models.CASCADE, blank=True, null=True
    )
    phone = PossiblePhoneNumberField(blank=True, default="")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    note = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)


    avatar = VersatileImageField(upload_to="user-avatars", default='placeholder540x540.png')

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        permissions = (
            (AccountPermissions.MANAGE_USERS.codename, "Manage investors."),
            (AccountPermissions.MANAGE_STAFF.codename, "Manage staff."),
        )

    def get_full_name(self):
        if self.first_name or self.last_name:
            return ("%s %s" % (self.first_name, self.last_name)).strip()
        return self.email

    def get_short_name(self):
        return self.email

    def get_city_country_address(self):
        address = ""
        if self.address == None:
            return address

        if self.address.city == None:
            if self.address.country.name == None:
                return address
            else:
                return self.address.country.name
        else:
            if self.address.country.name == None:
                return self.address.country.name
            else:
                return self.address.country.name + ", " + self.address.city
