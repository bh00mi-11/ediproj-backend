from django.core.mail import send_mail
from django.conf import settings

def send_match_email(to_email, case, matched_person):
    if not to_email or "@" not in to_email:
        print("❌ Invalid email, skipping mail")
        return False

    subject = "Missing Person Match Found"

    identity = matched_person.get('identity', 'Unknown')
    distance = matched_person.get('distance', 'N/A')

    message = f"""
Hello,

A facial match has been successfully verified.

📌 Submitted Case Details:
Name: {case.get('full_name')}
Age: {case.get('age')}
Gender: {case.get('gender')}
Birthdate: {case.get('birthdate')}
Contact (Provided): {case.get('contact_number')}
Last Seen: {case.get('last_seen_location')}

📷 Dataset Match Info:
Matched Image ID: {identity}
Similarity Score: {distance}

⚠️ Note:
The matched individual’s personal identity may not be fully available in the dataset.
Verification is based on facial similarity.

Please contact authorities for further investigation.

Regards,
AI Missing Person Portal
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )

    print("✅ Match email sent to:", to_email)
    return True


def send_no_match_email(to_email, case):
    if not to_email or "@" not in to_email:
        print("❌ Invalid email, skipping mail")
        return False

    subject = "Missing Person Verification Result"

    message = f"""
Hello,

We have completed the verification for the case you submitted.

📌 Submitted Case Details:
Name: {case.get('full_name')}
Age: {case.get('age')}
Gender: {case.get('gender')}
Birthdate: {case.get('birthdate')}
Contact (Provided): {case.get('contact_number')}
Last Seen: {case.get('last_seen_location')}

❌ Verification Result: No match found in the dataset.

Please contact authorities if you need further assistance.

Regards,
AI Missing Person Portal
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )

    print("✅ No-match email sent to:", to_email)
    return True
