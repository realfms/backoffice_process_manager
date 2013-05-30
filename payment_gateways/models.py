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

from processes.models import SubProcess

STATUS = (
    ('PENDING',   'PENDING'),
    ('VALIDATED', 'VALIDATED'),
    ('ERROR',     'ERROR'),
    ('CANCELED',  'CANCELED'),
)

CHANNEL = (
    ('ONLINE',       'ONLINE'),
    ('DIRECT_SALES', 'DIRECT_SALES'),
)

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

class PaymentMethod(models.Model):

    gateway = models.ForeignKey(PaymentGateway)
    account = models.CharField(max_length = 20)
    
    recurrent_order_code = models.CharField(max_length=10)
    
    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')

class Order(models.Model):

    total    = models.IntegerField()
    currency = models.CharField(max_length = 3)
    country  = models.CharField(max_length = 3)
    
    order_code  = models.CharField(max_length=10)
    account     = models.CharField(max_length = 20)

    statement = models.CharField(max_length = 200)

    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')
    result = models.TextField()

    payment_method = models.ForeignKey(PaymentMethod)

class Contract(models.Model):

    account     = models.ForeignKey(Account)
    subprocess  = models.ForeignKey(SubProcess, null=True)

    contract_id = models.CharField(max_length = 20, null=True)
    tos         = models.URLField(max_length = 200)
    sign_date   = models.DateTimeField()
    start_date  = models.DateTimeField()
    end_date    = models.DateTimeField(null=True)

    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')