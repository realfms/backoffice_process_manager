#!/usr/bin/python
#coding=utf-8 

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
Created on 17/10/2012

@author: mac@tid.es
'''

import uuid

class PaymentGateway(object):

    def __init__(self, model):
        self.URL = model.endpoint

        self.USERNAME = model.merchant
        self.PASSWORD = model.password

        self.SUCCESS_CALLBACK = model.success_callback
        self.ERROR_CALLBACK = model.error_callback
        self.PENDING_CALLBACK = model.pending_callback

        self.MONEY    = 100
        self.CURRENCY = 'EUR'

        self.order = self.compute_order_id()

    def get_order(self):
        return self.order
    
    def compute_order_id(self):
        uid = uuid.uuid4()
        
        # Order = ten first characters of uuid
        return uid.hex[:10]
 
    ###########################################################
    # Should be overwritten by specific implementations of Payment Gateways
    ########################################################### 

    def get_redirect_url(self, user_data):
        pass
    
    def recurrent_payment(self, order_data, master_info):
        pass
