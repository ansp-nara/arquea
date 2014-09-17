# -*- coding: utf-8 -*-

from django.template.response import TemplateResponse
from django.contrib.auth.decorators import permission_required, login_required

from models import *
from utils.functions import render_to_pdf


def processos(request, pdf=False):
    
    areas = []
    for a in Area.objects.all():
        area = {'area':a}
        grupos = []
        for g in a.grupo_set.all():
            grupo = {'grupo':g}
            macroprocessos = []
            for m in g.macroprocesso_set.all():
                macroprocesso = {'macroprocesso':m, 'processos':m.processo_set.all()}
                macroprocessos.append(macroprocesso)
            grupo['macroprocessos'] = macroprocessos
            grupos.append(grupo)
        area['grupos'] = grupos
        areas.append(area)

    if pdf == '2':
        return render_to_pdf('processo/processos2.pdf', {'areas':areas}, request=request, filename='processos.pdf')
    elif pdf:
        return render_to_pdf('processo/processos.pdf', {'areas':areas, 'tamanho':pdf}, request=request, filename='processos.pdf')
    else:
        return TemplateResponse(request, 'processo/processos.html', {'areas':areas})
