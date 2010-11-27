### -*- coding: utf-8 -*- ####################################################
""" subscription signals """
from django.dispatch import Signal

paid = Signal(providing_args=["user", "object", "receipt"])
