### -*- coding: utf-8 -*- ####################################################

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from paypal.standard.conf import (POSTBACK_ENDPOINT, SANDBOX_POSTBACK_ENDPOINT, 
    RECEIVER_EMAIL, TEST)

from .models import Custom

def collect_params(request, obj, return_url, cancel_url):
    
    return {
        "business": RECEIVER_EMAIL,
        "amount": obj.price,
        "item_name": '%s: %s' % ( Site.objects.get_current().name, unicode(obj) ),
        "item_number": obj.pk,
        
        "custom": Custom(request.user, obj).serialize(),
        
        "email": request.user.email,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(return_url),
        "return": request.build_absolute_uri(return_url),
        "cancel_return": request.build_absolute_uri(cancel_url),
        
        "cmd": "_xclick",
        "charset": "utf-8",
        "currency_code": "USD",
        "no_shipping": 1, # No shipping
        
        "cbt": getattr(settings, 'SITE_NAME', 'Shop'),
        "image_url": "%s%s" % (settings.MEDIA_URL, getattr(settings, 'PAYPAL_IMAGE_URL', 'images/logo.png'))
    }
    #: TODO: define more variables: https://cms.paypal.com/us/cgi-bin/?cmd=_render-content&content_ID=developer/e_howto_html_Appx_websitestandard_htmlvariables#id08A6HI0709B

def get_params_with_endpoint(request, obj, return_url='/', cancel_url='/'):
    params = collect_params(request, obj, return_url, cancel_url)
    end_point = SANDBOX_POSTBACK_ENDPOINT if TEST else POSTBACK_ENDPOINT
    return params, end_point
