# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Tipo(models.Model):
	"""
	Tipo de ocorrência
	"""
	
	nome = models.CharField(max_length=50)
	
	def __unicode__(self):
		return '%s' % self.nome
	

class Estado(models.Model):
	"""
	Estado da ocorrência
	"""
	
	nome = models.CharField(max_length=50)
	
	def __unicode__(self):
		return '%s' % self.nome


class Natureza(models.Model):
	"""
	Natureza do ocorrido
	"""
	nome = models.CharField(max_length=50)
	
	def __unicode__(self):
		return '%s' % self.nome
		
		
class Ticket(models.Model):
	"""
	Tickets do OTRS
	"""
	ticket = models.IntegerField()
	repositorio = models.ForeignKey('repositorio.Repositorio')
	
	def __unicode__(self):
		return '%s' % self.ticket
		
class Repositorio(models.Model):
	"""
	Repositório de informações da ANSP, projetado para guardar todas
	as informações de ocorrências
	"""
	
	# o número é gerado automaticamente
	numero = models.IntegerField(editable=False)
	
	# data também gerada automaticamente
	data = models.DateField(auto_now_add=True)
	data_ocorrencia = models.DateField(u'Data da ocorrência')
	tipo = models.ForeignKey('repositorio.Tipo')
	estado = models.ForeignKey('repositorio.Estado')
	natureza = models.ForeignKey('repositorio.Natureza')
	ocorrencia = models.TextField(u'Ocorrência')
	obs = models.TextField(u'Observação', null=True, blank=True)
	
	memorandos = models.ManyToManyField('memorando.MemorandoSimples', null=True, blank=True)
	patrimonios = models.ManyToManyField('patrimonio.Patrimonio', verbose_name='Patrimônios', null=True, blank=True)
	responsavel = models.ForeignKey('membro.Membro', limit_choices_to={'historico__funcionario':True, 'historico__termino__isnull':True}, verbose_name='Responsável')
	demais = models.ManyToManyField('membro.Membro', verbose_name='Demais envolvidos', related_name='outros', null=True, blank=True)
	
	def __unicode__(self):
		return u'%s - %s - %s' % (self.num_rep(), self.tipo, self.responsavel)
		
	def num_rep(self):
		return '%s/%s' % (self.data.year, self.numero)
	num_rep.short_description = u'Número'
	
	def proximo_numero(self):
		from datetime import datetime
		from django.db.models import Max
		agora = datetime.now()
		n = Repositorio.objects.filter(data__year=agora.year).aggregate(Max('numero'))
		n = n['numero__max'] or 0
		return n + 1 
    
	def save(self, *args, **kwargs):
		if self.id is None:
			self.numero = self.proximo_numero()
		super(Repositorio, self).save(*args, **kwargs)
			
	class Meta:
		verbose_name = u'Repositório'
		verbose_name_plural = u'Repositórios'
		
		
class Anexo:
	"""
	Arquivos anexos ao repositório
	"""
	
	arquivo = models.FileField(upload_to='repositorio')
	palavras_chave = models.TextField(u'Palavras chave')
	
	def lista_palavras_chave(self):
		return self.palavras_chave.split()
