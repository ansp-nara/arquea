# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from models import Item, OrigemFapesp, Termo, Modalidade, Outorga, Natureza_gasto, Acordo
from utils.request_cache import get_request_cache

class OrigemFapespInlineForm(forms.ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(OrigemFapespInlineForm, self).__init__(data, files, auto_id, prefix, initial,
                                               error_class, label_suffix, empty_permitted, instance)

    
        cache = get_request_cache()
        if cache.get('outorga.Acordo.all') is None:
            cache.set('outorga.Acordo.all', [('','---------')] + [(p.id, p.__unicode__()) for p in Acordo.objects.all().order_by('descricao') ])
        self.fields['acordo'].choices =  cache.get('outorga.Acordo.all')

        cache = get_request_cache()
        if cache.get('outorga.Item.all') is None:
            cache.set('outorga.Item.all', [('','---------')] + [(p.id, p.__unicode__()) for p in Item.objects.all().select_related('natureza_gasto', 'natureza_gasto__termo') ])
        self.fields['item_outorga'].choices =  cache.get('outorga.Item.all')
        

    class Meta:
        model = OrigemFapesp
        fields = ('acordo', 'item_outorga')


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
        fields = ['natureza_gasto', 'descricao', 'entidade', 'quantidade', 'valor', 'justificativa', 'obs',]


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

#
        self.fields['acordo'].choices = [('','---------')] + [(p.id, p.__unicode__()) for p in Acordo.objects.all().order_by('descricao') ]
        self.fields['item_outorga'].choices = [('','---------')] + [(p.id, p.__unicode__()) for p in Item.objects.all().select_related('natureza_gasto', 'natureza_gasto__termo') ]


    # Define o modelo
    class Meta:
        model = OrigemFapesp
        fields = ['acordo', 'item_outorga',]

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

    def clean(self):
        cleaned_data = super(TermoAdminForm, self).clean()
        
        if any(self.errors):
            return self.cleaned_data

        ano = self.cleaned_data.get('ano')
        if ano == None:
            self._errors["ano"] = self.error_class([ u'O campo ANO não pode ser vazio.'])
            del cleaned_data["ano"]
        elif ano != None and ano < 1900:
            self._errors["ano"] = self.error_class([ u'O campo ANO deve possuir 4 dígitos.'])
            del cleaned_data["ano"]

        return self.cleaned_data




