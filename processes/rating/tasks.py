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

from rating                 import download_and_parse_sdr, rate_from_order
from processes.task_manager import TaskManager

from common.distributed.distributed import compute_uuid

from customers.models import Account
from ordering.models  import Order


@task(ignore_result=True)
def download_and_parse_sdr_task(success, bucket_key, tef_account, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'RATING', success, lambda : download_and_parse_sdr(bucket_key, tef_account))

@task(ignore_result=True)
def rate_from_order_task(success, order, line_items, billing_address, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'RATING', success, lambda : rate_from_order(order, line_items, billing_address))

@task(ignore_result=True)
def create_order_task(success, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'RATING', success, lambda : create_order(tm.get_subprocess_data(sp_id)))

def create_order(json):
    # Rating an SDR file
    customer_data = json['customer']

    total    = int(json['total'] * 100)
    currency = 'EUR'

    account_id  = customer_data['tef_account']
    country     = customer_data['country']
    order_code  = compute_uuid()

    account = Account.objects.get(account_id=account_id)

    order = Order(account=account, total=total, currency=currency, country=country, order_code=order_code, payment_method=None)
    order.save()

    json['order'] = order.to_dict()

    return (json, None)
