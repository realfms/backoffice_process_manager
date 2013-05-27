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
from payment_gateways.models import Order, PaymentMethod
from payment_gateways.services import ServiceManager

from processes.data_acquisition_process import DataAcquisitionProcess

class Adyen_Charger (PaymentGateway):

    def __init__(self, model):
        super(Adyen_Charger, self).__init__(model)
        self.service_manager          = ServiceManager()
        self.data_acquisition_manager = DataAcquisitionProcess(self.service_manager)

    def get_redirect_url(self, user_data):

        user_data = {
            'merchantReference': self.order,
            'paymentAmount': self.MONEY,
            'currencyCode': self.CURRENCY,
            'shipBeforeDate': datetime.now(),
            'shopperEmail': user_data.email,                   
            'shopperReference': user_data.tef_account,         
            'sessionValidity': datetime.now(),                  
            'recurringContract': 'RECURRING',     
        }

        adyen_data = Adyen(user_data)
        adyen_data.sign()

        return adyen_data.get_redirect_url()

    def recurrent_payment(self, order_data, master_info):
        ws = Api()

        statement = order_data.statement  
        reference = order_data.order_code

        shopper_email     = master_info.email
        shopper_reference = master_info.tef_account

        amount   = order_data.total
        currency = order_data.currency

        ws.authorise_recurring_payment(reference, statement, amount, currency, shopper_reference, shopper_email,
                                       shopper_ip=None, recurring_detail_reference='LATEST')

    def update_order_status(self, data, status):
        order_code = data['merchantReference']

        if data['success'] == "false":
            print "ERROR: PAYMENT GATEWAY PROBLEM"
            print data
            return False

        payment_methods = PaymentMethod.objects.filter(recurrent_order_code=order_code, status='PENDING')

        # Distinguising flows
        if len(payment_methods) == 1:
            return self.data_acquisition_flow(payment_methods[0], status)

        # Callback of recurrent payment flow
        orders = Order.objects.filter(order_code=order_code, status='PENDING')

        if len(orders) == 1:
            return self._recurrent_payment_flow(orders, status)

        # Neither data acquistion flow nor recurrent payment flow, this is an error!
        print "ERROR: NEITHER ACQUISITION NOR RECURRENT FLOW IN ADYEN CALLBACK"
        return False

    def data_acquisition_flow(self, payment_method, status):
        # Callback of payment data acquisition flow
        print "DATA ACQUISITION FLOW"
        print status

        payment_method.status = status
        payment_method.save()

        contract = self.data_acquisition_manager.get_contract_by_payment_method(payment_method)

        print contract.id

        # Start Async notify process
        self.data_acquisition_manager.start_notify_new_payment_method_data('Billable', payment_method, contract.subprocess, contract.contract_id)

        return True

    def _recurrent_payment_flow(self, orders, status):
        # Callback of recuerrent payment flow
        print "RECURRENT ORDER FLOW"

        order = orders[0]

        order.status = status
        order.save()

        return True