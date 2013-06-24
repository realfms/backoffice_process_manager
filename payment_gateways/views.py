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

from django.http        import HttpResponse
from django.db          import transaction

from processes.contracting_process import ContractingProcess
from services                      import PaymentGatewayManager, PaymentMethodManager
from customers.services            import CustomerManager

from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

import json

######################################################
# CONTRACTS
######################################################

class ContractController:

    contracting_process = ContractingProcess()
    customer_manager    = CustomerManager()

    @classmethod
    @transaction.commit_on_success
    @csrf_exempt
    def create(cls, request):
        if request.method != 'POST':
            return cls._build_error_response('Invalid HTTP method')

        body   = request.body
        params = json.loads(body)

        channel = params.get('channel', None)

        if channel not in settings.CHANNELS_TO_MARKET:
            return cls._build_error_response('Invalid channel')

        account  = cls.customer_manager.store_account(params)

        if not account:
            return cls._build_error_response('Missing account parameters')

        contract = cls.customer_manager.store_contract(params, account)

        # Starting Contracting process (in this case, STAND ALONE version
        # Async, request doesn't block until process finish
        stand_alone_fn = cls.contracting_process._start_standalone_contracting_process

        cls.contracting_process.start_contracting_process(contract, stand_alone_fn)

        return cls._build_ok_response('Contracting process started properly!')

    @classmethod
    def _build_error_response(cls, message):
        error_message = {'result': 'error', 'message': message}

        return HttpResponse(json.dumps(error_message), mimetype="application/json", status=405)

    @classmethod
    def _build_ok_response(cls, message):
        ok_message = {'result': 'ok', 'message': message}

        return HttpResponse(json.dumps(ok_message), mimetype="application/json", status=200)

    @classmethod
    def _build_redirect_response(cls, message, url):
        ok_message = {'result': 'ok', 'message': message, 'url': url}

        return HttpResponse(json.dumps(ok_message), mimetype="application/json", status=200)

    @classmethod
    def _build_ok_with_data_response(cls, message, data):
        ok_message = {'result': 'ok', 'message': message, 'data': data}

        return HttpResponse(json.dumps(ok_message), mimetype="application/json", status=200)

######################################################
# PAYMENT METHODS
######################################################

class PaymentMethodController:

    payment_gateways_manager = PaymentGatewayManager()
    customer_manager         = CustomerManager()
    payment_method_manager   = PaymentMethodManager()

    @classmethod
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

        payment_methods = cls.payment_method_manager.get_payment_methods(account, 'VALIDATED')

        payment_methods = [pm.to_dict() for pm in payment_methods]

        return ContractController._build_ok_with_data_response('Listing registered payment methods', payment_methods)

    @classmethod
    @csrf_exempt
    @transaction.commit_on_success
    def create(cls, request):

        if request.method == 'POST':

            body   = request.body
            params = json.loads(body)

            email = params.get('account', None)

            if not email:
                return ContractController._build_error_response('Missing account parameters')

            account = cls.customer_manager.get_account(email)

            if not account:
                return ContractController._build_error_response('Invalid account account parameters')

            billing_address = cls.customer_manager.get_billing_address(account)

            if not billing_address:
                return ContractController._build_error_response('Missing billing address. Add billing address before')

            url = cls.payment_gateways_manager.get_payment_gateway_redirect_url(billing_address)

            if not url:
                return ContractController._build_error_response('Problem with payment gateway')

            return ContractController._build_redirect_response('Redirecting to Payment Gateway', url)