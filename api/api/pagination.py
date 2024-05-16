from rest_framework import pagination
from rest_framework import response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
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
