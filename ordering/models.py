from django.db import models
from django.contrib import admin

from common.constants.constants import COMPLETION_STATUS, SUBSCRIPTION_STATUS, BILLING_TYPE, DATE_FORMAT

from customers.models import BillingAddress

from django.core.files.base import File

class Order(models.Model):
    total  = models.IntegerField()
    vat    = models.IntegerField()
    amount = models.IntegerField()

    currency = models.CharField(max_length = 3)
    country  = models.CharField(max_length = 3)

    order_code  = models.CharField(max_length=10)

    date = models.DateTimeField(auto_now=True)

    account        = models.ForeignKey('customers.Account')
    payment_method = models.ForeignKey('payment_gateways.PaymentMethod', null=True)

    status = models.CharField(max_length=10, choices=COMPLETION_STATUS, default='PENDING')

    def __unicode__(self):
        return self.order_code

    def to_dict(self):
        return {
            'total':        self.total,
            'currency':     self.currency,
            'country':      self.country,
            'order_code' :  self.order_code
        }

    def to_dict_for_revenue_report(self):

        invoice = Invoice.objects.get(order=self)
        billing = BillingAddress.objects.get(account=self.account)

        return {
            'A': invoice.invoice_code,
            'B': invoice.date.strftime(DATE_FORMAT),
            'C': billing.get_full_name(),
            'D': '',
            'E': self.amount,
            'F': self.vat,
            'G': self.total,
        }

class LineItem(models.Model):
    order    = models.ForeignKey('Order')
    product  = models.ForeignKey('Product')
    quantity = models.FloatField()

    def __unicode__(self):
        return unicode(self.order)

    def to_dict(self):
        return {
            'product':     self.product.code,
            'price':       self.product.price,
            'description': self.product.desc,
            'quantity' :   self.quantity
        }

class Product(models.Model):
    code = models.CharField(max_length=20, primary_key=True)

    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)

    type = models.CharField(max_length=10, choices=BILLING_TYPE, default='ONE SHOT')

    price = models.FloatField()

    def __unicode__(self):
        return self.code

    def create_subscription(self, account, payment_method):
        if self.type != 'RECURRENT':
            return None

        subs = Subscription(account=account, payment_method=payment_method, product=self)
        subs.save()

        return subs

class Subscription(models.Model):
    account = models.ForeignKey('customers.Account')
    payment_method = models.ForeignKey('payment_gateways.PaymentMethod', null=True)

    status  = models.CharField(max_length=10, choices=SUBSCRIPTION_STATUS, default='ACTIVE')
    product = models.ForeignKey('Product')

    def __unicode__(self):
        return unicode(self.account) + " " + unicode(self.product)

class Invoice(models.Model):
    invoice_code = models.CharField(max_length=20, unique=True)
    file_name    = models.CharField(max_length=50)

    order = models.ForeignKey('Order')

    content = models.FileField(upload_to='invoices')

    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.invoice_code)

    def set_content(self, name, file):
        self.content.save(name, File(file))
        self.save()

admin.site.register(Subscription)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(LineItem)
admin.site.register(Invoice)