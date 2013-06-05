from django.db import models

from common.constants.constants import ACTIVATION_STATUS, CHANNEL, COMPLETION_STATUS, DATE_FORMAT

class Account(models.Model):

    account_id  = models.CharField(max_length = 20, null=True, unique=True)
    email       = models.EmailField(null=True, unique=True)

    gender      = models.CharField(max_length = 100, null=True)

    first_name  = models.CharField(max_length = 100, null=True)
    last_name   = models.CharField(max_length = 100, null=True)

    city        = models.CharField(max_length = 100, null=True)
    address     = models.CharField(max_length = 200, null=True)
    postal_code = models.CharField(max_length = 10,  null=True)
    country     = models.CharField(max_length = 3,   null=True)
    phone       = models.CharField(max_length = 10,  null=True)

    channel     = models.CharField(max_length=10, choices=CHANNEL)

    def to_dict(self):
        return {
            'account_id':  self.account_id,
            'email':       self.email,

            'first_name':  self.first_name,
            'last_name':   self.last_name,

            'city':        self.city,
            'address':     self.address,
            'postal_code': self.postal_code,
            'phone':       self.phone,
            'country':     self.country,

            'channel':     self.channel
        }

class Contract(models.Model):

    account     = models.ForeignKey('Account')
    subprocess  = models.ForeignKey('processes.SubProcess', null=True)

    contract_id = models.CharField(max_length = 20, null=True)
    tos         = models.URLField(max_length = 200)
    sign_date   = models.DateTimeField()
    start_date  = models.DateTimeField()
    end_date    = models.DateTimeField(null=True)

    status = models.CharField(max_length=10, choices=ACTIVATION_STATUS, default='PENDING')

    def to_dict(self):
        return {
            'account_id':  self.account.account_id,
            'subprocess':  self.subprocess.id,

            'contract_id': self.contract_id,
            'tos':         self.tos,
            'sign_date':   self.sign_date.strftime(DATE_FORMAT),
            'start_date':  self.start_date.strftime(DATE_FORMAT),
            'end_date':    None if not self.end_date else self.end_date.strftime(DATE_FORMAT),

            'status':      self.status,
        }
    
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