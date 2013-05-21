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
Created on 21/05/2013

@author: mac@tid.es
'''

from celery import task

from processes.task_manager import TaskManager

from common.salesforce.salesforce import register_provision_event

@task(ignore_result=True)
def register_in_crm_task(success, sp_id, event_data):
    tm = TaskManager()

    return tm.process_task(sp_id, 'CRM', success, lambda : register_provision_event(event_data))


@task(ignore_result=True)
def register_in_billing_task(success, sp_id, event_data):
    tm = TaskManager()

    return tm.process_task(sp_id, 'BILLING', success, lambda : _register_event_in_billing(event_data))

def _register_event_in_billing(event_data):
    return (True, None)