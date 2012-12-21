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

@task(ignore_result=True)
def download_and_parse_sdr_task(bucket_key):
    return download_and_parse_sdr(bucket_key)

@task(ignore_result=True)
def generate_pdf_and_upload_task(invoiceJson):
    return generate_pdf_and_upload(invoiceJson)

@task(ignore_result=True)
def get_customer_details_from_sf_task(json):
    return customer_details_from_sf(json)

@task(ignore_result=True)
def uploadOrderLineToSalesForce(json):
    #TODOOOOO!
    return json

@task(ignore_result=True)
def send_email_task(json):
    return send_email(json)

def start_process_from_s3(bucket_key):
    chain = download_and_parse_sdr_task.s(bucket_key) | get_customer_details_from_sf_task.s() | generate_pdf_and_upload_task.s() | send_email_task.s() | uploadOrderLineToSalesForce.s()
            
    chain()

def start_sync_process_from_s3(bucket_key):
    json = download_and_parse_sdr_task(bucket_key)
    json = get_customer_details_from_sf_task(json)
    json = generate_pdf_and_upload_task(json) 
    json = send_email_task(json)