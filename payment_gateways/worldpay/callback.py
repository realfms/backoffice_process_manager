from django.shortcuts import render
from django.db        import transaction

from payment_gateways.services    import ServiceManager
from django.views.decorators.csrf import csrf_exempt

class WorldpayCallbackController:

    serviceManager = ServiceManager()

    @classmethod
    def getCharger(cls):
        return cls.serviceManager.get_charger_by_name("WORLDPAY")

    @classmethod
    @transaction.commit_on_success
    def success(cls, request):
        # TO BE REMOVED when a callback in worldpay is properly configured
        cls.callback(request)
        
        return render(request, 'payment_gateways/success.html', {})

    @classmethod
    @transaction.commit_on_success
    def pending(cls, request):
        # TO BE REMOVED when a callback in worldpay is properly configured
        cls.callback(request)
        
        return render(request, 'payment_gateways/pending.html', {})

    @classmethod
    @transaction.commit_on_success
    def error(cls, request):
        # TO BE REMOVED when a callback in worldpay is properly configured
        cls.callback(request)
        
        return render(request, 'payment_gateways/error.html', {})
    
    @classmethod
    @transaction.commit_on_success
    @csrf_exempt
    def callback(cls, request):
        # TO BE REVIEWED!
        # A professional deployment doesn't parse the URL of a http redirect but is useful for testing
        # Now testing data from redirection. A proper implementation of a callback will parse xml data comming from WP backend
        data = request.GET.dict()

        (charger, pgw) = cls.getCharger()

        print "FROM WorldPay Callback: {0}".format(data)

        charger.update_order_status(data)
