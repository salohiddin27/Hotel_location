from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Region, Hotel, HotelComment, Description
from .serializers import (
    DescriptionSerializer,
    HotelCommentSerializer,
    HotelListSerializer,
    HotelDetailSerializer,
    RegionListSerializer,
    RegionDetailSerializer, )


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all().order_by('id')
    serializer_class = RegionListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'location']
    search_fields = ['name']
    pagination_class = None

    def get_queryset(self):
        return Region.objects.prefetch_related(
            'hotels__descriptions',
            'hotels__comments',
            'hotels__amenities',
            'hotels__images',

        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RegionDetailSerializer
        return RegionListSerializer


@extend_schema(parameters=[OpenApiParameter("region_pk", type=int, location=OpenApiParameter.PATH)])
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'region']
    search_fields = ['name']

    def get_queryset(self):
        region_pk = self.kwargs.get("region_pk")
        qs = super().get_queryset()
        if region_pk:
            qs = qs.filter(region_id=region_pk)
        return qs.prefetch_related('descriptions', 'comments', 'amenities', 'images',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HotelDetailSerializer
        return HotelListSerializer


@extend_schema(parameters=[
    OpenApiParameter("region_pk", type=int, location=OpenApiParameter.PATH),
    OpenApiParameter("hotel_pk", type=int, location=OpenApiParameter.PATH)
])
class CommentViewSet(viewsets.ModelViewSet):
    queryset = HotelComment.objects.all()
    serializer_class = HotelCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        hotel_pk = self.kwargs.get("hotel_pk")
        qs = super().get_queryset()
        if hotel_pk:
            qs = qs.filter(hotel_pk=hotel_pk)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(parameters=[
    OpenApiParameter("region_pk", type=int, location=OpenApiParameter.PATH),

    OpenApiParameter("hotel_pk", type=int, location=OpenApiParameter.PATH),
])
class DescriptionViewSet(viewsets.ModelViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        hotel_pk = self.kwargs.get("hotel_pk")
        qs = super().get_queryset()
        if hotel_pk:
            qs = qs.filter(district_id=hotel_pk)
        return qs


