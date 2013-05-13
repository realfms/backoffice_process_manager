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
Created on 30/10/2012

@author: mac@tid.es
'''

from os import environ

AWS_ACCESS_KEY_ID     = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

SDR_REQUESTS_BUCKET  = 'com.telefonicadigital.bpm.sdr.requests'
SDR_RESPONSES_BUCKET = 'com.telefonicadigital.bpm.sdr.responses'
PDF_INVOICES_BUCKET  = 'com.telefonicadigital.bpm.pdf.invoices'

EMAIL_FROM  = 'mac@tid.es'
EMAIL_TITLE = 'Your invoice from Telefónica Digital'
EMAIL_BODY  = 'Please, find attached your invoice'