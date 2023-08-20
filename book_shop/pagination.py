from rest_framework.pagination import PageNumberPagination

class DefualtPagination(PageNumberPagination):
    page_size = 10