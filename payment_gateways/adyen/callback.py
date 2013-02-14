from payment_gateways.services import ServiceManager
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render

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

        if data['authResult'] == 'AUTHORISED':
            return success(request)
        else:
            return error(request)

    if request.method == 'POST':
        data = request.POST.dict()

        (charger, gw) = ServiceManager().get_charger_by_name('ADYEN')

        result = charger.update_order_status(data, "VALIDATED")

        print "CALLBACK RESULT:  {0}".format(result)

        if result:
            return HttpResponse("[accepted]", mimetype="text/plain")
        else:
            return HttpResponse("[error]", mimetype="text/plain")
