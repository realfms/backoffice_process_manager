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
Created on 15/10/2012

@author: mac@tid.es
'''

from celery import task

from customers.models          import Order, Account
from payment_gateways.services import PaymentGatewayManager

from processes.task_manager import TaskManager

from common.distributed.distributed import compute_uuid

@task(ignore_result=True)
def charge_user_task(success, sp_id):
    tm = TaskManager()

    data = tm.get_subprocess_data(sp_id)

    return tm.process_task(sp_id, 'CHARGING',success, lambda : charge_user(data))

def charge_user(json):
    customer_data = json['customer']

    total    = int(json['total'] * 100)
    currency = 'EUR'

    account_id  = customer_data['tef_account']
    country     = customer_data['country']
    order_code  = compute_uuid()
    
    account = Account.objects.get(account_id=account_id)

    order = Order(account=account, total=total, currency=currency, country=country, order_code=order_code, payment_method=None)
    order.save()

    PaymentGatewayManager().process_recurrent_payment(order)

    return (json, None)