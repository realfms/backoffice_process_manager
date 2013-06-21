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
Created on 30/10/2012

@author: mac@tid.es
'''

from django.shortcuts import render
from django.db        import transaction

from customers.views import ContractController

from order_to_cash_process import OrderToCashProcess
from collections_process   import CollectionProcess
from services              import BPMonitoringManager

from django.views.decorators.csrf import csrf_exempt

import json

class ProcessesController:

    order_to_cash_process = OrderToCashProcess()
    collection_process    = CollectionProcess()

    @classmethod
    @transaction.commit_on_success
    def launch_invoicing(cls, request):
        cls.order_to_cash_process.start_order_to_cash()

        return render(request, 'processes/invoicing.html', {})

    @classmethod
    @csrf_exempt
    @transaction.commit_on_success
    def launch_collections(cls, request):
        if request.method != 'POST':
            return ContractController._build_error_response('Invalid HTTP method')

        body   = request.body
        params = json.loads(body)

        account_id = params.get('account', None)
        start_date = params.get('start_date', None)
        end_date   = params.get('end_date', None)

        if not account_id or not start_date or not end_date:
            return ContractController._build_error_response('Missing parameters')

        result = cls.collection_process.start_collection_process(account_id, start_date, end_date)

        if not result:
            return ContractController._build_error_response('Invalid parameter')

        return ContractController._build_ok_response('Collection process started properly! An email will  be sent shortly!')

class BPMonitoringController:

    bp_monitoring_manager = BPMonitoringManager()

    @classmethod
    @csrf_exempt
    @transaction.commit_on_success
    def get_processes(cls, request, user_id):
        tree = cls.bp_monitoring_manager.get_process_tree(user_id)

        return render(request, 'processes/processes.html', tree)
