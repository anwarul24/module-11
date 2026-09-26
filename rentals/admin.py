from django.contrib import admin
from .models import RentalRequest


@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin):
    list_display = ("property", "tenant", "status", "request_date", "updated_at")
    list_filter = ("status",)
    search_fields = ("property__title", "tenant__username")
    autocomplete_fields = ["property", "tenant"]
