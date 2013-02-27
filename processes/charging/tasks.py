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

from payment_gateways.api_format import OrderData
from payment_gateways.services   import ServiceManager

from processes.task_manager import TaskManager

import uuid

@task(ignore_result=True)
def charge_user_task(success, sp_id):
    tm = TaskManager()

    data = tm.get_subprocess_data(sp_id)

    return tm.process_task(sp_id, 'CHARGING',success, lambda : charge_user(data))

def charge_user(json):
    customer_data = json['customer']

    total    = int(json['total'] * 100)
    currency = 'EUR'

    tef_account = customer_data['tef_account']
    country     = customer_data['country']
    statement   = "statement"
    order_code  = compute_order_id()

    print order_code

    data = OrderData(tef_account, total, currency, country, statement, order_code)

    ServiceManager().process_recurrent_payment(data)

    return (json, None)

# TODO: Guarantee uid is unique among different nodes if this code is distributed
def compute_order_id():
    uid = uuid.uuid4()

    # Order = ten first characters of uuid
    return uid.hex[:10]