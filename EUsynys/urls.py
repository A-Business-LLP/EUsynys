from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from rest_framework_simplejwt import authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api_v1.authentication import CookieJWTAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="REST APIs",
        default_version='v1',
        description="API documentation"
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
    authentication_classes=(CookieJWTAuthentication,)
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("admin/", admin.site.urls), 
    path("api/", include("api_v1.urls"))
]
