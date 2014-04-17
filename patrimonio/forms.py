# -*- coding: utf-8 -*-
import django
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from django.core.urlresolvers import reverse
from django.utils.html import mark_safe
from django.contrib.admin.widgets import FilteredSelectMultiple, RelatedFieldWidgetWrapper
from django.db.models.fields.related import ManyToOneRel
from django.forms.formsets import BaseFormSet
from django.forms.models import BaseInlineFormSet, inlineformset_factory


from models import *
from financeiro.models import Pagamento
from identificacao.models import Identificacao, Entidade, Endereco, EnderecoDetalhe, EntidadeHistorico
from outorga.models import Termo
from patrimonio.models import Equipamento, Patrimonio


from django.forms import widgets
from django.forms.util import flatatt

# Exibição de patrimonios filhos em forma de tabela, dentro do form de Patrimonio
class PatrimonioReadOnlyWidget(forms.Widget):
    def render(self, name, value, attrs):
        retorno = ''
        if value and len(value) > 0:
            retorno += u'<table>'
            retorno += "<tr><th>Nome</th><th>NS</th><th>Desc</th></tr>"
            if value:
                for v in value:        
                    id = v[0] or ''
                    retorno += "<tr>"
                    retorno += "<td style='white-space:nowrap;'><a href='/patrimonio/patrimonio/%s/'>%s</td>" % (id, v[1] or '')
                    retorno += "<td style='white-space:nowrap;'><a href='/patrimonio/patrimonio/%s/'>%s</td>" % (id, v[2] or '')
                    retorno += "<td><a href='/patrimonio/patrimonio/%s/'>%s</td>" % (id, v[3] or '')
                    retorno += "</tr>"
            retorno += "</table>" 
        return mark_safe(retorno)

    def _has_changed(self, initial, data):
        return False
    
class PatrimonioReadOnlyField(forms.FileField):
    widget = PatrimonioReadOnlyWidget
    def __init__(self, widget=None, label=None, initial=None, help_text=None):
        forms.Field.__init__(self, label=label, initial=initial,
            help_text=help_text, widget=widget)

    def clean(self, value, initial):
        self.widget.initial = initial
        return initial

        
