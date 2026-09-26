from django.contrib import admin
from .models import Property, FavoriteProperty


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "property_type", "location", "monthly_rent", "is_available", "created_at")
    list_filter = ("property_type", "is_available", "location")
    search_fields = ("title", "location", "owner__username")
    autocomplete_fields = ["owner"]


@admin.register(FavoriteProperty)
class FavoritePropertyAdmin(admin.ModelAdmin):
    list_display = ("tenant", "property", "created_at")
    search_fields = ("tenant__username", "property__title")
