# -*- coding: utf-8 -*-

from models import Item, OrigemFapesp, Termo, Modalidade, Outorga, Natureza_gasto
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList

class OrigemFapespForm(forms.ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(OrigemFapespForm, self).__init__(data, files, auto_id, prefix, initial,
                                               error_class, label_suffix, empty_permitted, instance)

        if instance:
            self.fields['item_outorga'].queryset = Item.objects.filter(id=instance.item_outorga.id)



class ItemAdminForm(forms.ModelForm):

    """
    O método '__init__' Redefine os campoa 'item' e 'natureza_gasto'
                        Cria os campos 'termo' e 'modalidade' para filtrar os campos 'item' e 'natureza_gasto'
    O método 'clean'	Verifica se o termo e a modalidade do item anterior são os mesmos do item em edição.
    A class 'Meta'	Define o modelo a ser utilizado.
    A class 'Media'     Define os arquivos .j que serão utilizados (ajax/javascript)
    """

    # Redefine os campos 'termo', 'modalidade' e 'item_outorga'.
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(ItemAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        if instance:
            # Permite selecionar as naturezas de gasto da outorga da natureza de gasto selecionada.
            n = self.fields['natureza_gasto']
            n.queryset = Natureza_gasto.objects.filter(termo=instance.natureza_gasto.termo)

            self.fields['termo'].initial = instance.natureza_gasto.termo.id


    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo'), required=False,
            widget=forms.Select(attrs={'onchange': 'ajax_filter_termo_natureza("/outorga/seleciona_termo_natureza", "natureza_gasto", this.value, this.id);'}))


    # Define o modelo
    class Meta:
        model = Item


    # Define os arquivos .js que serão utilizados.
    class Media:
        js = ('/site-media/js/selects.js',)



class OrigemFapespAdminForm(forms.ModelForm):

    """
    O método '__init__'	Redefine o campo 'item_outorga'
			Cria os campos 'termo' e 'modalidade' para filtrar o campo 'item_outorga'
    A class 'Meta'      Define o modelo a ser utilizado.
    A class 'Media'	Define os arquivos .j que serão utilizados (ajax/javascript)
    """


    # Redefine os campos 'termo', 'modalidade' e 'item_outorga'.
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(OrigemFapespAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        if instance:
            # Permite selecionar itens de outorga de um termo e modalidade específicos.
            i = self.fields['item_outorga']
            i.queryset = Item.objects.filter(natureza_gasto__termo=instance.item_outorga.natureza_gasto.termo, 
					     natureza_gasto__modalidade=instance.item_outorga.natureza_gasto.modalidade)


            # Permite selecionar modalidades de um termo.
            m = self.fields['modalidade']
            m.queryset = Modalidade.modalidades_termo(t=instance.item_outorga.natureza_gasto.termo)

#             self.fields['termo'].initial = instance.item_outorga.natureza_gasto.termo.id
#             self.fields['modalidade'].initial = instance.item_outorga.natureza_gasto.modalidade.id


#     termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo'), required=False,
#             widget=forms.Select(attrs={'onchange': 'ajax_filter_modalidade_item_inline("/outorga/escolhe_termo", this.value, this.id);'}))

#     modalidade = forms.ModelChoiceField(Modalidade.modalidades_termo(), label=_(u'Modalidade'), required=False,
#             widget=forms.Select(attrs={'onchange': 'ajax_filter_inline("/outorga/escolhe_modalidade", this.value, this.id);'}))

    item_outorga = forms.ModelChoiceField(Item.objects.all(), label=_(u'Item'), required=True)


    # Define o modelo
    class Meta:
        model = OrigemFapesp


    # Define os arquivos .js que serão utilizados.
    class Media:
        js = ('/site-media/js/selects.js', )



class ContratoAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(ContratoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['numero'].error_messages['required'] = u'O campo NUMERO é obrigatório'
        self.fields['data_inicio'].error_messages['required'] = u'O campo INÍCIO é obrigatório'
        self.fields['entidade'].error_messages['required'] = u'O campo ENTIDADE é obrigatório'
        self.fields['arquivo'].error_messages['required'] = u'O campo ARQUIVO é obrigatório'
        


class OutorgaAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(OutorgaAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['categoria'].error_messages['required'] = u'O campo CATEGORIA é obrigatório'
        self.fields['termo'].error_messages['required'] = u'O campo TERMO é obrigatório'
        self.fields['termino'].error_messages['required'] = u'O campo TÉRMINO é obrigatório'
        self.fields['data_solicitacao'].error_messages['required'] = u'O campo SOLICITAÇÃO é obrigatório'


class ModalidadeAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(ModalidadeAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

    def clean(self):
        cleaned_data = super(ModalidadeAdminForm, self).clean()
        
        if any(self.errors):
            return self.cleaned_data

        sigla = self.cleaned_data.get('sigla')
        if not sigla:
            self._errors["sigla"] = self.error_class([ u'Sigla não pode ser vazia'])
            del cleaned_data["sigla"]

        return self.cleaned_data


class TermoAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(TermoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['estado'].error_messages['required'] = u'O campo ESTADO é obrigatório'


#     estado = models.ForeignKey('outorga.Estado', verbose_name=_(u'Estado'))