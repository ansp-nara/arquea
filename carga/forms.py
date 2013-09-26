# -*- coding: utf-8 -*-
from models import *
from django import forms
from outorga.models import Termo, OrigemFapesp
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from protocolo.models import Protocolo
from django.forms.models import inlineformset_factory, BaseInlineFormSet

class UploadFileForm(forms.Form):
    file  = forms.FileField(label=_(u'Arquivo de patrimonios:'), )