from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from apps.profiles.models import Profile
from apps.ratings.serializers import RatingSerializer


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    gender = serializers.CharField(source="get_gender_display")
    full_name = serializers.CharField(source="user.get_full_name")
    country = CountryField(name_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "photo",
            "about_me",
            "licence",
            "gender",
            "country",
            "city",
            "is_buyer",
            "is_seller",
            "is_agent",
            "rating",
            "reviews",
        ]

    def get_reviews(self, obj):
        reviews = obj.agent_review.all()
        serializer = RatingSerializer(instance=reviews, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.top_agent:
            representation.setdefault("top_agent", True)
        return representation


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "photo",
            "about_me",
            "licence",
            "gender",
            "country",
            "city",
            "is_buyer",
            "is_seller",
            "is_agent",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.top_agent:
            representation.setdefault("top_agent", True)
        return representation
