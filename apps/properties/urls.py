from django.urls import path

from apps.properties import views

app_name = "properties"

urlpatterns = [
    path("list/", views.PropertyListAPIView.as_view(), name="property-list"),
    path(
        "agent/list/", views.AgentPropertyListAPIView.as_view(), name="agent-properties"
    ),
    path("create/", views.PropertyCreateAPIView.as_view(), name="property-create"),
    path(
        "detail/<slug:slug>/",
        views.PropertyDetailAPIView.as_view(),
        name="property-detail",
    ),
    path(
        "update/<slug:slug>/",
        views.PropertyUpdateAPIView.as_view(),
        name="property-update",
    ),
    path(
        "delete/<slug:slug>/",
        views.PropertyDeleteAPIView.as_view(),
        name="property-delete",
    ),
    path("search/", views.PropertySearchAPIView.as_view(), name="property-search"),
]
