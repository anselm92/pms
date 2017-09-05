from celery.task import task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from pms.settings import SITE


@task(name="send_mail")
def send_async(subject, content, address):
    email = EmailMultiAlternatives('Subject', subject)
    email.subject = subject
    email.attach_alternative(content, "text/html")
    email.to = [address]
    return email.send()


class Email(object):
    subject = 'Subject'
    template_name = ''
    order = None
    subscription = None

    def send(self):
        c = {'order': self.order, 'subscription': self.subscription, 'site': SITE}
        html_content = render_to_string(self.template_name, c)
        send_async.delay(self.subject, html_content, self.subscription.customer.mail_address)

    def get_object(self):
        return self.order


class CommentEmail(Email):
    def __init__(self, order, subscription):
        self.order = order
        self.subscription = subscription
        self.subject = f'New comment for order {order}'
        self.template_name = 'printing/mail/new_comment.html'


class OrderReceivedEmail(Email):
    def __init__(self, order, subscription):
        self.order = order
        self.subscription = subscription
        self.subject = f'Thanks for your order {order}'
        self.template_name = 'printing/mail/order_received.html'
