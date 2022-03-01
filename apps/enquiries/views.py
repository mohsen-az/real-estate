from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.enquiries.models import Enquiry
from apps.enquiries.serializers import EnquirySerializer
from apps.enquiries.utils.notification import email_notification
from config.settings.development import DEFAULT_FROM_EMAIL


class SendEnquiryEmail(generics.CreateAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        data = self.request.data
        try:
            email_notification(
                subject=data["subject"],
                message=data["message"],
                from_email=data["email"],
                recipient_list=[DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception:
            return Response({"fail": "Enquiry was not sent. Please try again"})
        else:
            serializer.save()
