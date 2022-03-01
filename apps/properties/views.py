import logging

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.properties.models import Property, PropertyViews
from apps.properties.paginations import PropertyPagination
from apps.properties.permissions import IsOwner
from apps.properties.serializers import (PropertyCreateSerializer,
                                         PropertySerializer,
                                         PropertyUpdateSerializer,
                                         PropertyViewSerializer)

logger = logging.getLogger(__name__)


class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.order_by("-created_time")
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination


class AgentPropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.order_by("-created_time")
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(user=user).order_by("-created_time")


class PropertyViewsListAPIView(generics.ListAPIView):
    queryset = PropertyViews.objects.all()
    serializer_class = PropertyViewSerializer


class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.published.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]
    lookup_url_kwarg = "slug"
    lookup_field = "slug"

    def get_object(self):
        obj = super().get_object()

        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")

        if not PropertyViews.objects.filter(property=obj, ip=ip).exists():
            PropertyViews.objects.create(property=obj, ip=ip)

            obj.views += 1
            obj.save()

        return obj


class PropertyUpdateAPIView(generics.UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_url_kwarg = "slug"
    lookup_field = "slug"


class PropertyCreateAPIView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info(
            f"property {serializer.data.get('title')} created by {self.request.user.username}"
        )


class PropertyDeleteAPIView(generics.DestroyAPIView):
    queryset = Property.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_url_kwarg = "slug"
    lookup_field = "slug"


class PropertySearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        queryset = Property.published.all()
        data = request.data

        advert_type = data["advert_type"]
        queryset = queryset.filter(advert_type__iexact=advert_type)

        property_type = data["property_type"]
        queryset = queryset.filter(property_type__iexact=property_type)

        price = data["price"]
        if price == "$0+":
            price = 0
        elif price == "$50,000+":
            price = 50000
        elif price == "$100,000+":
            price = 100000
        elif price == "$200,000+":
            price = 200000
        elif price == "$400,000+":
            price = 400000
        elif price == "$600,000+":
            price = 600000
        elif price == "Any":
            price = -1

        if price != -1:
            queryset = queryset.filter(price__gte=price)

        bedrooms = data["bedrooms"]
        if bedrooms == "1+":
            bedrooms = 1
        elif bedrooms == "2+":
            bedrooms = 2
        elif bedrooms == "3+":
            bedrooms = 3
        elif bedrooms == "4+":
            bedrooms = 4
        elif bedrooms == "5+":
            bedrooms = 5

        queryset = queryset.filter(bedrooms__gte=bedrooms)

        bathrooms = data["bathrooms"]
        if bathrooms == "1+":
            bathrooms = 1
        elif bathrooms == "2+":
            bathrooms = 2
        elif bathrooms == "3+":
            bathrooms = 3
        elif bathrooms == "4+":
            bathrooms = 4
        elif bathrooms == "5+":
            bathrooms = 5

        queryset = queryset.filter(bathrooms__gte=bathrooms)

        catch_phrase = data["catch_phrase"]
        queryset = queryset.filter(description__icontains=catch_phrase)

        serializer = PropertySerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
