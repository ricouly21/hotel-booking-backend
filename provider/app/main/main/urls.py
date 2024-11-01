from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path, include

from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from provider.views import EventsViewset


schema_view = get_schema_view(
    openapi.Info(
        title="Provider Service API",
        default_version="v1",
        description="N/A",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"events", EventsViewset, basename="events")

urlpatterns = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", include(router.urls)),
]
