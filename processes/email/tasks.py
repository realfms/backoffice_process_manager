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

from email import send_email
from processes.task_manager import TaskManager

from common.aws.constants import EMAIL_FROM, INVOCE_EMAIL_TITLE, INVOICE_EMAIL_BODY, COLLECTIONS_EMAIL_BODY, COLLECTIONS_EMAIL_TITLE

@task(ignore_result=True)
def send_invoice_email_task(success, sp_id):
    tm = TaskManager()

    json = tm.get_subprocess_data(sp_id)

    customer_email = json['customer']['email']
    file_name      = json['pdf_file_name']

    return tm.process_task(sp_id, 'SENDING EMAIL', success, lambda : send_email(INVOCE_EMAIL_TITLE, INVOICE_EMAIL_BODY, EMAIL_FROM, customer_email, file_name, 'application/pdf', json))

@task(ignore_result=True)
def send_collections_email_task(success, customer_email, sp_id):
    tm = TaskManager()

    json = tm.get_subprocess_data(sp_id)

    file_name = json['file_name']

    return tm.process_task(sp_id, 'SENDING EMAIL', success, lambda : send_email(COLLECTIONS_EMAIL_TITLE, COLLECTIONS_EMAIL_BODY, EMAIL_FROM, customer_email, file_name, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', json))
