
from django.contrib import admin
from django.urls import include, path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    return Response(
        {
            "message": "Recipe Management API",
            "register": reverse("register", request=request),
            "login": reverse("login", request=request),
            "logout": reverse("logout", request=request),
            "me": reverse("user-me", request=request),
            "categories": reverse("category-list", request=request),
            "ingredients": reverse("ingredient-list", request=request),
            "recipes": reverse("recipe-list", request=request),
        }
    )


urlpatterns = [
    path("", api_root, name="api-root"),
    path('admin/', admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/users/", include("users.profile_urls")),
    path("api/", include("recipes.urls")),
]
