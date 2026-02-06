from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_nested import routers
from django.views.generic import RedirectView
from .views import RegionViewSet, DistrictViewSet, CommentViewSet, DescriptionViewSet, BookingViewSet, SendOTPView, \
    VerifyOTPView

router = routers.SimpleRouter()
router.register(r'regions', RegionViewSet, basename='regions')

districts_router = routers.NestedSimpleRouter(router,r'regions', 'region')
districts_router.register(r'districts', DistrictViewSet, basename='districts')

comments_router = routers.NestedSimpleRouter(districts_router,r'districts','district')
comments_router.register(r'comments', CommentViewSet, basename='comments')
comments_router.register(r'descriptions', DescriptionViewSet, basename='description')
comments_router.register(r'bookings', BookingViewSet, basename='bookings')


urlpatterns = [
    # 'api/' so'zini bu yerdan olib tashlang!
    path('auth/send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),

    path('', include(router.urls)),
    path('', include(districts_router.urls)),
    path('', include(comments_router.urls)),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]