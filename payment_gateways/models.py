#!/usr/bin/python
#coding=utf-8 

"""
Copyright 2012 Telefonica Investigación y Desarrollo, S.A.U

This file is part of Billing_PoC.

Billing_PoC is free software: you can redistribute it and/or modify it under the terms 
of the GNU Affero General Public License as published by the Free Software Foundation, either 
version 3 of the License, or (at your option) any later version.
Billing_PoC is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even 
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero 
General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with Billing_PoC. 
If not, see http://www.gnu.org/licenses/.

For those usages not covered by the GNU Affero General Public License please contact with::mac@tid.es
""" 

'''
Created on 16/10/2012

@author: mac@tid.es
'''

from django.db import models
from django.contrib import admin

from common.constants.constants import ACTIVATION_STATUS, DATE_FORMAT

class PaymentGateway(models.Model):

    name = models.CharField(max_length = 100)

    endpoint = models.CharField(max_length = 200)

    success_callback = models.CharField(max_length = 200)
    error_callback   = models.CharField(max_length = 200)
    pending_callback = models.CharField(max_length = 200)

    merchant = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)

    module_name = models.CharField(max_length = 200)
    class_name  = models.CharField(max_length = 50)
    
    country    = models.CharField(max_length = 3)

    def __unicode__(self):
        return self.name


class PaymentMethod(models.Model):

    gateway = models.ForeignKey('PaymentGateway')
    account = models.ForeignKey('customers.Account')

    mask = models.CharField(max_length=20, null=True)

    month = models.IntegerField(null=True)
    year  = models.IntegerField(null=True)
    
    recurrent_order_code = models.CharField(max_length=10)
    
    status = models.CharField(max_length=10, choices=ACTIVATION_STATUS, default='PENDING')

    def __unicode__(self):
        return self.mask if self.mask else self.recurrent_order_code

    def to_dict(self):
        return {
            'id':         self.id,
            'mask':       self.mask,
            'expiration': None if not self.month else "{0}/{1}".format(self.month, self.year)
        }

admin.site.register(PaymentMethod)
admin.site.register(PaymentGateway)