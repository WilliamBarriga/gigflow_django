from typing import List
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

BASEPAGE = 1


class CustomPagination(PageNumberPagination):
    page: int = BASEPAGE
    page_size: int = 5
    page_size_query_param: str = "page_size"

    def get_paginated_response(self, data: List[dict]) -> Response:
        """Custom pagination response
        Args:
            data (List[dict]): data to paginate
        Returns:
            Response: paginated response
        """
        return Response(
            {
                "current_page": int(self.request.query_params.get("page", BASEPAGE)),
                "data": data,
                "last_page_url": self.get_previous_link(),
                "next_page_url": self.get_next_link(),
                "count": self.page.paginator.count,
            }
        )

    def get_paginated_response_schema(self, schema: List[dict]) -> dict:
        """Custom pagination response schema
        Args:
            schema (List[dict]): schema to paginate
        Returns:
            dict: paginated response schema
        """
        return {
            "type": "object",
            "properties": {
                "current_page": {"type": "integer", "example": 1},
                "data": schema,
                "last_page_url": {"type": "string", "nullable": True, "format": "uri"},
                "next_page_url": {"type": "string", "nullable": True, "format": "uri"},
                "total": {"type": "integer", "example": 100},
            },
        }
