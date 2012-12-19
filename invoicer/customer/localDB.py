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
Created on 16/10/2012

@author: mac@tid.es
'''

from django.contrib.auth.models import User

from payment.services import access_customer_data

def customer_details(invoice_data):
    username = invoice_data['contract']
    
    # Adding customer details
    invoice_data['customer'] = load_user_profile(username)
    
    return invoice_data

def load_user_profile(username):
    users = User.objects.filter(username=username)
    
    if (len(users) != 1):
        print "Unknown user: " + username
        return {}
    
    user = users[0]

    return access_customer_data(user)
