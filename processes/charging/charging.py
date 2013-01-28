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
Created on 22/01/2013

@author: mac@tid.es
'''

import httplib, urllib

from django.conf import settings

import uuid

def charge_user(json):
    total = int(json['total'] * 100)
    order = compute_order_id()

    invoke_payment_enabler(order, "1928jj2js", "EUR",
                           total, "BR", "January invoice")

    return json

def invoke_payment_enabler(order_code, tef_account, currency, total, country, statement):

    data = {'order_code': order_code, 'tef_account': tef_account,
            'currency': currency, 'total': total,
            'country': country,  'statement': statement}

    params = urllib.urlencode(data)

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(settings.PAYMENT_ENABLER)

    conn.request("POST", "/recurrent", params, headers)

    response = conn.getresponse()

    print response.status, response.reason

    data = response.read()
    conn.close()

# TODO: Guarantee uid is unique among different nodes if this code is distributed
def compute_order_id():
    uid = uuid.uuid4()

    # Order = ten first characters of uuid
    return uid.hex[:10]