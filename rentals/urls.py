from django.urls import path
from . import views

app_name = "rentals"

urlpatterns = [
    path("send/<int:property_pk>/", views.send_request, name="send"),
    path("<int:pk>/cancel/", views.cancel_request, name="cancel"),
    path("owner/", views.owner_requests, name="owner_requests"),
    path("mine/", views.tenant_requests, name="tenant_requests"),
    path("<int:pk>/<str:action>/", views.respond_request, name="respond"),
]
