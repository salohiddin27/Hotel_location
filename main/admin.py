from django.contrib import admin

from .models import District, Region, DistrictComment, Description, Booking, DistrictImage, Amenity


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
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


@admin.register(DistrictComment)
class DistrictCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'district', 'rating', 'created_at')
    list_filter = ('district', 'rating', 'created_at')
    search_fields = ('user__username', 'district__name', 'text')
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'district', 'key', 'value')
    search_fields = ('district__name', 'key', 'value')
    list_per_page = 20


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'district', 'check_in', 'check_out', 'guests', 'created_at')
    list_filter = ('check_in', 'check_out', 'district')
    search_fields = ('user__username', 'district__name')
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(DistrictImage)
class DistrictImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'district', 'image')
    search_fields = ('district__name',)
    list_per_page = 20
