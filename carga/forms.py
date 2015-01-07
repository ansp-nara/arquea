# -*- coding: utf-8 -*-
from models import *
from django import forms
from django.utils.translation import ugettext_lazy as _

class UploadFileForm(forms.Form):
    file  = forms.FileField(label=_(u'Arquivo de patrimonios:'), )