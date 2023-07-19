from celery import shared_task
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from django.conf import settings
from twilio.rest import Client
from django.contrib.auth import get_user_model

sendgrid_key = settings.SENDGRID_API_KEY
twilio_number = settings.TWILIO_NUMBER
User = get_user_model()
from fcm_django.models import FCMDevice


@shared_task
def welcome_user(user_id):
    user = User.objects.get(id=user_id)
    receipient = user.email
    mail_subject = 'Welcome To African Design Matters'
    body = 'Dear {}, \n\n Your registration was successful. Please sign in with your credentials and discover another world of design. Thank You'.format(
        user.first_name)
    message = Mail(
        from_email='creativecharwey@gmail.com', to_emails=receipient,
        subject=mail_subject,
        html_content=body,

    )
    message.dynamic_template_data = {

        'first_name': '{}'.format(user.first_name),
    }
    message.template_id = 'd-2c030ee2524846238e992e1329d19df0'
    try:
        sg = SendGridAPIClient(api_key=sendgrid_key)
        sg.send(message)
    except Exception as e:
        print(e)


@shared_task()
def send_welcome_sms(user_id):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    user = User.objects.get(id=user_id)
    first_name = user.first_name
    client = Client(account_sid, auth_token)
    message = client.messages.create(
            body='Welcome {}'.format(first_name),
            from_= twilio_number,
            to=user.tel_no.as_e164
        )


    print(message.sid)
    
