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

from models     import PaymentGateway, PaymentMethod, Order, Account, Contract

from processes.payment_method_process import PaymentMethodProcess

from common.salesforce.salesforce import create_contract

import importlib
import uuid


class ServiceManager:

    def __init__(self):
        self.payment_method_process = PaymentMethodProcess(self)

    def store_account(self, params):

        account_id  = params.get('account',     None)
        email       = params.get('email',       None)
        city        = params.get('city',        None)
        address     = params.get('address',     None)
        postal_code = params.get('postal_code', None)
        country     = params.get('country',     None)
        phone       = params.get('phone',       None)
        gender      = params.get('gender',      None)
        first_name  = params.get('first_name',  None)
        last_name   = params.get('last_name',   None)
        channel     = params.get('channel',     None)

        if (not account_id or not channel):
            return None

        account = Account  (account=account_id, city=city, address=address, postal_code=postal_code, country=country,
                            phone=phone, email=email, gender=gender, first_name=first_name, last_name=last_name,
                            channel=channel)

        account.save()

        return account

    def store_contract(self, params, account):

        tos        = params.get('tos',        None)
        sign_date  = params.get('ign_date',   None)
        start_date = params.get('start_date', None)
        end_date   = params.get('end_date',   None)

        if (not tos or not sign_date or not start_date or account):
            return None

        contract = Contract(account=account, tos=tos, start_date=start_date, end_data=end_date)

        contract.save()

        return contract

    def get_contract_by_payment_method(self, payment_method):
        contracts = Contract.objects.filter(payment_method=payment_method)

        if len(contracts) != 1:
            print "Incorrect number of contracts"
            return None

        return contracts[0]

    def get_payment_gateway_redirect_url(self, params):

        # Storing account info
        account  = self.update_account(params)

        # Checking if this user has already set up payment data
        (registered, payment_method) = self.is_billable_account(payment_data_details)

        # Creating inactive contract a
        contract_id = self.create_contract(payment_data_details)

        print contract_id

        if (registered):
            # We already have payment data, so activating contract
            self.payment_method_process.create_notify_payment_method_process('Billable', payment_method, contract_id)
            url = "/payment/gw/worldpay/success"
        else:
            # Start payment data acquisition flow from the very beginning
            url = self.initial_payment_url(token, contract_id)

        return url

    def is_billable_account(self, payment_method):
        return payment_method.status == "VALIDATED"


    def create_contract(self, user_data):
        return create_contract(user_data)

    def initial_payment_url(self, token, contract_id):
        payment_method_details = self.get_payment_method_details(token)

        (charger, gw) = self.get_first_available_charger_by_country(payment_method_details.country)
        if (charger == None):
            return "/error"

        url = charger.get_redirect_url(payment_method_details)

        self.store_payment_method(payment_method_details, charger.get_order(), gw, contract_id)

        return url

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

    def get_charger_by_tef_account_and_country(self, tef_account, country):
        master_info = self.get_payment_method_by_tef_account_and_country(tef_account, country)

        if master_info == None:
            return (None, None)

        gw = master_info.gateway

        return (self.dynamically_loading_charger(gw), master_info)

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

    def get_payment_method_by_tef_account_and_country(self, tef_account, country):
        payment_methods = PaymentMethod.objects.filter(tef_account=tef_account, gateway__country=country)

        if len(payment_methods) == 0:
            return None

        # If several, getting the first one
        return payment_methods[0]

    def get_charger_by_payment_method(self, country):
        gw = self.get_gateway_by_country(country)

        if gw == None:
            return None

        return self.dynamically_loading_charger(gw)

    def process_recurrent_payment(self, order_data):

        self.store_order(order_data)

        tef_account = order_data.tef_account
        country     = order_data.country

        (charger, master_info) = self.get_charger_by_tef_account_and_country(tef_account, country)
        if charger == None:
            return False

        charger.recurrent_payment(order_data, master_info)

        return True


    def store_payment_method(self, payment_method_details, recurrent_order_code, gateway, contract_id):
        # Creating subprocese
        subprocess = self.payment_method_process.create_acquire_payment_method_subprocess(payment_method_details.tef_account)

        # Creating PaymentMethod
        payment_method = PaymentMethod(tef_account=payment_method_details.tef_account, recurrent_order_code=recurrent_order_code,
                                       gateway=gateway, email=payment_method_details.email, payment_method_details=payment_method_details)
        payment_method.save()

        #Creating and Linking Contract
        contract = Contract(subprocess=subprocess, contract_id=contract_id, payment_method=payment_method)
        contract.save()

    def store_order(self, order_data):
        order = Order(total=order_data.total, currency=order_data.currency, country=order_data.country,
                      tef_account=order_data.tef_account, statement=order_data.statement,
                      order_code=order_data.order_code)

        order.save()


    def dynamically_loading_charger(self, gw):
        charger_module = importlib.import_module(gw.module_name)
        charger = getattr(charger_module, gw.class_name)(gw)

        return charger

    def get_payment_method_details(self, account):
        return Account.objects.get(account=account)

    def update_account(self, params):
        email = params.get('account_id', None)

        account = Account.objects.get(email=email)

        account.first_name  = params.get('first_name',  account.first_name)
        account.last_name   = params.get('last_name',   account.last_name)
        account.address     = params.get('address',     account.address)
        account.city        = params.get('city',        account.city)
        account.postal_code = params.get('postal_code', account.postal_code)
        account.gender      = params.get('gender',      account.gender)
        account.phone       = params.get('phone',       account.phone)
        account.country     = params.get('country',     account.country)

        params.save()

        return params

    def compute_unique_id(self):
        uid = uuid.uuid4()

        return uid.hex[:10]

