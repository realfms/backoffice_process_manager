#!/usr/bin/python
#coding=utf-8

"""
Copyright 2012 Telefonica Investigacion y Desarrollo, S.A.U

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

"""
Created on 16/01/2013

@author: mac@tid.es
"""

import manage

from customers.services  import CustomerManager
from contracting_process import ContractingProcess
from ordering.services import OrderManager

from models import BusinessProcess, SubProcess, Task

from django.test.utils import override_settings

# Loading environment variables prior to initialice django framework
manage.read_env('.env')

from django.test import TestCase

class TestContractingProcess(TestCase):

    customer_manager = CustomerManager()
    contracting_process = ContractingProcess()
    order_manager = OrderManager()

    def setUp(self):
        self.dummy_account  = self.create_dummy_account()
        self.dummy_contract = self.create_dummy_contract()

    def create_dummy_account(self):
        params = {'channel': 'ONLINE', 'email': 'FAKE@tid.es'}

        return self.customer_manager.store_account(params)

    def create_dummy_contract(self):
        params = {'sign_date': '29/05/2013', 'tos': 'http://contratos.com', 'start_date': '29/05/2013', 'account': self.dummy_account}

        return self.customer_manager.store_contract(params, self.dummy_account)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS = True, CELERY_ALWAYS_EAGER = True, BROKER_BACKEND = 'memory')
    def test_valid_salesforce_contracting_process(self):
        fn = self.contracting_process._start_salesforce_contracting_process

        self.contracting_process.start_contracting_process(self.dummy_contract, fn)

        bp = BusinessProcess.objects.get(account=self.dummy_account, name='CONTRACTING')
        sp = SubProcess.objects.get(process=bp, name='NOTIFYING CONTRACT')

        tasks = Task.objects.filter(subprocess=sp)

        self.assertEquals(len(tasks), 3, 'Wrong number of tasks in salesforce contracting process')

    def test_valid_standalone_contracting_process(self):
        fn = self.contracting_process._start_standalone_contracting_process

        self.contracting_process.start_contracting_process(self.dummy_contract, fn)

        bp = BusinessProcess.objects.get(account=self.dummy_account, name='CONTRACTING')
        sp = SubProcess.objects.get(process=bp, name='NOTIFYING CONTRACT')

        tasks = Task.objects.filter(subprocess=sp)

        self.assertEquals(len(tasks), 0, 'Wrong number of tasks in standalone contracting process')

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS = True, CELERY_ALWAYS_EAGER = True, BROKER_BACKEND = 'memory')
    def test_valid_online_standalone__order_to_cash_process(self):

        events = [{'rated_by_billing': {'billing_code': 'ER_SUBSCRIPTION', 'units': 1, 'exponent': 0}}]
        params = {'account': 'mac@tid.es', 'payment_method': 1, 'events': events}

        self.order_manager.create_order(params)
