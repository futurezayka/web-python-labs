from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("prometheus-xyzabc/", include("django_prometheus.urls")),
    path("healthcheck/", lambda r: HttpResponse("OK"), name="healthcheck"),
]
