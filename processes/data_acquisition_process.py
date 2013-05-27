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

from notifications.tasks  import notify_salesforce_task, activate_contract_task

class DataAcquisitionProcess:

    def __init__(self, service_manager):
        self.service_manager = service_manager

    def create_acquire_payment_method_subprocess(self, tef_account):
        return self._generate_acquire_data_process(tef_account)

    def create_notify_payment_method_process(self, status, payment_method, contract_id):
        subprocess =  self._generate_notify_acquired_data_process(payment_method.tef_account)

        return self.start_notify_new_payment_method_data(status, payment_method, subprocess, contract_id)

    def start_notify_new_payment_method_data(self, status, payment_method, subprocess, contract_id):

        tef_account = payment_method.tef_account
        order_code  = payment_method.recurrent_order_code
        sp_id       = subprocess.id

        payment_method_details = payment_method.payment_method_details

        invoicing_address = {}
        invoicing_address['address']     = payment_method_details.address
        invoicing_address['postal_code'] = payment_method_details.postal_code

        chain = activate_contract_task.s(True, contract_id, sp_id) | notify_salesforce_task.s(status, tef_account, invoicing_address, order_code, sp_id)

        chain()

    def get_contract_by_payment_method(self, payment_method):
            return self.service_manager.get_contract_by_payment_metrhod(payment_method)

    ################################################################################
    # Generating Processes
    ################################################################################

    def _generate_acquire_data_process(self, tef_account):
        process = BusinessProcess(tef_account=tef_account, name='ACQUIRE PAYMENT DATA')
        process.save()

        sub_process = SubProcess(process=process, name='ACQUIRE DATA')
        sub_process.save()

        return sub_process

    def _generate_notify_acquired_data_process(self, tef_account):
        process = BusinessProcess(tef_account=tef_account, name='ACQUIRE PAYMENT DATA')
        process.save()

        sub_process = SubProcess(process=process, name='NOTIFY ACQUIRED DATA')
        sub_process.save()

        return sub_process

    ################################################################################
    # Generating SubProcesses
    ################################################################################

    def _generate_notify_acquired_data_subprocess(previous_subprocess):
        process = BusinessProcess.objects.get(id=previous_subprocess)

        sub_process = SubProcess(process=process, name='NOTIFY ACQUIRED DATA')
        sub_process.save()

        return sub_process