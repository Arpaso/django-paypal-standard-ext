### -*- coding: utf-8 -*- ####################################################

from django import forms

from paypal.standard.widgets import ValueHiddenInput
from paypal.standard.forms import PayPalPaymentsForm as PayPalForm


class PaymentFormMixin(forms.Form):
    
    #User properties
    email = forms.CharField(widget=ValueHiddenInput())
    first_name = forms.CharField(widget=ValueHiddenInput())
    last_name = forms.CharField(widget=ValueHiddenInput())
    
    #Style
    image_url = forms.URLField(widget=ValueHiddenInput())

class PayPalPaymentsForm(PayPalForm, PaymentFormMixin):
    pass
