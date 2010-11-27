### -*- coding: utf-8 -*- ####################################################

from django.http import QueryDict
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.ipn.views import ipn

@require_POST
@csrf_exempt
def done(request):
    ipn(request)
    return redirect('index')
