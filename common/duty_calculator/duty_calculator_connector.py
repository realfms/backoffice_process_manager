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
Created on 21/03/2013

@author: mac@tid.es
'''

from BeautifulSoup import BeautifulSoup

import urllib2

class DutyCalculator():

    BASE_URL = "http://www.dutycalculator.com/api2.1/sandbox/5295f62bad0be300/"

    HS_CODE_BY_CAT_URL = "get-hscode&to={0}&cat[0]={1}&detailed_result=1"
    HS_CODE_BY_SKU_URL = "get-hscode&to={0}&sku[0]={1}&detailed_result=1"

    def getTaxByCategory(self, country, category):
        url = self.BASE_URL + self.HS_CODE_BY_CAT_URL.format(country, category)

        f = urllib2.urlopen(url)

        response = f.read()

        return self._parseResponse(response)

    def getTaxBySKU(self, country, sku):
        url = self.BASE_URL + self.HS_CODE_BY_SKU_URL.format(country, sku)

        f = urllib2.urlopen(url)

        response = f.read()

        return response

    def getTaxByCountriesAndCategory(self, countries, category):

        result = {}

        for country in countries:
            url = self.BASE_URL + self.HS_CODE_BY_CAT_URL.format(country, category)

            f = urllib2.urlopen(url)

            response = f.read()

            result[country] = self._parseResponse(response)

        print result

        return result

    def _parseResponse(self, xml):

        doc = BeautifulSoup(xml)

        duty = doc.find('duty').string
        VAT  = doc.find('sales-tax', {'name': 'VAT'}).string

        # Converting to float
        duty = self._parseTax(duty)
        VAT  = self._parseTax(VAT)

        return (VAT, duty)

    def _parseTax(self, tax):
        return float(tax[0:-1])
