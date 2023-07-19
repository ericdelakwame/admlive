from celery import shared_task
from sendgrid.helpers.mail import Mail
from django.contrib.auth import get_user_model
from sendgrid import SendGridAPIClient
from django.conf import settings
from orders.models import Order
sendgrid_api_key = settings.SENDGRID_API_KEY


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    first_name= order.first_name
    last_name = order.last_name
    recipient = order.email
    tel_no = order.tel_no
    mail_subject = 'Your order has been received'
    body = 'Dear {}, \n\n Your order is being processed. You will receive an update from the vendor regarding deliveries. Thank You'.format(first_name)
    message = Mail(
        from_email='simoncharwey@gmail.com',
        to_emails=recipient,
        subject=mail_subject,
        html_content=body
    )
    message.dynamic_template_data = {
        'first_name': '{}'.format(first_name),
    }
    message_template_id = ''
    try:
        sg =SendGridAPIClient(api_key=sendgrid_api_key)
        sg.send(message)
    except Exception as e:
        print(e)
         


