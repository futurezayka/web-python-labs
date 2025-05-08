from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from core.api.views.auth.register import RegisterView
from core.api.views.author import AuthorViewSet
from core.api.views.book import BookViewSet
from core.api.views.genre import GenreViewSet

__all__ = ["urlpatterns"]


router = DefaultRouter()

urlpatterns = [
    path("auth/login/", obtain_auth_token, name="auth-login"),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
]

router.register(r"author", AuthorViewSet, basename="author")
router.register(r"genre", GenreViewSet, basename="genre")
router.register(r"book", BookViewSet, basename="book")


urlpatterns += router.urls
