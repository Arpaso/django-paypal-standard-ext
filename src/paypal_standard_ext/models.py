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

#===============================================================================
# class Category(MPTTModel):
#    """
#    Category of video. Used for grouping videos.
#    
#        - **title** -- title of category
#        - **external_slug** -- original unique string identifier, base on title
#    
#    Get or create new category 
#    
#    >>> obj, created = Category.objects.get_or_create(title="News", external_slug="news")
#    >>> obj
#    <Category: News>
#    
#    Validation. Both fields are required. Pair (Title, Parent) is unique.
#    
#    >>> Category().full_clean()
#    Traceback (most recent call last):
#    ...
#    ValidationError: {'external_slug': [u'This field cannot be blank.'], 'title': [u'This field cannot be blank.']}
#    >>> Category(title="News", parent=obj, external_slug="news1").save()
#    >>> Category(title="News", parent=obj, external_slug="news2").full_clean()
#    Traceback (most recent call last):
#    ...
#    ValidationError: {'__all__': [u'Category with this Parent and Title already exists.']}
#    """
# 
#    title = models.CharField(_("Title"), max_length=255)
#    external_slug = models.CharField(_("External slug"), unique=True, max_length=255, db_index=True)
#    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
# 
#    class MPTTMeta:
#        order_insertion_by = ('title',)
#    
#    class Meta:
#        verbose_name = _("category")
#        verbose_name_plural = _("categories")
#    
#    def __unicode__(self):
#        return self.title
# 
# class Video(models.Model):
#    """
#    Stores information about video fragment:
#    
#        - **category** -- reference to category
#        - **external_ident** -- Original identifier. string
#        - **title** -- title of press, required and unique string
#        - **external_slug** -- original unique string identifier, based on title
#    
#    >>> category = Category.objects.get(pk=1)
#    >>> obj, created = Video.objects.get_or_create(category=category, external_ident='123', 
#    ...                    title="Some video", external_slug="some_video")
#    >>> obj
#    <Video: Some video>
#    
#    Validation
#    
#    >>> from django.core.exceptions import ValidationError
#    
#    All fields are required.
#    
#    >>> Video().full_clean()
#    Traceback (most recent call last):
#    ...
#    ValidationError: {'category': [u'This field cannot be null.'], 'external_ident': [u'This field cannot be blank.'], 'external_slug': [u'This field cannot be blank.'], 'title': [u'This field cannot be blank.']}
#    
#    """
# 
#    category = models.ForeignKey(Category, related_name="videos")
#    external_ident = models.CharField(_("External identifier"), max_length=20, db_index=True)
#    external_slug = models.CharField(_("External slug"), max_length=255, db_index=True)
#    title = models.CharField(_("Title"), max_length=255)
# 
#    class Meta:
#        unique_together = ('external_ident', 'external_slug')
#        verbose_name = _("video reference")
#        verbose_name_plural = _("video references")
# 
#    def __unicode__(self):
#        return self.title
# 
#    def external_url(self, base_url="http://etvnet.com"):
#        """ 
#        Concatenates base url, external slug and ident
#        
#        >>> obj = Video(external_ident="123", external_slug="test_slug")
#        >>> obj.external_url()
#        'http://etvnet.com/test_slug/123/'
#        """
#        return "%s/%s/%s/" % (base_url, self.external_slug, self.external_ident)
#===============================================================================
