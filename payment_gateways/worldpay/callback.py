from django.shortcuts import render
from payment_gateways.services import change_order_status


def success(request):
    params = request.GET.get

    order = params('orderKey')
    order_id = order.split("^")
    change_order_status(order_id[2], "VALIDATED")

    return render(request, 'payment_gateways/success.html', {})


def pending(request):
    return render(request, 'payment_gateways/pending.html', {})


def error(request):
    params = request.GET.get

    order = params('orderKey')
    order_id = order.split("^")

    change_order_status(order_id[2], "ERROR")

    return render(request, 'payment_gateways/error.html', {})
