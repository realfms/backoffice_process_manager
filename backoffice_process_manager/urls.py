from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import settings

urlpatterns = patterns('',

    url(r'^$', 'processes.views.index'),

    url(r'^launchInvoicing/$',      'processes.views.launchInvoicing'),
    url(r'^launchSyncInvoicing/$',  'processes.views.launchSyncInvoice'),

    url(r'^chargingCallback/$',   'processes.views.chargingCallback'),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
)
