from payment_gateways.services import PaymentGatewayManager
from django.views.decorators.csrf import csrf_exempt

from django.http      import HttpResponse
from django.shortcuts import render
from django.db        import transaction

class AdyenCallbackController:

    gateways_manager = PaymentGatewayManager()

    @classmethod
    def getCharger(cls):
        return cls.gateways_manager.get_charger_by_name("ADYEN")

    @classmethod
    def success(cls, request):
        return render(request, 'payment_gateways/success.html', {})

    @classmethod
    def pending(cls, request):
        return render(request, 'payment_gateways/pending.html', {})

    @classmethod
    def error(cls, request):
        return render(request, 'payment_gateways/error.html', {})

    @classmethod
    @transaction.commit_on_success
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

            (charger, pgw) = cls.getCharger()

            print data

            result = charger.update_order_status(data)

            print "CALLBACK RESULT:  {0}".format(result)

            if result:
                return HttpResponse("[accepted]", mimetype="text/plain")
            else:
                return HttpResponse("[error]", mimetype="text/plain")
