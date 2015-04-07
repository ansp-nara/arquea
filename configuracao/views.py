# -*- coding: utf-8 -*-
from .models import ClassesExtra
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

# Create your views here.

@login_required
def help_text(request, app_name, model):

    text = ClassesExtra.objects.get(content_type__app_label=app_name, content_type__model=model).help

    return TemplateResponse(request, 'configuracao/help.html', {'text':text})