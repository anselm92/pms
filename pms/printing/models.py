from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    first_name = models.CharField(max_length=99)
    last_name = models.CharField(max_length=99)
    mail_address = models.CharField(max_length=99)


class StaffCustomer(Customer):
    user = models.ForeignKey(User)


class CostCenter(models.Model):
    name = models.CharField(max_length=99)


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
    # TODO: File path?
    customer = models.ForeignKey(Customer)
    status = models.SmallIntegerField(choices=ORDER_STATUS, default=ORDER_STATUS_OPEN)


class Material(models.Model):
    name = models.CharField(max_length=99)
    color_code = models.CharField(max_length=99)
    cost_per_unit = models.FloatField()


class Comment(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class StaffComment(Comment):
    user = models.ForeignKey(User)
    public = models.BooleanField(default=False)


class ExternalComment(Comment):
    customer = models.ForeignKey(Customer)
