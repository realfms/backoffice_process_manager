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

from services           import PaymentGatewayManager, PaymentMethodManager
from customers.services import CustomerManager

from common.constants.constants import DATE_FORMAT

import unittest
import urlparse

# Loading environment variables prior to initialice django framework
manage.read_env('.env')

#@unittest.skip("Making tests faster")
class TestPaymentDataAcquisition(TestCase):

    gateways_manager = PaymentGatewayManager()
    customer_manager = CustomerManager()

    payment_method_manager = PaymentMethodManager()

    def setUp(self):
        self.dummy_account         = self.create_dummy_account()
        self.dummy_billing_address = self.create_dummy_billing_address()

    def create_dummy_account(self):
        params = {'channel': 'ONLINE', 'email': 'FAKE@tid.es'}

        return self.customer_manager.store_account(params)

    def create_dummy_billing_address(self):
        params  = { 'email': 'FAKE@tid.es', 'first_name': 'nombre', 'last_name': 'apellidos', 'address': 'direccion',
                    'postal_code': '28393', 'city': 'madrid', 'country': "ES"}

        return self.customer_manager.store_billing_address(params)

    def test_valid_redirection_to_adyen(self):
        self.dummy_billing_address.country = 'BR'
        self.dummy_billing_address.save()

        url = self.gateways_manager.get_payment_gateway_redirect_url(self.dummy_billing_address)

        self.assertTrue(url.startswith('https://test.adyen.com/hpp/pay.shtml'), 'Accounts from BR should redirect to Adyen')

    def test_valid_redirection_to_worldpay(self):
        self.dummy_billing_address.country = 'ES'
        self.dummy_billing_address.save()

        url = self.gateways_manager.get_payment_gateway_redirect_url(self.dummy_billing_address)

        self.assertTrue(url.startswith('https://secure-test.worldpay.com/wcc/dispatcher'), 'Accounts from ES should redirect to WorldPay')

    def test_valid_billing_address_storage(self):
        # Storing number of billing method BEFORE calling
        num_before = len(self.payment_method_manager.get_payment_methods(self.dummy_account, 'PENDING'))

        url = self.gateways_manager.get_payment_gateway_redirect_url(self.dummy_billing_address)

        # Storing number of billing method AFTER calling
        num_after = len(self.payment_method_manager.get_payment_methods(self.dummy_account, 'PENDING'))

        self.assertEqual(num_before, 0, 'No payment method should be registered!')
        self.assertEqual(num_after,  1, '1 payment method should be registered!')

    def test_worldpay_validated_payment_method_callback(self):
        data = dict(urlparse.parse_qsl('orderKey=TELEFONICA^GLOBALBILLINGEUR^c99831a4b9&paymentStatus=AUTHORISED&mask=1&expiration=29-12-2019'))

        # Marking callback data as VALID
        data['paymentStatus'] = 'AUTHORISED'

        charger, gateway = self.gateways_manager.get_charger_by_name("WORLDPAY")

        num_before = len(self.payment_method_manager.get_payment_methods(self.dummy_account, 'VALIDATED'))

        self.payment_method_manager.store_payment_method(self.dummy_account, 'c99831a4b9', gateway)

        charger.update_order_status(data)

        num_after = len(self.payment_method_manager.get_payment_methods(self.dummy_account, 'VALIDATED'))

        self.assertEqual(num_before, 0, 'No VALIDATED payment method should be registered!')
        self.assertEqual(num_after,  1, '1 VALIDATED payment method should be registered!')

    def test_worldpay_pending_payment_method_callback(self):
        data = dict(urlparse.parse_qsl('orderKey=TELEFONICA^GLOBALBILLINGEUR^c99831a4b9&paymentStatus=ERROR&mask=1&expiration=29/12/2019'))

        # Marking callback data as ERROR
        data['paymentStatus'] = 'ERROR'

        charger, gateway = self.gateways_manager.get_charger_by_name("WORLDPAY")

        num_before = len(self.payment_method_manager.get_payment_methods(self.dummy_account, 'VALIDATED'))

        self.payment_method_manager.store_payment_method(self.dummy_account, 'c99831a4b9', gateway)

        charger.update_order_status(data)

        num_after = len(self.payment_method_manager.get_payment_methods(self.dummy_account, 'VALIDATED'))

        self.assertEqual(num_before, 0, 'No VALIDATED payment method should be registered!')
        self.assertEqual(num_after,  0, 'No VALIDATED payment method should be registered!')

    def test_worldpay_store_masked_card(self):
        data = dict(urlparse.parse_qsl('orderKey=TELEFONICA^GLOBALBILLINGEUR^c99831a4b9&paymentStatus=ERROR&mask=1&expiration=29/12/2019'))

        # Marking callback data as ERROR
        data['paymentStatus'] = 'AUTHORISED'

        data['mask']       = '4111 **** **** 1111'
        data['expiration'] = '29/03/2014'

        charger, gateway = self.gateways_manager.get_charger_by_name("WORLDPAY")

        self.payment_method_manager.store_payment_method(self.dummy_account, 'c99831a4b9', gateway)

        charger.update_order_status(data)

        payment_gateway = self.payment_method_manager.get_payment_methods(self.dummy_account, 'VALIDATED')[0]

        self.assertEqual(payment_gateway.mask, data['mask'], 'Mask does not fit')
        self.assertEqual(payment_gateway.expiration.strftime(DATE_FORMAT), data['expiration'], 'Expiration date does not fit')


