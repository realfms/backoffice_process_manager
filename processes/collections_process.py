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
Created on 29/05/2013

@author: mac@tid.es
'''

from process import Process

from common.dates.dates import format_date

from customers.services import CustomerManager
from ordering.models import Order

from collections.tasks import generate_journal_task, generate_revenue_report_task
from email.tasks import send_collections_email_task

class CollectionProcess(Process):

    customer_manager = CustomerManager()

    ######################################################
    # PUBLIC
    ######################################################

    def start_collection_process(self, account_id, start, end):

        (account, start_date, end_date) = self._validate_params(account_id, start, end)

        if not account or not start_date or not end_date:
            return None

        process    = self.create_process_model(account,    'COLLECTION')
        subprocess = self.create_subprocess_model(process, 'HARVESTING INVOICE DATA')

        self._start_collection_process(subprocess, account, start_date, end_date)

        return True

    ######################################################
    # PRIVATE
    ######################################################

    def _start_collection_process(self, subprocess, account, start_date, end_date):

        sp_id = subprocess.id
        email = account.email

        orders = [order.to_dict_for_revenue_report() for order in Order.objects.filter(date__gte=start_date, date__lte=end_date)]

        chain = generate_revenue_report_task.s(True, orders, sp_id) | generate_journal_task.s(orders, sp_id) | send_collections_email_task.s(email, sp_id)

        chain()

    def _validate_params(self, account_id, start, end):
        try:
            start_date =  format_date(start)
            end_date = format_date(end)
        except:
            return (None, None, None)

        account = self.customer_manager.get_account(account_id)

        if not account:
            return (None, None, None)

        return (account, start_date, end_date)