class EquipamentoContidoModelChoiceField(forms.ModelChoiceField):
    """
    Classe para exibição de Equipamentos - contidos em.
    Restringe a exibição da descrição em 200 caracteres com a adição de reticências para não exceder a largura da tela
    """
    def label_from_instance(self, obj):
        info = (obj.__unicode__()[:200] + '..') if len(obj.__unicode__()) > 200 else obj.__unicode__()
        return u'%s' % (info)


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

    O método '__init__'        Define as opções do campo 'protocolo' (apenas protocolos diferentes de 'Contrato', 'OS' e 'Cotação'.
    O campo 'termo'        Foi criado para filtrar o campo 'protocolo'
    O campo 'protocolo'        Foi criado para filtrar o campo 'itemprotocolo'
    A class 'Meta'        Define o modelo que será utilizado.
    A class 'Media'        Define os arquivos .js que serão utilizados.
    """
        
    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo de outorga'), required=False)

    npgto = forms.CharField(label=_(u'Número do cheque ou do documento'), required=False,
            widget=forms.TextInput(attrs={'onchange': 'ajax_filter_pagamentos("/patrimonio/escolhe_pagamento", this.value);'}))

    part_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'onchange':'ajax_patrimonio_existente(this.value);'}))

    nf = forms.CharField(label=_(u'Número da NF ou NS'), required=False,
            widget=forms.TextInput(attrs={'onchange': 'ajax_filter_patrimonio(this.value);'}))

    tem_numero_fmusp = forms.BooleanField(label=u'Tem número de patrimônio FMUSP?', required=False, 
            widget=forms.CheckboxInput(attrs={'onchange':'ajax_numero_fmusp();'}))

    descricao = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'2', 'cols':'152'}))
    
    filtro_equipamento = forms.CharField(label=_(u'Filtro para busca de Equipamento'), required=False,\
        widget = forms.TextInput(attrs={'onchange': 'ajax_filter_equipamento(this.value);'}))
    
    # Uso de Model específico para a adição de reticências na descrição
    # e javascript para adição de link no label para a página do Equipamento selecionado 
    equipamento = EquipamentoModelChoiceField(queryset=Equipamento.objects.all(), 
                                     required=False,
                                     label=mark_safe('<a href="#" onclick="window.open(\'/patrimonio/equipamento/\'+$(\'#id_equipamento\').val() + \'/\', \'_blank\');return true;">Equipamento</a>'),
                                     widget=forms.Select(attrs={'style':'width:800px'}),
                                     )
    
    patrimonio = EquipamentoContidoModelChoiceField(queryset=Patrimonio.objects.all(), 
                                     required=False,
                                     label=mark_safe('<a href="#" onclick="window.open(\'/patrimonio/patrimonio/\'+$(\'#id_patrimonio\').val() + \'/\', \'_blank\');return true;">Contido em</a>'),
                                     widget=forms.Select(attrs={'style':'width:800px'}),
                                     empty_label='---'
                                     )
    
    entidade_procedencia = forms.ModelChoiceField(queryset=Entidade.objects.all(),
                                                 required=False, 
                                                 label=mark_safe('<a href="#" onclick="window.open(\'/identificacao/entidade/\'+$(\'#id_entidade_procedencia\').val() + \'/\', \'_blank\');return true;">Procedência</a>'),)

    pagamento = forms.ModelChoiceField(queryset=Pagamento.objects.all(), 
                                       required=False, 
                                       label=mark_safe('<a href="#" onclick="window.open(\'/admin/financeiro/pagamento/\'+$(\'#id_pagamento\').val() + \'/\', \'_blank\');return true;">Pagamento</a>'),)


    form_filhos = PatrimonioReadOnlyField()
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if instance: 
            if initial:
                initial.update({'equipamento':instance.equipamento})
            else:
                initial = {'equipamento':instance.equipamento}
                
            initial.update({'patrimonio':instance.patrimonio})
            initial.update({'form_filhos': [(p.id, p.apelido, p.ns, p.descricao) for p in Patrimonio.objects.filter(patrimonio=instance)]})
            if instance.pagamento:
                initial.update({'termo':instance.pagamento.protocolo.termo})
                                                     
        super(PatrimonioAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)
        
        pg = self.fields['pagamento']
        if data and 'termo' in data and data['termo']:
            t = data['termo']
            t = Termo.objects.get(id=t)
            pg.queryset = Pagamento.objects.filter(protocolo__termo=t)
        elif instance and instance.pagamento:
            pg.choices = [(p.id, p.__unicode__()) for p in Pagamento.objects.filter(id=instance.pagamento.id)]
        else:
            pg.queryset = Pagamento.objects.filter(id__lte=0)

        pt = self.fields['patrimonio']
        if data and 'patrimonio' in data and data['patrimonio']:
            pt.choices = [(p.id, p.__unicode__()) for p in Patrimonio.objects.filter(id=data['patrimonio'])]
        elif instance and instance.patrimonio:
            pt.choices = [(p.id, p.__unicode__()) for p in Patrimonio.objects.filter(id=instance.patrimonio.id)]
        else:
            pt.queryset = Patrimonio.objects.filter(id__lte=0)
        
        # Configurando a relação entre Patrimonio e Equipamento para aparecer o botão de +
        # O self.admin_site foi declarado no admin.py
        if django.VERSION[0:2] >= (1, 6):
            rel = ManyToOneRel(field=Patrimonio._meta.get_field('equipamento'), to=Equipamento, field_name='id')
        else:
            rel = ManyToOneRel(Equipamento, 'id')
            
        self.fields['equipamento'].widget = RelatedFieldWidgetWrapper(self.fields['equipamento'].widget, rel, self.admin_site)
        
        # Configurando a relação entre Equipamento e Entidade para aparecer o botão de +
        # O self.admin_site foi declarado no admin.py
        if django.VERSION[0:2] >= (1, 6):
            rel = ManyToOneRel(field=Patrimonio._meta.get_field('entidade_procedencia'), to=Entidade, field_name='id')
        else:
            rel = ManyToOneRel(Entidade, 'id')
            
        self.fields['entidade_procedencia'].widget = RelatedFieldWidgetWrapper(self.fields['entidade_procedencia'].widget, rel, self.admin_site)

        """
        et = self.fields['entidade_procedencia']
        if data and data['entidade_procedencia']:
            t = data['entidade_procedencia']
            et.queryset = Entidade.objects.filter(pk=t)
        elif instance and instance.entidade_procedencia:
            et.choices = [(p.id, p.__unicode__()) for p in Entidade.objects.filter(id=instance.entidade_procedencia.id)]
        else:
            # ************ROGERIO: MODIFICAR PARA UM FILTRO POR ATRIBUTO/ FLAG
            #entidadeHistoricoList = EntidadeHistorico.objects.filter(tipo__nome= 'Fabricante').values_list('entidade_id', flat=True)
            #et.queryset = Entidade.objects.filter(id__in=entidadeHistoricoList)
            et.queryset = Entidade.objects.all()
        """
        # Exibe a quantidade de patrimonios filhos no label
        self.fields['form_filhos'].label = u'Patrimônios contidos (%s)' % Patrimonio.objects.filter(patrimonio=instance).count()
        if instance:
            if instance.equipamento:
                self.fields['filtro_equipamento'].widget = widget=forms.TextInput(attrs={'onchange': 'ajax_filter_equipamento(this.value, "%s", "%s");'%(instance.id, instance.equipamento.id)})
            else:
                self.fields['filtro_equipamento'].widget = widget=forms.TextInput(attrs={'onchange': 'ajax_filter_equipamento(this.value, "%s");'%(instance.id)})
                
    class Meta:
        model = Patrimonio

    class Media:
        js = ('/media/js/selects.js', '/media/js/patrimonio.js')

    def clean(self):
        cleaned_data = super(PatrimonioAdminForm, self).clean()
        # Retorna erro para erros de sistemas não tratados
        if any(self.errors):
            raise forms.ValidationError(u'Erro sistema %s'%self.errors)
        
        if not cleaned_data.get("equipamento"):
            # Verifica se há equipamento selecionado para o patrimonio
            raise forms.ValidationError(u'Patrimônio deve ter um equipamento associado.')

        
        return cleaned_data


class HistoricoLocalAdminForm(forms.ModelForm):
    
    class Meta:
        model = HistoricoLocal

    class Media:
        js = ('/media/js/selects.js',)


    patrimonio = forms.ModelChoiceField(Patrimonio.objects.all().select_related('pagamento', 'pagamento__protocolo', 'pagamento__protocolo__num_documento'), \
                                        widget=forms.Select(attrs={'style':'width:800px'}),)

    endereco = forms.ModelChoiceField(EnderecoDetalhe.objects.all().select_related('detalhe', 'endereco'))
    
    descricao = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'2'}))    

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if initial:
            if instance:
                if instance.endereco and instance.endereco.endereco and instance.endereco.endereco.entidade:
                    entidade.update({'entidade':instance.endereco.endereco.entidade})
                if instance.patrimonio:
                    patrimonio.update({'patrimonio':instance.patrimonio})
                if instance.endereco:
                    endereco.update({'endereco':instance.endereco})
        else:
            initial = {}
            if instance and instance.endereco and instance.endereco.endereco and instance.endereco.endereco.entidade:
                initial['entidade'] = instance.endereco.endereco.entidade
                logger.debug(initial['entidade'] )
            if instance and instance.patrimonio:
                initial['patrimonio'] = instance.patrimonio
            if instance and instance.endereco:
                initial['endereco'] = instance.endereco

        super(HistoricoLocalAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        end= None
        end = EnderecoDetalhe.objects.filter(id=instance.endereco.id)

        if not end:
            end = EnderecoDetalhe.objects.filter(id__lte=0)

        self.fields['endereco'].choices = [(e.id, e.__unicode__()) for e in end]


class PatrimonioHistoricoLocalAdminForm(forms.ModelForm):
    
    class Meta:
        model = HistoricoLocal

    class Media:
        js = ('/media/js/selects.js',)


    entidade = forms.ModelChoiceField(Entidade.objects.all(), required=False,
                widget=forms.Select(attrs={'onchange': 'ajax_select_endereco(this.id);'}))

    descricao = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'2'}))    


    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if initial:
            if instance:
                if instance.endereco and instance.endereco.endereco and instance.endereco.endereco.entidade:
                    entidade.update({'entidade':instance.endereco.endereco.entidade})
        else:
            initial = {}
            if instance and instance.endereco and instance.endereco.endereco and instance.endereco.endereco.entidade:
                initial['entidade'] = instance.endereco.endereco.entidade

        super(PatrimonioHistoricoLocalAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        end= None
        if data:
            end_id = data.get(u'%s-endereco' % prefix)
            if end_id and end_id.isdigit():
                end = EnderecoDetalhe.objects.filter(id=end_id)
        elif instance:
            end = EnderecoDetalhe.objects.filter(id=instance.endereco.id)

#         if data and not end:
#             if data.has_key('%s-entidade' % prefix) and data['%s-entidade' % prefix]:
#                 end = EnderecoDetalhe.objects.filter(endereco__entidade__id=data['%s-entidade' % prefix])
#             elif data.has_key('%s-endereco' % prefix) and data['%s-endereco' % prefix]:
#                 end = EnderecoDetalhe.objects.filter(endereco__id=data['%s-endereco' % prefix])

        if not end:
            end = EnderecoDetalhe.objects.filter(id__lte=0)

        #self.fields['endereco'].queryset = end
        self.fields['endereco'].choices = [(e.id, e.__unicode__()) for e in end]
        

class BaseHistoricoLocalAdminFormSet(BaseInlineFormSet):
    """
    Formset para checagem do Historico de Localidade de um Patrimonio.
    Faz a verificação se o Patrimonio está contido em outro Patrimonio na mesma localidade.
    """
    
    def clean(self):
        cleaned_data = super(BaseHistoricoLocalAdminFormSet, self).clean()
        # Retorna erro para erros de sistemas não tratados
        if any(self.errors):
            raise forms.ValidationError(u'Erro sistema %s'%self.errors)
        
        form_mais_recente = None
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            
            data = form.cleaned_data.get('data')
            if data:
                if (not form_mais_recente) or (form_mais_recente and data > form_mais_recente.cleaned_data.get('data')):
                    form_mais_recente = form;
                     
        if form_mais_recente:
            cleaned_data = form_mais_recente.cleaned_data
             
            if cleaned_data.get("patrimonio") and cleaned_data.get("patrimonio").patrimonio:
                contido_em = cleaned_data.get("patrimonio").patrimonio
                endereco = cleaned_data.get("endereco")
                
                logger.debug(contido_em.historico_atual.endereco)
                logger.debug(endereco)
                
                # Verifica se está no mesmo endereço do patrimonio pai
                if (contido_em.historico_atual and contido_em.historico_atual.endereco != endereco):
                    raise forms.ValidationError(u'Patrimônio deve estar na mesma localização do patrimônio em que está contido.')
                        
                historicolocal = HistoricoLocal(posicao=cleaned_data.get("posicao"))
                
                # Verifica se está no mesmo rack do patrimonio pai
                if (contido_em.historico_atual and \
                    historicolocal and \
                    contido_em.historico_atual.posicao_rack != historicolocal.posicao_rack):
                    
                   raise forms.ValidationError(u'Patrimônio deve estar no mesmo rack do patrimônio em que está contido.')

                # Verifica o furo para os patrimonios que estiverem dentro de um Rack
                if (contido_em.equipamento.tipo.nome != 'Rack' and \
                    contido_em.historico_atual.posicao_furo != historicolocal.posicao_furo):
                    
                    raise forms.ValidationError(u'Patrimônio deve estar no mesmo furo do patrimônio em que está contido.')

        
        return cleaned_data

HistoricoLocalAdminFormSet = inlineformset_factory(Patrimonio, HistoricoLocal, formset=BaseHistoricoLocalAdminFormSet, fk_name='patrimonio')




class EquipamentoAdminForm(forms.ModelForm):
    entidade_fabricante = forms.ModelChoiceField(queryset=Entidade.objects.all(),
                                                 required=False, 
                                                 label=mark_safe('<a href="#" onclick="window.open(\'/identificacao/entidade/\'+$(\'#id_entidade_fabricante\').val() + \'/\', \'_blank\');return true;">Marca</a>'),)
    
    url_equipamento = forms.CharField(widget=forms.TextInput(attrs={'size':120}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(EquipamentoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)
        
        # Configurando a relação entre Equipamento e Entidade para aparecer o botão de +
        # O self.admin_site foi declarado no admin.py                
        if django.VERSION[0:2] >= (1, 6):
            rel = ManyToOneRel(field=Equipamento._meta.get_field('entidade_fabricante'), to=Entidade, field_name='id')
        else:
            rel = ManyToOneRel(Entidade, 'id')
            
        self.fields['entidade_fabricante'].widget = RelatedFieldWidgetWrapper(self.fields['entidade_fabricante'].widget, rel, self.admin_site)
        
        
    def clean(self):
        cleaned_data = super(EquipamentoAdminForm, self).clean()
        
        return cleaned_data
