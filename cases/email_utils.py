from django.core.mail import send_mail
from django.conf import settings

def send_match_email(to_email, person):
    send_mail(
        subject="Missing Person Match Found",
        message=f"""
Match Found!

Name: {person['full_name']}
Age: {person['age']}
Last Seen: {person['last_seen_location']}
Contact: {person['contact']}
        """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
