from django.core.mail import send_mail


def send_user_password_to_mail(email, password):
    send_mail(subject='Password', message=password, from_email='info@andys.md',
              recipient_list=[email])


def send_change_request_notification(*args, **kwargs):
    send_mail(subject='Password', message="New Change Password Request", from_email='info@andys.md',
              recipient_list=[args[0].username])


def send_change_password_email(to: str, token: str):
    send_mail(subject='Password', message=f"Token for changing password {token}", from_email='info@andys.md',
              recipient_list=[to])


def send_change_request_decline_notification(to: str):
    send_mail(subject='Password', message="You change password request was declined", from_email='info@andys.md',
              recipient_list=[to])
