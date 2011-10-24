# -*- coding: utf-8 -*-

from financeiro.models import Pagamento
from django import forms
from django.forms.util import ErrorList
from outorga.models import Termo
from financeiro.models import Pagamento
from models import *
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE
from django.utils.html import strip_tags
from utils import widgets

class MemorandoRespostaForm(forms.ModelForm):
    introducao = forms.CharField(required=False, label=u'Introdução', widget=TinyMCE(attrs={'cols': 160, 'rows': 180}, mce_attrs={'height':500}))
    conclusao = forms.CharField(required=False, label=u'Conclusão', widget=TinyMCE(attrs={'cols': 160, 'rows': 180}, mce_attrs={'height':500}))
    memorando = forms.ModelChoiceField(MemorandoFAPESP.objects.all(), label=u'Memorando FAPESP',
                      widget=forms.Select(attrs={'onchange':'ajax_filter_perguntas(this.value);'}))

    class Meta:
        model = MemorandoResposta

class PerguntaAdminForm(forms.ModelForm):
    questao = forms.CharField(label=u'Questão', widget=TinyMCE(attrs={'cols': 100, 'rows': 30}, mce_attrs={'height':120}))    

    class Meta:
        model = Pergunta

class MemorandoSimplesForm(forms.ModelForm):
    corpo = forms.CharField(widget=TinyMCE(attrs={'cols': 160, 'rows': 180}, mce_attrs={'height':500}))


    class Meta:
        model = MemorandoSimples


class CorpoAdminForm(forms.ModelForm):
    pergunta = forms.ModelChoiceField(Pergunta.objects.all(), label=_(u'Pergunta'),
              widget=forms.Select(attrs={'onchange': 'ajax_select_pergunta(this.id);'}))
    perg = forms.CharField(label='Texto da pergunta', widget=widgets.PlainTextWidget, required=False)
    resposta = forms.CharField(label='Resposta', widget=TinyMCE(attrs={'cols': 70, 'rows': 30}, mce_attrs={'height':120}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(CorpoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)
	if data:
            pergunta_id = data.get('pergunta')
            if pergunta_id:
                pgta = Pergunta.objects.get(id=pergunta_id)
                self.fields['perg'].initial = pgta.questao
        elif instance and hasattr(instance, 'pergunta'):
            self.fields['perg'].initial = instance.pergunta.questao

    class Meta:
        model = Corpo

    class Media:
        js = ('/media/js/jquery.js', '/media/js/selects.js')

	
class BaseCorpoInlineFormSet(BaseInlineFormSet):
    
    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None):

        super(BaseCorpoInlineFormSet, self).__init__(data=data, files=files,
                 instance=instance, save_as_new=save_as_new, prefix=prefix, queryset=queryset)

        if data:
            memorando_id = data.get('memorando')
            if memorando_id:
                m = MemorandoResposta.objects.get(id=memorando_id)
                for f in self.forms:
                    f.fields['pergunta'].queryset = Pergunta.objects.filter(memorando=m)
                self.empty_form.fields['pergunta'].queryset = Pergunta.objects.filter(memorando=m)

        elif instance and hasattr(instance,'memorando'):
            m = instance.memorando
            for f in self.forms:
                f.fields['pergunta'].queryset = Pergunta.objects.filter(memorando=m)
            self.empty_form.fields['pergunta'].queryset = Pergunta.objects.filter(memorando=m)

        else:
            for f in self.forms:
                f.fields['pergunta'].queryset = Pergunta.objects.none()
            self.empty_form.fields['pergunta'].queryset = Pergunta.objects.none()
                


CorpoFormSet = inlineformset_factory(MemorandoResposta, Corpo, formset=BaseCorpoInlineFormSet)
