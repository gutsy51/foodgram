from rest_framework.pagination import PageNumberPagination


class PageNumberSizedPagination(PageNumberPagination):
    """An extended PageNumberPagination with `limit` (page size) parameter."""
    page_size_query_param = 'limit'
