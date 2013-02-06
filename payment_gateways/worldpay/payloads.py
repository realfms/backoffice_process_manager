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
Created on 17/10/2012

@author: mac@tid.es
'''

FIRST_PAYMENT_PAYLOAD = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE paymentService PUBLIC "-//WorldPay/DTD WorldPay PaymentService v1//EN" "http://dtd.worldpay.com/paymentService_v1.dtd">
    <paymentService version="1.4" merchantCode="%(merchantCode)s">
    <submit>
    <order orderCode="%(ordercode)s">
    <description>TEST First Payment Order</description>
    <amount value="%(fillmoney)s" currencyCode="EUR" exponent="2" />
    <orderContent>TEST TEF PAYMENT ORDER V4444333322221111, MC5100080000000000 </orderContent>
    <paymentMethodMask>
    <include code="ALL"/>
    </paymentMethodMask>
    <shopper><shopperEmailAddress>globalbilling-internal@tid.es</shopperEmailAddress></shopper>
    <shippingAddress>
    <address>
    <firstName>Instant Server</firstName>
    <lastName>Telefonica Digital Online Channel</lastName>
    <address1>%(address)s</address1>
    <address2></address2>
    <address3></address3>
    <postalCode>%(postal_code)s</postalCode>
    <city>%(city)s</city>
    <countryCode>%(country)s</countryCode>
    <telephoneNumber>%(phone)s</telephoneNumber>
    </address>
    </shippingAddress>
    </order>
    </submit>
    </paymentService>"""

RECURRENT_PAYMENT_PAYLOAD = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE paymentService PUBLIC "-//WorldPay/DTD WorldPay PaymentService v1//EN" "http://dtd.worldpay.com/paymentService_v1.dtd">
    <paymentService version="1.4" merchantCode="%(merchantCode)s">
    <submit>
    <order orderCode="%(ordercode)s">
     <description>RECURRENT PAyment associated to First Order: %(lastordercode)s </description>
    <amount value="%(fillmoney)s" currencyCode="EUR" exponent="2" />
    <orderContent>TEST RECURRENT TEF PAYMENT ORDER %(lastordercode)s </orderContent>
    <payAsOrder orderCode="%(lastordercode)s" merchantCode="%(firstMerchantCode)s"> 
    <amount value="128" currencyCode="EUR" exponent="2" />
    </payAsOrder>
    </order>
    </submit>
    </paymentService>"""