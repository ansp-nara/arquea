# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

def proximo_numero():
    from datetime import datetime
    from django.db.models import Max
    agora = datetime.now()
    n1 = MemorandoSimples.objects.filter(data__year=agora.year).aggregate(Max('numero'))
    n2 = MemorandoResposta.objects.filter(data__year=agora.year).aggregate(Max('numero'))
    n1 = n1['numero__max'] or 0
    n2 = n2['numero__max'] or 0

    return max(n1, n2) + 1

class Estado(models.Model):

    """
    Uma instância dessa classe é um estado (ex. Aguardando assinatura).
    O método '__unicode__'	Retorna o nome.
    A class 'Meta'		Define a ordem de apresentação dos dados pelo nome.

    >>> e, created = Estado.objects.get_or_create(nome='Aguardando assinatura')

    >>> e.__unicode__()
    'Aguardando assinatura'
    """


    nome = models.CharField(_(u'Nome'), max_length=30, help_text=_(u'ex. Aguardando assinatura'), unique=True)


    # Retorna o nome.
    def __unicode__(self):
        return "%s" % self.nome


    # Define a ordenação dos dados pelo nome.
    class Meta:
        ordering = ("nome", )


class Assunto(models.Model):
    descricao = models.CharField(max_length=100)
    
    def __unicode__(self):
	return self.descricao


class MemorandoFAPESP(models.Model):
    termo = models.ForeignKey('outorga.Termo')
    numero = models.CharField(_(u'Número do memorando'), max_length=15)
    arquivo = models.FileField(upload_to='memorando', null=True, blank=True)
   
    def __unicode__(self):
	    return self.numero

    class Meta:
        verbose_name = _(u'Memorando da FAPESP')
        verbose_name_plural = _(u'Memorandos da FAPESP')


class Pergunta(models.Model):
    memorando = models.ForeignKey('memorando.MemorandoFAPESP')
    numero = models.CharField(_(u'Número da pergunta'), max_length=10)
    questao = models.TextField(_(u'Questão'))

    def __unicode__(self):
        return '%s - pergunta %s' % (self.memorando, self.numero)

    class Meta:
        ordering = ('numero',)

class MemorandoResposta(models.Model):
    memorando = models.ForeignKey('memorando.MemorandoFAPESP')
    estado = models.ForeignKey('memorando.Estado')
    assunto = models.ForeignKey('memorando.Assunto')
    assinatura = models.ForeignKey('membro.Assinatura')
    numero = models.IntegerField(editable=False)
    identificacao = models.ForeignKey('identificacao.Identificacao', verbose_name=_(u'Identificação'))
    data = models.DateField()
    arquivo = models.FileField(upload_to='memorando', null=True, blank=True)
    protocolo = models.FileField(upload_to='memorando', null=True, blank=True)
    obs = models.TextField(null=True, blank=True)
    introducao = models.TextField(_(u'Introdução'), null=True, blank=True)
    conclusao = models.TextField(_(u'Conclusão'), null=True, blank=True)

    def __unicode__(self):
        return '%s/%s' % (self.data.year, self.numero)

    '''
    O método para salvar uma instância é sobrescrito para que o número sequencial
    do memorando seja gerado automaticamente para cada ano.
    '''
    def save(self, *args, **kwargs):
	    if self.id is None:
	        self.numero = proximo_numero()
	    super(MemorandoResposta, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'Memorando de resposta à FAPESP')
        verbose_name_plural = _(u'Memorandos de resposta à FAPESP')
        ordering = ('-data',)

    def termo(self):
        return self.memorando.termo
    
class Corpo(models.Model):
    """ Cada item de um memorando da FAPESP """

    memorando = models.ForeignKey('memorando.MemorandoResposta')
    pergunta = models.ForeignKey('memorando.Pergunta')
    resposta = models.TextField()
    anexo = models.FileField(upload_to='memorando', null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.pergunta.numero

    class Meta:
        ordering = ('pergunta__numero',)
	
class MemorandoSimples(models.Model):
    data = models.DateField(auto_now_add=True)
    destinatario = models.TextField()
    numero = models.IntegerField(editable=False)
    assunto = models.ForeignKey('memorando.Assunto')
    corpo = models.TextField()
    equipamento = models.BooleanField('Equipamento?')
    envio = models.BooleanField('Envio?')
    assinatura = models.ForeignKey('membro.Membro')
    assinado = models.FileField(_(u'Memorando assinado'), upload_to='memorandos', null=True, blank=True)

    def __unicode__(self):
        return '%s/%s' % (self.data.year, self.numero)
        
    class Meta:
	    verbose_name_plural = u'Memorandos Simples'
	
    '''
    O método para salvar uma instância é sobrescrito para que o número sequencial
    do memorando seja gerado automaticamente para cada ano.
    '''
    def save(self, *args, **kwargs):
        if self.id is None:
            self.numero = proximo_numero()
        super(MemorandoSimples, self).save(*args, **kwargs)
	
    def destino(self):
	    dest = self.destinatario.split('\n')
	    return '<br />'.join(dest)		

