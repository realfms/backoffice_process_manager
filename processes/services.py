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

from processes.models import BusinessProcess
from customers.services import CustomerManager

class BPMonitoringManager:

    customer_manager = CustomerManager()

    ################################################################################
    # PUBLIC METHODS
    ################################################################################

    def get_process_tree(self, account_id):
        processes = self._get_processes_by_user(account_id)

        subprocesses = {}
        tasks = {}

        for process in processes:
            subprocess = self._get_subprocesses_by_process(process)
            subprocesses[process] = subprocess

            for sub in subprocess:
                tasks[sub] = self._get_tasks_by_subprocess(sub)

        args = {
            "processes"   : processes,
            "subprocesses": subprocesses,
            "tasks"       : tasks
        }

        return args
    
    ################################################################################
    # PRIVATE METHODS
    ################################################################################

    def _get_processes_by_user(self, email):
        account = self.customer_manager.get_account(email)

        if not account:
            return []

        processes = BusinessProcess.objects.filter(account=account).order_by("start")

        return processes.reverse()

    def _get_subprocesses_by_process(self, process):
        return process.subprocess_set.all()

    def _get_tasks_by_subprocess(self, subprocess):
        return subprocess.task_set.all()