from rest_framework.pagination import PageNumberPagination

from foodgram.constants import PAGE_SIZE_API


class PageNumberSizedPagination(PageNumberPagination):
    """An extended PageNumberPagination with `limit` (page size) parameter."""
    page_size_query_param = 'limit'
    page_size = PAGE_SIZE_API
