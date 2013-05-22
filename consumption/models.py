from django.db import models

BILLING_MODEL = (
    # DIRECT. Starts inmediatly a Business Process that invokes the payment gateway and issues an invoice.
    ('DIRECT',   'Direct'),

    # POSTPAID. Build up billable events until billing period is ended, then a periodic business process is run.
    ('POSTPAID', 'Postpaid'),

    # PREPAID. Inmediately discount the product rate from the account cash. When no cash is available, a business process is run
    ('PREPAID',  'Prepaid'),
)

class Account(models.Model):
    code = models.CharField(max_length=20, primary_key=True)

class Provider(models.Model):
    code = models.CharField(max_length=10, primary_key=True)

    name = models.CharField(max_length=50)

class Product(models.Model):
    code = models.CharField(max_length=20, primary_key=True)

    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)

class PriceBookEntry(models.Model):
    price    = models.SmallIntegerField()
    provider = models.ForeignKey(Provider)

    billing_model = models.CharField(max_length=10, choices=BILLING_MODEL)

    start_date = models.DateTimeField(auto_now=True)
    active     = models.SmallIntegerField(default=0)

class Contract(models.Model):
    account = models.ForeignKey(Account)
    product = models.ForeignKey(Product)

    start_date = models.DateTimeField(auto_now=True)
    end_date   = models.DateTimeField(null=True)

class ProvisionEvent(models.Model):
    account = models.ForeignKey(Account)
    product = models.ForeignKey(Product)

    start_date = models.DateTimeField(auto_now=True)
    end_date   = models.DateTimeField(null=True)