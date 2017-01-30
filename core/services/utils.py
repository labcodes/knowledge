from django.core.mail import EmailMessage


def send_created_user_email(password, email):
    message = 'You can login the Knowledge admin with your username: \'Your email\' and password: ' + password
    email = EmailMessage('Knowledge Email', message, to=[email])
    email.send()
