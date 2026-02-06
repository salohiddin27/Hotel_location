import random

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Region, Hotel, HotelComment, Description, Booking, Profile
from .serializers import (
    DescriptionSerializer,
    HotelCommentSerializer,
    HotelListSerializer,
    HotelDetailSerializer,
    RegionListSerializer,
    RegionDetailSerializer, BookingSerializer,
)


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
        return qs.prefetch_related('descriptions', 'comments', 'amenities', 'images')

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


@extend_schema(parameters=[
    OpenApiParameter("region_pk", type=int, location=OpenApiParameter.PATH),
    OpenApiParameter("hotel_pk", type=int, location=OpenApiParameter.PATH),
])
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        hotel_pk = self.kwargs.get("hotel_pk")
        if hotel_pk:
            return self.queryset.filter(district_id=hotel_pk)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class SendOTPView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    @extend_schema(responses={200: dict},
                   request={"application/json": {"type": "object", "properties": {"email": {"type": "string"}}}})
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email kiritish shart"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(email=email, defaults={'username': email})

        otp = str(random.randint(10000, 99999))

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.otp_code = otp
        profile.save()

        # Emailga kodni yuborish jarayoni

        try:
            send_mail(
                'Sizning tasdiqlash kodingiz',
                f'Sizning login kodingiz: {otp}',  # email matni
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({"message": "Kod emailga yuborildi"}, status=status.HTTP_200_OK)
        except Exception as e:
            # Agar email yuborishda muammo bo'lsa (internet yoki SMTP xatosi)
            return Response({"error": f"Emal yuborish xatoligi: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Email va Kodni tekshirib, Token (Login) qaytaradigan View
@method_decorator(csrf_exempt, name='dispatch')  # Buni ham qo'shing
class VerifyOTPView(APIView):
    authentication_classes = []

    # Swagger uchun so'rov parametrlarini ko'rsatish
    @extend_schema(responses={200: dict}, request={
        "application/json": {"type": "object", "properties": {"email": {"type": "string"}, "otp": "string"}}})
    def post(self, request):
        # Frontend yuborgan email va otp kodni olish
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            # Bazadan ushbu emailga ega foydalanuvchini topish
            user = User.objects.get(email=email)
            # Foydalanuvchining profilini olish
            profile = user.profile

            if profile.otp_code == otp:
                token, _ = Token.objects.get_or_create(user=user)
                # Bir marta ishlatilgan kodni xavfsizlik uchun bazadan o'chirish
                profile.otp_code = None
                profile.email_confirmed = True

                profile.save()

                return Response({
                    "token": token.key,
                    "message": "Muvaffaqiyatli login qilindi"
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Kod noto'g'ri"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi "}, status=status.HTTP_404_NOT_FOUND)

