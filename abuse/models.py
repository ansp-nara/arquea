# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Instituicao(models.Model):
    nome = models.CharField(max_length=100)
    display = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = u'Instituição'
        verbose_name_plural = u'Instituições'

class Tipo(models.Model):
    nome = models.CharField(max_length=50)
    palavras_chave = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nome

class Mensagem(models.Model):
    assunto = models.CharField(max_length=100)
    data = models.DateTimeField()
    tipo = models.ForeignKey('abuse.Tipo')
    instituicao = models.ForeignKey('abuse.Instituicao', verbose_name=u'Instituição')
    quantidade = models.IntegerField()
    ip = models.CharField(max_length=15)

    def __unicode__(self):
        return u'%s - %s' % (self.tipo.nome, self.instituicao.nome)

    class Meta:
        verbose_name_plural = 'Mensagens'
