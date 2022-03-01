from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from apps.profiles.models import Profile
from apps.profiles.renderers import ProfileJSONRenderer
from apps.profiles.serializers import (ProfileSerializer,
                                       UpdateProfileSerializer)


class CommonProfileAPIView:
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]


class GetProfileAPIView(generics.RetrieveAPIView, CommonProfileAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        user = self.request.user
        try:
            obj = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise ValidationError(
                code=404, detail=_("The requested profile does not exist.")
            )
        self.check_object_permissions(self.request, obj)
        return obj


class UpdateProfileAPIView(generics.UpdateAPIView, CommonProfileAPIView):
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        user = self.request.user
        try:
            obj = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise ValidationError(
                code=404, detail=_("The requested profile does not exist.")
            )
        self.check_object_permissions(self.request, obj)
        return obj


class AgentListAPIView(generics.ListAPIView):
    queryset = Profile.objects.filter(is_agent=True)
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class TopAgentListAPIView(generics.ListAPIView):
    queryset = Profile.objects.filter(top_agent=True)
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
