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

from models import BusinessProcess, SubProcess

from customer.tasks      import get_customer_details_from_sf_task
from charging.tasks      import charge_user_task
from rating.tasks        import download_and_parse_sdr_task
from pdf.tasks           import generate_pdf_and_upload_task
from email.tasks         import send_email_task
from notifications.tasks import create_order_summary_on_salesforce_task

from process import Process

class OrderToCashProcess(Process):

    ################################################################################
    # CREATE & START PROCESS
    ################################################################################
    def start_order_to_cash_process(self, bucket_key, account):
        
        process    = self.create_process_model(account,    'ORDER TO CASH')
        subprocess = self.create_subprocess_model(process, 'BILLING')

        self._start_order_to_cash_process(bucket_key, account, subprocess)

    def sync_order_to_cash(self, bucket_key, account):

        process    = self.create_process_model(account,    'ORDER TO CASH')
        subprocess = self.create_subprocess_model(process, 'BILLING')

        sp_id      = subprocess.id
        account_id = account.account_id

        success = download_and_parse_sdr_task(True, bucket_key, account_id, sp_id)
        success = get_customer_details_from_sf_task(success, sp_id)
        success = generate_pdf_and_upload_task(success, sp_id)
        success = send_email_task(success, sp_id)
        success = charge_user_task(success, sp_id)

        return success
    
    ################################################################################
    # PRIVATE METHODS
    ################################################################################

    def _start_order_to_cash_process(self, bucket_key, account, subprocess):
        
        sp_id      = subprocess.id
        account_id = account.account_id
        
        chain = download_and_parse_sdr_task.s(True, bucket_key, account_id, sp_id) | get_customer_details_from_sf_task.s(sp_id) | generate_pdf_and_upload_task.s(sp_id) | send_email_task.s(sp_id) | charge_user_task.s(sp_id) | create_order_summary_on_salesforce_task.s(sp_id)

        chain()
