def test_enquiry_representation(enquiry):
    return enquiry.__str__() == enquiry.email