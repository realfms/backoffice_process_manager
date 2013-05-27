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

from services   import ServiceManager

import unittest

# Loading environment variables prior to initialice django framework
manage.read_env('.env')

class TestPaymentDataAcquisition(TestCase):

    service_manager = ServiceManager()

    #@unittest.skip("Making tests faster")
    def test_redirect_to_adyen(self):

        token  = 'ccf0ff7333'
        params = {}

        url = self.service_manager.get_payment_gateway_redirect_url(token, params)

        self.assertTrue(url.startswith('https://test.adyen.com/hpp/pay.shtml'), 'Problem testing connection with Adyen')

    #@unittest.skip("Making tests faster")
    def test_already_registered(self):

        token  = 'mac'
        params = {}

        url = self.service_manager.get_payment_gateway_redirect_url(token, params)

        print url

        self.assertTrue(url.startswith('https://test.adyen.com/hpp/pay.shtml'), 'Problem testing connection with Adyen')

