from django.urls import path, include
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import RegionViewSet, DistrictViewSet, CommentViewSet, DescriptionViewSet, home

router = routers.SimpleRouter()
router.register(r'regions', RegionViewSet, basename='regions')

districts_router = routers.NestedSimpleRouter(
    parent_router=router,
    parent_prefix='regions',
    lookup='region'
)
districts_router.register(r'districts', DistrictViewSet, basename='districts')


comments_router = routers.NestedSimpleRouter(
    parent_router=districts_router,
    parent_prefix='districts',
    lookup='district'
)
comments_router.register(r'comments', CommentViewSet, basename='comments')


descriptions_router = routers.NestedSimpleRouter(
    parent_router=districts_router,
    parent_prefix='districts',
    lookup='district'
)
descriptions_router.register(r'descriptions', DescriptionViewSet, basename='descriptions')


urlpatterns = [

    path('', include(router.urls)),
    path('', include(districts_router.urls)),
    path('', include(comments_router.urls)),
    path('', include(descriptions_router.urls)),
    path("", home, name="home"),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
