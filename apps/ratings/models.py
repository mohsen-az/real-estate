from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel
from apps.profiles.models import Profile

User = get_user_model()


class Range(models.IntegerChoices):
    POOR = (1, _("Poor"))
    FAIR = (2, _("Fair"))
    GOOD = (3, _("Good"))
    VERY_GOOD = (4, _("Very Good"))
    EXCELLENT = (5, _("Excellent"))


class Rating(TimeStampedUUIDModel):
    rater = models.ForeignKey(
        User,
        verbose_name=_("User providing the rating"),
        on_delete=models.SET_NULL,
        related_name="rater_review",
        null=True,
    )
    agent = models.ForeignKey(
        Profile,
        verbose_name=_("Agent being rated"),
        on_delete=models.SET_NULL,
        related_name="agent_review",
        null=True,
    )
    rating = models.IntegerField(
        verbose_name=_("Rating"),
        choices=Range.choices,
        help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent",
        default=0,
    )
    comment = models.TextField(verbose_name=_("Comment"))

    class Meta:
        unique_together = ["rater", "agent"]

    def __str__(self):
        return f"{self.agent} rated at {self.rating}"
