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

from notifications.tasks            import create_contract_on_salesforce_task, activate_contract_on_salesforce_task, send_contracting_email_task
from common.distributed.distributed import compute_uuid

class CollectionProcess(Process):

    def start_collection_process(self, account, start_date, end_date):
        process    = self.create_process_model(account, 'COLLECTION')
        subprocess = self.create_subprocess_model(process,       'HARVESTING INVOICE DATA')

        self._start_collection_process(subprocess, start_date, end_date)

    def _start_collection_process(self, subprocess, start_date, end_date):

        sp_id   = subprocess.id

        chain = get__task.s(True, account_dict, sp_id) | create_contract_on_salesforce_task.s(contract_dict, sp_id)

        chain()

