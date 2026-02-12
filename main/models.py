from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Region(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='regions/')
    location = models.URLField(max_length=200)


    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=100)
    price_per_night = models.PositiveIntegerField(default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    amenities = models.ManyToManyField(Amenity, blank=True)
    average_rating = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profile"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        today = timezone.now().date()

        if self.check_in and self.check_in < today:
            raise ValidationError({
                "check_in": f"Check-in time can't be ago time. today: {today}"
            })

        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError({
                "check_out": "Check-out sanasi check-in dan keyin bo'lishi shart!"
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class HotelComment(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.rating is not None and not (1 <= self.rating <= 5):
            raise ValidationError("Rating 1 da  5 gacha bolishi kerak.")
        super().save(*args, **kwargs)

        ratings = self.hotel.comments.exclude(rating__isnull=True)
        if ratings.exists():
            self.hotel.average_rating = (sum(r.rating for r in ratings) / ratings.count())
        else:
            self.hotel.average_rating = 0

        self.hotel.save()

    def __str__(self):
        return f"{self.user} - {self.rating}"


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='districts/gallery/')

    def __str__(self):
        return f"Image of {self.hotel.name}"


class Description(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True, related_name='descriptions')
    key = models.CharField(max_length=350)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value}"

