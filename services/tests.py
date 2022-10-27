# Django
from django.test import TestCase
from django.urls import reverse

# Models
from services.models import services as services_models


class ServiceTypeViewTests(TestCase):
    def test_no_data_paginated_service_types(self):
        """get no data paginated response"""
        response = self.client.get(reverse("service_types"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["next_page_url"], None)
        self.assertEqual(response.data["last_page_url"], None)
        self.assertEqual(response.data["data"], [])

    def test_add_service_type(self):
        """create a service type"""
        data = {"name": "add_service_type", "active": True}
        response = self.client.post(
            reverse("service_types"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["active"], data["active"])

    def test_paginated_service_types(self):
        """get paginated response and validate pagination functionality"""

        for i in range(0, 5):
            data = {"name": f"paginated_service_type_{i}", "active": True}
            response = self.client.post(
                reverse("service_types"), data=data, content_type="application/json"
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data["name"], data["name"])
            self.assertEqual(response.data["active"], data["active"])

        query_params = "?page=1&page_size=2"
        response = self.client.get(f'{reverse("service_types")}{query_params}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 5)
        self.assertIsNotNone(response.data["next_page_url"])
        self.assertIsNone(response.data["last_page_url"])
        self.assertEqual(len(response.data["data"]), 2)

        query_params = "?page=3&page_size=2"
        response = self.client.get(f'{reverse("service_types")}{query_params}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 5)
        self.assertIsNone(response.data["next_page_url"])
        self.assertIsNotNone(response.data["last_page_url"])
        self.assertEqual(len(response.data["data"]), 1)

    def test_patch_service_type(self):
        """patch a service type"""
        data = {"name": "patch_service_type", "active": True}
        response = self.client.post(
            reverse("service_types"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["active"], data["active"])

        data = {"name": "patched_service_type"}
        response = self.client.patch(
            reverse("one_service_type", kwargs={"service_type_id": response.data["id"]}),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["active"], True)

    def test_delete_service_type(self):
        """delete a service type"""
        data = {"name": "delete_service_type", "active": True}
        response = self.client.post(
            reverse("service_types"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["active"], data["active"])

        response = self.client.delete(
            reverse("one_service_type", kwargs={"service_type_id": response.data["id"]})
        )
        self.assertEqual(response.status_code, 204)

    def test_create_duplicate_service_type(self):
        """create a duplicate service type"""
        data = {"name": "duplicate_service_type", "active": True}
        response = self.client.post(
            reverse("service_types"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["active"], data["active"])

        response = self.client.post(
            reverse("service_types"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


class ServiceViewTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        service_types = [
            services_models.ServiceType(name=f"test {i}", active=True)
            for i in range(0, 5)
        ]
        service_types = services_models.ServiceType.objects.bulk_create(service_types)

        self.len_service_types = len(service_types)
        self.service_type = service_types[0]

    def test_create_service(self):
        """create a service"""
        data = {
            "title": "create_service",
            "description": "create_service_description",
            "price": 100.25,
            "tasks": "create_service_tasks",
            "service_type_id": self.service_type.id,
            "active": True,
        }
        response = self.client.post(
            reverse("services"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["active"], data["active"])
        self.assertEqual(response.data["service_type"]["id"], data["service_type_id"])

    def test_craete_service_with_invalid_service_type(self):
        """create a service with invalid service type"""
        data = {
            "title": "create_service",
            "description": "create_service_description",
            "price": 100.25,
            "tasks": "create_service_tasks",
            "service_type_id": 100,
            "active": True,
        }
        response = self.client.post(
            reverse("services"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_patch_service(self):
        """patch a service"""
        data = {
            "title": "patch_service",
            "description": "patch_service_description",
            "price": 100.25,
            "tasks": "patch_service_tasks",
            "service_type_id": self.service_type.id,
            "active": True,
        }
        response = self.client.post(
            reverse("services"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["active"], data["active"])
        self.assertEqual(response.data["service_type"]["id"], data["service_type_id"])

        data = {
            "title": "patch_service_updated",
            "description": "patch_service_description_updated",
            "price": 100.25,
            "tasks": "patch_service_tasks_updated",
            "service_type_id": self.service_type.id,
            "active": False,
        }
        response = self.client.patch(
            reverse("one_service", kwargs={"service_id": response.data["id"]}),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["active"], data["active"])
        self.assertEqual(response.data["service_type"]["id"], data["service_type_id"])

    def test_delete_service(self):
        """delete a service"""
        data = {
            "title": "delete_service",
            "description": "delete_service_description",
            "price": 100.25,
            "tasks": "delete_service_tasks",
            "service_type_id": self.service_type.id,
            "active": True,
        }
        service = self.client.post(
            reverse("services"), data=data, content_type="application/json"
        )
        self.assertEqual(service.status_code, 201)
        self.assertEqual(service.data["title"], data["title"])
        self.assertEqual(service.data["active"], data["active"])
        self.assertEqual(service.data["service_type"]["id"], data["service_type_id"])

        response = self.client.delete(
            reverse("one_service", kwargs={"service_id": service.data["id"]})
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            reverse("one_service", kwargs={"service_id": service.data["id"]})
        )
        self.assertEqual(response.status_code, 404)

    def test_create_duplicated_service(self):
        """create a duplicated service"""
        data = {
            "title": "duplicate_service",
            "description": "duplicate_service_description",
            "price": 100.25,
            "tasks": "duplicate_service_tasks",
            "service_type_id": self.service_type.id,
            "active": True,
        }
        response = self.client.post(
            reverse("services"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["active"], data["active"])
        self.assertEqual(response.data["service_type"]["id"], data["service_type_id"])

        response = self.client.post(
            reverse("services"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_filter_services(self):
        """filter services"""
        data = {
            "title": "filter_service",
            "description": "filter_service_description",
            "price": 100.25,
            "tasks": "filter_service_tasks",
            "service_type_id": self.service_type.id,
            "active": True,
        }
        service = self.client.post(
            reverse("services"), data=data, content_type="application/json"
        )
        self.assertEqual(service.status_code, 201)
        self.assertEqual(service.data["title"], data["title"])
        self.assertEqual(service.data["active"], data["active"])
        self.assertEqual(service.data["service_type"]["id"], data["service_type_id"])

        query_params = f'?title={data["title"]}'
        response = self.client.get(reverse("services") + query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
