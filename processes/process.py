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

from models import BusinessProcess, SubProcess

class Process:

    ################################################################################
    # Generating Processes
    ################################################################################

    # account: customers.models.Account
    # name: text
    # return: customers.models.Account
    def create_process_model(self, account, name):
        process = BusinessProcess(account=account, name=name)
        process.save()

        return process

    ################################################################################
    # Generating Subprocesses
    ################################################################################

    def create_subprocess_model(self, process, name):
        subprocess = SubProcess(process=process, name=name)
        subprocess.save()

        return subprocess