from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    first_name = models.CharField(max_length=99)
    last_name = models.CharField(max_length=99)
    mail_address = models.CharField(max_length=99)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class StaffCustomer(Customer):
    user = models.ForeignKey(User)


class ExternalCustomer(Customer):
    pass


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
    # TODO: File path?
    customer = models.ForeignKey(Customer)
    status = models.SmallIntegerField(choices=ORDER_STATUS, default=ORDER_STATUS_OPEN)

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.text


class StaffComment(Comment):
    user = models.ForeignKey(User)
    public = models.BooleanField(default=False)


class ExternalComment(Comment):
    customer = models.ForeignKey(Customer)
