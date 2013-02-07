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

from models     import PaymentGateway, MasterInformation, Order, AcquiredData
from api_format import UserData

from django.conf import settings

import importlib
import uuid

def get_charger_by_name(name):
    gw = get_gateway_by_name(name)

    if gw == None:
        return (None, None)

    return (dynamically_loading_charger(gw), gw)

def get_first_available_charger_by_country(country):
    gw = get_gateway_by_country(country)

    if gw == None:
        return (None, None)

    return (dynamically_loading_charger(gw), gw)

def get_charger_by_tef_account_and_country(tef_account, country):
    master_info = get_master_info_by_tef_account_and_country(tef_account, country)

    if master_info == None:
        return (None, None)

    gw = master_info.gateway

    return (dynamically_loading_charger(gw), master_info)

def get_gateway_by_name(name):
    gws = PaymentGateway.objects.filter(name=name)

    if len(gws) == 0:
        return None

    return gws[0]

def get_gateway_by_country(country):
    gws = PaymentGateway.objects.filter(country=country)

    if len(gws) == 0:
        return None

    # If several, getting the first one
    return gws[0]

def get_master_info_by_tef_account_and_country(tef_account, country):
    master_infos = MasterInformation.objects.filter(tef_account=tef_account, gateway__country=country)

    if len(master_infos) == 0:
        return None

    # If several, getting the first one
    return master_infos[0]

def get_charger_by_master_information(country):
    gw = get_gateway_by_country(country)

    if gw == None:
        return None

    return dynamically_loading_charger(gw)


def initial_payment_url(token):

    user_data = get_user_data(token)

    (charger, gw) = get_first_available_charger_by_country(user_data.country)
    if (charger == None):
        return "/error"

    url = charger.get_redirect_url(user_data)

    store_master_information(user_data, charger.get_order(), gw)

    return url


def process_recurrent_payment(order_data):

    store_order(order_data)

    tef_account = order_data.tef_account
    country     = order_data.country

    (charger, master_info) = get_charger_by_tef_account_and_country(tef_account, country)
    if charger == None:
        return False

    charger.recurrent_payment(order_data, master_info)

    return True


def store_master_information(user_data, recurrent_order_code, gateway):
    master_info = MasterInformation(tef_account=user_data.tef_account, recurrent_order_code=recurrent_order_code,
                                     gateway=gateway, email=user_data.email)
    master_info.save()


def store_order(order_data):
    order = Order(total=order_data.total, currency=order_data.currency, country=order_data.country,
                  tef_account=order_data.tef_account, statement=order_data.statement,
                  order_code=order_data.order_code)

    order.save()


def dynamically_loading_charger(gw):
    charger_module = importlib.import_module(gw.module_name)
    charger = getattr(charger_module, gw.class_name)(gw)

    return charger


def get_user_data(token):
    acquired_data = AcquiredData.objects.get(token=token)

    user_data = UserData(tef_account=acquired_data.tef_account, address=acquired_data.address,
                         city=acquired_data.city, country=acquired_data.country,
                         postal_code=acquired_data.postal_code, email=acquired_data.email,
                         phone=acquired_data.phone)

    return user_data


def generate_form_url(user_data):
    token = compute_unique_id()

    acquired_data = AcquiredData(tef_account=user_data.tef_account, email=user_data.email,
                                 city=user_data.city, address=user_data.address,
                                 postal_code=user_data.postal_code, country=user_data.country,
                                 token=token)

    acquired_data.save()

    return settings.DEPLOY_URL + "/payment/acquire/form/" + token


def compute_unique_id():
    uid = uuid.uuid4()
    return uid.hex[:10]

