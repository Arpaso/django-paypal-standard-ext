### -*- coding: utf-8 -*- ####################################################

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from native_tags.decorators import function

from paypal_standard_ext.forms import PayPalPaymentsForm
from paypal_standard_ext.models import Custom

def paypal_shortcut(request, obj, return_url='payment_done', cancel_url='index', form_class=PayPalPaymentsForm):
    if request.user.is_authenticated():
        form = form_class(initial={
            "amount": obj.price,
            "item_name": '%s: %s' % ( Site.objects.get_current().name, unicode(obj) ),
            "item_number": obj.pk,
            
            "custom": Custom(request.user, obj).serialize(),
            
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            
            "no_shipping": 1, # No shipping
            
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return_url": request.build_absolute_uri(reverse(return_url)),
            "cancel_return": request.build_absolute_uri(reverse(cancel_url)),
            
            "cbt": getattr(settings, 'SITE_NAME', 'Shop'),
            "image_url": "%s%s" % (settings.MEDIA_URL, getattr(settings, 'PAYPAL_IMAGE_URL', 'images/logo.png'))
        })
        #: TODO: define more variables: https://cms.paypal.com/us/cgi-bin/?cmd=_render-content&content_ID=developer/e_howto_html_Appx_websitestandard_htmlvariables#id08A6HI0709B
        
        return form.sandbox() if getattr(settings, 'PAYPAL_TEST', False) else form.render()
paypal_shortcut = function(paypal_shortcut, takes_request=True)
