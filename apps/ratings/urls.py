from django.urls import path

from apps.ratings import views

app_name = "ratings"

urlpatterns = [
    path(
        "<str:profile_id>/",
        views.CreateAgentReviewAPIView.as_view(),
        name="create-rating",
    )
]
