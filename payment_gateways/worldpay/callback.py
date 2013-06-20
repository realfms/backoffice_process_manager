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

from django.shortcuts import render
from django.db        import transaction

from payment_gateways.services    import PaymentGatewayManager
from django.views.decorators.csrf import csrf_exempt

class WorldpayCallbackController:

    gateways_manager = PaymentGatewayManager()

    WORLDPAY_CALLBACK_XML = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE paymentService PUBLIC "-//WorldPay//DTD WorldPay PaymentService v1//EN" "http://dtd.worldpay.com/paymentService_v1.dtd">
    <paymentService version="1.4" merchantCode="GLOBALBILLINGEUR">
       <notify>
         <orderStatusEvent orderCode="{0}">
                <payment>
                     <paymentMethod>ECMC-SSL</paymentMethod>
                     <paymentMethodDetail>
                        <card number="4111********1111" type="creditcard">
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

    @classmethod
    def getCharger(cls):
        return cls.gateways_manager.get_charger_by_name("WORLDPAY")

    @classmethod
    @transaction.commit_on_success
    def success(cls, request):

        ############################################################
        # Redicect invoking callback logic!
        # THIS IS ONLY FOR DEMO PURPOSES! Remove this when Payment Gateway is properly configred to make callbacks!
        params = request.GET.dict()

        (charger, pgw) = cls.getCharger()

        order_key = params['orderKey']
        size      = len(charger.USERNAME) + 1

        order_code = order_key[order_key.find(charger.USERNAME)+size:]

        xml = cls.WORLDPAY_CALLBACK_XML.format(order_code)

        cls.process_callback(xml)
        ############################################################

        return render(request, 'payment_gateways/success.html', {'url': '/demo/order'})

    @classmethod
    @transaction.commit_on_success
    def pending(cls, request):
        return render(request, 'payment_gateways/pending.html', {})

    @classmethod
    @transaction.commit_on_success
    def error(cls, request):
        return render(request, 'payment_gateways/error.html', {})
    
    @classmethod
    @transaction.commit_on_success
    @csrf_exempt
    def callback(cls, request):
        xml = request.POST.body

        cls.process_callback(xml)

    @classmethod
    def process_callback(cls, xml):
        (charger, pgw) = cls.getCharger()

        print xml
        print "FROM WorldPay Callback: {0}".format(xml)

        charger.update_order_status(xml)
