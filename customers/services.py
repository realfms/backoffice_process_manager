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
Created on 01/06/2013

@author: mac@tid.es
'''

from models                    import Account, Contract
from customers.models          import BillingAddress

from common.dates.dates import format_date

class CustomerManager:

    def get_billing_address(self, account):
        try:
            return BillingAddress.objects.get(account=account)
        except BillingAddress.DoesNotExist:
            return None

    def store_account(self, params):

        email   = params.get('email',       None)
        channel = params.get('channel',     None)

        if not email or not channel:
            return None

        account, created = Account.objects.get_or_create(email=email)

        if created:
            account.channel = channel
            account.save()

        return account

    def store_billing_address(self, params):

        email       = params.get('email',       None)
        city        = params.get('city',        None)
        address     = params.get('address',     None)
        postal_code = params.get('postal_code', None)
        country     = params.get('country',     None)
        phone       = params.get('phone',       None)
        first_name  = params.get('first_name',  None)
        last_name   = params.get('last_name',   None)

        if not email:
            return None

        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return None

        if not city or not address or not postal_code or not country or not first_name or not last_name:
            return None

        billing_address, _ = BillingAddress.objects.get_or_create(account=account)

        billing_address.city        = city
        billing_address.address     = address
        billing_address.postal_code = postal_code
        billing_address.country     = country
        billing_address.phone       = phone
        billing_address.first_name  = first_name
        billing_address.last_name   = last_name

        billing_address.save()

        return billing_address

    def store_contract(self, params, account):

        tos        = params.get('tos',        None)
        sign_date  = params.get('sign_date',  None)
        start_date = params.get('start_date', None)

        end_date_string = params.get('end_date',   None)

        if not tos or not sign_date or not start_date or not account:
            return None

        start_date = format_date(start_date)
        sign_date  = format_date(sign_date)

        if not start_date or not sign_date:
            return None

        end_date = format_date(end_date_string)

        if end_date_string and not end_date:
            return None

        contract = Contract(account=account, tos=tos, start_date=start_date, end_date=end_date, sign_date=sign_date)

        contract.save()

        return contract

    def get_account(self, email):
        try:
            return Account.objects.get(email=email)
        except Account.DoesNotExist:
            return None
