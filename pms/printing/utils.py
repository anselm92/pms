from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from pms.settings import SITE


class Email(object):
    subject = 'Subject'
    template_name = ''
    order = None
    subscription = None

    def send(self):
        c = {'order': self.order, 'subscription': self.subscription, 'site': SITE}
        html_content = render_to_string(self.template_name, c)
        email = EmailMultiAlternatives('Subject', self.subject)
        email.subject = self.subject
        email.attach_alternative(html_content, "text/html")
        email.to = [self.subscription.customer.mail_address]
        email.send()

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
