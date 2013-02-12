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
from charging.charging   import charge_user

from django.utils import simplejson

from common.salesforce.salesforce import update_contact

from models import Task, SubProcess

######################################################
# DATA ACQUISITION
######################################################

@task(ignore_result=True)
def notify_salesforce_task(success, status, contact_id, sp_id):
    return process_task(sp_id, 'NOTIFY SALESFORCE', success, lambda : update_contact(status, contact_id))

@task(ignore_result=True)
def notify_tef_accounts_task(success, status, contact_id, sp_id):
    return (True, None)


######################################################
# RECURRENT CHARGING
######################################################

@task(ignore_result=True)
def payment_gateway_invocation_task(charging_result):
    return charging_result

######################################################
# ORDER TO CASH
######################################################

@task(ignore_result=True)
def download_and_parse_sdr_task(success, bucket_key, sp_id):
    return process_task(sp_id, 'RATING', success, lambda : download_and_parse_sdr(bucket_key))

@task(ignore_result=True)
def generate_pdf_and_upload_task(success, sp_id):
    return process_task(sp_id, 'INVOICING', success, lambda : generate_pdf_and_upload(_get_subprocess_data(sp_id)))

@task(ignore_result=True)
def get_customer_details_from_sf_task(success, sp_id):
    return process_task(sp_id, 'CUSTOMER DATA', success, lambda : customer_details_from_sf(_get_subprocess_data(sp_id)))

@task(ignore_result=True)
def charge_user_task(success, sp_id):
    return process_task(sp_id, 'CHARGING',success, lambda : charge_user(_get_subprocess_data(sp_id)))

@task(ignore_result=True)
def send_email_task(success, sp_id):
    return process_task(sp_id, 'SENDING EMAIL', success, lambda : send_email(_get_subprocess_data(sp_id)))

######################################################
# COLLECTIONS TASKS
######################################################

@task(ignore_result=True)
def update_charging_result(charging_result):
    return charging_result

@task(ignore_result=True)
def create_financial_accounting_record(json):
    return json

######################################################
# AUX FUNCTIONS
######################################################

def _generate_task(sp_id, name):
    subprocess = SubProcess.objects.get(id=sp_id)

    task = Task(subprocess=subprocess, name=name)
    task.save()

    return task

def _get_subprocess_data(sp_id):
    subproccess = SubProcess.objects.get(id=sp_id)
    
    return simplejson.loads(subproccess.result)

def process_task(sp_id, name, success, fn):
    
    if not success:
        return False
    
    try:
        task = _generate_task(sp_id, name)
        
        (result, remarkable_data) = fn()
        
        task.set_now_as_end()
        task.set_remarkable_data(remarkable_data)
        task.set_result(simplejson.dumps(result))
        task.set_status('OK')

        task.save()

        return True
    except Exception as e:  
        
        trace = {
                  'type': type(e),
                  'args': e.args,
                  'text': unicode(e)
                  }
        
        if (task):
            try:
                task.set_remarkable_data(trace)
                task.set_status('ERROR')
                
                task.save()
            except:
                pass
        
        # Writing log
        print "### LOG ### {0} cloud't be processed! {1} {2} {3}".format(name, type(e), e.args, unicode(e))
        
        return False

