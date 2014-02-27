# -*- coding: utf-8 -*-
from django import forms
from repositorio.models import Repositorio

class RepositorioAdminForm(forms.ModelForm):
	
	class Meta:
		model = Repositorio
		
	class Media:
		js = ('/media/js/selects.js',)
		
	filtra_patrimonio = forms.CharField(label=u'Filtro do patrimônio', required=False,
							widget=forms.TextInput(attrs={'onchange':'ajax_filter_patrimonios();'}))
