from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import settings

urlpatterns = patterns('',

    url(r'^$',                    'invoicer.views.index'),

    url(r'^launchInvoice/$',      'invoicer.views.launchInvoice'),
    url(r'^launchSyncInvoice/$',  'invoicer.views.launchSyncInvoice'),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
)
