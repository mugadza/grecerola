from enum import Enum

from django.contrib.auth.models import Permission


class BasePermissionEnum(Enum):
    @property
    def codename(self):
        return self.value.split(".")[1]


class AccountPermissions(BasePermissionEnum):
    MANAGE_USERS = "account.manage_users"
    MANAGE_STAFF = "account.manage_staff"


class CampaignPermissions(BasePermissionEnum):
    MANAGE_CAMPAIGNS = "campaign.manage_campaigns"


PERMISSIONS_ENUMS = [
    CampaignPermissions,
    AccountPermissions
]


def split_permission_codename(permissions):
    return [permission.split(".")[1] for permission in permissions]


def get_permissions_codename():
    permissions_values = [
        enum.codename
        for permission_enum in PERMISSIONS_ENUMS
        for enum in permission_enum
    ]
    return permissions_values


def get_permissions_enum_list():
    permissions_list = [
        (enum.name, enum.value)
        for permission_enum in PERMISSIONS_ENUMS
        for enum in permission_enum
    ]
    return permissions_list


def get_permissions(permissions=None):
    if permissions is None:
        codenames = get_permissions_codename()
    else:
        codenames = split_permission_codename(permissions)
    return (
        Permission.objects.filter(codename__in=codenames)
        .prefetch_related("content_type")
        .order_by("codename")
    )