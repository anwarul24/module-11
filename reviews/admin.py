from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("property", "tenant", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("property__title", "tenant__username", "comment")
    autocomplete_fields = ["property", "tenant"]
