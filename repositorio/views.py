from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.core import serializers
from patrimonio.models import Patrimonio
from django.db.models import Q 

# Create your views here.

def seleciona_patrimonios(request):
	if request.method == 'POST':
		raise Http404
		
	search_string = request.GET.get('string')
	patrimonios = Patrimonio.objects.filter(Q(ns__icontains=search_string)|Q(descricao__icontains=search_string)|Q(pagamento__protocolo__num_documento__icontains=search_string))
	return HttpResponse(serializers.serialize('json', patrimonios))
