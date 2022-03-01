from django.core.mail import send_mail


def email_notification(
    subject, message, from_email, recipient_list, fail_silently=True
):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
    )
