from django.db import models

from common.constants.constants import ACTIVATION_STATUS, CHANNEL, COMPLETION_STATUS

class Account(models.Model):

    account_id  = models.CharField(max_length = 20, null=True)
    email       = models.EmailField()

    gender      = models.CharField(max_length = 100, null=True)

    first_name  = models.CharField(max_length = 100, null=True)
    last_name   = models.CharField(max_length = 100, null=True)

    city        = models.CharField(max_length = 100, null=True)
    address     = models.CharField(max_length = 200, null=True)
    postal_code = models.CharField(max_length = 10,  null=True)
    country     = models.CharField(max_length = 3,   null=True)
    phone       = models.CharField(max_length = 10,  null=True)

    channel     = models.CharField(max_length=10, choices=CHANNEL)

class Contract(models.Model):

    account     = models.ForeignKey('Account')
    subprocess  = models.ForeignKey('processes.SubProcess', null=True)

    contract_id = models.CharField(max_length = 20, null=True)
    tos         = models.URLField(max_length = 200)
    sign_date   = models.DateTimeField()
    start_date  = models.DateTimeField()
    end_date    = models.DateTimeField(null=True)

    status = models.CharField(max_length=10, choices=ACTIVATION_STATUS, default='PENDING')
    
class Order(models.Model):

    total    = models.IntegerField()
    currency = models.CharField(max_length = 3)
    country  = models.CharField(max_length = 3)
    
    order_code  = models.CharField(max_length=10)
    
    account        = models.ForeignKey('Account')
    payment_method = models.ForeignKey('payment_gateways.PaymentMethod', null=True)

    status = models.CharField(max_length=10, choices=COMPLETION_STATUS, default='PENDING')

class Product(models.Model):
    code = models.CharField(max_length=20, primary_key=True)

    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)