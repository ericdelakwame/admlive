from django.conf import settings
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from blog.models import Comment, Post
from celery import shared_task
from django.contrib.auth import get_user_model

sendgrid_key = settings.SENDGRID_API_KEY
User = get_user_model()

@shared_task
def caution_comment_author(post_id):
    post = Post.objects.get(id=post_id)
    user = post.author
    post_date = post.created
    receipient = user.email
    mail_subject = 'Comment Removed'
    body = 'Dear {}, \n\n Your comment, posted on {} is in violation of ADM policy. Please be aware that any further occurences of such violation may result in termination of your membership on the site. Thank You'.format(
        user.first_name, post_date.strftime("%Y-%m-%d %H:%M:%S"))
    message = Mail(
        from_email='creativecharwey@gmail.com', to_emails=receipient,
        subject=mail_subject,
        html_content=body,

    )
    # message.dynamic_template_data = {

    #     'first_name': '{}'.format(user.first_name),
    # }
    # message.template_id = 'd-2c030ee2524846238e992e1329d19df0'
    try:
        sg = SendGridAPIClient(api_key=sendgrid_key)
        sg.send(message)
    except Exception as e:
        print(e)

    
