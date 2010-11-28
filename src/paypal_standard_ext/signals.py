### -*- coding: utf-8 -*- ####################################################
from django.dispatch import Signal

paid = Signal(providing_args=["user", "obj", "receipt"])
