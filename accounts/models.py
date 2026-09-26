from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with a role field.

    ROLE choices drive authorization throughout the project:
    - OWNER  : can list/manage properties and respond to rental requests.
    - TENANT : can browse properties, send rental requests, leave reviews.
    """

    class Role(models.TextChoices):
        OWNER = "OWNER", "Property Owner"
        TENANT = "TENANT", "Tenant"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.TENANT)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)

    @property
    def is_owner(self):
        return self.role == self.Role.OWNER

    @property
    def is_tenant(self):
        return self.role == self.Role.TENANT

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
