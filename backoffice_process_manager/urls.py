from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import settings

from payment_gateways.views import PaymentMethodController, ContractController
from customers.views        import BillingAddressController, OrderController
from processes.views        import ProcessesController
from processes.tos          import ToSController
from demo.views             import DemoController


from payment_gateways.adyen.callback    import AdyenCallbackController
from payment_gateways.worldpay.callback import WorldpayCallbackController

urlpatterns = patterns('',


    ######################################################
    # ADMIN
    ######################################################
    ('^admin/', include(admin.site.urls)),

    ######################################################
    # CONTRACT URLS
    ######################################################

    # contract management API
    url(r'^contract/new$', ContractController.create),

    ######################################################
    # PAYMENT METHOD URLS
    ######################################################

    # payment method acquisition API
    url(r'^payment_method$',     PaymentMethodController.list),
    url(r'^payment_method/new$', PaymentMethodController.create),

    # billing address API
    url(r'^billing_address$',     BillingAddressController.list),
    url(r'^billing_address/new$', BillingAddressController.create),

    # adyen callback API
    url(r'^payment_gateway/adyen$', AdyenCallbackController.callback),

    # worldpay callback API
    url(r'^payment_gateway/worldpay/success$',  WorldpayCallbackController.success),
    url(r'^payment_gateway/worldpay/pending$',  WorldpayCallbackController.pending),
    url(r'^payment_gateway/worldpay/error$',    WorldpayCallbackController.error),
    url(r'^payment_gateway/worldpay/callback$', WorldpayCallbackController.callback),

    ######################################################
    # ORDERING
    ######################################################

    # ordering API
    url(r'^order/new$', OrderController.create),

    ######################################################
    # PROCESSES
    ######################################################

    url(r'^processes/launch_provision$',         ProcessesController.launch_provision),
    url(r'^processes/launch_invoicing/$',        ProcessesController.launch_invoicing),
    url(r'^processes/launch_sync_invoicing/$',   ProcessesController.launch_sync_invoice),
    url(r'^processes/getinfo/(?P<user_id>\w+)$', ProcessesController.get_processes),

    ######################################################
    # TERMS OF SERVICE
    ######################################################

    url(r'^tos/$', ToSController.show),

    ######################################################
    # DEMO
    ######################################################

    url(r'^demo/$',                DemoController.index),
    url(r'^demo/opt_in$',          DemoController.opt_in),
    url(r'^demo/billing_address$', DemoController.billing_address),
    url(r'^demo/payment_method$',  DemoController.payment_method),
    url(r'^demo/order$',           DemoController.order),


    ######################################################
    # STATIC CONTENT
    ######################################################

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
)
