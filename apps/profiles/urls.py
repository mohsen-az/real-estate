from django.urls import path

from apps.profiles import views

app_name = "profiles"

urlpatterns = [
    path("me/", views.GetProfileAPIView.as_view(), name="get-profile"),
    path("update/", views.UpdateProfileAPIView.as_view(), name="update-profile"),
    path("agent/list/", views.AgentListAPIView.as_view(), name="agent-list"),
    path("top-agent/list/", views.TopAgentListAPIView.as_view(), name="top-agent-list"),
]
