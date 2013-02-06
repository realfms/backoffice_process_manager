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
import urllib, httplib

# Loading environment variables prior to initialice django framework
manage.read_env('../.env')

from django.test import TestCase

from tasks import notify_salesforce_task
from customer.salesforce import get_customer_details_from_sf

class TestGenerator(TestCase):
    
    def test_recurrent_charging_invocation(self):
        
        data = {'order_code': 40, 'tef_account': '1928jj2js', 'currency': 'EUR', 
                'total': 100, 'country': 'BR', 'statement': 'testing from backoffice'}
        
        params = urllib.urlencode(data)
        
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("localhost:8000")
        
        conn.request("POST", "/payment/recurrent", params, headers)
        
        response = conn.getresponse()
        
        print response.status, response.reason
        
        data = response.read()
        conn.close()

    def test_salesforce_update_contact(self):

        result = notify_salesforce_task('Billable', '003d000000lKGP2AAO')

        print result

    def test_salesforce_get_gustomer(self):

        result = get_customer_details_from_sf('003d000000kC2JHAA0')

        print result