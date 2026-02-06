from django.utils import timezone
from rest_framework import serializers

from .models import Region, District, DistrictComment, Description, DistrictImage, Amenity, Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'district', 'check_in', 'check_out', 'guests', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        today = timezone.now().date()

        if data.get('check_in') and data['check_in'] < today:
            raise serializers.ValidationError({
                "check_in": "You can't bron ago time!"
            })

        if data.get('check_in') and data.get('check_out'):
            if data['check_out'] <= data['check_in']:
                raise serializers.ValidationError({
                    "check_out": "check-out time must be after check-in time"
                })
        return data


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ['id', 'key', 'value']


class DistrictImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictImage
        fields = ['id', 'image']


class DistrictCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DistrictComment
        fields = ['id', 'user', 'text', 'rating', 'created_at']


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'icon']


class DistrictListSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)
    images = DistrictImageSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = [
            'id',
            'name',
            'price_per_night',
            'latitude',
            'longitude',
            'average_rating',
            'is_active',
            'created_at',
            'updated_at',
            'amenities',
            'images'
        ]


class DistrictDetailSerializer(serializers.ModelSerializer):
    descriptions = DescriptionSerializer(many=True, read_only=True)
    comments = DistrictCommentSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    images = DistrictImageSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = [
            'id',
            'name',
            'price_per_night',
            'latitude',
            'longitude',
            'average_rating',
            'is_active',
            'created_at',
            'updated_at',
            'descriptions',
            'comments',
            'amenities',
            'images',
        ]


class RegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'location', 'image']


class RegionDetailSerializer(serializers.ModelSerializer):
    districts = DistrictListSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'location', 'image', 'districts']
