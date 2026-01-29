from rest_framework import serializers

from .models import Region, District, DistrictComment, Description, DistrictImage, Amenity


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


