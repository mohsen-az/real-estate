from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/profile/", include("apps.profiles.urls", namespace="profiles")),
    path("api/v1/property/", include("apps.properties.urls", namespace="properties")),
    path("api/v1/rating/", include("apps.ratings.urls", namespace="ratings")),
    path("api/v1/enquiry/", include("apps.enquiries.urls", namespace="enquiries")),
]

admin.site.site_header = "Real Estate Admin"
admin.site.title = "Real Estate Admin Portal"
admin.site.index_title = "Welcome to the Real Estate Portal"
