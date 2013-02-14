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
 
from rating.rating       import download_and_parse_sdr
from pdf.invoice         import generate_pdf_and_upload
from customer.salesforce import customer_details_from_sf
from email.email         import send_email

from task_manager import TaskManager


######################################################
# ORDER TO CASH
######################################################

@task(ignore_result=True)
def download_and_parse_sdr_task(success, bucket_key, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'RATING', success, lambda : download_and_parse_sdr(bucket_key))

@task(ignore_result=True)
def generate_pdf_and_upload_task(success, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'INVOICING', success, lambda : generate_pdf_and_upload(tm.get_subprocess_data(sp_id)))

@task(ignore_result=True)
def get_customer_details_from_sf_task(success, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'CUSTOMER DATA', success, lambda : customer_details_from_sf(tm.get_subprocess_data(sp_id)))

@task(ignore_result=True)
def send_email_task(success, sp_id):
    tm = TaskManager()
    return tm.process_task(sp_id, 'SENDING EMAIL', success, lambda : send_email(tm.get_subprocess_data(sp_id)))

######################################################
# COLLECTIONS TASKS
######################################################

@task(ignore_result=True)
def update_charging_result(charging_result):
    return charging_result

@task(ignore_result=True)
def create_financial_accounting_record(json):
    return json
