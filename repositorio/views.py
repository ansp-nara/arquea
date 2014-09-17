# -* coding: utf-8 -*-
from django.contrib.auth.decorators import permission_required, login_required
from django.core import serializers
from django.db.models import Q 
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe

from patrimonio.models import Patrimonio

@login_required
@require_safe
def ajax_seleciona_patrimonios(request):
	search_string = request.GET.get('string')
	patrimonios = Patrimonio.objects.filter(Q(ns__icontains=search_string)|Q(descricao__icontains=search_string)|Q(pagamento__protocolo__num_documento__icontains=search_string))
	return HttpResponse(serializers.serialize('json', patrimonios))
