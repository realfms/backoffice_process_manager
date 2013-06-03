#!/usr/bin/python
#coding=utf-8 

"""
Copyright 2012 Telefonica Investigacion y Desarrollo, S.A.U

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

"""
Created on 16/01/2013

@author: mac@tid.es
"""

import manage

from django.test import TestCase

from services           import PaymentGatewayManager
from customers.services import CustomerManager

import unittest

# Loading environment variables prior to initialice django framework
manage.read_env('.env')

#@unittest.skip("Making tests faster")
class TestPaymentDataAcquisition(TestCase):

    service_manager  = PaymentGatewayManager()
    customer_manager = CustomerManager()

    def setUp(self):
        self.create_dummy_account()

    def create_dummy_account(self):
        params = {'channel': 'ONLINE', 'email': 'mac@tid.es'}

        return self.customer_manager.store_account(params)

    def test_wrong_invalid_payment_data(self):
        params = {'channel': 'ONLINE', 'email': 'mac@tid.es'}

        url = self.service_manager.get_payment_gateway_redirect_url(params)

        self.assertEquals(url, None, 'Response should be None when this params')

    def test_valid_redirection_to_adyen(self):
        country = 'BR'
        params  = { 'email': 'mac@tid.es', 'first_name': 'nombre', 'last_name': 'apellidos', 'address': 'direccion',
                   'postal_code': '28393', 'city': 'madrid', 'country': country}

        url = self.service_manager.get_payment_gateway_redirect_url(params)

        self.assertTrue(url.startswith('https://test.adyen.com/hpp/pay.shtml'), 'Accounts from BR should redirect to Adyen')

    def test_valid_redirection_to_adyen(self):
        country = 'ES'
        params  = { 'email': 'mac@tid.es', 'first_name': 'nombre', 'last_name': 'apellidos', 'address': 'direccion',
                   'postal_code': '28393', 'city': 'madrid', 'country': country}

        url = self.service_manager.get_payment_gateway_redirect_url(params)

        self.assertTrue(url.startswith('https://secure-test.worldpay.com/wcc/dispatcher'), 'Accounts from ES should redirect to WorldPay')
