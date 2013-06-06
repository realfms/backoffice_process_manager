#!/usr/bin/python
# coding=utf-8

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
Created on 01/06/2013

@author: mac@tid.es
'''

from django.db import models

from common.constants.constants import ACTIVATION_STATUS, CHANNEL, COMPLETION_STATUS, DATE_FORMAT

class Account(models.Model):

    account_id = models.CharField(max_length = 20, null=True, unique=True)

    email   = models.EmailField(null=True, unique=True)
    channel = models.CharField(max_length=10, choices=CHANNEL)

    gender  = models.CharField(max_length=100, null=True)

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'email':      self.email,
            'channel':    self.channel,
            'gender' :    self.gender
        }

class BillingAddress(models.Model):

    account = models.ForeignKey('Account')

    first_name  = models.CharField(max_length = 100)
    last_name   = models.CharField(max_length = 100)

    city        = models.CharField(max_length = 100)
    address     = models.CharField(max_length = 200)
    postal_code = models.CharField(max_length = 10)
    country     = models.CharField(max_length = 3)
    phone       = models.CharField(max_length = 10, null=True)

    def to_dict(self):
        return {
            'account_id':  self.account.account_id,

            'first_name':  self.first_name,
            'last_name':   self.last_name,

            'city':        self.city,
            'address':     self.address,
            'postal_code': self.postal_code,
            'phone':       self.phone,
            'country':     self.country,
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