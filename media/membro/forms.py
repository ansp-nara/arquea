# -*- coding: utf-8 -*-

from models import Membro, Equipe, Tarefa, DadoBancario
from identificacao.models import Entidade
from django.forms.util import ErrorList
from django import forms
import re


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



class TarefaAdminForm(forms.ModelForm):

    """
    Uma instância dessa classe faz algumas definições/limitações para a tela de cadastramento do modelo 'Tarefa'.

    O método '__init__'		Limita a seleção do campo 'membro' para selecionar apenas funcionários.
    O campo 'entidade'		Foi criado para filtrar o campo 'equipe'.
    A class 'Meta' 		Define o modelo que será utilizado.
    A class 'Media'		Define os arquivos .js que serão utilizados.
    """


    entidade = forms.ModelChoiceField(Entidade.objects.all(), required=False,
            widget=forms.Select(attrs={'onchange': 'filter_select("id_equipe", "id_entidade");'}))

    class Meta:
        model = Tarefa


    class Media:
        js = ('/site-media/js/selects.js', '/site-media/js/membro.js')



class DadoBancarioAdminForm(forms.ModelForm):

    """
    Uma instância dessa classe faz algumas definições/limitações para a tela de cadastramento do modelo 'Tarefa'.

    O método '__init__'		Limita a seleção do campo 'membro' para selecionar apenas funcionários.
    O campo 'entidade'		Foi criado para filtrar o campo 'equipe'.
    A class 'Meta'		Define o modelo que será utilizado.
    A class 'Media'		Define os arquivo .js que serão utilizados.
    """


    tarefa = forms.ModelChoiceField(Tarefa.objects.all(), required=False,
            widget=forms.Select(attrs={'onchange': 'filter_select("id_membro", "membro_tarefa");'}))


    class Meta:
        model = DadoBancario


    class Media:
        js = ('/site-media/js/selects.js', '/site-media/js/membro.js')

