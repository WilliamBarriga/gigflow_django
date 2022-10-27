# Django REST Framework
from rest_framework import serializers
# Models
from services.models import services as services_models


class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = services_models.ServiceType
        exclude = ('created_at', 'updated_at')


class ServiceSerializer(serializers.ModelSerializer):

    service_type = ServiceTypeSerializer(read_only=True)
    service_type_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=services_models.ServiceType.objects.filter(
            active=True),
        source='service_type')

    class Meta:
        model = services_models.Service
        fields = '__all__'
