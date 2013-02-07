from payment_gateways.services import get_charger_by_name
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render

import sys


def success(request):
    return render(request, 'payment_gateways/success.html', {})


def pending(request):
    return render(request, 'payment_gateways/pending.html', {})


def error(request):
    return render(request, 'payment_gateways/error.html', {})

@csrf_exempt
def callback(request):

    if request.method == 'GET':
        data = request.GET.dict()

        if data['success']:
            return success(request)
        else:
            return error(request)

    if request.method == 'POST':
        data = request.POST.dict()

        (charger, gw) = get_charger_by_name('ADYEN')

        result = charger.update_order_status(data, "VALIDATED")

        if result:
            print "VALID"
            return HttpResponse("[accepted]", mimetype="text/plain")
        else:
            print "ERROR"
            return HttpResponse("[error]", mimetype="text/plain")
