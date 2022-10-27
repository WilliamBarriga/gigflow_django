# Django
from django.db.models import Q

# Django REST Framework
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions

# Models
from services.models import services as services_models

# Serializers
from services.serializers import services as services_serializers

# Docs
from gigflow.drf_spectacular import views_schema


class ServiceTypeView(GenericAPIView):

    serializer_class = services_serializers.ServiceTypeSerializer

    @views_schema.get_many_schema(
        responses={
            200: services_serializers.ServiceTypeSerializer(many=True),
        }
    )
    def get(self, request: Request) -> Response:
        """get all service types"""
        queryset = services_models.ServiceType.objects.filter(
            self._get_filters(request.query_params)
        ).order_by("id")
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @views_schema.base_schema(
        request=services_serializers.ServiceTypeSerializer,
        responses={
            201: services_serializers.ServiceTypeSerializer,
        },
    )
    def post(self, request: Request) -> Response:
        """create a service type"""
        data = request.data.copy()
        serializer = self.get_serializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_filters(self, params: dict) -> Q:
        """get filters from query params

        Args:
            params (dict): query params to filter
        Returns:
            Q: filters
        """
        filters = Q()
        if "active" in params:
            active = True if params["active"] == "true" else False
            filters &= Q(active=active)
        if "name" in params:
            filters &= Q(name__icontains=params["name"])
        return filters


class ServiceTypeOneView(GenericAPIView):

    serializer_class = services_serializers.ServiceTypeSerializer

    @views_schema.base_schema(
        responses={
            200: services_serializers.ServiceTypeSerializer,
        }
    )
    def get(self, request: Request, service_type_id: int) -> Response:
        """get a service type"""
        queryset = services_models.ServiceType.objects.filter(id=service_type_id)
        if not queryset.exists():
            raise exceptions.NotFound("Service type not found")
        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @views_schema.base_schema(
        request=services_serializers.ServiceTypeSerializer,
        responses={
            200: services_serializers.ServiceTypeSerializer,
        },
    )
    def patch(self, request: Request, service_type_id: int) -> Response:
        """partial update a service type"""
        queryset = services_models.ServiceType.objects.filter(id=service_type_id)
        if not queryset.exists():
            raise exceptions.NotFound("Service type not found")
        data = request.data.copy()
        serializer = self.get_serializer(queryset.first(), data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @views_schema.base_schema()
    def delete(self, request: Request, service_type_id: int) -> Response:
        """deactivate a service type"""
        queryset = services_models.ServiceType.objects.filter(
            id=service_type_id, active=True
        )
        if not queryset.exists():
            raise exceptions.NotFound("Service type not found")
        queryset = queryset.first()
        queryset.active = False
        queryset.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceView(GenericAPIView):

    serializer_class = services_serializers.ServiceSerializer

    @views_schema.get_many_schema(
        responses={
            200: services_serializers.ServiceSerializer(many=True),
        }
    )
    def get(self, request: Request) -> Response:
        """get all services"""
        queryset = (
            services_models.Service.objects.select_related("service_type")
            .filter(self._get_filters(request.query_params))
            .order_by("-created_at")
        )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @views_schema.base_schema(
        request=services_serializers.ServiceSerializer,
        responses={
            201: services_serializers.ServiceSerializer,
        },
    )
    def post(self, request: Request) -> Response:
        """create a service"""
        data = request.data.copy()
        serializer = self.get_serializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_filters(self, params: dict) -> Q:
        """get filters from query params

        Args:
            params (dict): query params to filter

        Returns:
            Q: filters
        """
        filters = Q()
        if "active" in params:
            active = True if params["active"] == "true" else False
            filters &= Q(active=active)
        if "title" in params:
            filters &= Q(title__icontains=params["title"])
        if "service_type" in params:
            filters &= Q(service_type__id=params["service_type"])
        if "minimum_price" in params:
            filters &= Q(price__gte=params["minimum_price"])
        if "maximum_price" in params:
            filters &= Q(price__lte=params["maximum_price"])
        if start_date := params.get("start_date"):
            if end_date := params.get("end_date"):
                filters &= Q(created_at__range=[start_date, end_date])
            else:
                filters &= Q(created_at__gte=start_date)
        return filters


class SeriviceOneView(GenericAPIView):

    serializer_class = services_serializers.ServiceSerializer

    @views_schema.base_schema(
        responses={
            200: services_serializers.ServiceSerializer,
        }
    )
    def get(self, request: Request, service_id: int) -> Response:
        """get a service"""
        queryset = services_models.Service.objects.select_related(
            "service_type"
        ).filter(id=service_id, active=True)
        if not queryset.exists():
            raise exceptions.NotFound("Service not found")
        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @views_schema.base_schema(
        request=services_serializers.ServiceSerializer,
        responses={
            200: services_serializers.ServiceSerializer,
        },
    )
    def patch(self, request: Request, service_id: int) -> Response:
        """partial update a service"""
        queryset = services_models.Service.objects.filter(id=service_id)
        if not queryset.exists():
            raise exceptions.NotFound("Service not found")
        data = request.data.copy()
        serializer = self.get_serializer(queryset.first(), data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @views_schema.base_schema()
    def delete(self, request: Request, service_id: int) -> Response:
        """deactivate a service"""
        queryset = services_models.Service.objects.filter(id=service_id, active=True)
        if not queryset.exists():
            raise exceptions.NotFound("Service not found")
        queryset = queryset.first()
        queryset.active = False
        queryset.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
