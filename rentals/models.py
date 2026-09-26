from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from properties.models import Property


class RentalRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rental_requests")
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rental_requests",
        limit_choices_to={"role": "TENANT"},
    )
    message = models.TextField(blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-request_date"]
        constraints = [
            # A tenant cannot have two PENDING requests for the same property.
            # (Accepted/Rejected requests are allowed to persist for history.)
            models.UniqueConstraint(
                fields=["property", "tenant"],
                condition=models.Q(status="PENDING"),
                name="unique_pending_request_per_tenant_property",
            )
        ]

    def clean(self):
        if self.tenant_id and self.property_id and self.property.owner_id == self.tenant_id:
            raise ValidationError("You cannot send a rental request for your own property.")

    def __str__(self):
        return f"{self.tenant} → {self.property} [{self.status}]"
