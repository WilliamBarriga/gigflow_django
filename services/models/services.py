# Django
from django.db import models


class ServiceType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "service_types"

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    tasks = models.TextField()
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "services"
        unique_together = ("title", "service_type")

    def __str__(self):
        return self.title
