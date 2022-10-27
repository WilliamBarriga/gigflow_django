# Django
from django.urls import path

# Views
from services.views import services as services_views

urlpatterns = [
    path("", services_views.ServiceView.as_view(), name="services"),
    path(
        "<int:service_id>/",
        services_views.SeriviceOneView.as_view(),
        name="one_service",
    ),
    path(
        "service-types/", services_views.ServiceTypeView.as_view(), name="service_types"
    ),
    path(
        "service-types/<int:service_type_id>/",
        services_views.ServiceTypeOneView.as_view(),
        name="one_service_type",
    ),
]
