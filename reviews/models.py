from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from properties.models import Property


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reviews")
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        limit_choices_to={"role": "TENANT"},
    )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("property", "tenant")

    def __str__(self):
        return f"{self.tenant} rated {self.property} {self.rating}/5"
