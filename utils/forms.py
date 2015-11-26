# -*- coding: utf-8 -*-

from django import forms
from django.contrib.admin.widgets import AdminDateWidget


NARA_DATE_FORMATS = ('%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d')


class NARADateField(forms.DateField):

    def __init__(self, input_formats=None, *args, **kwargs):
        super(NARADateField, self).__init__(input_formats=NARA_DATE_FORMATS, *args, **kwargs)
        self.widget = AdminDateWidget()
