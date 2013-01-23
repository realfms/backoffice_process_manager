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

from jinja2 import Template

from common.salesforce.salesforce import get_catalogue

import codecs

TEMPLATE_PATH  = "catalogue/catalogue.tpl"
CATALOGUE_PATH = "processes/rating/catalogue.py"

def generate_catalogue_from_sf():
    
    catalogue = get_catalogue()
    
    with codecs.open(TEMPLATE_PATH, 'r', 'utf-8') as f:
        template_content = f.read()
        
    template = Template(template_content)
    
    with open (CATALOGUE_PATH, "wb") as f:
        f.write(template.render(catalogue))
    
    return CATALOGUE_PATH