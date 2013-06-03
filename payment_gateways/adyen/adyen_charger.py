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
Created on 14/01/2013

@author: mac@tid.es
'''


from datetime import datetime

from py_adyen.adyen import Adyen
from py_adyen.api import Api

from payment_gateways.gateway_interface.PaymentGateway import PaymentGateway

class Adyen_Charger (PaymentGateway):

    def __init__(self, model):
        super(Adyen_Charger, self).__init__(model)

    def get_redirect_url(self, account):

        data = {
            'merchantReference': self.order,
            'paymentAmount':     self.MONEY,
            'currencyCode':      self.CURRENCY,
            'shipBeforeDate':    datetime.now(),
            'shopperEmail':      account.email,
            'shopperReference':  account.account_id,
            'sessionValidity':   datetime.now(),
            'recurringContract': 'RECURRING',     
        }

        adyen_data = Adyen(data)
        adyen_data.sign()

        return adyen_data.get_redirect_url()

    def recurrent_payment(self, order, payment_method):
        ws = Api()

        account   = payment_method.account
        reference = order.order_code

        shopper_email     = account.email
        shopper_reference = account.account_id

        amount   = order.total
        currency = order.currency
        
        statement = "TBD"

        ws.authorise_recurring_payment(reference, statement, amount, currency, shopper_reference, shopper_email,
                                       shopper_ip=None, recurring_detail_reference='LATEST')

    def update_order_status(self, data):
        order_code = data['merchantReference']

        if data['success'] == "false":
            print "ERROR: PAYMENT GATEWAY PROBLEM"
            print data
            return False
        
        return self.identify_successful_flow(order_code, 'VALIDATED')