from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from properties import views as property_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", property_views.home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("properties/", include("properties.urls")),
    path("requests/", include("rentals.urls")),
    path("reviews/", include("reviews.urls")),
    path("dashboard/", include("dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
