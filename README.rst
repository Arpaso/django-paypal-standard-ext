PayPal Standard Payment Extension.
==================================

Use django-paypal branch: (https://github.com/dcramer/django-paypal)

Forms (paypal-standard-ext.forms)
-----

This module provides form mixin with fields:
	- email
	- first_name
	- last_name
	- image_url

Signals
-------

There is a 'paid' signal providing arguments: "user", "object", "receipt"

Models
------

class Custom, which has important fields:
	- user_pk
	- object_pk
	- content_type : (natural key)

Paypal's payment_was_successful signal's handler, which sends our 'paid' signal with user and object as arguments

Template tags
-------------

This package provides one module with template tags: shortcut, which has one defined tag: paypal_shortcut.
This tag returns rendered form to buy something.

Example::

	{% paypal_shortcut book %}
		
All arguments:
	- obj : purchased object
	- return_url : 'payment_done' by default
	- cancel_url : 'index' by default
	- form_class : paypal-standard-ext.forms.PayPalPaymentsForm by default

Settings
--------

PAYPAL_IMAGE_URL : related url to use as top image on PayPal site. "images/logo.png" by default.

SITE_NAME : PayPal site's merchant button's title. "Shop" by default.
