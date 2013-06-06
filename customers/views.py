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
General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with Billing_PoC.
If not, see http://www.gnu.org/licenses/.

For those usages not covered by the GNU Affero General Public License please contact with::mac@tid.es
"""

'''
Created on 01/06/2013

@author: mac@tid.es
'''

from django.views.decorators.csrf import csrf_exempt

from customers.services import CustomerManager
from payment_gateways.views import ContractController

from django.db          import transaction
from django.utils       import simplejson

######################################################
# BILLING ADDRESS
######################################################

class BillingAddressController:

    customer_manager = CustomerManager()

    @classmethod
    @transaction.commit_on_success
    @csrf_exempt
    def create(cls, request):
        if request.method != 'POST':
            return ContractController._build_error_response('Invalid HTTP method')

        body   = request.body
        params = simplejson.loads(body)

        billing_address = cls.customer_manager.store_billing_address(params)

        if not billing_address:
            return ContractController._build_error_response('Missing parameters')

        return ContractController._build_ok_response('Billing address updated!')

    @classmethod
    @transaction.commit_on_success
    @csrf_exempt
    def list(cls, request):
        if request.method != 'GET':
            return ContractController._build_error_response('Invalid HTTP method')

        params = request.GET

        email = params.get('account', None)

        if not email:
            return ContractController._build_error_response('Missing account parameter')

        account = cls.customer_manager.get_account(email)

        if not account:
            return ContractController._build_error_response('Invalid account')

        billing_address = cls.customer_manager.get_billing_address(account)

        return ContractController._build_ok_with_data_response('Listing registered payment methods', billing_address.to_dict())
