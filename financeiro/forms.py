# -*- coding: utf-8 -*-
from models import *
from django import forms
from outorga.models import Termo, OrigemFapesp
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from protocolo.models import Protocolo

class PagamentoAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
		   
        super(PagamentoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)


        # Permite selecionar apenas as despesas com valor superior a soma dos valores de suas fontes pagadoras.
        if data:
	    if data.has_key('termo'):
	      termo = data['termo']
	      try:
		t = Termo.objects.get(id=termo)
		self.fields['protocolo'].queryset = Protocolo.objects.filter(termo=t).order_by('descricao2__entidade__nome', 'descricao2__descricao')
		self.fields['origem_fapesp'].queryset = OrigemFapesp.objects.filter(item_outorga__natureza_gasto__termo=t)
	      except:
		pass
	elif instance:
	    termo = instance.protocolo.termo
	    try:
		t = termo #Termo.objects.get(id=termo)
		self.fields['protocolo'].queryset = Protocolo.objects.filter(id=instance.protocolo.id)
		self.fields['origem_fapesp'].queryset = OrigemFapesp.objects.filter(id=instance.origem_fapesp.id)
		self.fields['termo'].value = t
	    except:
		pass
	    
	else:
	    self.fields['protocolo'].queryset = Protocolo.objects.filter(id__lte=0)
	    self.fields['origem_fapesp'].queryset = OrigemFapesp.objects.filter(id__lte=0)
	    #self.fields['conta_corrente'].queryset = ExtratoCC.objects.filter(id__lte=0)

    class Meta:
        model = Pagamento
        
    class Media:
        js = ('/media/js/jquery.js', '/media/js/selects.js',)

    cod_oper = forms.CharField(label=_(u'Código da operação'), required=False,
    	      widget=forms.TextInput(attrs={'onchange':'ajax_filter_cc_cod(this.value);'}))

    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo'), required=False,
	      widget=forms.Select(attrs={'onchange': 'ajax_filter_origem_protocolo(this.id, this.value);'}))
	      
    numero = forms.CharField(label=_(u'Número do protocolo'), required=False,
	      widget=forms.TextInput(attrs={'onchange': 'ajax_filter_protocolo_numero(this.value);'}))
	     

    def clean(self):
        valor = self.cleaned_data.get('valor_fapesp')
        origem = self.cleaned_data.get('origem_fapesp')

	if valor and not origem:
	    raise forms.ValidationError(u'Valor da FAPESP obriga a ter uma origem da FAPESP')

    	return self.cleaned_data


class ExtratoCCAdminForm(forms.ModelForm):

    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo'), required=False,
                  widget=forms.Select(attrs={'onchange': 'ajax_filter_financeiro(this.value);'}))

    class Meta:
    	model = ExtratoCC
