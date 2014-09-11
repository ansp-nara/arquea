# -*- coding: utf-8 -*-
from django import forms
from repositorio.models import Repositorio
from django.forms.util import ErrorList
from patrimonio.models import Patrimonio
from django.db.models import Q

class RepositorioAdminForm(forms.ModelForm):
	
	def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
		super(RepositorioAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)
                                       
		pt = self.fields['patrimonios']
        
		if data:
			search_string = data['filtra_patrimonio']
			pt.queryset = Patrimonio.objects.filter(Q(ns__icontains=search_string)|Q(descricao__icontains=search_string)|Q(pagamento__protocolo__num_documento__icontains=search_string))
		elif instance:
			pt.queryset = instance.patrimonios
		else:
			pt.queryset = Patrimonio.objects.filter(id__in=[0])
			
	class Meta:
		model = Repositorio
		fields = ['data_ocorrencia', 'tipo', 'natureza', 'estado', 'servicos', 'ocorrencia', 'anterior', 'memorandos', 'filtra_patrimonio', 'patrimonios', 'responsavel', 'demais', 'obs',]

		
	class Media:
		js = ('/media/js/selects.js',)
		
	filtra_patrimonio = forms.CharField(label=u'Filtro do patrimônio', required=False,
							widget=forms.TextInput(attrs={'onchange':'ajax_filter_patrimonios();'}))
