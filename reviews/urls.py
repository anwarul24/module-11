from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("add/<int:property_pk>/", views.add_review, name="add"),
]
