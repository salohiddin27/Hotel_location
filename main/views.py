from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Region, District, DistrictComment, Description
from .serializers import (
    DescriptionSerializer,
    DistrictCommentSerializer,
    DistrictListSerializer,
    DistrictDetailSerializer,
    RegionListSerializer,
    RegionDetailSerializer,
)


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'location']
    search_fields = ['name']

    def get_queryset(self):
        return Region.objects.prefetch_related(
            'districts__descriptions',
            'districts__comments',
            'districts__amenities',
            'districts__images',
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RegionDetailSerializer
        return RegionListSerializer

@extend_schema(parameters=[OpenApiParameter("region_pk", type=int, location=OpenApiParameter.PATH)])
class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictDetailSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'region']
    search_fields = ['name']

    def get_queryset(self):
        region_pk = self.kwargs.get("region_pk")
        qs = super().get_queryset()
        if region_pk:
            qs = qs.filter(region_id=region_pk)
        return qs.prefetch_related('descriptions', 'comments', 'amenities', 'images')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DistrictDetailSerializer
        return DistrictListSerializer

@extend_schema(parameters=[
    OpenApiParameter("region_pk", type=int, location=OpenApiParameter.PATH),
    OpenApiParameter("district_pk", type=int, location=OpenApiParameter.PATH)
])
class CommentViewSet(viewsets.ModelViewSet):
    # ...class CommentViewSet(viewsets.ModelViewSet):
    queryset = DistrictComment.objects.all()
    serializer_class = DistrictCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        district_pk = self.kwargs.get("district_pk")
        qs = super().get_queryset()
        if district_pk:
            qs = qs.filter(district_id=district_pk)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(parameters=[
    OpenApiParameter("region_pk", type=int, location=OpenApiParameter.PATH),

    OpenApiParameter("district_pk", type=int, location=OpenApiParameter.PATH),
])
class DescriptionViewSet(viewsets.ModelViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        district_pk = self.kwargs.get("district_pk")
        qs = super().get_queryset()
        if district_pk:
            qs = qs.filter(district_id=district_pk)
        return qs



from django.shortcuts import render
from .models import Region, District

def home(request):
    regions = Region.objects.all()
    districts = District.objects.filter(is_active=True).prefetch_related('images', 'amenities')
    # prefetch_related('images') - bu har bir hotelning rasmlarini bazadan tezroq olib keladi
    return render(request, 'index.html', {'regions': regions, 'districts': districts})