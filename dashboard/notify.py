from django.conf import settings
from fcm_django.models import FCMDevice

import firebase_admin
from firebase_admin import messaging, credentials

firebase_credentials = credentials.Certificate(
    settings.GOOGLE_APPLICATION_CREDENTIALS)
firebase_app = firebase_admin.initialize_app(firebase_credentials)


def get_fcm_token():
    token = firebase_app.credential.get_access_token()
    print(token)
    return token


def subscribe_news(tokens):  # tokens is a list of registration tokens
    tokens = get_fcm_token()
    topic = 'African Design Matters News'
    response = messaging.subscribe_to_topic(tokens, topic)
    if response.failure_count > 0:
        print(
            f'Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason, response.errors))}')
    print(response)



def send_topic_push(title, body):
    tokens = get_fcm_token()
    subscribe_news(tokens)
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        topic= 'African Design Matters News'
    )
    messaging.send(message)
    print('success')
