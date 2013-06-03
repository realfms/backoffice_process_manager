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
Created on 30/10/2012

@author: mac@tid.es
'''

from models import PaymentGateway, PaymentMethod

from processes.payment_method_process import PaymentMethodProcess
from customers.services               import CustomerManager

from common.salesforce.salesforce import create_contract

import importlib
import uuid


class ServiceManager:

    def __init__(self):
        self.payment_method_process = PaymentMethodProcess(self)
        self.customer_manager       = CustomerManager()

    def get_payment_gateway_redirect_url(self, params):
        # Storing account info
        account  = self.customer_manager.update_account_with_payment_details(params)

        if not account:
            return None

        return self.initial_payment_url(account)

    def is_billable_account(self, payment_method):
        return payment_method.status == "VALIDATED"

    def create_contract(self, user_data):
        return create_contract(user_data)

    def initial_payment_url(self, account):
        (charger, gw) = self.get_first_available_charger_by_country(account.country)
        if (charger == None):
            return None

        return charger.get_redirect_url(account)

    def get_charger_by_name(self, name):
        gw = self.get_gateway_by_name(name)

        if gw == None:
            return (None, None)

        return (self.dynamically_loading_charger(gw), gw)

    def get_first_available_charger_by_country(self, country):
        gw = self.get_gateway_by_country(country)

        if gw == None:
            return (None, None)

        return (self.dynamically_loading_charger(gw), gw)

    def get_charger_by_account_and_country(self, account, country):
        payment_method = self.get_payment_method_by_account_and_country(account, country)

        if not payment_method:
            return (None, None)

        gw = payment_method.gateway

        return (self.dynamically_loading_charger(gw), payment_method)

    def get_gateway_by_name(self, name):
        gws = PaymentGateway.objects.filter(name=name)

        if len(gws) == 0:
            return None

        return gws[0]

    def get_gateway_by_country(self, country):
        gws = PaymentGateway.objects.filter(country=country)

        if len(gws) == 0:
            return None

        # If several, getting the first one
        return gws[0]

    def get_payment_method_by_account_and_country(self, account, country):
        payment_methods = PaymentMethod.objects.filter(account=account, gateway__country=country, status='VALIDATED')

        if len(payment_methods) == 0:
            return None

        # If several, getting the first one
        return payment_methods[0]

    def get_charger_by_payment_method(self, country):
        gw = self.get_gateway_by_country(country)

        if gw == None:
            return None

        return self.dynamically_loading_charger(gw)

    def process_recurrent_payment(self, order):

        account = order.account
        country = order.country

        (charger, payment_method) = self.get_charger_by_account_and_country(account, country)
        if charger == None:
            return False

        charger.recurrent_payment(order, payment_method)

        return True


    def store_payment_method(self, account, recurrent_order_code, gateway):
        # Creating subprocese
        subprocess = self.payment_method_process.create_acquire_payment_method_subprocess(payment_method_details.account_id)

        # Creating PaymentMethod
        payment_method = PaymentMethod(account=account, recurrent_order_code=recurrent_order_code,
                                       gateway=gateway, email=payment_method_details.email, payment_method_details=payment_method_details)
        payment_method.save()

    def dynamically_loading_charger(self, gw):
        charger_module = importlib.import_module(gw.module_name)
        charger = getattr(charger_module, gw.class_name)(gw)

        return charger

    def compute_unique_id(self):
        uid = uuid.uuid4()

        return uid.hex[:10]


