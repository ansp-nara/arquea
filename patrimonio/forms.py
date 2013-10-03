# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from django.core.urlresolvers import reverse
from django.utils.html import mark_safe
from django.contrib.admin.widgets import FilteredSelectMultiple, RelatedFieldWidgetWrapper
from django.db.models.fields.related import ManyToOneRel

from models import *
from financeiro.models import Pagamento
from identificacao.models import Identificacao, Entidade, Endereco, EnderecoDetalhe
from outorga.models import Termo
from patrimonio.models import Equipamento, Patrimonio



class EquipamentoModelChoiceField(forms.ModelChoiceField):
    """
    Classe para exibição de Equipamentos.
    Restringe a exibição da descrição em 150 caracteres com a adição de reticências para não exceder a largura da tela
    """
    def label_from_instance(self, obj):
        info = (obj.descricao[:150] + '..') if len(obj.descricao) > 150 else obj.descricao
        return u'%s - %s' % (info, obj.part_number)

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

        if instance and instance.pagamento: 
            if initial:
                initial.update({'termo':instance.pagamento.protocolo.termo})
                initial.update({'equipamento':instance.equipamento})
            else:
                initial = {'termo':instance.pagamento.protocolo.termo}
                initial.update({'equipamento':instance.equipamento})
                                                     
        super(PatrimonioAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

    	pt = self.fields['patrimonio']
        pg = self.fields['pagamento']
        
        if data and data['termo']:
    	    t = data['termo']
    	    t = Termo.objects.get(id=t)
    	    pg.queryset = Pagamento.objects.filter(protocolo__termo=t)
        elif instance and instance.pagamento:
            pg.choices = [(p.id, p.__unicode__()) for p in Pagamento.objects.filter(id=instance.pagamento.id)]
        else:
            pg.queryset = Pagamento.objects.filter(id__lte=0)
    
            if instance and instance.patrimonio:
                pt.choices = [(p.id, p.__unicode__()) for p in Patrimonio.objects.filter(id=instance.patrimonio.id)]
            elif data:
                pt.queryset = Patrimonio.objects.all()
            else:
                pt.queryset = Patrimonio.objects.filter(id__lte=0)
                
        # Configurando a relação entre Patrimonio e Equipamento para aparecer o botão de +                
        rel = ManyToOneRel(Equipamento, 'id')
        self.fields['equipamento'].widget = RelatedFieldWidgetWrapper(self.fields['equipamento'].widget, rel, self.admin_site)
        
    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo de outorga'), required=False)

    npgto = forms.CharField(label=_(u'Número do cheque ou do documento'), required=False,
            widget=forms.TextInput(attrs={'onchange': 'ajax_filter_pagamentos("/patrimonio/escolhe_pagamento", this.value);'}))

    part_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'onchange':'ajax_patrimonio_existente(this.value);'}))

    nf = forms.CharField(label=_(u'Número da NF ou NS'), required=False,
            widget=forms.TextInput(attrs={'onchange': 'ajax_filter_patrimonio(this.value);'}))

    tem_numero_fmusp = forms.BooleanField(label=u'Tem número de patrimônio FMUSP?', required=False, 
            widget=forms.CheckboxInput(attrs={'onchange':'ajax_numero_fmusp();'}))

    descricao = forms.CharField(required=False, widget=forms.Textarea(attrs={'class' : 'textDuplaLinhaClass'}))
    
    # Uso de Model específico para a adição de reticências na descrição
    # e javascript para adição de link no label para a página do Equipamento selecionado 
    equipamento = EquipamentoModelChoiceField(queryset=Equipamento.objects.all(), 
                                     required=False,
                                     label=mark_safe('<a href="#" onclick="window.open(\'/patrimonio/equipamento/\'+$(\'#id_equipamento\').val() + \'/\', \'_blank\');return true;">Equipamento</a>'),)
    
    class Meta:
        model = Patrimonio


    class Media:
        js = ('/media/js/selects.js', '/media/js/patrimonio.js')


class HistoricoLocalAdminForm(forms.ModelForm):
    
    class Meta:
        model = HistoricoLocal

    class Media:
        js = ('/media/js/selects.js',)


    entidade = forms.ModelChoiceField(Entidade.objects.all(), required=False,
                widget=forms.Select(attrs={'onchange': 'ajax_select_endereco(this.id);'}))
    
    descricao = forms.CharField(required=False, widget=forms.Textarea(attrs={'class' : 'textDuplaLinhaClass'}))    

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(HistoricoLocalAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        end = EnderecoDetalhe.objects.filter(id__lte=0)
        if instance or data:
            if instance:
                end = EnderecoDetalhe.objects.filter(id=instance.endereco.id)
            #else:
            #    if data.has_key('%s-entidade' % prefix) and data['%s-entidade' % prefix]:
            #        end = EnderecoDetalhe.objects.filter(endereco__entidade__id=data['%s-entidade' % prefix])
            #    elif data.has_key('%s-endereco' % prefix) and data['%s-endereco' % prefix]:
            #        end = EnderecoDetalhe.objects.filter(endereco__id=data['%s-endereco' % prefix])

        else:
            end = EnderecoDetalhe.objects.filter(id__lte=0)

        #self.fields['endereco'].queryset = end
        self.fields['endereco'].choices = [(e.id, e.__unicode__()) for e in end]
