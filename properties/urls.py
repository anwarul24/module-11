from django.urls import path
from . import views

app_name = "properties"

urlpatterns = [
    path("", views.property_list, name="list"),
    path("add/", views.property_create, name="create"),
    path("mine/", views.my_properties, name="mine"),
    path("favorites/", views.my_favorites, name="favorites"),
    path("<int:pk>/", views.property_detail, name="detail"),
    path("<int:pk>/edit/", views.property_edit, name="edit"),
    path("<int:pk>/delete/", views.property_delete, name="delete"),
    path("<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
]
