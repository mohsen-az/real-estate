from apps.enquiries.serializers import EnquirySerializer


def test_enquiry_serializer(enquiry):
    expected_serialized_data = {
        'name': enquiry.name,
        'phone_number': enquiry.phone_number,
        'email': enquiry.email,
        'subject': enquiry.subject,
        'message': enquiry.message
    }
    serializer = EnquirySerializer(instance=enquiry)
    assert serializer.data == expected_serialized_data
