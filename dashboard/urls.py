from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_redirect, name="redirect"),
    path("owner/", views.owner_dashboard, name="owner"),
    path("tenant/", views.tenant_dashboard, name="tenant"),
]
