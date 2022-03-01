from rest_framework import serializers

from apps.enquiries.models import Enquiry


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = ["name", "phone_number", "email", "subject", "message"]
