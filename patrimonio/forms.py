# -*- coding: utf-8 -*-

from models import *
from financeiro.models import Pagamento
from identificacao.models import Identificacao, Entidade, Endereco, EnderecoDetalhe
from outorga.models import Termo
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList


class PatrimonioAdminForm(forms.ModelForm):

    """
    Uma instância dessa classe faz algumas definições para a tela de cadastramento do modelo 'Patrimonio'.

    O método '__init__'		Define as opções do campo 'protocolo' (apenas protocolos diferentes de 'Contrato', 'OS' e 'Cotação'.
    O campo 'termo'		Foi criado para filtrar o campo 'protocolo'
    O campo 'protocolo'		Foi criado para filtrar o campo 'itemprotocolo'
    A class 'Meta'		Define o modelo que será utilizado.
    A class 'Media'		Define os arquivos .js que serão utilizados.
    """



    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(PatrimonioAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        pg = self.fields['pagamento']
        if instance:
	    pg.queryset = Pagamento.objects.filter(protocolo__termo=instance.pagamento.protocolo.termo)
	elif data and data['termo']:
	    t = data['termo']
	    t = Termo.objects.get(id=t)
	    pg.queryset = Pagamento.objects.filter(protocolo__termo=t)
	else:
            pg.queryset = Pagamento.objects.filter(id__lte=0)
        
    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo de outorga'), required=False)

    npgto = forms.CharField(label=_(u'Número do cheque ou da nota'), required=False,
            widget=forms.TextInput(attrs={'onchange': 'ajax_filter_pagamentos("/patrimonio/escolhe_pagamento", this.value);'}))

    part_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'onchange':'ajax_patrimonio_existente(this.value);'}))

    class Meta:
        model = Patrimonio


    class Media:
        js = ('/media/js/jquery.js', '/media/js/selects.js')




class HistoricoLocalAdminForm(forms.ModelForm):
    
    class Meta:
        model = HistoricoLocal

    class Media:
        js = ('/media/js/selects.js', '/media/js/jquery.js')


    entidade = forms.ModelChoiceField(Entidade.objects.all(), required=False,
                widget=forms.Select(attrs={'onchange': 'ajax_select_endereco(this.id);'}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(HistoricoLocalAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        end = EnderecoDetalhe.objects.filter(id__lte=0)
        if instance or data:
            if instance:
                end = EnderecoDetalhe.objects.filter(id=instance.endereco.id)
            else:
                if data.has_key('%s-entidade' % prefix) and data['%s-entidade' % prefix]:
                    end = EnderecoDetalhe.objects.filter(endereco__entidade__id=data['%s-entidade' % prefix])
                elif data.has_key('%s-endereco' % prefix) and data['%s-endereco' % prefix]:
                    end = EnderecoDetalhe.objects.filter(endereco__id=data['%s-endereco' % prefix])

        else:
            end = EnderecoDetalhe.objects.filter(id__lte=0)

        self.fields['endereco'].queryset = end

