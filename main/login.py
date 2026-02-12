import random

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, Booking
from .serializers import BookingSerializer


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
                f'Sizning login kodingiz: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({"message": "Kod emailga yuborildi"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Emal yuborish xatoligi: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Email va Kodni tekshirib, Token (Login) qaytaradigan View
@method_decorator(csrf_exempt, name='dispatch')
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

