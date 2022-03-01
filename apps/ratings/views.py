from uuid import UUID

from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from apps.profiles.models import Profile
from apps.ratings.models import Rating
from apps.ratings.serializers import RatingSerializer


class CreateAgentReviewAPIView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            profile_id = UUID(self.kwargs.get("profile_id"), version=4)
        except (AttributeError, ValueError):
            raise ValidationError(code=403, detail=_("The profile id is not valid."))

        try:
            agent_profile = Profile.objects.get(id=profile_id, is_agent=True)
        except Profile.DoesNotExist:
            raise ValidationError(
                code=404, detail=_("The requested profile does not exist.")
            )

        if agent_profile.user == self.request.user:
            raise ValidationError(code=403, detail=_("You can't rate yourself"))

        already_exists = agent_profile.agent_review.filter(
            agent__pkid=agent_profile.user.pkid
        )

        if already_exists.exists():
            raise ValidationError(code=400, detail=_("Profile already reviewed"))

        serializer.save(rater=self.request.user, agent=agent_profile)

        total_reviews = agent_profile.agent_review.all()
        length_total_reviews = len(total_reviews)
        agent_profile.reviews = length_total_reviews

        total = 0
        for review in total_reviews:
            total += review.rating

        agent_profile.rating = round(total / length_total_reviews, 2)
        agent_profile.save()
