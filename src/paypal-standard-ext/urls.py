### -*- coding: utf-8 -*- ####################################################

from django.conf.urls.defaults import *

urlpatterns = patterns('',

    (r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^done/$', 'meegenius.billing.views.done', name="payment_done"),
    
)
