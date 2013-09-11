# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.functions import formata_moeda
from utils.models import NARADateField
from decimal import Decimal
from django.db.models import Q, Max
from protocolo.models import Protocolo, Estado as EstadoProtocolo, Cotacao
from membro.models import *
import datetime
from django.db.models import Sum

CODIGO_FINANCEIRO = (
  ('COMP', 'Concessao Bens/Serv. Pais'),
  ('PGMP', 'Pgto. Bens/Serv. Pais'),
  ('DVMP', 'Devl. Bens/Serv. Pais'),
  ('SUMP', 'Supl. Bens/Serv. Pais'),
  ('ANMP', 'Anulacao'),
  ('ESMP', 'Estorno ANMP'),
  ('CAMP', 'Canc. Bens/Serv. Pais'),
)
class ExtratoCC(models.Model):
    extrato_financeiro = models.ForeignKey('financeiro.ExtratoFinanceiro', verbose_name=_(u'Extrato Financeiro'), blank=True, null=True) 
    data_oper = NARADateField(_(u'Data da operação'))
    cod_oper = models.IntegerField(_(u'Documento'))
    despesa_caixa = models.BooleanField(_(u'Despesa de caixa?'))
    valor = models.DecimalField(_(u'Valor'), max_digits=12, decimal_places=2)
    historico = models.CharField(_(u'Histórico'), max_length=30)
    data_extrato = NARADateField(_(u'Data do extrato'), null=True, blank=True)
    imagem = models.ImageField(_(u'Imagem do cheque'), upload_to='extratocc', null=True, blank=True)
    capa = models.TextField(null=True, blank=True)
    obs = models.TextField(null=True, blank=True)
    
    class Meta:
	verbose_name = _(u'Extrato de Conta corrente')
	verbose_name_plural = _(u'Extratos de Conta corrente')
	ordering = ('-data_oper',)
	
    def __unicode__(self):
	    return u'%s - %s - %s - %s' % (self.data_oper, self.cod_oper, self.historico, self.valor)
      

    @property
    def saldo(self):
        s = ExtratoCC.objects.filter(data_oper__lte=self.data_oper).aggregate(Sum('valor'))
	return s['valor__sum']
	
    @property
    def saldo_anterior(self):
        s = ExtratoCC.objects.filter(data_oper__lt=self.data_oper).aggregate(Sum('valor'))
	return s['valor__sum']
	
    def parciais(self):
	mods = {}		    
	for p in self.pagamento_set.all():
            if p.origem_fapesp:
                modalidade = p.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
                if modalidade not in mods.keys():
                    mods[modalidade] = {}
    	            for a in p.auditoria_set.all():
		        if not a.parcial in mods[modalidade].keys():
		  	    mods[modalidade][a.parcial] = []
                        if not a.pagina in mods[modalidade][a.parcial]:
                            mods[modalidade][a.parcial].append(a.pagina)
			
	    
	parc = ''
	for modalidade in mods.keys():
	    parc += '%s [parcial ' % modalidade
	    for p in mods[modalidade].keys():
		pags = mods[modalidade][p]
		pags.sort()
		parc += '%s (%s)' % (p, ','.join([str(k) for k in pags]))
            parc += ']  '

	return parc
class TipoComprovanteFinanceiro(models.Model):
    nome = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nome

class ExtratoFinanceiro(models.Model):
    termo = models.ForeignKey('outorga.Termo', verbose_name=_(u'Termo de outorga'))
    data_libera = NARADateField(_(u'Data'))
    cod = models.CharField(_(u'Código'), max_length=4, choices=CODIGO_FINANCEIRO)
    historico = models.CharField(_(u'Histórico'), max_length=40)
    valor = models.DecimalField(_(u'Valor'), max_digits=12, decimal_places=2)
    comprovante = models.FileField(_(u'Comprovante da operação'), upload_to='extratofinanceiro', null=True, blank=True)
    tipo_comprovante = models.ForeignKey('financeiro.TipoComprovanteFinanceiro', null=True, blank=True)
    parcial = models.IntegerField(null=True, blank=True)
  
    class Meta:
	verbose_name = _(u'Extrato do Financeiro')
	verbose_name_plural = _(u'Extratos do Financeiro')
	ordering = ('-data_libera',)

    def __unicode__(self):
	    return u'%s - %s - %s - %s' % (self.data_libera, self.cod, self.historico, self.valor)
    
    def save(self, *args, **kwargs):
	for (cod, hist) in CODIGO_FINANCEIRO:
	    if self.cod == cod:
		self.historico = hist
		break
		
	super(ExtratoFinanceiro, self).save(*args, **kwargs)
   
    @property
    def despesa_caixa(self):
        try:
            return self.tipo_comprovante == TipoComprovanteFinanceiro.objects.get(nome=u'Despesa de caixa')
        except:
            return False

