### -*- coding: utf-8 -*- ####################################################
"""
$Id: models.py 100 2010-11-02 15:34:03Z admin $
"""
import pickle
import base64

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from paypal.standard.ipn.signals import payment_was_successful

from .signals import paid


class Custom(object):
    user_pk = ''
    object_pk = ''
    content_type = ()
    
    def __init__(self, user, obj):
        self.user_pk = user.pk 
        self.object_pk = obj.pk 
        self.content_type = ContentType.objects.get_for_model(obj).natural_key()
        super(Custom, self).__init__()
        
    def get_object(self):
        return ContentType.objects.get_by_natural_key(*self.content_type).get_object_for_this_type(pk=self.object_pk)
    
    def get_user(self):
        return User.objects.get(pk=self.user_pk)
    
    def serialize(self):
        pickled = pickle.dumps(self, pickle.HIGHEST_PROTOCOL)
        return base64.urlsafe_b64encode(pickled).decode("utf-8")
    
    @staticmethod
    def deserialize(serialized):
        b64 = base64.urlsafe_b64decode(serialized.encode("utf-8"))
        return pickle.loads(b64)


# Handle PayPal signals

def handle_payment_was_successful(sender, **kwargs):
    """Extends object and user objects from PayPal IPN receipt and sends a paid signal"""
    custom = Custom.deserialize(sender.custom)
    obj = custom.get_object()
    paid.send(type(obj), user=custom.get_user(), obj = obj, receipt=sender)
payment_was_successful.connect(handle_payment_was_successful)

