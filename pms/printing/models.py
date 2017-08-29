import secrets

from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    first_name = models.CharField(max_length=99)
    last_name = models.CharField(max_length=99)
    mail_address = models.EmailField()

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class StaffCustomer(Customer):
    user = models.ForeignKey(User)


class ExternalCustomer(Customer):
    order_token = models.CharField(max_length=30)


class CostCenter(models.Model):
    name = models.CharField(max_length=99)

    def __str__(self):
        return self.name


ORDER_STATUS_OPEN = 1
ORDER_STATUS_IN_PROGRESS = 2
ORDER_STATUS_DENIED = 3
ORDER_STATUS_PRINTING = 4
ORDER_STATUS_DONE = 5
ORDER_STATUS = ((ORDER_STATUS_OPEN, 'Open'),
                (ORDER_STATUS_IN_PROGRESS, 'In Progress'),
                (ORDER_STATUS_DENIED, 'Denied'),
                (ORDER_STATUS_PRINTING, 'Printing'),
                (ORDER_STATUS_DONE, 'Done'),)


class Order(models.Model):
    title = models.CharField(max_length=99)
    amount = models.IntegerField()
    order_hash = models.CharField(max_length=20, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # TODO: File path?
    customer = models.ForeignKey(Customer)
    status = models.SmallIntegerField(choices=ORDER_STATUS, default=ORDER_STATUS_OPEN)
    assignee = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.order_hash is None or len(self.order_hash) == 0:
            self.order_hash = secrets.token_urlsafe(20)
        models.Model.save(self, force_insert, force_update, using, update_fields)


class Material(models.Model):
    name = models.CharField(max_length=99)
    color_code = models.CharField(max_length=99)
    cost_per_unit = models.FloatField()  # Cost in Euros

    def __str__(self):
        return self.name


class Comment(models.Model):
    order = models.ForeignKey(Order)
    create_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.text


class StaffComment(Comment):
    user = models.ForeignKey(User)


class ExternalComment(Comment):
    customer = models.ForeignKey(Customer)


class Subscription(models.Model):
    customer = models.ForeignKey(Customer)
    order = models.ForeignKey(Order)
    token = models.CharField(max_length=30, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.token is None or len(self.token) == 0:
            self.token = secrets.token_urlsafe(20)
        models.Model.save(self, force_insert, force_update, using, update_fields)


class OrderHistoryEntry(models.Model):
    order = models.ForeignKey(Order)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class OrderHistoryStaffEntry(OrderHistoryEntry):
    user = models.ForeignKey(User)


class OrderHistoryExternalEntry(OrderHistoryEntry):
    customer = models.ForeignKey(Customer)
