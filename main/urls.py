from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_nested import routers

from .views import RegionViewSet, HotelViewSet, CommentViewSet, DescriptionViewSet
from .login import BookingViewSet, SendOTPView, VerifyOTPView
router = routers.SimpleRouter()
router.register(r'regions', RegionViewSet, basename='regions')

hotel_router = routers.NestedSimpleRouter(router, r'regions', 'region')
hotel_router.register(r'hotels', HotelViewSet, basename='hotels')

comments_router = routers.NestedSimpleRouter(hotel_router, r'hotels', 'hotel')
comments_router.register(r'comments', CommentViewSet, basename='comments')
comments_router.register(r'descriptions', DescriptionViewSet, basename='description')
comments_router.register(r'bookings', BookingViewSet, basename='bookings')

urlpatterns = [
    path('auth/send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),

    path('', include(router.urls)),
    path('', include(hotel_router.urls)),
    path('', include(comments_router.urls)),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
