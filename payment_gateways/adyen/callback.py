from payment_gateways.services import ServiceManager
from django.views.decorators.csrf import csrf_exempt

from django.http      import HttpResponse
from django.shortcuts import render

from adyen_charger import Adyen_Charger

class AdyenCallbackController:

    serviceManager = ServiceManager()

    def getCharger(cls):
        return cls.serviceManager.get_charger_by_name("ADYEN")

    def success(cls, request):
        return render(request, 'payment_gateways/success.html', {})


    def pending(cls, request):
        return render(request, 'payment_gateways/pending.html', {})


    def error(cls, request):
        return render(request, 'payment_gateways/error.html', {})

    @csrf_exempt
    def callback(cls, request):

        if request.method == 'GET':
            data = request.GET.dict()

            if data['authResult'] == 'AUTHORISED':
                return cls.success(request)
            else:
                return cls.error(request)

        if request.method == 'POST':
            data = request.POST.dict()

            charger = cls.getCharger()

            result = charger.update_order_status(data, "VALIDATED")

            print "CALLBACK RESULT:  {0}".format(result)

            if result:
                return HttpResponse("[accepted]", mimetype="text/plain")
            else:
                return HttpResponse("[error]", mimetype="text/plain")
