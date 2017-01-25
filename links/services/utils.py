from django.core.mail import EmailMessage


def send_created_user_email(password):
    message = 'You can login the Knowledge admin with your username: \'Your first name\' and password: ' + password
    email = EmailMessage('Knowledge Email', message, to=[author.email])
    email.send()
