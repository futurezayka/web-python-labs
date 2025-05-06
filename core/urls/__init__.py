from django.contrib import admin
from django.urls import path
from core.api.urls import urlpatterns as api_urls

urlpatterns = [path("admin/", admin.site.urls), *api_urls]
