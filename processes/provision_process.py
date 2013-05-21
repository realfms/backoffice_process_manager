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

from provision.tasks  import register_in_crm_task, register_in_billing_task

class ProvisionProcess:

    def __init__(self):
        pass

    def start_provision_process(self, tef_account, event_data):

        sub_process =  self._generate_provision_process(tef_account)
        sp_id = sub_process.id

        chain = register_in_crm_task.s(True, sp_id, event_data) | register_in_billing_task.s(sp_id, event_data)

        chain()

    ################################################################################
    # Generating Processes
    ################################################################################

    def _generate_provision_process(self, tef_account):
        process = BusinessProcess(tef_account=tef_account, name='PROVISION EVENT')
        process.save()

        sub_process = SubProcess(process=process, name='PROVISION EVENT')
        sub_process.save()

        return sub_process