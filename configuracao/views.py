# -*- coding: utf-8 -*-
from .models import ClassesExtra, FieldsHelp
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.http import HttpResponse

# Create your views here.


@login_required
def help_text(request, app_name, model):

    try:
        ce = ClassesExtra.objects.get(content_type__app_label=app_name, content_type__model=model)
        text = ce.help
    except ClassesExtra.DoesNotExist:
        text = ''

    return TemplateResponse(request, 'configuracao/help.html', {'text': text})


def has_help_text(request, app_name, model):
    return HttpResponse(ClassesExtra.objects.filter(content_type__app_label=app_name,
                                                    content_type__model=model).count())


def tooltip(request, app_name, model):
    field_name = request.GET.get('field_name')
    try:
        fh = FieldsHelp.objects.get(model__content_type__app_label=app_name, model__content_type__model=model,
                                    field=field_name)
        ret = fh.help
    except FieldsHelp.DoesNotExist:
        ret = field_name
    return HttpResponse(ret)