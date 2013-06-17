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

import urlparse

# Loading environment variables prior to initialice django framework
manage.read_env('.env')

WORLDPAY_CALLBACK_XML = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE paymentService PUBLIC "-//WorldPay//DTD WorldPay PaymentService v1//EN" "http://dtd.worldpay.com/paymentService_v1.dtd">
<paymentService version="1.4" merchantCode="GLOBALBILLINGEUR">
   <notify>
     <orderStatusEvent orderCode="c99831a4b9">
            <payment>
                 <paymentMethod>ECMC-SSL</paymentMethod>
                 <paymentMethodDetail>
                    <card number="5454********5454" type="creditcard">
                        <expiryDate><date month="01" year="2016"/></expiryDate>
                    </card>
                 </paymentMethodDetail>
                 <amount value="100" currencyCode="EUR" exponent="2" debitCreditIndicator="credit"/>

                 <lastEvent>AUTHORISED</lastEvent>
                 <CVCResultCode description="APPROVED"/>
                 <AVSResultCode description="APPROVED"/>

                 <cardHolderName><![CDATA[A S Yadav]]></cardHolderName>
                 <issuerCountryCode>N/A</issuerCountryCode>
                 <balance accountType="IN_PROCESS_AUTHORISED"><amount value="100" currencyCode="EUR" exponent="2" debitCreditIndicator="credit"/></balance>
                 <riskScore value="-79"/>
            </payment>
            <journal journalType="AUTHORISED">
                 <bookingDate>
                    <date dayOfMonth="06" month="11" year="2012"/>
                 </bookingDate>
                <accountTx accountType="IN_PROCESS_AUTHORISED" batchId="29">
                    <amount value="100" currencyCode="EUR" exponent="2" debitCreditIndicator="credit"/>
                </accountTx>
            </journal>
     </orderStatusEvent>
 </notify>
</paymentService>"""


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

    def test_worldpay_callback_xml(self):
        charger, gateway = self.gateways_manager.get_charger_by_name("WORLDPAY")

        payment_method = self.payment_method_manager.store_payment_method(self.dummy_account, 'c99831a4b9', gateway)

        charger.update_order_status(WORLDPAY_CALLBACK_XML)

        payment_method = self.payment_method_manager.get_payment_methods_by_order_code('c99831a4b9', 'VALIDATED')

        payment_method_dict = payment_method.to_dict()

        self.assertEqual(payment_method_dict['mask'], '5454********5454', 'Mask does not fit')
        self.assertEqual(payment_method_dict['expiration'], '01/2016', 'Expiration date does not fit')


