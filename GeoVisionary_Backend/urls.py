from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",lambda request : redirect("admin/")),
    path("api/", include("users.urls")),
    path("proxy/",include("proxy.urls")),
    path("neo4jDB/",include("neo4jDB.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)