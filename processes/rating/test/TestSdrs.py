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
Created on 14/11/2012

@author: mac@tid.es
'''

from django.utils import unittest

from test1_sdr import XML
from catalogue import CATALOGUE, TAX

from processes.rating.rating import parse_sdr

class TestSdrs(unittest.TestCase):
    
    file_name = 'test1'
    
    def test_test1_sdr(self):
        
        data = parse_sdr(XML, self.file_name, CATALOGUE, TAX)
        
        self.assertEqual(data['total'],         float(1365.25))
        self.assertEqual(data['sdr_file_name'], self.file_name)