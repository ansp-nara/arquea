# -*- coding: utf-8 -*-
import django
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.contrib.admin.widgets import FilteredSelectMultiple, RelatedFieldWidgetWrapper
from django.db.models.fields.related import ManyToOneRel
from django.utils.html import mark_safe

from models import *
from outorga.models import Termo, OrigemFapesp
from protocolo.models import Protocolo

from rede.models import PlanejaAquisicaoRecurso, Recurso


class RecursoInlineAdminForm(forms.ModelForm):

    planejamento = forms.ModelChoiceField(PlanejaAquisicaoRecurso.objects.all().select_related('os', 'os__tipo', 'projeto', 'tipo', ),
                                                 label=mark_safe('<a href="#" onclick="window.open(\'/admin/rede/planejaaquisicaorecurso/\'+$(\'#id_planejamento\').val() + \'/\', \'_blank\');return true;">Planejamento</a>'),)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
                                                     
        super(RecursoInlineAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)
        # Configurando a relação entre Patrimonio e Equipamento para aparecer o botão de +
        # O self.admin_site foi declarado no admin.py
        if django.VERSION[0:2] >= (1, 6):
            rel = ManyToOneRel(field=Recurso._meta.get_field('planejamento'), to=PlanejaAquisicaoRecurso, field_name='id')
        else:
            rel = ManyToOneRel(PlanejaAquisicaoRecurso, 'id')
            
        self.fields['planejamento'].widget = RelatedFieldWidgetWrapper(self.fields['planejamento'].widget, rel, self.admin_site)


class PagamentoAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
	
        if instance and not data:
            initial = {'termo': instance.protocolo.termo.id}
	   
        super(PagamentoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)


        # Permite selecionar apenas as despesas com valor superior a soma dos valores de suas fontes pagadoras.
        if data:
	    if data.has_key('termo'):
	      termo = data['termo']
	      try:
		t = Termo.objects.get(id=termo)
		self.fields['protocolo'].queryset = Protocolo.objects.filter(termo=t).select_related('tipo_documento').order_by('tipo_documento', 'num_documento', 'data_vencimento')
		self.fields['origem_fapesp'].queryset = OrigemFapesp.objects.filter(item_outorga__natureza_gasto__termo=t).select_related('acordo', 'item_outorga').order_by('acordo__descricao', 'item_outorga__descricao')
	      except:
		pass
	elif instance:
	    termo = instance.protocolo.termo
	    try:
		t = termo #Termo.objects.get(id=termo)
		self.fields['protocolo'].queryset = Protocolo.objects.filter(termo=t).select_related('tipo_documento').order_by('tipo_documento', 'num_documento', 'data_vencimento')
		self.fields['origem_fapesp'].queryset = OrigemFapesp.objects.filter(item_outorga__natureza_gasto__termo=t).select_related('acordo', 'item_outorga').order_by('acordo__descricao', 'item_outorga__descricao')
	    except:
		pass
	    
	else:
	    self.fields['protocolo'].queryset = Protocolo.objects.filter(id__lte=0).select_related('tipo_documento')
	    self.fields['origem_fapesp'].queryset = OrigemFapesp.objects.filter(id__lte=0).select_related('acordo', 'item_outorga')
	    #self.fields['conta_corrente'].queryset = ExtratoCC.objects.filter(id__lte=0)

    class Meta:
        model = Pagamento
        
    class Media:
        js = ('/media/js/selects.js',)

    cod_oper = forms.CharField(label=_(u'Código da operação'), required=False,
    	      widget=forms.TextInput(attrs={'onchange':'ajax_filter_cc_cod(this.value);'}))

    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo'), required=False,
	      widget=forms.Select(attrs={'onchange': 'ajax_filter_origem_protocolo(this.id, this.value);'}))
	      
    numero = forms.CharField(label=_(u'Número do protocolo'), required=False,
	      widget=forms.TextInput(attrs={'onchange': 'ajax_filter_protocolo_numero(this.value);'}))
	     
    origem_fapesp = forms.ModelChoiceField(OrigemFapesp.objects.all(), label=_(u'Origem Fapesp'),
              required=False, widget=forms.Select(attrs={'onchange':'ajax_prox_audit(this.value);'}))

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



class AuditoriaPagamentoChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.unicode_para_auditoria()
    
class AuditoriaAdminForm(forms.ModelForm):

    parcial = forms.IntegerField(label=u'Parcial', widget=forms.TextInput(attrs={'onchange': 'ajax_nova_pagina(this);'}))

    pagamento = AuditoriaPagamentoChoiceField(queryset=Pagamento.objects.all().select_related('protocolo', 'origem_fapesp__item_outorga__natureza_gasto__modalidade'),
                                                 required=False, 
                                                 label=mark_safe('<a href="#" onclick="window.open(\'/financeiro/pagamento/\'+$(\'#id_pagamento\').val() + \'/\', \'_blank\');return true;">Pagamento</a>'),)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None, widget=None, label=None, help_text=None):
        
        super(AuditoriaAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        # Configurando a relação entre Equipamento e Entidade para aparecer o botão de +
        # O self.admin_site foi declarado no admin.py
        if django.VERSION[0:2] >= (1, 6):
            rel = ManyToOneRel(field=Auditoria._meta.get_field('pagamento'), to=Pagamento, field_name='id')
        else:
            rel = ManyToOneRel(Pagamento, 'id')
        
        self.fields['pagamento'].widget = RelatedFieldWidgetWrapper(self.fields['pagamento'].widget, rel, self.admin_site)


            
    class Meta:
        model = Auditoria


