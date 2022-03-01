from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from apps.properties.models import Property, PropertyImages, PropertyViews


class PropertyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ["id", "photo"]


class PropertySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    country = CountryField(name_only=True)
    cover_photo = serializers.SerializerMethodField()
    property_images = PropertyImagesSerializer(many=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "user",
            "title",
            "slug",
            "ref_code",
            "description",
            "country",
            "city",
            "postal_code",
            "street_address",
            "property_number",
            "price",
            "tax",
            "final_property_price",
            "plot_area",
            "total_floors",
            "bedrooms",
            "bathrooms",
            "advert_type",
            "property_type",
            "cover_photo",
            "property_images",
            "published_status",
            "views",
        ]

    def get_cover_photo(self, obj):
        return obj.cover_photo.url


class PropertyCreateSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Property
        exclude = ["pkid", "id", "user", "slug", "ref_code", "updated_time", "views"]


class PropertyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            "title",
            "description",
            "country",
            "city",
            "postal_code",
            "street_address",
            "property_number",
            "price",
            "tax",
            "plot_area",
            "total_floors",
            "bedrooms",
            "bathrooms",
            "advert_type",
            "property_type",
            "cover_photo",
            "published_status",
        ]


class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyViews
        exclude = ["updated_time", "pkid"]
