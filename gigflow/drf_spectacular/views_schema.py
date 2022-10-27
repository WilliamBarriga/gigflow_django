from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

base_get_many_parameters = [
    OpenApiParameter(
        "page", OpenApiTypes.INT, OpenApiParameter.QUERY, description="Page number"
    ),
    OpenApiParameter(
        "page_size", OpenApiTypes.INT, OpenApiParameter.QUERY, description="Page size"
    ),
]


def base_schema(**kwargs):
    def decorator(function):
        return extend_schema(**kwargs)(function)

    return decorator


def get_many_schema(**kwargs):
    if "parameters" in kwargs:
        kwargs["parameters"] += base_get_many_parameters
    else:
        kwargs["parameters"] = base_get_many_parameters

    def decorator(function):
        return base_schema(**kwargs)(function)

    return decorator
