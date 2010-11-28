### -*- coding: utf-8 -*- ####################################################

from native_tags.decorators import function
from paypal.standard.conf import TEST

from paypal_standard_ext.forms import PayPalPaymentsForm
from paypal_standard_ext.utils import collect_params


def paypal_shortcut(request, obj, return_url='/', cancel_url='/', form_class=PayPalPaymentsForm):
    if request.user.is_authenticated():
        form = form_class(initial=collect_params(request, obj, return_url, cancel_url))
        return form.sandbox() if TEST else form.render()
    else:
        return ''
paypal_shortcut = function(paypal_shortcut, takes_request=True)
