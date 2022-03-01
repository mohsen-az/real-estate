from django.urls import path

from apps.enquiries import views

app_name = "enquiries"

urlpatterns = [path("", views.SendEnquiryEmail.as_view(), name="send-enquiry")]
