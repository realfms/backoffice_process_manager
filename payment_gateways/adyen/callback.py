from payment_gateways.services import change_order_status
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
    elif request.method == 'POST':
        data = request.POST.dict()

        if data['success']:
            print "VALID"
            sys.stdout.flush()
            change_order_status(data['merchantReference'], "VALIDATED")
            return HttpResponse("[accepted]", mimetype="text/plain")
        else:
            print "ERROR"
            sys.stdout.flush()
            change_order_status(data['merchantReference'], "ERROR")
            return HttpResponse("[error]", mimetype="text/plain")
