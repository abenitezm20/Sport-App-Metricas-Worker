from sqs_service_provider import SqsClientNotification

class Notificator:
    @staticmethod
    def user_notification(data):
        try:
            SqsClientNotification.enqueue(data)
        except Exception as e:
            print('notification error: ', e)