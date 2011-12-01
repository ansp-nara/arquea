# -*- coding: utf-8 -*-

from models import *
from identificacao.models import Entidade
from django.forms.util import ErrorList
from django import forms
import re
from django.forms.models import BaseInlineFormSet, inlineformset_factory

EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain


# Faz a validação de um e-mmail
def is_valid_email(value):
    return EMAIL_RE.search(value)
        

class MembroAdminForm(forms.ModelForm):

    """
    O método '__init__'		É usado para recuperar o 'id' do membro. 
    O método 'clean_email'	Identifica cada e-mail do campo 'email' e verifica se eles são validos.
    O método 'clean_cpf'	Verifica se o CPF informado pertence a um membro cadastrado.
    A class 'Meta'		Define o modelo a ser usado.
    """

    # Redefine os campos 'data_vencimento', 'protocolo', 'tipo_documento' e 'identificacao'.
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(MembroAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        try:
            self.id = instance.id
        except:
            self.id = None


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


    # Verifica a unicidade do CPF.
    def clean_cpf(self):
        index = self.id
        value = self.cleaned_data['cpf']

        if not value:
            return value

        membro = Membro.objects.filter(cpf=value)
        for mb in membro:
            if mb.id != self.id:
                raise forms.ValidationError(u'O CPF %s já está cadastrado' % value)

        # Always return the cleaned data.
        return value


    class Meta:
        model = Membro



class DadoBancarioAdminForm(forms.ModelForm):

    """
    Uma instância dessa classe faz algumas definições/limitações para a tela de cadastramento do modelo 'Tarefa'.

    O método '__init__'		Limita a seleção do campo 'membro' para selecionar apenas funcionários.
    O campo 'entidade'		Foi criado para filtrar o campo 'equipe'.
    A class 'Meta'		Define o modelo que será utilizado.
    A class 'Media'		Define os arquivo .js que serão utilizados.
    """



    class Meta:
        model = DadoBancario


    class Media:
        js = ('/site-media/js/selects.js', '/site-media/js/membro.js')


class FeriasAdminForm(forms.ModelForm):
    """
    Inicializar o 'queryset' do campo membro com os valores corretos (apenas funcionarios)
    """

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(FeriasAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        funcionarios = Membro.objects.all()
        for m in funcionarios:
            if not m.funcionario: funcionarios = funcionarios.exclude(id=m.id)
        self.fields['membro'].queryset = funcionarios

    class Meta:
        model = Ferias


class ControleFeriasAdminForm(forms.ModelForm):

    def clean(self):
        termino = self.cleaned_data.get('termino')

        if not termino:
            return self.cleaned_data

        inicio = self.cleaned_data.get('inicio')
        if inicio > termino:
            raise forms.ValidationError(u"Data de término anterior à data de início")

        oficial = self.cleaned_data.get('oficial')

        dias = termino - inicio
        if oficial and dias.days != 19 and dias.days != 29:
            raise forms.ValidationError(u'Férias oficiais devem durar 20 ou 30 dias')
        
        return self.cleaned_data


    class Meta:
        model = ControleFerias

class BaseControleFeriasAdminFormSet(BaseInlineFormSet):

    def clean(self):
        if any(self.errors):
            return

        
        if self.total_form_count() > 3:
            raise forms.ValidationError(u'Não pode haver mais de 3 Controles de Férias')

        oficiais = 0
        nao_oficiais = 1
        for i in range(0, self.total_form_count()-1):
            form = self.forms[i]
            if form.cleaned_data.get('oficial') is True: oficiais += 1
            else: nao_oficiais += 1


        if oficiais > 1 or nao_oficiais > 2:
            raise forms.ValidationError(u'No máximo um período oficial e dois não oficiais')

ControleFeriasAdminFormSet = inlineformset_factory(Ferias, ControleFerias, formset=BaseControleFeriasAdminFormSet)
