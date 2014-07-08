# -*- coding: utf-8 -*-
import django
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple, RelatedFieldWidgetWrapper
from django.db.models.fields.related import ManyToOneRel
from django.forms.util import ErrorList
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from models import *
from outorga.models import Termo, OrigemFapesp
from protocolo.models import Protocolo
from memorando.models import Pergunta
from rede.models import PlanejaAquisicaoRecurso, Recurso
from financeiro.models import ExtratoPatrocinio, Estado, TipoComprovante


class RecursoInlineAdminForm(forms.ModelForm):
    # Foi codificado no label um Checkbox para exibir somente os recursos vigentes
    # Ele chama um AJAX para repopular o SELECT 
    # O estado inicial é exibir somente os vigentes
    planejamento = forms.ModelChoiceField(PlanejaAquisicaoRecurso.objects.filter(os__estado__nome='Vigente').select_related('os', 'os__tipo', 'projeto', 'tipo', ),
                                                 label=mark_safe('<a href="#"  onclick="window.open(\'/admin/rede/planejaaquisicaorecurso/\'+$(\'#\'+$(this).parent().attr(\'for\')).val() + \'/\', \'_blank\');return true;">Planejamento:</a>'\
                                                                 + '<script type="text/javascript">function get_recursos(obj) {var check = obj.is(":checked")?"Vigente":""; ajax_get_recursos("#"+obj.parent().attr("for"), check); }</script>'
                                                                 + ' <input type="checkbox" checked onclick="get_recursos($(this));"> Exibir somente os vigentes.'),)
    
    obs = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'3', 'style':'width:400px'}))

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

        if self.fields.has_key('pergunta'):
            self.fields['pergunta'].queryset = Pergunta.objects.all().select_related('memorando')
            
        if self.fields.has_key('patrocinio'):
            self.fields['patrocinio'].queryset = ExtratoPatrocinio.objects.all().select_related('localiza')
        
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
                self.fields['origem_fapesp'].queryset = OrigemFapesp.objects.filter(item_outorga__natureza_gasto__termo=t).select_related('acordo', 'item_outorga', 'item_outorga__natureza_gasto', 'item_outorga__natureza_gasto__termo').order_by('acordo__descricao', 'item_outorga__descricao')
            except:
                pass
        else:
            self.fields['protocolo'].queryset = Protocolo.objects.filter(id__lte=0).select_related('tipo_documento')
            self.fields['origem_fapesp'].queryset = OrigemFapesp.objects.filter(id__lte=0).select_related('acordo', 'item_outorga')
            
        # mensagens de erro
        self.fields['protocolo'].error_messages['required'] = u'O campo PROTOCOLO é obrigatório'
        self.fields['valor_fapesp'].error_messages['required'] = u'O campo VALOR ORIGINÁRIO DA FAPESP é obrigatório'
        self.fields['valor_patrocinio'].error_messages['required'] = u'O campo VALOR ORIGINÁRIO DE PATROCÍNI é obrigatório'


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

    # tornando clicável o label do campo conta_corrente
    conta_corrente = forms.ModelChoiceField(queryset=ExtratoCC.objects.all(), 
                                       required=False, 
                                       label=mark_safe('<a href="#" onclick="window.open(\'/admin/financeiro/extratocc/\'+$(\'#id_conta_corrente\').val() + \'/\', \'_blank\');return true;">Conta corrente</a>'),)
    # tornando clicável o label do campo protocolo
    protocolo = forms.ModelChoiceField(queryset=Protocolo.objects.all(), 
                                       label=mark_safe('<a href="#" onclick="window.open(\'/admin/protocolo/protocolo/\'+$(\'#id_protocolo\').val() + \'/\', \'_blank\');return true;">Protocolo</a>'),)

    def clean(self):
        cleaned_data = super(PagamentoAdminForm, self).clean()
        
        if any(self.errors):
            return self.cleaned_data

        valor = self.cleaned_data.get('valor_fapesp')
        origem = self.cleaned_data.get('origem_fapesp')

        if valor and not origem:
            #raise forms.ValidationError()
            self._errors["origem_fapesp"] = self.error_class([ u'Valor da FAPESP obriga a ter uma origem da FAPESP'])
            del cleaned_data["origem_fapesp"]

        return self.cleaned_data


class ExtratoFinanceiroAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
    
        super(ExtratoFinanceiroAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['termo'].error_messages['required'] = u'O campo TERMO DE OUTORGA é obrigatório'
        self.fields['data_libera'].error_messages['required'] = u'O campo DATA é obrigatório'
        self.fields['cod'].error_messages['required'] = u'O campo CODIGO é obrigatório'
        self.fields['valor'].error_messages['required'] = u'O campo VALOR é obrigatório'


    class Meta:
        model = ExtratoFinanceiro


class ExtratoPatrocinioAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
    
        super(ExtratoPatrocinioAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['localiza'].error_messages['required'] = u'O campo LOCALIZAÇÃO DO PATROCÍONIO é obrigatório'
        self.fields['data_oper'].error_messages['required'] = u'O campo DATA DA OPERAÇÃO é obrigatório'
        self.fields['cod_oper'].error_messages['required'] = u'O campo CÓDIGO DA OPERAÇÃO é obrigatório'
        self.fields['valor'].error_messages['required'] = u'O campo VALOR é obrigatório'
        self.fields['historico'].error_messages['required'] = u'O campo HISTÓRICO é obrigatório'
        self.fields['obs'].error_messages['required'] = u'O campo OBS é obrigatório'


    class Meta:
        model = ExtratoPatrocinio

class ExtratoCCAdminForm(forms.ModelForm):

    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo'), required=False,
                  widget=forms.Select(attrs={'onchange': 'ajax_filter_financeiro(this.value);'}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
    
        super(ExtratoCCAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['data_oper'].error_messages['required'] = u'O campo DATA DA OPERAÇÃO é obrigatório'
        self.fields['cod_oper'].error_messages['required'] = u'O campo DOCUMENTO é obrigatório'
        self.fields['historico'].error_messages['required'] = u'O campo HISTORICO é obrigatório'
        self.fields['valor'].error_messages['required'] = u'O campo VALOR é obrigatório'


    class Meta:
    	model = ExtratoCC

    def clean_imagem(self):
        """
        Verificando a extensão do arquivo de imagem. Pode conter somente JPEG.
        """
        imagem = self.cleaned_data.get('imagem', False)
        if imagem and imagem.name:
            imagem_split = imagem.name.split('.')
            
            extensao = ''
            if len(imagem_split) > 1:
                extensao = imagem_split[-1]
            
            if not (extensao.lower() in ['jpeg', 'jpg']):
                raise forms.ValidationError(_(u'Somente utilizar imagens JPEG.'))

        return imagem


class AuditoriaPagamentoChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.unicode_para_auditoria()
    
class AuditoriaAdminForm(forms.ModelForm):

    parcial = forms.IntegerField(label=u'Parcial', widget=forms.TextInput(attrs={'onchange': 'ajax_nova_pagina(this);'}))
    pagamento = AuditoriaPagamentoChoiceField(queryset=Pagamento.objects.all().select_related('protocolo', 'origem_fapesp__item_outorga__natureza_gasto', 'origem_fapesp__item_outorga__natureza_gasto__modalidade'),
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
        
        # mensagens de erro
        self.fields['pagamento'].error_messages['required'] = u'O campo PAGAMENTO é obrigatório'
        self.fields['estado'].error_messages['required'] = u'O campo ESTADO é obrigatório'
        self.fields['tipo'].error_messages['required'] = u'O campo TIPO é obrigatório'
        self.fields['parcial'].error_messages['required'] = u'O campo PARCIAL é obrigatório'
        self.fields['pagina'].error_messages['required'] = u'O campo PAGINA é obrigatório'

    class Meta:
        model = Auditoria


class PagamentoAuditoriaAdminInlineForm(forms.ModelForm):
    """
    Form de Auditoria utilizado como inline dentro do form do Pagamento
    """
    estado = forms.ModelChoiceField(Estado.objects.all(), 
                                    label=u'Estado', 
                                    widget=forms.Select(attrs={'onchange': 'ajax_prox_audit($("#id_origem_fapesp").val());'}))
    
    tipo = forms.ModelChoiceField(TipoComprovante.objects.all(), 
                                    label=u'Tipo', 
                                    widget=forms.Select(attrs={'onchange': 'ajax_prox_audit($("#id_origem_fapesp").val());'}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None, widget=None, label=None, help_text=None):
        
        super(PagamentoAuditoriaAdminInlineForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

            
    class Meta:
        model = Auditoria


