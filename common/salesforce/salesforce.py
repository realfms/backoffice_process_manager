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
Created on 06/11/2012

@author: mac@tid.es
'''

from sforce.enterprise import SforceEnterpriseClient

from os import environ

SF_PRICELIST_ID = 'a13J0000000CtwvIAC'

def connect():
    c = SforceEnterpriseClient(environ.get('SF_WSDL_PATH'))
    c.login(environ.get('SF_LOGIN'), environ.get('SF_PWD'), environ.get('SF_TOKEN'))
    
    return c

def get_customers(account_id):
    
    c = connect()
    
    soql = """SELECT Email, Account.Name, Account.BillingCity, Account.BillingCountry, Account.BillingPostalCode, 
                     Account.BillingState, Account.BillingStreet 
              FROM   Contact
              WHERE  AccountId='{0}'""".format(account_id)

    results = c.query(soql)
    
    if results.size < 1:
        return None, None
    
    contact = results.records[0]
    account = contact.Account[0]
    
    return contact, account

def get_catalogue():
    c = connect()
    
    soql = """SELECT Name, Price_per_Hour__c, Price_per_Month__c, Product_Code__c
              FROM Rate_Card_Item__c
              WHERE Rate_Card__c = '{0}'
            """.format(SF_PRICELIST_ID)

    results =  c.query(soql)
    
    catalogue = {}
    
    products = []
    
    for product in results.records:
        products.append({
                         'code'        : product.Product_Code__c, 
                         'description' : product.Name,
                         'price'       : product.Price_per_Hour__c
                         })
    
    catalogue['products'] = products
    
    return catalogue
