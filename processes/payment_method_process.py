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

from process import Process

from notifications.tasks  import update_contact_on_salesforce_task

class PaymentMethodProcess(Process):

    def __init__(self, service_manager):
        self.service_manager = service_manager

    ################################################################################
    # CREATE PROCESS
    ################################################################################
    def start_payment_method_acquisition_process(self, account, payment_method):
        process    = self.create_process_model(account,    'ACQUIRE PAYMENT METHOD')
        subprocess = self.create_subprocess_model(process, 'NOTIFYING CONTRACT')

        self._start_payment_method_acquisition_process(account, payment_method, subprocess)

    def _start_payment_method_acquisition_process(self, account, payment_method, subprocess):
        chain = update_contact_on_salesforce_task.s(True, account, payment_method, subprocess.id)

        chain()

    def get_contract_by_payment_method(self, payment_method):
        return self.service_manager.get_contract_by_payment_method(payment_method)