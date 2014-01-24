# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from django.utils.html import mark_safe

from models import *
from outorga.models import Termo, OrigemFapesp
from protocolo.models import Protocolo
from financeiro.models import Pagamento

class PlanejaAquisicaoRecursoAdminForm(forms.ModelForm):

    referente = forms.CharField(widget=forms.TextInput(attrs={'size':'150'}), required=False)
    class Meta:
	model = PlanejaAquisicaoRecurso


class RecursoAdminForm(forms.ModelForm):
    """
    Uma instância dessa classe faz algumas definições para a tela de cadastramento do modelo 'Patrimonio'.

    O campo 'termo'             Foi criado para filtrar o campo 'protocolo'
    A class 'Meta'              Define o modelo que será utilizado.
    A class 'Media'             Define os arquivos .js que serão utilizados.
    """
#    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo de outorga'), required=False, 
#            widget=forms.Select(attrs={'onchange': 'ajax_filter_pagamentos2("/rede/escolhe_pagamento");'}))

    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo de outorga'), required=False)

    pagamento = forms.ModelChoiceField(Pagamento.objects.all().select_related('protocolo', 'origem_fapesp', 'protocolo', 'origem_fapesp__item_outorga__natureza_gasto__modalidade'),
                                                 label=mark_safe('<a href="#" onclick="window.open(\'/financeiro/pagamento/\'+$(\'#id_pagamento\').val() + \'/\', \'_blank\');return true;">Pagamento</a>'),)

    planejamento = forms.ModelChoiceField(PlanejaAquisicaoRecurso.objects.all().select_related('os', 'os__tipo', 'projeto', 'tipo', ),
                                                 label=mark_safe('<a href="#" onclick="window.open(\'/admin/rede/planejaaquisicaorecurso/\'+$(\'#id_planejamento\').val() + \'/\', \'_blank\');return true;">Planejamento</a>'),)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if instance: 
            if initial:
                initial.update({'termo':instance.pagamento.protocolo.termo.id})
            else:
                initial = {'termo':instance.pagamento.protocolo.termo.id}

        super(RecursoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        pg = self.fields['pagamento']
        if instance:
            if instance.pagamento is not None:
                pg.queryset = Pagamento.objects.filter(protocolo__termo__id=instance.pagamento.protocolo.termo.id).select_related('protocolo', 'origem_fapesp', 'protocolo', 'origem_fapesp__item_outorga__natureza_gasto__modalidade')
            else:
                pg.queryset = Pagamento.objects.filter(id__lte=0).select_related('protocolo', 'origem_fapesp', 'protocolo', 'origem_fapesp__item_outorga__natureza_gasto__modalidade')
        elif data and data['termo']:
            t = data['termo']
            pg.queryset = Pagamento.objects.filter(protocolo__termo=t).select_related('protocolo', 'origem_fapesp', 'protocolo', 'origem_fapesp__item_outorga__natureza_gasto__modalidade')
        else:
            pg.queryset = Pagamento.objects.filter(id__lte=0).select_related('protocolo', 'origem_fapesp', 'protocolo', 'origem_fapesp__item_outorga__natureza_gasto__modalidade')


    class Meta:
        model = Recurso

    class Media:
        js = ('/media/js/selects.js',)

