# -*- coding: utf-8 -*-

from django import forms
from django.utils.html import mark_safe
from models import *
import re


EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'  # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain


# Faz a validação de um e-mmail
def is_valid_email(value):
    return EMAIL_RE.search(value)


class ContatoAdminForm(forms.ModelForm):

    """
    A função 'clean_email' identifica cada e-mail do campo 'email' e verifica se eles são validos.
    """

    # Define o modelo
    class Meta:
        model = Contato
        fields = ['primeiro_nome', 'ultimo_nome', 'ativo', 'email', 'tel', 'documento']

    # Verifica se os e-mail são válidos.
    def clean_email(self):
        
        value = self.cleaned_data['email']
        
        if not value:
            return value
        emails = [e.strip() for e in value.split(',')]
        for email in emails:
            if not is_valid_email(email):
                raise forms.ValidationError(u'%s não é um e-mail válido.' % email)

        # Always return the cleaned data.
        return value


class EnderecoAdminForm(forms.ModelForm):

    entidade = forms.ModelChoiceField(Entidade.objects.all(), required=False,
                                      widget=forms.Select(attrs={'onchange': 'ajax_select_endereco2();'}))

    class Meta:
        model = Endereco
        fields = ['entidade', 'rua', 'num', 'compl', 'cep', 'bairro', 'cidade', 'estado', 'pais']

    class Media:
        js = ('/site-media/js/selects.js', '/site-media/js/identificacao.js')


class EnderecoDetalheAdminForm(forms.ModelForm):

    # Campo de filtro por Entidade para reduzir a seleção do campo Endereço
    entidade = forms.ModelChoiceField(Entidade.objects.all(), required=False,
                                      widget=forms.Select(attrs={'onchange': 'ajax_select_endereco2();',
                                                                 'class': 'auxiliary'}))

    def __init__(self, *args, **kwargs):
        super(EnderecoDetalheAdminForm, self).__init__(*args, **kwargs)
        
        # Adicionando link para o label do campo de Tipo de Conector
        self.fields['endereco'].label = mark_safe('<a href="#" onclick="window.open(\'/admin/identificacao/endereco/\''
                                                  '+$(\'#id_endereco\').val() + \'/\', \'_blank\');return true;">%s</a>'
                                                  % self.fields['endereco'].label)
        self.fields['detalhe'].label = mark_safe('<a href="#" onclick="window.open(\'/admin/identificacao/endereco'
                                                 'detalhe/\'+$(\'#id_detalhe\').val() + \'/\', \'_blank\');return true;'
                                                 '">%s</a>' % self.fields['detalhe'].label)

    def clean(self):
        cleaned_data = self.cleaned_data
        endereco = cleaned_data.get('endereco')
        detalhe = cleaned_data.get('detalhe')

        if endereco is None and detalhe is None:
            raise forms.ValidationError(u'Endereço e detalhe do endereço não podem ser ambos nulos')
        elif endereco and detalhe:
            raise forms.ValidationError(u'Endereço e detalhe do endereço não podem ser ambos utilizados')

        return cleaned_data

    class Meta:
        model = EnderecoDetalhe
        fields = ['entidade', 'endereco', 'detalhe', 'tipo', 'complemento',]

    class Media:
        js = ('js/selects.js',)
