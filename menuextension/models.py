# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import Library
from django.core.urlresolvers import resolve
from treemenus.models import MenuItem


register = Library()


class MenuItemExtension(models.Model):
    menu_item = models.OneToOneField (MenuItem, related_name="extension")
    visivel = models.BooleanField(default=False)
    css = models.CharField(_(u'CSS style'), null=True, blank=True, max_length=300)

