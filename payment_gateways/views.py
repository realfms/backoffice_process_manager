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
Created on 16/10/2012

@author: mac@tid.es
'''

from django.http        import HttpResponse
from django.shortcuts   import render
from django.http        import HttpResponseRedirect
from django.db          import transaction
from django.utils       import  simplejson

from services   import initial_payment_url, process_recurrent_payment, generate_form_url
from api_format import UserData, OrderData

from django.views.decorators.csrf import csrf_exempt

import sys

@transaction.commit_on_success
@csrf_exempt
def acquire_service(request):

    if request.method == 'POST':

        body = request.body

        print body
        sys.stdout.flush()

        json = simplejson.loads(body)

        tef_account = json.get('tef_account', None)
        city        = json.get('city', None)
        address     = json.get('address', None)
        postal_code = json.get('postal_code', None)
        country     = json.get('country', None)
        phone       = json.get('phone', None)
        email       = json.get('email', None)

        if (not tef_account or not city or not address or not postal_code or
            not country or not phone or not email):
            return HttpResponse('<h1>Insufficient parameters!</h1>', status=405)

        print "VALIDATED"
        print tef_account
        print city
        print address
        print postal_code
        print country
        print phone
        print email
        sys.stdout.flush()

        user_data = UserData(tef_account, city, address, postal_code, country, phone, email)

        url = generate_form_url(user_data)

        return HttpResponse(url, content_type='text/plain')
    else:
        return HttpResponse('<h1>Invalid Method</h1>', status=405)


def acquire_form(request, token):

    if request.method == 'GET':
        return render(request, 'payment_gateways/acquire_form.html', {'code': token } )
    else:
        return HttpResponse('<h1>Invalid Method</h1>', status=405)

@transaction.commit_on_success
def acquire_redirect(request):

    if request.method == 'POST':

        params = request.POST.get

        token = params('token', None)
        
        url = initial_payment_url(token)
    
        return HttpResponseRedirect(url)
    else:
        return HttpResponse('<h1>Invalid Method</h1>', status=405)