class Pagamento(models.Model):
    patrocinio = models.ForeignKey('financeiro.ExtratoPatrocinio', verbose_name=_(u'Extrato do patrocínio'), null=True, blank=True)
    conta_corrente = models.ForeignKey('financeiro.ExtratoCC', null=True, blank=True)
    protocolo = models.ForeignKey('protocolo.Protocolo')
    valor_fapesp = models.DecimalField(_(u'Valor originário da Fapesp'), max_digits=12, decimal_places=2)
    valor_patrocinio = models.DecimalField(_(u'Valor originário de patrocínio'), max_digits=12, decimal_places=2, null=True, blank=True)
    reembolso = models.BooleanField(default=False)
    membro = models.ForeignKey('membro.Membro', null=True, blank=True)
    origem_fapesp = models.ForeignKey('outorga.OrigemFapesp', null=True, blank=True)
    pergunta = models.ManyToManyField('memorando.Pergunta', null=True, blank=True)
    
    def __unicode__(self):
    	if self.valor_patrocinio:
            valor = self.valor_fapesp+self.valor_patrocinio
    	else: valor = self.valor_fapesp
    	mod = ''
    	if self.origem_fapesp:
    	   mod = self.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
           a = self.auditoria_set.all()
           if a:
               a = a[0]
               return u"%s - %s - %s, parcial %s, página %s    ID: %s" % (self.protocolo.num_documento, valor, mod, a.parcial, a.pagina, self.pk)
    	return u"%s - %s - %s    ID: %s" % (self.protocolo.num_documento, valor, mod, self.pk)

    def codigo_operacao(self):
    	return self.conta_corrente.cod_oper
    codigo_operacao.short_description = 'Operação Bancária'
    codigo_operacao.admin_order_field = 'conta_corrente__cod_oper'

    def anexos(self):
        retorno = u'Não'
    	if self.auditoria_set.count() > 0:
	   retorno = u'Sim'

	return retorno

    def save(self, *args, **kwargs):

        e, created = EstadoProtocolo.objects.get_or_create(nome=u'Pago')
	if not self.id:
	   self.protocolo.estado = e
	   self.protocolo.save()

	super(Pagamento, self).save(*args, **kwargs)

    def termo(self):
    	return '%s' % self.protocolo.termo.__unicode__()

    def item(self):
        if self.origem_fapesp:
	   return '%s' % self.origem_fapesp.item_outorga.__unicode__()
	else: return u'Não é Fapesp'
    item.short_description = u'Item do orçamento'	

    def data(self):
        return self.protocolo.data_vencimento
    data.admin_order_field = 'protocolo__data_vencimento'

    def nota(self):
        return self.protocolo.num_documento
    nota.short_description = 'NF'
    nota.admin_order_field = 'protocolo__num_documento'

    def formata_valor_fapesp(self):
        moeda = 'R$'
        if self.origem_fapesp and self.origem_fapesp.item_outorga.natureza_gasto.modalidade.moeda_nacional == False:
	    moeda = 'US$'
        return '%s %s' % (moeda, formata_moeda(self.valor_fapesp, ','))
    formata_valor_fapesp.short_description = 'Valor Fapesp'
    formata_valor_fapesp.admin_order_field = 'valor_fapesp'

    def pagina(self):
        if self.auditoria_set.count() > 0:
            return self.auditoria_set.all()[0].pagina
        return ''
    pagina.short_description = u'Página'
    pagina.admin_order_field = 'auditoria__pagina'

    def parcial(self):
        if self.auditoria_set.count() > 0:
            return self.auditoria_set.all()[0].parcial
        return ''
    parcial.admin_order_field = 'auditoria__parcial'

    class Meta:
    	ordering = ('conta_corrente',)

class LocalizaPatrocinio(models.Model):
    consignado = models.CharField(max_length=50)
    
    class Meta:
	    verbose_name = _(u'Localização do patrocínio')
	    verbose_name_plural = _(u'Localização dos patrocínios')

    def __unicode__(self):
	    return self.consignado
	
class ExtratoPatrocinio(models.Model):
    localiza = models.ForeignKey('financeiro.LocalizaPatrocinio', verbose_name=_(u'Localização do patrocínio'))
    data_oper = NARADateField(_(u'Data da operação'))
    cod_oper = models.IntegerField(_(u'Código da operação'))
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    historico = models.CharField(max_length=30)
    obs = models.TextField()
    
    class Meta:
	    verbose_name = _(u'Extrato do patrocínio')
	    verbose_name_plural = _(u'Extratos dos patrocínios')

    def __unicode__(self):
	    return u'%s - %s - %s' % (self.localiza.consignado, self.data_oper, self.valor)
	
class Estado(models.Model):
    nome = models.CharField(max_length=30)
    
    def __unicode__(self):
	    return self.nome
	
def ultimaparcial():
    from outorga.models import Termo
    from financeiro.models import Auditoria
	
    t = Termo.objects.aggregate(Max('ano'))
    a = Auditoria.objects.filter(pagamento__protocolo__termo__ano=t['ano__max']).aggregate(Max('parcial'))
    return a['parcial__max']
	
def ultimapagina():
    from outorga.models import Termo
    from financeiro.models import Auditoria
	
    t = Termo.objects.aggregate(Max('ano'))
    p = Auditoria.objects.filter(pagamento__protocolo__termo__ano=t['ano__max'], parcial=ultimaparcial()).aggregate(Max('pagina'))
    return p['pagina__max']+1

class Auditoria(models.Model):
    estado = models.ForeignKey('financeiro.Estado')
    pagamento = models.ForeignKey('financeiro.Pagamento')
    tipo = models.ForeignKey('financeiro.TipoComprovante')
    arquivo = models.FileField(upload_to='auditoria', null=True, blank=True)
    parcial = models.IntegerField()
    pagina = models.IntegerField()
    obs = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
	    return u'Parcial: %s, página: %s' % (self.parcial, self.pagina)
	 

class TipoComprovante(models.Model):
    nome = models.CharField(max_length=100)
    
    class Meta:
	verbose_name = _(u'Tipo de comprovante')
	verbose_name_plural = _(u'Tipos de comprovante')
        ordering = ('nome',)

    def __unicode__(self):
	    return self.nome



