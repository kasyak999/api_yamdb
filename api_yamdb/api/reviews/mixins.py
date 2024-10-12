from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import IsAdminOrReadOnly


class CategoryGenreMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
