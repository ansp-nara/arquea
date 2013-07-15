# -*- coding: utf-8 -*-

from django.template import Library
from identificacao.models import *
from django.contrib.admin.templatetags.admin_list import result_list

register = Library()

def busca(ed):
    ret = [ed]
    for e in ed.enderecodetalhe_set.order_by('complemento'):
        ret = ret + busca(e)
    return ret

@register.inclusion_tag("admin/change_list_results.html")
def result_list_patrimonio(cl):
    res = result_list(cl)
    results = res['results']
    results = [r for r in results if r.endereco]
    results = sorted(results, key=lambda x: x.endereco.entidade)

    lista = []
    for r in results:
        lista = lista + busca(r)

    res.update({'results':lista})
    return res
