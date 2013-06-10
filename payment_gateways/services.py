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

import importlib

class PaymentGatewayManager:

    def __init__(self):
        self.payment_method_process = PaymentMethodProcess()
        self.customer_manager       = CustomerManager()
        self.payment_method_manager = PaymentMethodManager()

    def get_payment_gateway_redirect_url(self, billing_address):
        (charger, gw) = self._get_charger_by_country(billing_address.country)

        if charger == None:
            return None

        url = charger.get_redirect_url(billing_address)

        if not url:
            return None

        # Correct invocation to Payment Gateway
        # Storing payment method details

        order_code = charger.get_order()
        gw         = charger.get_gateway()
        account    = billing_address.account

        self.payment_method_manager.store_payment_method(account, order_code, gw)

        return url

    def process_recurrent_payment(self, order):
        account = order.account
        country = order.country

        (charger, payment_method) = self._get_charger_by_account_and_country(account, country)
        if charger == None:
            return False

        charger.recurrent_payment(order, payment_method)

        return True

    def get_charger_by_name(self, name):
        gw = self._get_gateway_by_name(name)

        if gw == None:
            return (None, None)

        return (self._dynamically_loading_charger(gw), gw)

    ######################################################
    # PRIVATE METHODS
    ######################################################

    def _get_charger_by_country(self, country):
        gw = self._get_gateway_by_country(country)

        if gw == None:
            return (None, None)

        return (self._dynamically_loading_charger(gw), gw)

    def _get_charger_by_account_and_country(self, account, country):
        payment_method = self._get_payment_method_by_account_and_country(account, country)

        if not payment_method:
            return (None, None)

        gw = payment_method.gateway

        return (self._dynamically_loading_charger(gw), payment_method)

    def _get_gateway_by_country(self, country):
        try:
            return  PaymentGateway.objects.get(country=country)
        except PaymentMethod.DoesNotExist:
            return None

    def _get_gateway_by_name(self, name):
        try:
            return  PaymentGateway.objects.get(name=name)
        except PaymentMethod.DoesNotExist:
            return None

    def _get_payment_method_by_account_and_country(self, account, country):
        try:
            return PaymentMethod.objects.get(account=account, gateway__country=country, status='VALIDATED')
        except PaymentMethod.DoesNotExist:
            return None

    def _dynamically_loading_charger(self, gw):
        charger_module = importlib.import_module(gw.module_name)
        charger = getattr(charger_module, gw.class_name)(gw)

        return charger

class PaymentMethodManager:

    payment_method_process = PaymentMethodProcess()

    def get_payment_methods(self, account, status):
        return PaymentMethod.objects.filter(account=account, status=status)

    def get_valid_payment_methods(self, account):
        return PaymentMethod.objects.filter(account=account, status='VALIDATED')

    def get_valid_payment_method(self, pm_id, account):
        try:
            return PaymentMethod.objects.get(id=pm_id, account=account, status='VALIDATED')
        except PaymentMethod.DoesNotExist:
            return None

    def store_payment_method(self, account, recurrent_order_code, gateway):

        # Creating PaymentMethod
        payment_method = PaymentMethod(account=account, recurrent_order_code=recurrent_order_code, gateway=gateway)
        payment_method.save()

        return payment_method

    def start_new_payment_method_notification_process(self, payment_method, fn):

        fn = self.payment_method_process._start_standalone_new_payment_method_process

        # Async. Starting notification process
        self.payment_method_process.start_new_payment_method_notification_process(payment_method, fn)


