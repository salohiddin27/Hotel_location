from django.contrib import admin

from .models import Hotel, Region, HotelComment, Description, Booking, HotelImage, Amenity


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'price_per_night', 'average_rating', 'is_active')
    list_filter = ('region', 'is_active', 'amenities')
    search_fields = ('name', 'region__name')
    filter_horizontal = ('amenities',)
    ordering = ('-average_rating',)
    list_per_page = 20


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(HotelComment)
class DistrictCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotel', 'rating', 'created_at')
    list_filter = ('hotel', 'rating', 'created_at')
    search_fields = ('user__username', 'hotel__name', 'text')
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'key', 'value')
    search_fields = ('hotel__name', 'key', 'value')
    list_per_page = 20


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotel', 'check_in', 'check_out', 'guests', 'created_at')
    list_filter = ('check_in', 'check_out', 'hotel')
    search_fields = ('user__username', 'hotel__name')
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(HotelImage)
class DistrictImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'image')
    search_fields = ('hotel__name',)
    list_per_page = 20