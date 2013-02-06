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
Created on 05/02/2013

@author: mac@tid.es
'''

from tasks import notify_salesforce_task, notify_tef_accounts_task, payment_gateway_invocation_task,\
                  download_and_parse_sdr_task, get_customer_details_from_sf_task, \
                  generate_pdf_and_upload_task, send_email_task, charge_user_task, update_charging_result, \
                  create_financial_accounting_record

######################################################
# DATA ACQUISITION PROCESS
######################################################

def start_notify_data_acquisition_result(state):
    chain = notify_salesforce_task.s(state) | notify_tef_accounts_task.s(state)

    chain()

def sync_notify_data_acquisition_result(state):
    json = notify_salesforce_task(state)
    json = notify_tef_accounts_task(state)

    return json

######################################################
# RECURRENT PAYMENT PROCESSES
######################################################

def start_invoke_gateway(json, p_gw):
    chain = payment_gateway_invocation_task.s(json)

    chain()

def sync_invoke_gateway(json, p_gw):
    result = payment_gateway_invocation_task(json)

    return result

######################################################
# ORDER TO CASH PROCESS
######################################################

def start_order_to_cash_process(bucket_key):
    chain = download_and_parse_sdr_task.s(bucket_key) | get_customer_details_from_sf_task.s() | generate_pdf_and_upload_task.s() | send_email_task.s() | charge_user_task.s()

    chain()

def sync_order_to_cash(bucket_key):
    json = download_and_parse_sdr_task(bucket_key)
    json = get_customer_details_from_sf_task(json)
    json = generate_pdf_and_upload_task(json)
    json = send_email_task(json)
    json = charge_user_task(json)

    return json

######################################################
# COLLECTIONS PROCESS
######################################################

def start_collections_process(json):
    chain = update_charging_result.s(json) | create_financial_accounting_record.s()

    chain()