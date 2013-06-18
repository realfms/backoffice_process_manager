from django.shortcuts import render
from django.db        import transaction

from payment_gateways.services    import PaymentGatewayManager
from django.views.decorators.csrf import csrf_exempt

class WorldpayCallbackController:

    gateways_manager = PaymentGatewayManager()

    @classmethod
    def getCharger(cls):
        return cls.gateways_manager.get_charger_by_name("WORLDPAY")

    @classmethod
    @transaction.commit_on_success
    def success(cls, request):
        return render(request, 'payment_gateways/success.html', {})

    @classmethod
    @transaction.commit_on_success
    def pending(cls, request):
        return render(request, 'payment_gateways/pending.html', {})

    @classmethod
    @transaction.commit_on_success
    def error(cls, request):
        return render(request, 'payment_gateways/error.html', {})
    
    @classmethod
    @transaction.commit_on_success
    @csrf_exempt
    def callback(cls, request):
        data = request.POST.body

        (charger, pgw) = cls.getCharger()

        print data
        print "FROM WorldPay Callback: {0}".format(data)

        charger.update_order_status(data)
