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


from django.test import TestCase

from services import CustomerManager

from customers.models import Account, Contract

class TestValidations(TestCase):

    customer_manager = CustomerManager()

    def dummy_account(self):

        params = {'channel': 'ONLINE', 'email': 'FAKE@tid.es'}

        return self.customer_manager.store_account(params)

    def test_wrong_account_without_identification(self):

        params = {'channel': 'ONLINE'}

        result = self.customer_manager.store_account(params)

        self.assertEquals(result, None, 'Account validation should return None')

    def test_valid_account_with_email(self):

        params = {'channel': 'ONLINE', 'email': 'FAKE@tid.es'}

        result = self.customer_manager.store_account(params)

        self.assertEquals(type(result), Account, 'Should return an Account instance')

    def test_valid_contract(self):

        account = self.dummy_account()

        params = {'sign_date': '29/05/2013', 'tos': 'http://contratos.com', 'start_date': '29/05/2013'}

        result = self.customer_manager.store_contract(params, account)

        self.assertEquals(type(result), Contract, 'Should return a Contract instance')

    def test_wrong_contract_with_invalid_date_format(self):

        account = self.dummy_account()

        params = {'sign_date': '29-05-2013', 'tos': 'http://contratos.com', 'start_date': '29-05-2013'}

        result = self.customer_manager.store_contract(params, account)

        self.assertEquals(result, None, 'Contract validation should return None')

    def test_wrong_contract_with_invalid_end_date(self):

        account = self.dummy_account()

        params = {'sign_date': '29/05/2013', 'tos': 'http://contratos.com', 'start_date': '29/05/2013',
                  'end_date': '29-05-2013'}

        result = self.customer_manager.store_contract(params, account)

        self.assertEquals(result, None, 'Contract validation should return None')