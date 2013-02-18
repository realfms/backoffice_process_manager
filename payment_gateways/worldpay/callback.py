from django.shortcuts import render

from payment_gateways.services import ServiceManager


class WorldpayCallbackController:

    serviceManager = ServiceManager()

    def getCharger(cls):
        return cls.serviceManager.get_charger_by_name("ADYEN")

    def success(cls, request):
        params = request.GET.get

        order = params('orderKey')
        order_id = order.split("^")

        charger = cls.getCharger()

        charger.update_order_status(order_id[2], "VALIDATED")

        return render(request, 'payment_gateways/success.html', {})


    def pending(cls, request):
        return render(request, 'payment_gateways/pending.html', {})


    def error(cls, request):
        params = request.GET.get

        order = params('orderKey')
        order_id = order.split("^")

        charger = cls.getCharger()

        charger.update_order_status(order_id[2], "ERROR")

        return render(request, 'payment_gateways/error.html', {})
