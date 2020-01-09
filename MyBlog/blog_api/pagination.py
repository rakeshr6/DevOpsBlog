from rest_framework.pagination import LimitOffsetPagination


class PostLimitOffPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 5
