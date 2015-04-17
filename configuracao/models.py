# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

class Papelaria(models.Model):
    papel_timbrado_retrato_a4 = models.FileField(upload_to='papel_timbrado_retrato_a4', null=True, blank=True)
    retrato_a4_margem_superior = models.DecimalField(_(u'Margem superior em cm'), max_digits=3, decimal_places=2, null=True, blank=True)
    retrato_a4_margem_inferior = models.DecimalField(_(u'Margem inferior em cm'), max_digits=3, decimal_places=2, null=True, blank=True)
    
    papel_timbrado_paisagem_a4 = models.FileField(upload_to='papel_timbrado_paisagem_a4', null=True, blank=True)
    paisagem_a4_margem_superior = models.DecimalField(_(u'Margem superior em cm'), max_digits=3, decimal_places=2, null=True, blank=True)
    paisagem_a4_margem_inferior = models.DecimalField(_(u'Margem inferior em cm'), max_digits=3, decimal_places=2, null=True, blank=True)
    
    papel_timbrado_retrato_a3 = models.FileField(upload_to='papel_timbrado_retrato_a3', null=True, blank=True)
    retrato_a3_margem_superior = models.DecimalField(_(u'Margem superior em cm'), max_digits=3, decimal_places=2, null=True, blank=True)
    retrato_a3_margem_inferior = models.DecimalField(_(u'Margem inferior em cm'), max_digits=3, decimal_places=2, null=True, blank=True)
    
    papel_timbrado_paisagem_a3 = models.FileField(upload_to='papel_timbrado_paisagem_a3', null=True, blank=True)
    paisagem_a3_margem_superior = models.DecimalField(_(u'Margem superior em cm'), max_digits=3, decimal_places=2, null=True, blank=True)
    paisagem_a3_margem_inferior = models.DecimalField(_(u'Margem inferior em cm'), max_digits=3, decimal_places=2, null=True, blank=True)
    
    
    valido = models.BooleanField(u'Template válido?', default=True)

    def has_files(self):
        import os.path
 
        return self.papel_timbrado_retrato_a4 != None and self.papel_timbrado_retrato_a4.name and os.path.isfile(self.papel_timbrado_retrato_a4.name) and \
               self.papel_timbrado_paisagem_a4 != None and self.papel_timbrado_paisagem_a4.name and os.path.isfile(self.papel_timbrado_paisagem_a4.name) and \
               self.papel_timbrado_retrato_a3 != None and self.papel_timbrado_retrato_a3.name and os.path.isfile(self.papel_timbrado_retrato_a3.name) and \
               self.papel_timbrado_paisagem_a3 != None and self.papel_timbrado_paisagem_a3.name and os.path.isfile(self.papel_timbrado_paisagem_a3.name)
               


class Cheque(models.Model):
    nome_assinatura = models.CharField(_(u'Assinatura'), max_length=150)


class Variavel(models.Model):
    DATACENTER_IDS = 'DATACENTER_IDS'
    
    _NOMES = (
                (DATACENTER_IDS, 'ID da Entidade do Datacenter principal.'),
            )
    nome = models.CharField(_(u'Nome da variável'), max_length=60, unique=True, choices=_NOMES)
    valor = models.CharField(_(u'Valor'), max_length=60, help_text=u'', )
    obs = models.TextField(null=True, blank=True) 
  
    class Meta:
        verbose_name = _(u'Variável')
        verbose_name_plural = _(u'Variáveis')
        ordering = ('nome',)



class ClassesExtra(models.Model):
    content_type = models.ForeignKey(ContentType)
    help = models.TextField()

    def __unicode__(self):
        return '%s/%s - extra' % (self.content_type.app_label, self.content_type.model)

    class Meta:
        ordering = ('content_type__app_label', 'content_type__model')
        verbose_name = u'Ajuda dos modelos'
        verbose_name_plural = u'Ajudas dos modelos'

class FieldsHelp(models.Model):
    model = models.ForeignKey(ClassesExtra)
    field = models.CharField(max_length=30)
    help = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s/%s - %s' % (self.model.content_type.app_label, self.model.content_type.model, self.field)