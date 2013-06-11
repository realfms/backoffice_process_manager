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
Created on 16/10/2012

@author: mac@tid.es
'''
from common.aws.s3   import get_sdr_request_keys

from processes.models import BusinessProcess
from customers.models import Account

from processes.order_to_cash_process import OrderToCashProcess
from processes.provision_process     import ProvisionProcess

class ProcessManager:

    def __init__(self):
        self.order_to_cash_process = OrderToCashProcess()
        self.provision_process     = ProvisionProcess()

    def start_provision(self, account_id, event_data):
        self.provision_process.start_provision_process(account_id, event_data)

    def start_order_to_cash(self):
        keys = get_sdr_request_keys()

        for key in keys:
            self.order_to_cash_process.start_cdr_order_to_cash_process(key.name, self._get_account(key))

    def sync_first_order_to_cash(self):
        keys = get_sdr_request_keys()

        for key in keys:
            self.order_to_cash_process.sync_order_to_cash(key.name, self._get_account(key))
            break

    def get_processes_by_user(self, user_id):
        processes = BusinessProcess.objects.filter(tef_account=user_id).order_by("start")

        return processes.reverse()

    def get_subprocesses_by_process(self, process):
        return process.subprocess_set.all()

    def get_tasks_by_subprocess(self, subprocess):
        return subprocess.task_set.all()
    
    ################################################################################
    # PRIVATE METHODS
    ################################################################################
    
    # return customers.model.Account
    def _get_account(self, key):
        # By convention, by removing the last 4 characters from key, the tef_account is returned!
        account_id = key.name[0:-4]
        
        try:
            return Account.objects.get(account_id=account_id)
        except Exception, e:
            print "Missing account: {0}".format(account_id)
            return None