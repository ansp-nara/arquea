# -*- coding: utf-8 -*-
from models import *
from django import forms
from outorga.models import Termo, OrigemFapesp
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
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



    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if instance and not data and instance.pagamento is not None:
            initial = initial or {}
            initial.update({'termo':instance.pagamento.protocolo.termo.id})

        super(RecursoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        pg = self.fields['pagamento']
        if instance:
            if instance.pagamento is not None:
                pg.queryset = Pagamento.objects.filter(protocolo__termo__id=instance.pagamento.protocolo.termo.id)
            else:
                pg.queryset = Pagamento.objects.filter(id__lte=0)
        elif data and data['termo']:
            t = data['termo']
            t = Termo.objects.get(id=t)
            pg.queryset = Pagamento.objects.filter(protocolo__termo=t)
        else:
            pg.queryset = Pagamento.objects.filter(id__lte=0)

    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo de outorga'), required=False, 
            widget=forms.Select(attrs={'onchange': 'ajax_filter_pagamentos2("/rede/escolhe_pagamento");'}))


    class Meta:
        model = Recurso

    class Media:
        js = ('/media/js/selects.js',)

