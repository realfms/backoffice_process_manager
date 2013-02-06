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

from api_format import OrderData, UserData
from models     import PaymentGateway, MasterInformation, Order
from services   import initial_payment_url, process_recurrent_payment

# Loading environment variables prior to initialice django framework
manage.read_env('../.env')

class TestGenerator(TestCase):
    
    def test_adyen_data_acquisition(self):
        
        user_data = UserData(tef_account="inexistent", city="city", address="street", 
                             postal_code="28282", country="BR", phone="28282", email="mac@tid.es")
        
        initial_payment_url(user_data)
        
        gw = PaymentGateway.objects.get(name="ADYEN")
        
        master_infos = MasterInformation.objects.filter(tef_account=user_data.tef_account, 
                                                        gateway__country=user_data.country)
        
        self.assertEqual(len(master_infos), 1)

        master_info = master_infos[0]
        
        self.assertEqual(master_info.gateway, gw)
        self.assertEqual(master_info.tef_account, user_data.tef_account)
        self.assertEqual(master_info.email, user_data.email)
        self.assertEqual(master_info.status, 'PENDING')
    
    def test_adyen_recurrent_payment(self):
        
        order_data = OrderData(tef_account="1928jj2js", total=100, currency='EUR', country='BR', 
                               statement="statement", order_code="20")
        
        process_recurrent_payment(order_data)
        
        order = Order.objects.get(order_code=order_data.order_code)
        
        self.assertEqual(order.currency, order_data.currency)
        self.assertEqual(order.country, order_data.country)
        self.assertEqual(order.total, order_data.total)
        self.assertEqual(order.statement, order_data.statement)
        self.assertEqual(order.tef_account, order_data.tef_account)
