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

from models import Account, Contract

from django.utils.timezone import utc
from datetime              import datetime

class CustomerManager:

    DATE_FORMAT = '%d/%m/%Y'

    def store_account(self, params):

        account_id  = params.get('account_id',  None)
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

        # Identified if account_id or email is provided
        identified = account_id or email

        if not identified or not channel:
            return None

        account = Account  (account_id=account_id, city=city, address=address, postal_code=postal_code, country=country,
            phone=phone, email=email, gender=gender, first_name=first_name, last_name=last_name,
            channel=channel)

        account.save()

        return account

    def store_contract(self, params, account):

        tos        = params.get('tos',        None)
        sign_date  = params.get('sign_date',  None)
        start_date = params.get('start_date', None)

        end_date_string = params.get('end_date',   None)

        if (not tos or not sign_date or not start_date or not account):
            return None

        start_date = self._format_date(start_date)
        sign_date  = self._format_date(sign_date)

        if not start_date or not sign_date:
            return None

        end_date = self._format_date(end_date_string)

        if end_date_string and not end_date:
            return None

        contract = Contract(account=account, tos=tos, start_date=start_date, end_date=end_date, sign_date=sign_date)

        contract.save()

        return contract

    def update_account_with_payment_details(self, params):

        email      = params.get('email',      None)
        account_id = params.get('account_id', None)

        if not email and not account_id:
            return None

        account = self._get_account(email, account_id)

        if not account:
            return None

        first_name  = params.get('first_name',  None)
        last_name   = params.get('last_name',   None)
        address     = params.get('address',     None)
        city        = params.get('city',        None)
        country     = params.get('country',     None)
        postal_code = params.get('postal_code', None)

        if not first_name or not last_name or not address or not city or not country or not postal_code:
            return None

        gender      = params.get('gender',      None)
        phone       = params.get('phone',       None)

        account.first_name  = first_name
        account.last_name   = last_name
        account.address     = address
        account.city        = city
        account.postal_code = postal_code
        account.gender      = gender
        account.phone       = phone
        account.country     = country

        account.save()

        return account

    ######################################################
    # PRIVATE METHODS
    ######################################################

    def _format_date(self, date_string):
        try:
            return datetime.strptime(date_string, self.DATE_FORMAT).replace(tzinfo=utc)
        except Exception:
            return None

    def _get_account(self, email, account_id):
        try:
            account = Account.objects.get(account_id=account_id)
        except Account.DoesNotExist:
            try:
                account = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return None

        return account
