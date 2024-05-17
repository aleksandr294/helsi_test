"""
Module providing a custom pagination class for paginating API responses.

This module defines a custom pagination class, `CustomPagination`, which extends
the `PageNumberPagination` class provided by Django REST Framework. It allows for
customization of pagination parameters such as page size and maximum page size.
"""

from rest_framework import pagination
from rest_framework import response


class CustomPagination(pagination.PageNumberPagination):
    """Custom pagination class to paginate API responses."""

    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data: list):
        """
        Return a paginated response for the provided data.

        Args:
            data (list): List of serialized data objects.

        Returns:
            Response: Paginated response containing count, total pages,
                      next and previous page numbers, and results.s

        """
        return response.Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "next_page": (
                    self.page.next_page_number() if self.page.has_next() else None
                ),
                "previous_page": (
                    self.page.previous_page_number()
                    if self.page.has_previous()
                    else None
                ),
                "results": data,
            }
        )
