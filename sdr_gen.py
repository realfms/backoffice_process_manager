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

@author: ablazquez@conwet.com
@author: sperez@conwet.com
'''

import random, datetime

from common.aws.s3 import upload_invoice_to_s3


def gen_sdr():
    # def gen_sdr(tefaccount_id):
    now = str(datetime.datetime.now())
    xml = """
          <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <fichero_consumos_variables>
            <fecha_envio>#{now}</fecha_envio>
            <consumos_variables total_registros="4">
                <consumo_variable>
                    <id>#{tefaccount_id}</id>
                    <contrato>#{contract_id}</contrato>
                    <servicio_comercial>0</servicio_comercial>
                    <concepto_facturable>10052</concepto_facturable>
                    <fecha_consumo>2012-07Z</fecha_consumo>
                    <unidades>348.0</unidades>
                    <posicion>1</posicion>
                    <total_posiciones>1</total_posiciones>
                </consumo_variable>
            </consumos_variables>
            </fichero_consumos_variables>
          """

    xml = xml.replace("#{now}", now)
    xml = xml.replace("#{tefaccount_id}", str(random.randint(1, 3000000)))
    xml = xml.replace("#{contract_id}", str(random.randint(1, 3000000)))

    print xml

    file_name = 'sdr-' + now
    f = open(file_name, 'w')
    f.write(xml)
    f.close()

    upload_invoice_to_s3(file_name)

gen_sdr()
