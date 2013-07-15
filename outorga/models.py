# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.functions import formata_moeda
from utils.models import NARADateField
from django.db.models import Q, Sum
from decimal import Decimal
import datetime
#import copy


# Retorna o caminho para onde o arquivo será feito upload.
def upload_dir(instance, filename):
    return 'outorga/%s/%s' % (str(instance.id), filename)

def upload_dir_os(instance, filename):
    return 'OS/%s/%s' % (str(instance.os.id), filename)

# Create your models here.
class Modalidade(models.Model):

    """
    Uma instância dessa classe é uma das modalidades de gasto autorizadas pelo Departamento de Auditoria da FAPESP.

    O método '__unicode__' 		Retorna a sigla e o nome da modalidade.
    A classmethod 'modalidades_termo'	Retorna as modalidades de um termo que possuem itens de outorga com o campo 'item=None'.
    A class 'Meta'			Define a ordenação dos dados pela sigla.


    Cria Modalidade
    >>> e, created = Estado.objects.get_or_create(nome='Vigente')
    >>> c, created = Categoria.objects.get_or_create(nome='Inicial')
    >>> m, created = Modalidade.objects.get_or_create(sigla='OUT', defaults={'nome': 'Outros', 'moeda_nacional': True})


    Cria Natureza de Gasto
    >>> t, created = Termo.objects.get_or_create(ano=2008, processo=51885, digito=8, defaults={'inicio': datetime.date(2008,1,1), 'estado': e})
    >>> o, created = Outorga.objects.get_or_create(termo=t, categoria=c, data_solicitacao=datetime.date(2007,12,1), termino=datetime.date(2008,12,31), data_presta_contas=datetime.date(2009,1,31))
    >>> n, created = Natureza_gasto.objects.get_or_create(modalidade=m, outorga=o)

    >>> m.__unicode__()
    u'OUT - Outros'

    >>> Modalidade.modalidades_termo(t)
    [<Modalidade: OUT - Outros>]
    """


    sigla = models.CharField(_(u'Sigla'), max_length=10, blank=True, help_text=_(u'ex. STB'), unique=True)
    nome = models.CharField(_(u'Nome'), max_length=40, blank=True, help_text=_(u'ex. Serviços de Terceiros no Brasil'))
    moeda_nacional = models.BooleanField(_(u'R$'), help_text=_(u'ex. Moeda Nacional?'), default=True)


    # Retorna a sigla e o nome da modalidade.
    def __unicode__(self):
        return u'%s - %s' % (self.sigla, self.nome)


    # Retorna as modalidades de um termo que possuem itens do pedido de outorga com o campo 'item=None'.
    @classmethod
    def modalidades_termo(cls, t=None):
        modalidades = cls.objects.all()
        if t:
            for m in modalidades:
                ng = m.natureza_gasto_set.filter(termo=t)
                if not ng:
                    modalidades = modalidades.exclude(pk=m.id)
                else:
                    for n in ng:
                        i = n.item_set.all()
                        if not i:
                            modalidades = modalidades.exclude(pk=m.id)
        return modalidades


    # Define ordenação dos dados pela sigla.
    class Meta:
        ordering = ('sigla', )



class Estado(models.Model):

    """
    Uma instância dessa classe representa um estado (ex. Quitado, Vigente).

    O método '__unicode__'	Retorna o nome do estado.
    A class 'Meta'		Define a ordenação dos dados pelo nome.


    Cria Estado
    >>> e, created = Estado.objects.get_or_create(nome='Vigente')

    >>> e.__unicode__()
    u'Vigente'
    """


    nome = models.CharField(_(u'Nome'), max_length=30, blank=True, help_text=_(u'ex. Vigente'), unique=True)


    # Retorna o nome.
    def __unicode__(self):
        return u'%s' % self.nome


    # Define ordena dos dados pelo nome.
    class Meta:
        ordering = ('nome', )



class Termo(models.Model):

    """
    Uma instância dessa classe representa um Termo de Outorga.

    O método '__unicode__'				Retorna o número completo do processo no formato 'ano/número-digito'.
    O método 'mostra_membro'				Retorna o nome do outorgado.
    O método 'save'					Não permite que o número do termo de ortorga seja alterado.
    O atributo 'real'                                   Calcula a concessão total em reais de um termo somando os totalizadores das naturezas de gasto
							considerando todos os pedidos de concessão.
    O método 'termo_real'                               Formata o atributo 'real' em formato moeda.
    O atributo 'dolar'                                  Calcula a concessão total em dolares de um termo somando os totalizadores das naturezas de gasto
							considerando todos os pedidos pedidos de concessão.
    O método 'termo_dolar'                              Formata o atributo 'dolar' em formato moeda.
    O método 'duracao_meses'				Calcula em meses a vigência do termo de outorga a partir das informações dos pedidos de
							concessão.
    O atributo 'total_realizado_real'                   Calcula o total das despesas realizadas em reais de um termo somando os totalizadores das 
							naturezas de gasto considerando todos os pedidos de concessão.
    O método 'formata_realizado_real'                   Formata o atributo 'total_realizado_real' em formato moeda.
    O atributo 'total_realizado_dolar'                  Calcula o total das despesas realizadas em dolares de um termo somando os totalizadores das 
							naturezas de gasto considerando todos os pedidos de concessão.
    O método 'formata_realizado_dolar'                  Formata o atributo 'total_realizado_dolar' em formato moeda.

    O atributo 'vigencia'				Foi criado para retornar o método 'duracao_meses'.
    O atributo 'num_processo'				Foi criado para retornar o método '__unicode__'.

    A classmethod 'termos_auditoria_fapesp_em_aberto'   Retorna os termos que possuem fontes pagadoras (fapesp) que ainda não possuem registro no
                                                        modelo Auditoria FAPESP.
    A classmethod 'termos_auditoria_interna_em_aberto'  Retorna os termos que possuem fontes pagadoras (interna) que ainda não possuem registro no
                                                        modelo Auditoria Interna.

    A 'class Meta'					Define a descrição do modelo (singular e plural) e a ordenação dos dados pelo ano.


    Cria Termo
    >>> e, created = Estado.objects.get_or_create(nome='Vigente')
    >>> t, create = Termo.objects.get_or_create(ano=2008, processo=22222, digito=2, defaults={'inicio': datetime.date(2008,1,1), 'estado'= e})


    Cria Outorga
    >>> c1, created = Categoria.objects.get_or_create(nome='Inicial')
    >>> c2, created = Categoria.objects.get_or_create(nome='Aditivo')

    >>> o1, created = Outorga.objects.get_or_create(termo=t, categoria=c1, data_solicitacao=datetime.date(2007,12,1), defaults={'termino': datetime.date(2008,12,31), 'data_presta_contas': datetime.date(2008,2,28)})
    >>> o2, created = Outorga.objects.get_or_create(termo=t, categoria=c2, data_solicitacao=datetime.date(2008,4,1), defaults={'termino': datetime.date(2008,12,31), 'data_presta_contas': datetime.date(2008,2,28)})


    Cria Natureza de gasto
    >>> m1, created = Modalidade.objects.get_or_create(sigla='STB', defaults={'nome': 'Servicos de Terceiro no Brasil', 'moeda_nacional': True})
    >>> m2, created = Modalidade.objects.get_or_create(sigla='STE', defaults={'nome': 'Servicos de Terceiro no Exterior', 'moeda_nacional': False})

    >>> n1, created = Natureza_gasto.objects.get_or_create(modalidade=m1, outorga=o1)
    >>> n2, created = Natureza_gasto.objects.get_or_create(modalidade=m2, outorga=o1)
    >>> n3, created = Natureza_gasto.objects.get_or_create(modalidade=m1, outorga=o2)
    >>> n4, created = Natureza_gasto.objects.get_or_create(modalidade=m2, outorga=o2)


    Cria Item de Outorga
     from identificacao.models import Entidade, Contato, Identificacao

    >>> ent1, created = Entidade.objects.get_or_create(sigla='GTECH', defaults={'nome': 'Granero Tech', 'cnpj': '00.000.000/0000-00', 'ativo': False, 'fisco': True, 'url': ''})
    >>> ent2, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'SAC do Brasil', 'cnpj': '00.000.000/0000-00', 'ativo': True, 'fisco': True, 'url': ''})
    >>> ent3, created = Entidade.objects.get_or_create(sigla='TERREMARK', defaults={'nome': 'Terremark do Brasil', 'cnpj': '00.000.000/0000-00', 'ativo': True, 'fisco': True, 'url': ''})

    >>> i1, created = Item.objects.get_or_create(entidade=ent1, natureza_gasto=n1, descricao='Armazenagem', defaults={'justificativa': 'Armazenagem de equipamentos', 'quantidade': 12, 'valor_unit': 2500})
    >>> i2, created = Item.objects.get_or_create(entidade=ent2, natureza_gasto=n2, descricao='Serviço de Conexão Internacional', defaults={'justificativa': 'Link Internacional', 'quantidade': 12, 'valor_unit': 250000})
    >>> i3, created = Item.objects.get_or_create(entidade=ent3, natureza_gasto=n3, descricao='Serviço de Conexão', defaults={'justificativa': 'Ligação SP-CPS', 'quantidade': 12, 'valor_unit': 100000})
    >>> i4, created = Item.objects.get_or_create(entidade=ent3, natureza_gasto=n4, descricao='Serviço de Conexão Internacional', defaults={'justificativa': 'Ajuste na cobrança do Link Internacional', 'quantidade': 6, 'valor_unit': 50000, 'item: i2})


    Cria Protocolo
    from protocolo.models import Protocolo, ItemProtocolo, TipoDocumento, Origem, Estado as EstadoProtocolo

    >>> ep, created = EstadoProtocolo.objects.get_or_create(nome='Aprovado')
    >>> td, created = TipoDocumento.objects.get_or_create(nome='Nota Fiscal')
    >>> og, created = Origem.objects.get_or_create(nome='Motoboy')

    >>> cot1, created = Contato.objects.get_or_create(nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})
    >>> cot2, created = Contato.objects.get_or_create(nome='Alex', defaults={'email': 'alex@alex.com.br', 'tel': ''})
    >>> cot3, created = Contato.objects.get_or_create(nome='Marcos', defaults={'email': 'alex@alex.com.br', 'tel': ''})

    >>> iden1, created = Identificacao.objects.get_or_create(entidade=ent1, contato=cot1, defaults={'funcao': 'Tecnico', 'area': 'Estoque', 'ativo': True})
    >>> iden2, created = Identificacao.objects.get_or_create(entidade=ent2, contato=cot2, defaults={'funcao': 'Gerente', 'area': 'Redes', 'ativo': True})
    >>> iden3, created = Identificacao.objects.get_or_create(entidade=ent3, contato=cot3, defaults={'funcao': 'Diretor', 'area': 'Redes', 'ativo': True})

    >>> p1, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden1, tipo_documento=td, data_chegada=datetime.datetime(2008,9,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 8888, 'data_vencimento': datetime.date(2008,10,5), 'descricao': 'Conta mensal - armazenagem 09/2008', 'valor_total': None})
    >>> p2, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden2, tipo_documento=td, data_chegada=datetime.datetime(2008,9,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 7777, 'data_vencimento': datetime.date(2008,10,10), 'descricao': 'Serviço de Conexão Internacional - 09/2009', 'valor_total': None})
    >>> p3, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden3, tipo_documento=td, data_chegada=datetime.datetime(2008,9,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 5555, 'data_vencimento': datetime.date(2008,10,15), 'descricao': 'Serviço de Conexão Local - 09/2009', 'valor_total': None})


    Cria Item do Protocolo
    >>> ip1 = ItemProtocolo.objects.get_or_create(protocolo=p1, descricao='Tarifa mensal - 09/2009', quantidade=1, valor_unitario=2500)
    >>> ip2 = ItemProtocolo.objects.get_or_create(protocolo=p1, descricao='Reajuste tarifa mensal - 09/2009', quantidade=1, valor_unitario=150)
    >>> ip3 = ItemProtocolo.objects.get_or_create(protocolo=p2, descricao='Conexão Internacional - 09/2009', quantidade=1, valor_unitario=250000)
    >>> ip4 = ItemProtocolo.objects.get_or_create(protocolo=p2, descricao='Reajuste do serviço de Conexão Internacional - 09/2009', quantidade=1, valor_unitario=50000)
    >>> ip5 = ItemProtocolo.objects.get_or_create(protocolo=p3, descricao='Conexão Local - 09/2009', quantidade=1, valor_unitario=85000)
    >>> ip6 = ItemProtocolo.objects.get_or_create(protocolo=p3, descricao='Reajuste do serviço de Conexão Local - 09/2009', quantidade=1, valor_unitario=15000)

    Criar Fonte Pagadora
     from financeiro.models import OrigemOutrasVerbas, FontePagadora, OrigemFapesp, ExtratoCC, Estato as EstadoFinanceiro

    >>> ef1, created = EstadoFinanceiro.objects.get_or_create(nome='Aprovado')
    >>> ef2, created = EstadoFinanceiro.objects.get_or_create(nome='Concluído')

    >>> ex1, created = ExtratoCC.objects.get_or_create(data_extrato=datetime.date(2008,10,30), data_oper=datetime.date(2008,10,5), cod_oper=333333, valor='2650', historico='TED')
    >>> ex2, created = ExtratoCC.objects.get_or_create(data_extrato=datetime.date(2008,10,30), data_oper=datetime.date(2008,10,10), cod_oper=4444, valor='250000', historico='TED')
    >>> ex3, created = ExtratoCC.objects.get_or_create(data_extrato=datetime.date(2008,10,30), data_oper=datetime.date(2008,10,10), cod_oper=4444, valor='50000', historico='TED')
    >>> ex4, created = ExtratoCC.objects.get_or_create(data_extrato=datetime.date(2008,10,30), data_oper=datetime.date(2008,10,15), cod_oper=5555, valor='100000', historico='TED')

    >>> a1, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e GTech')
    >>> a2, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')
    >>> a3, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e Terremark')
    >>> a4, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo de patrocínio entre ANSP e Telefônica')

    >>> of1, created = OrigemFapesp.objects.get_or_create(acordo=a1, item_outorga=i1)
    >>> of2, created = OrigemFapesp.objects.get_or_create(acordo=a2, item_outorga=i2)
    >>> of3, created = OrigemFapesp.objects.get_or_create(acordo=a3, item_outorga=i3)

    >>> oov, created = OrigemOutrasVerbas.objects.get_or_create(acordo=a4, item_outorga=i2)

    >>> fp1 = FontePagadora.objects.get_or_create(protocolo=p1, extrato=ex1, origem_fapesp=of1, estado=ef2, valor='2650')
    >>> fp2 = FontePagadora.objects.get_or_create(protocolo=p2, extrato=ex2, origem_fapesp=of2, estado=ef2, valor='250000')
    >>> fp3 = FontePagadora.objects.get_or_create(protocolo=p2, extrato=ex3, origem_outras_verbas=oov, estado=ef2, valor='50000')
    >>> fp4 = FontePagadora.objects.get_or_create(protocolo=p3, extrato=ex4, origem_fapesp=of3, estado=ef2, valor='100000')


    >>> t.__unicode__()
    '08/22222-2'

    >>> t.real
    Decimal('102500')

    >>> t.termo_real()
    'R$ 102.500,00'

    >>> t.dolar
    Decimal('300000')

    >>> t.termo_dolar()
    '$ 300,000.00'

    >>> t.duracao_meses()
    '12 meses'

    >>> t.total_realizado_real
    Decimal('102650')

    >>> t.formata_realizado_real()
    'R$ 102.650,00'

    >>> t.total_realizado_dolar
    Decimal('250000')

    >>> t.formata_realizado_dolar()
    '$ 250,000.00'

    >>> t.num_processo
    '08/22222-2'

    >>> t.vigencia
    '12 meses'

    >>> Termo.termos_auditoria_fapesp_em_aberto()
    [<Termo: 08/22222-2>]

    >>> Termo.termos_auditoria_interna_em_aberto()
    [<Termo: 08/22222-2>]
    """


    ano = models.IntegerField(_(u'Ano'), help_text=_(u'ex. 2008'), default=0)
    processo = models.IntegerField(_(u'Processo'), help_text=_(u'ex. 52885'), default=0)
    digito = models.IntegerField(_(u'Dígito'), help_text=_(u'ex. 8'), default=0)
    inicio = NARADateField(_(u'Início'), help_text=_(u'Data de início do processo'), null=True, blank=True)
    estado = models.ForeignKey('outorga.Estado', verbose_name=_(u'Estado'))
    modalidade = models.ManyToManyField('outorga.Modalidade', through='Natureza_gasto', verbose_name=_(u'Pasta'))
    parecer = models.FileField(u'Parecer inicial', upload_to='termo', blank=True, null=True)
    parecer_final = models.FileField(u'Parecer final', upload_to='termo', blank=True, null=True)
    orcamento = models.FileField(_(u'Orçamento'), upload_to='termo', blank=True, null=True)
    quitacao = models.FileField(_(u'Quitação'), upload_to='termo', blank=True, null=True)
    doacao = models.FileField(_(u'Doação'), upload_to='termo', blank=True, null=True)
    extrato_financeiro = models.FileField(upload_to='termo', blank=True, null=True)
#    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Outorga'))


    # Retorna o número completo do processo (ano, número e dígito).
    def __unicode__(self):
        ano = str(self.ano)[2:]
        return '%s/%s-%s' % (ano, self.processo, self.digito)


    # Retorna o outorgado.
#    def mostra_membro(self):
#        return self.membro.nome
#    mostra_membro.short_description = _(u'Outorgado')


    # Não permite fazer alteração no número do processo.
    def save(self, force_insert=False, force_update=False):
        pk = self.pk
        try:
            antigo = Termo.objects.get(pk=pk)
        except Termo.DoesNotExist:
            antigo = None
        
        if antigo and (antigo.ano != 0 or antigo.processo != 0 or antigo.digito != 0):
            self.ano = antigo.ano
            self.processo = antigo.processo
            self.digito = antigo.digito
            
        super(Termo, self).save(force_insert, force_update)

    
    # Retorna a soma das naturezas (moeda nacional) de um termo.
    @ property
    def real(self):
        total = Decimal('0.00')
        for ng in self.natureza_gasto_set.all():
            if ng.modalidade.moeda_nacional == True and ng.modalidade.sigla != 'REI':
                total += ng.valor_concedido
        return total


    # Formata o valor do atributo real.
    def termo_real(self):
        if self.real > 0:
            return '<b>R$ %s</b>' % (formata_moeda(self.real, ','))
        return '-'
    termo_real.allow_tags=True
    termo_real.short_description=_(u'Concessão  sem REI')


    # Retorna a soma das naturezas (dolar) de um termo.
    @ property
    def dolar(self):
        total = Decimal('0.00')
        for ng in self.natureza_gasto_set.all():
            if ng.modalidade.moeda_nacional == False:
                total += ng.valor_concedido
        return total


    # Formata o valor do atributo tdolar.
    def termo_dolar(self):
        if self.dolar > 0:
            return '$ %s' % (formata_moeda(self.dolar, '.'))
        return '-'
    termo_dolar.short_description=_(u'Concessão')


    @property
    def termino(self):
        termino = datetime.date.min

        for pedido in self.outorga_set.all():
            if pedido.termino > termino: termino = pedido.termino

        return termino

    # Duracao do termo como um 'timedelta'
    def duracao(self):
        return self.termino - self.inicio

    # Calcula os meses de duração do processo a partir dos dados do modelo Outorga
    def duracao_meses(self):
        dif = self.duracao()
        meses = (dif.days) / 30
        if (dif.days) % 30 >= 28:
            meses = meses + 1

	if meses > 0:
	    if meses > 1:
        	return "%s meses" % meses
            return "%s mês" % meses
	return '-'
    duracao_meses.short_description=_(u'Vigência')


    # Calcula total de despesas (R$) realizadas durante o termo.
    @ property
    def total_realizado_real_old(self):
        total = Decimal('0.00')
	for n in self.natureza_gasto_set.all():
	    if n.modalidade.moeda_nacional:
		total += n.total_realizado
        return total

    @property
    def total_realizado_real(self):
        from financeiro.models import Pagamento
        total = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=True, origem_fapesp__item_outorga__natureza_gasto__termo=self).aggregate(Sum('valor_fapesp'))
        return total['valor_fapesp__sum'] or Decimal('0.0')

    # Retorna o total de despesas (R$) em formato moeda.
    def formata_realizado_real(self):
        if not self.total_realizado_real:
            return '-'

        valor = formata_moeda(self.total_realizado_real, ',')
	if self.real < self.total_realizado_real:
            return '<span style="color: red"><b>R$ %s</b></span>' % valor

        return '<b>R$ %s</b>' % valor
    formata_realizado_real.allow_tags = True
    formata_realizado_real.short_description=_(u'Realizado')


    # Calcula total de despesas ($) realizadas durante o termo.
    @ property
    def total_realizado_dolar(self):
        total = Decimal('0.00')
	for n in self.natureza_gasto_set.all():
	    if not n.modalidade.moeda_nacional:
		total += n.total_realizado
        return total


    # Retorna o total de despesas ($) em formato moeda.
    def formata_realizado_dolar(self):
        if not self.total_realizado_dolar:
            return '-'

        valor = formata_moeda(self.total_realizado_dolar, '.')
        if self.dolar < self.total_realizado_dolar:
            return '<span style="color: red">$ %s</span>' % valor
        return '$ %s' % valor
    formata_realizado_dolar.allow_tags = True
    formata_realizado_dolar.short_description=_(u'Realizado')


    def saldo_real(self):
	return self.real - self.total_realizado_real

    def saldo_dolar(self):
	return self.dolar - self.total_realizado_dolar


    def formata_saldo_real(self):
	return '<b>R$ %s</b>' % formata_moeda(self.saldo_real(), ',')
    formata_saldo_real.allow_tags=True
    formata_saldo_real.short_description=_(u'Saldo')

    def formata_saldo_dolar(self):
        return '$ %s' % formata_moeda(self.saldo_dolar(), '.')
    formata_saldo_dolar.short_description=_(u'Saldo')

    # Define atributos.
    vigencia = property(duracao_meses)
    num_processo = property(__unicode__)


    # Retorna os termos que possuem fontes pagadoras não-fapesp sem registro de auditoriainterna.
    @classmethod
    def termos_auditoria_interna_em_aberto(cls, ai=None):
        from financeiro.models import FontePagadora

        termos = [fp.protocolo.termo.id for fp in FontePagadora.objects.filter((Q(origem_fapesp=None) & ~Q(origem_outras_verbas=None) & Q(auditoriainterna=None)) | Q(auditoriainterna=ai))]
        t = list(set(termos))
        return cls.objects.filter(id__in=t)


    # Retorna os termos que possuem fontes pagadoras fapesp sem registro de auditoriafapesp.
    @classmethod
    def termos_auditoria_fapesp_em_aberto(cls, af=None):
        from financeiro.models import FontePagadora

        termos = [fp.protocolo.termo.id for fp in FontePagadora.objects.filter((~Q(origem_fapesp=None) & Q(origem_outras_verbas=None) & Q(auditoriafapesp=None)) | Q(auditoriafapesp=af))]
        t = list(set(termos))
        return cls.objects.filter(id__in=t)


    # Define a descrição do modelo (singular e plural), a ordenação dos dados pelo ano.
    class Meta:
        verbose_name = _(u'Termo de Outorga')
        verbose_name_plural = _(u'Termos de Outorga')
        ordering = ("-ano", )

    @classmethod
    def termo_ativo(cls):
        hoje = datetime.datetime.now().date()
        for t in Termo.objects.order_by('-inicio'):
	    if t.inicio <= hoje and t.termino >= hoje:
		return t

        return None

class Categoria(models.Model):

    """
    Uma instância dessa classe representa um tipo de categoria de um pedido de concessão.

    O método '__unicode__'	Retorna o campo 'nome'.
    A class 'Meta'		Define a ordenação dos dados pelo nome.


    Cria Categoria
    >>> c, created = Categoria.objects.get_or_create(nome='Transposicao')
    
    >>> c.__unicode__()
    u'Transposicao'
    """


    nome = models.CharField(_(u'Nome'), max_length=60, help_text=_(u'ex. Aditivo'), unique=True)


    # Retorna o nome da Categoria
    def __unicode__(self):
        return u'%s' % self.nome


    # Define a ordenação dos dados pelo nome.
    class Meta:
        ordering = ('nome', )



class Outorga(models.Model):

    """
    Uma instância dessa classe representa um pedido de concessão.

    O método '__unicode__'		Retorna o termo e a categoria do pedido de concessão.
    O método 'inicio'			Retorna a data de início do termo.
    O método 'mostra_categoria'		Retorna o nome da categoria.
    O método 'mostra_termo'		Retorna o termo.
    O método 'existe_arquivo'		Retorna um ícone com link para consulta dos arquivos anexados.
    O atributo 'treal'			Retorna a soma de das naturezas de gasto com moeda nacional (Total Concedido em reais para o pedido de concessão).
    O método 'total_real'		Retorna o atributo 'treal' em formato moeda (R$).
    O atributo 'tdolar'			Retorna a soma das naturezas de gasto com moeda estrangeira (Total Concedido em dólares para o pedido de concessão).
    O métodoo 'total_dolar' 		Retorna o atributo 'tdolar' em formato moeda ($).
    A class 'Meta'			Define a descrição do modelo (singular e plural) e a ordenação dos dados pela data de solicitação.


    Cria Termo
    >>> e, created = Estado.objects.get_or_create(nome='Vigente')
    >>> t, create = Termo.objects.get_or_create(ano=2008, processo=22222, digito=2, defaults={'inicio': datetime.date(2008,1,1), 'estado'= e})


    Cria Outorga
    >>> c1, created = Categoria.objects.get_or_create(nome='Inicial')
    >>> o1, created = Outorga.objects.get_or_create(termo=t, categoria=c1, data_solicitacao=datetime.date(2007,12,1), defaults={'termino': datetime.date(2008,12,31), 'data_presta_contas': datetime.date(2008,2,28)})


    Cria Natureza de gasto
    >>> m1, created = Modalidade.objects.get_or_create(sigla='STB', defaults={'nome': 'Servicos de Terceiro no Brasil', 'moeda_nacional': True})
    >>> m2, created = Modalidade.objects.get_or_create(sigla='STE', defaults={'nome': 'Servicos de Terceiro no Exterior', 'moeda_nacional': False})

    >>> n1, created = Natureza_gasto.objects.get_or_create(modalidade=m1, outorga=o1)
    >>> n2, created = Natureza_gasto.objects.get_or_create(modalidade=m2, outorga=o1)


    Cria Item de Outorga
     from identificacao.models import Entidade, Contato, Identificacao

    >>> ent1, created = Entidade.objects.get_or_create(sigla='GTECH', defaults={'nome': 'Granero Tech', 'cnpj': '00.000.000/0000-00', 'ativo': False, 'fisco': True, 'url': ''})
    >>> ent2, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'SAC do Brasil', 'cnpj': '00.000.000/0000-00', 'ativo': True, 'fisco': True, 'url': ''})

    >>> i1, created = Item.objects.get_or_create(entidade=ent1, natureza_gasto=n1, descricao='Armazenagem', defaults={'justificativa': 'Armazenagem de equipamentos', 'quantidade': 12, 'valor_unit': 2500})
    >>> i2, created = Item.objects.get_or_create(entidade=ent2, natureza_gasto=n2, descricao='Serviço de Conexão Internacional', defaults={'justificativa': 'Link Internacional', 'quantidade': 12, 'valor_unit': 250000})


    >>> o1.__unicode__()
    '08/22222-2 - Inicial'

    >>> o1.inicio()
    '01/01/2008'

    >>>.o1.mostra_categoria()
    'Inicio'

    >>> o1.mostra_termo()
    '08/22222-2'

    >>> o1.existe_arquivo()
    ' '

    >>> o1.treal
    Decimal('2500')

    >>> o1.total_real()
    'R$ 2500,00'

    >>> o1.tdolar
    Decimal('250000')

    >>> o1.total_dolar()
    '$ 250,000.00'
    """


    categoria = models.ForeignKey('outorga.Categoria', verbose_name=_(u'Categoria'))
    termo = models.ForeignKey('outorga.Termo', verbose_name=_(u'Termo'))
    termino = NARADateField(_(u'Término'), help_text=_(u'Término da vigência do processo'))
    obs = models.TextField(_(u'Observação'), blank=True)
    data_solicitacao = NARADateField(_(u'Data de solicitação'), blank=True, null=True, help_text=_(u'Data de início desta outorga, caso não seja inicial. Um aditivo, por exemplo.'))
    data_presta_contas = NARADateField(_(u'Prest. Contas'), blank=True, null=True, help_text=_(u'Data de Prestação de Contas'))
    data_solicitacao = NARADateField(_(u'Solicitação'), help_text=_(u'Data de Solicitação do Pedido de Concessão'))
    arquivo = models.FileField(upload_to=upload_dir, null=True, blank=True)
    protocolo = models.FileField(upload_to=upload_dir, null=True, blank=True)

    # Retorna o termo e a categoria.
    def __unicode__(self):
        return u'%s - %s' % (self.termo.num_processo, self.categoria.nome)


    # Início do processo
    @ property
    def inicio(self):
        return self.termo.inicio.strftime("%d/%m/%Y")
    #inicio.short_description = _(u'Início')


    # Retorna a categoria.
    def mostra_categoria(self):
        return self.categoria.nome
    mostra_categoria.short_description = _(u'Categoria')


    # Retorna o termo.
    def mostra_termo(self):
        return self.termo.num_processo
    mostra_termo.short_description = _(u'Termo')


    # Retorna um ícone se o pedido de concessão tiver arquivos.
    def existe_arquivo(self):
        a = '<center><a href="/admin/outorga/arquivo/?outorga__id__exact=%s"><img src="/media/img/arquivo.png" /></a></center>' % self.id
        if self.arquivo_set.count() > 0:
            return a
        return ' '
    existe_arquivo.allow_tags = True
    existe_arquivo.short_description = _(u'Arquivo')


    ## Salva o novo pedido com as infomações do pedido anterior.
    #def save(self, force_insert=False, force_update=False):
        #pk = self.pk
        #try:
            #antigo = Outorga.objects.get(pk=pk)
        #except Outorga.DoesNotExist:
            #antigo = None

        #super(Outorga, self).save(force_insert, force_update)
        #ant = self.anterior
        #if ant and not pk:
            #for ng in ant.natureza_gasto_set.all():
                #ngc = copy.copy(ng)
                #ngc.outorga = self
                #ngc.id = None
                #ngc.save(force_insert=True, force_update=False)
                #for i in ng.item_set.all():
                    #ic = copy.copy(i)
                    #ic.natureza_gasto = ngc
                    #ic.id = None
                    #ic.save(force_insert=True, force_update=False)

        #elif self.estado.nome == u'Aprovado' and antigo and antigo.estado.nome != u'Aprovado':
            #for item in Item.objects.filter(natureza_gasto__outorga=self).iterator():
                #item.estado = self.estado
                #item.save()


    # Define a descrição do modelo e a ordenação dos dados pelo termo.
    class Meta:
        verbose_name = _(u'Concessão')
        verbose_name_plural = _(u'Histórico de Concessões')
        ordering = ('data_solicitacao', )



class Natureza_gasto(models.Model):

    """
    Uma instância dessa classe representa a conexão de uma modalidade a um pedido de concessão.

    O método '__unidode__'		Retorna o termo, a categoria do pedido de concessão e o nome da modalidade.
    O método 'mostra_termo'		Retorna o termo.
    O método 'mostra_modalidade'	Retorna o nome da modalidade.
    O método 'get_absolute_url'		Retorna a URL de uma natureza de gasto.
    O método 'formata_valor'		Retorna um valor em formato moeda conforme a moeda especificada no modelo Modalidade.
    O atributo 'total_realizado'	Retorna o total das despesas realizadas associadas a uma modalidade e termo.
    O método 'formata_total_realizado'	Retorna o atributo 'total_realizado' em formato moeda.
    O método 'soma_itens'		Retorna a soma dos itens da natureza de gasto de um pedido de concessão e marca em vermelho se for diferente do 
					valor_concedido.
    O método 'todos_itens'		Retorna os itens que não estão subordinados a outro item, considerando todos os pedidos de uma determinada
					modalidade e termo.
    O método 'soma_geral'		Retorna a soma das naturezas de gasto de uma determinada modalidade e termo.
    O método 'formata_soma_geral'	Retorna o valor do método 'soma_geral' em formato moeda.
    O método 'v_concedido' 		Retorna o valor do campo 'valor_concedido' em formato de moeda e marca em vermelho se o valor concedido for 
					diferente do total dos itens.
    A class 'Meta' 			Define a descrição do modelo (singular e plural) e a ordem de apresentação dos dados pela data de solicitação
					do pedido de concessão.

    Cria Termo
    >>> e, created = Estado.objects.get_or_create(nome='Vigente')
    >>> t, create = Termo.objects.get_or_create(ano=2008, processo=22222, digito=2, defaults={'inicio': datetime.date(2008,1,1), 'estado'= e})


    Cria Outorga
    >>> c1, created = Categoria.objects.get_or_create(nome='Inicial')
    >>> c2, created = Categoria.objects.get_or_create(nome='Aditivo')

    >>> o1, created = Outorga.objects.get_or_create(termo=t, categoria=c1, data_solicitacao=datetime.date(2007,12,1), defaults={'termino': datetime.date(2008,12,31), 'data_presta_contas': datetime.date(2008,2,28)})
    >>> o2, created = Outorga.objects.get_or_create(termo=t, categoria=c2, data_solicitacao=datetime.date(2008,4,1), defaults={'termino': datetime.date(2008,12,31), 'data_presta_contas': datetime.date(2008,2,28)})


    Cria Natureza de gasto
    >>> m1, created = Modalidade.objects.get_or_create(sigla='STB', defaults={'nome': 'Servicos de Terceiro no Brasil', 'moeda_nacional': True})

    >>> n1, created = Natureza_gasto.objects.get_or_create(modalidade=m1, outorga=o1, valor_concedido=Decimal('30000'))
    >>> n2, created = Natureza_gasto.objects.get_or_create(modalidade=m1, outorga=o2, valor_concedido=Decimal('1000000'))


    Cria Item de Outorga
     from identificacao.models import Entidade, Contato, Identificacao

    >>> ent1, created = Entidade.objects.get_or_create(sigla='GTECH', defaults={'nome': 'Granero Tech', 'cnpj': '00.000.000/0000-00', 'ativo': False, 'fisco': True, 'url': ''})
    >>> ent2, created = Entidade.objects.get_or_create(sigla='TERREMARK', defaults={'nome': 'Terremark do Brasil', 'cnpj': '00.000.000/0000-00', 'ativo': True, 'fisco': True, 'url': ''})

    >>> i1, created = Item.objects.get_or_create(entidade=ent1, natureza_gasto=n1, descricao='Armazenagem', defaults={'justificativa': 'Armazenagem de equipamentos', 'quantidade': 12, 'valor_unit': 2500})
    >>> i2, created = Item.objects.get_or_create(entidade=ent2, natureza_gasto=n2, descricao='Servico de Conexao', defaults={'justificativa': 'Ligação SP-CPS', 'quantidade': 12, 'valor_unit': 100000})


    Cria Protocolo
     from protocolo.models import Protocolo, ItemProtocolo, TipoDocumento, Origem, Estado as EstadoProtocolo

    >>> ep, created = EstadoProtocolo.objects.get_or_create(nome='Aprovado')
    >>> td, created = TipoDocumento.objects.get_or_create(nome='Nota Fiscal')
    >>> og, created = Origem.objects.get_or_create(nome='Motoboy')

    >>> cot1, created = Contato.objects.get_or_create(nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})
    >>> cot2, created = Contato.objects.get_or_create(nome='Marcos', defaults={'email': 'alex@alex.com.br', 'tel': ''})

    >>> iden1, created = Identificacao.objects.get_or_create(entidade=ent1, contato=cot1, defaults={'funcao': 'Tecnico', 'area': 'Estoque', 'ativo': True})
    >>> iden2, created = Identificacao.objects.get_or_create(entidade=ent2, contato=cot2, defaults={'funcao': 'Diretor', 'area': 'Redes', 'ativo': True})

    >>> p1, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden1, tipo_documento=td, data_chegada=datetime.datetime(2008,9,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 8888, 'data_vencimento': datetime.date(2008,10,5), 'descricao': 'Conta mensal - armazenagem 09/2008', 'valor_total': None})
    >>> p2, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden2, tipo_documento=td, data_chegada=datetime.datetime(2008,9,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 5555, 'data_vencimento': datetime.date(2008,10,15), 'descricao': 'Serviço de Conexão Local - 09/2009', 'valor_total': None})


    Cria Item do Protocolo
    >>> ip1 = ItemProtocolo.objects.get_or_create(protocolo=p1, descricao='Tarifa mensal - 09/2009', quantidade=1, valor_unitario=2500)
    >>> ip2 = ItemProtocolo.objects.get_or_create(protocolo=p1, descricao='Reajuste tarifa mensal - 09/2009', quantidade=1, valor_unitario=150)
    >>> ip3 = ItemProtocolo.objects.get_or_create(protocolo=p2, descricao='Conexão Local - 09/2009', quantidade=1, valor_unitario=85000)
    >>> ip4 = ItemProtocolo.objects.get_or_create(protocolo=p2, descricao='Reajuste do serviço de Conexão Local - 09/2009', quantidade=1, valor_unitario=15000)


    Criar Fonte Pagadora
     from financeiro.models import OrigemOutrasVerbas, FontePagadora, OrigemFapesp, ExtratoCC, Estato as EstadoFinanceiro

    >>> ef1, created = EstadoFinanceiro.objects.get_or_create(nome='Aprovado')
    >>> ef2, created = EstadoFinanceiro.objects.get_or_create(nome='Concluído')

    >>> ex1, created = ExtratoCC.objects.get_or_create(data_extrato=datetime.date(2008,10,30), data_oper=datetime.date(2008,10,5), cod_oper=333333, valor='2650', historico='TED')
    >>> ex2, created = ExtratoCC.objects.get_or_create(data_extrato=datetime.date(2008,10,30), data_oper=datetime.date(2008,10,15), cod_oper=5555, valor='100000', historico='TED')

    >>> a1, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e GTech')
    >>> a2, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e Terremark')

    >>> of1, created = OrigemFapesp.objects.get_or_create(acordo=a1, item_outorga=i1)
    >>> of2, created = OrigemFapesp.objects.get_or_create(acordo=a2, item_outorga=i2)

    >>> fp1 = FontePagadora.objects.get_or_create(protocolo=p1, extrato=ex1, origem_fapesp=of1, estado=ef2, valor='2650')
    >>> fp2 = FontePagadora.objects.get_or_create(protocolo=p2, extrato=ex2, origem_fapesp=of2, estado=ef2, valor='100000')


    >>> n1.__unicode__()
    '08/22222-2_Inicial - STB'

    >>> n1.mostra_termo()
    '08/22222-2'

    >>> n1.mostra_modalidade()
    'STB'

    >>> n1.get_absolute_url()
    '/admin/outorga/natureza_gasto/8'

    >>> n1.formata_valor(i3.valor)
    'R$ 1.200.000,00'

    >>> n1.total_realizado
    Decimal('102650')

    >>> n1.formata_total_realizado()
    'R$ 102.650,00'

    >>> n1.soma_itens()
    'R$ 30.000,00'

    >>> n2.soma_itens()
    '<span style="color: red">R$ 1.200.000,00</span>'

    >>> n1.todos_itens()
    [<Item: 08/22222-2_STB - Armazenagem>, <Item: 08/22222-2_STB - Servico de conexao>]

    >>> n1.soma_geral()
    Decimal('1230000')
 
    >>> n1.formata_soma_geral()
    'R$ 1.230.000,00'

    >>> n1.v_concedido()
    'R$ 30.000,00'
    """


    modalidade = models.ForeignKey('outorga.Modalidade', verbose_name=_(u'Modalidade'))
    termo = models.ForeignKey('outorga.Termo', verbose_name=_(u'Termo de outorga'))
    valor_concedido =  models.DecimalField(_(u'Valor Concedido'), max_digits=12, decimal_places=2, help_text=_(u'ex. 150500.50'))
    obs = models.TextField(_(u'Observação'), blank=True)


    # Retorna o pedido de concessão e a sigla da modalidade.
    def __unicode__(self):
        return u'%s - %s' % (self.mostra_termo(), self.modalidade.sigla)


    # Retorna o Termo do pedido de concessão.
    def mostra_termo(self):
        return '%s' % self.termo.num_processo
    mostra_termo.short_description = _(u'Termo')


    # Retorna a modalidade da Natureza do Gasto.
    def mostra_modalidade(self):
        return u'%s' % self.modalidade.sigla
    mostra_modalidade.short_description = _(u'Modalidade')


    # Retorna a URL de uma natureza de gasto.
    def get_absolute_url(self):
        return '/admin/outorga/natureza_gasto/%s' % self.id


    # Formata um valor em formato moeda conforme campo 'moeda_nacional' do modelo 'Modalidade'.
    def formata_valor(self, v):
        if self.modalidade.moeda_nacional == True:
            moeda = 'R$'
            sep_decimal = ','
        else:
            moeda = '$'
            sep_decimal = '.'
        return moeda + ' ' + formata_moeda(v, sep_decimal)


    # Calcula o total de despesas realizadas de uma modalidade e termo.
    @ property
    def total_realizado(self):
        total = Decimal('0.00')
        for item in self.todos_itens():
            total += item.valor_realizado_acumulado
        return total


    # Retorna o total de despesas realizadas em formato moeda.
    def formata_total_realizado(self):
       if not self.total_realizado:
           return '-'

       if self.valor_concedido < self.total_realizado  :
            return '<span style="color: red">%s</span>' % self.formata_valor(self.total_realizado)
       return self.formata_valor(self.total_realizado)
    formata_total_realizado.allow_tags = True
    formata_total_realizado.short_description=_(u'Total Realizado')

        
    # Calcula a soma de todos os itens da natureza do gasto e marca em vermelho se o valor for diferente do valor_concedido.
    def soma_itens(self):
        total = Decimal('0.00')
        for item in self.item_set.all():
            total += item.valor

        if self.valor_concedido != total != 0:
            return '<span style="color: red">%s</span>' % (self.formata_valor(total))

        if total != 0:
            return self.formata_valor(total)
	return '-'
    soma_itens.allow_tags = True
    soma_itens.short_description=_(u'Total dos Itens')


    # Retorna todos os itens de uma natureza de gasto que não estão subordinados a outro item, considerando todas as concessões de um determinado Termo.
    def todos_itens(self):
        return Item.objects.filter(natureza_gasto__modalidade=self.modalidade,
                                   natureza_gasto__termo=self.termo)


    # Retorna a soma do valor total de todos os itens de uma modalidade considerando todas as concessões de um Termo.
    def soma_geral(self):
        total = Decimal('0.00')
        for item in self.todos_itens():
            total += item.valor_total()
        return total


    # Retorna a soma do valor total concedido considerando todas as naturezas de gasto de uma modalidade e Termo.
    def total_concedido_mod_termo(self):
        total = Decimal('0.00')
        for ng in Natureza_gasto.objects.filter(modalidade=self.modalidade, termo=self.termo):
            total += ng.valor_concedido
        return self.formata_valor(total)
    total_concedido_mod_termo.short_description=_(u'Total concedido para a Modalidade')


    # Retorna a soma geral em formato de moeda.
    def formata_soma_geral(self):
        return self.formata_valor(self.soma_geral())


    # Formata o valor do atributo 'valor_concedido'
    def v_concedido(self):
        if self.valor_concedido or self.valor_concedido==0:
            return self.formata_valor(self.valor_concedido)
        return '-'
    v_concedido.short_description=_(u'Valor Concedido')


    def saldo(self):
        if self.total_realizado > self.valor_concedido:
            return '<span style="color: red">%s</span>' % self.formata_valor(self.valor_concedido - self.total_realizado)
        return self.formata_valor(self.valor_concedido - self.total_realizado)
    saldo.allow_tags = True
	
    # Define a descrição e a ordenação dos dados pelo Termo de Outorga.
    class Meta:
        verbose_name = _(u'Pasta')
        verbose_name_plural = _(u'Pastas')
	ordering = ('-termo__ano', )
        #ordering = ('-outorga__data_solicitacao', )



class Item(models.Model):

    """
    Uma instância dessa classe representa um item de um pedido de concessão.

    O método '__unicode__'			Retorna a descrição do item.
    O método 'mostra_termo'			Retorna o termo.
    O método 'mostra_descricao'			Retorna a descrição do item.
    O método 'mostra_concessao'			Retorna a categoria do pedido de concessão.
    O método 'mostra_modalidade'		Retorna a sigla da modalidade.
    O método 'mostra_solicitação'		Retorna a data de solicitação do pedido de concessão no formato dd/mm/aa.
    O método 'mostra_termino'			Retorna a data de término do pedido de concessão no formato dd/mm/aa.
    O atributo 'valor' 				Calcula o valor total do item (quantidade * valor unitário). 
    O método 'mostra_valor'			Retorna o atributo 'valor' em formato moeda.
    O método 'mostra_valor_unit'		Retorna o campo 'valor_unit' em formato moeda.
    O método 'mostra_quantidade'		Retorna o campo 'quantidade'.
    O método 'mostra_valor_total'		Retorna o atributo o valor total em formato moeda.
    O método 'valor_total'			Retorna a soma dos itens conectados entre si.
    O método 'calcula_total_despesas'		Retorna a soma das fontespagadoras 'fapesp' referentes a um item.
    O atributo 'valor_realizado_acumulado' 	Foi definido para retornar o método 'calcula_total_despesa'.
    O método 'mostra_valor_realizado'		Retorna o atributo 'valor_realizado_acumulado' em formato moeda.
    A class 'Meta'				Define a descrição do modelo (singular e plural) e a ordenação dos dados pela data de solicitação 
						do pedido de concessão.

    Cria Termo
    >>> e, created = Estado.objects.get_or_create(nome='Vigente')
    >>> t, create = Termo.objects.get_or_create(ano=2008, processo=22222, digito=2, defaults={'inicio': datetime.date(2008,1,1), 'estado'= e})


    Cria Outorga
    >>> c1, created = Categoria.objects.get_or_create(nome='Inicial')
    >>> c2, created = Categoria.objects.get_or_create(nome='Aditivo')

    >>> o1, created = Outorga.objects.get_or_create(termo=t, categoria=c1, data_solicitacao=datetime.date(2007,12,1), defaults={'termino': datetime.date(2008,12,31), 'data_presta_contas': datetime.date(2008,2,28)})
    >>> o2, created = Outorga.objects.get_or_create(termo=t, categoria=c2, data_solicitacao=datetime.date(2008,4,1), defaults={'termino': datetime.date(2008,12,31), 'data_presta_contas': datetime.date(2008,2,28)})


    Cria Natureza de gasto
    >>> m1, created = Modalidade.objects.get_or_create(sigla='STE', defaults={'nome': 'Servicos de Terceiro no Exterior', 'moeda_nacional': False})

    >>> n1, created = Natureza_gasto.objects.get_or_create(modalidade=m1, outorga=o1)
    >>> n2, created = Natureza_gasto.objects.get_or_create(modalidade=m1, outorga=o2)


    Cria Item de Outorga
     from identificacao.models import Entidade, Contato, Identificacao

    >>> ent1, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'SAC do Brasil', 'cnpj': '00.000.000/0000-00', 'ativo': True, 'fisco': True, 'url': ''})

    >>> i1, created = Item.objects.get_or_create(entidade=ent1, natureza_gasto=n1, descricao='Serviço de Conexão Internacional', defaults={'justificativa': 'Link Internacional', 'quantidade': 12, 'valor_unit': 250000})
    >>> i2, created = Item.objects.get_or_create(entidade=ent1, natureza_gasto=n2, descricao='Serviço de Conexão Internacional', defaults={'justificativa': 'Ajuste na cobrança do Link Internacional', 'quantidade': 6, 'valor_unit': 50000, 'item: i2})


    Cria Protocolo
    from protocolo.models import Protocolo, ItemProtocolo, TipoDocumento, Origem, Estado as EstadoProtocolo

    >>> ep, created = EstadoProtocolo.objects.get_or_create(nome='Aprovado')
    >>> td, created = TipoDocumento.objects.get_or_create(nome='Nota Fiscal')
    >>> og, created = Origem.objects.get_or_create(nome='Motoboy')

    >>> cot1, created = Contato.objects.get_or_create(nome='Alex', defaults={'email': 'alex@alex.com.br', 'tel': ''})

    >>> iden1, created = Identificacao.objects.get_or_create(entidade=ent1, contato=cot1, defaults={'funcao': 'Gerente', 'area': 'Redes', 'ativo': True})

    >>> p1, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden1, tipo_documento=td, data_chegada=datetime.datetime(2008,9,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 7777, 'data_vencimento': datetime.date(2008,10,10), 'descricao': 'Serviço de Conexão Internacional - 09/2009', 'valor_total': None})
    >>> p2, created = Protocolo.objects.get_or_create(termo=t, identificacao=iden1, tipo_documento=td, data_chegada=datetime.datetime(2008,10,30,10,10), defaults={'origem': og, 'estado': ep, 'num_documento': 5555, 'data_vencimento': datetime.date(2008,11,10), 'descricao': 'Serviço de Conexão Internacional - 10/2009', 'valor_total': None})


    Cria Item do Protocolo
    >>> ip1 = ItemProtocolo.objects.get_or_create(protocolo=p1, descricao='Conexão Internacional - 09/2009', quantidade=1, valor_unitario=250000)
    >>> ip2 = ItemProtocolo.objects.get_or_create(protocolo=p1, descricao='Reajuste do serviço de Conexão Internacional - 09/2009', quantidade=1, valor_unitario=50000)
    >>> ip3 = ItemProtocolo.objects.get_or_create(protocolo=p2, descricao='Conexão Internacional - 10/2009', quantidade=1, valor_unitario=250000)
    >>> ip4 = ItemProtocolo.objects.get_or_create(protocolo=p2, descricao='Reajuste do serviço de Conexão Internacional - 10/2009', quantidade=1, valor_unitario=50000)


    Criar Fonte Pagadora
     from financeiro.models import OrigemOutrasVerbas, FontePagadora, OrigemFapesp, ExtratoCC, Estato as EstadoFinanceiro

    >>> ef1, created = EstadoFinanceiro.objects.get_or_create(nome='Aprovado')
    >>> ef2, created = EstadoFinanceiro.objects.get_or_create(nome='Concluído')

    >>> ex1, created = ExtratoCC.objects.get_or_create(data_extrato=datetime.date(2008,10,30), data_oper=datetime.date(2008,10,10), cod_oper=333333, valor='300000', historico='TED')
    >>> ex2, created = ExtratoCC.objects.get_or_create(data_extrato=datetime.date(2008,11,30), data_oper=datetime.date(2008,11,10), cod_oper=444444, valor='300000', historico='TED')

    >>> a1, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')

    >>> of1, created = OrigemFapesp.objects.get_or_create(acordo=a1, item_outorga=i1)

    >>> fp1 = FontePagadora.objects.get_or_create(protocolo=p1, extrato=ex1, origem_fapesp=of1, estado=ef2, valor='300000')
    >>> fp2 = FontePagadora.objects.get_or_create(protocolo=p2, extrato=ex2, origem_fapesp=of1, estado=ef2, valor='300000')


    >>> i1.__unicode__()
    'Serviço de Conexão Internacional'

    >>> i1.mostra_termo()
    '08/22222-2'

    >>> i1.mostra_descricao()
    'Serviço de Conexão Internacional'

    >>> i1.mostra_concessao()
    'Inicial'

    >>> i1.mostra_modalidade()
    'STE'

    >>> i1.mostra_solicitacao()
    '01/12/07'

    >>> i1.mostra_termino()
    '31/12/08'

    >>> i1.valor
    Decimal('3000000')

    >>> i1.mostra_valor()
    '$ 3,000,000.00'

    >>> i1.mostra_valor_unit()
    '$ 250,000.00'

    >>> i1.mostra_quantidade()
    12

    >>> i1.valor_total()
    Decimal('3600000')

    >>> i1.mostra_valor_total()
    '$ 3,600,000.00'

    >>> i1.calcula_total_despesas()
    Decimal('600000')

    >>> i1.valor_realizado_acumulado
    Decimal('600000')

    >>> i1.mostra_valor_realizado()
    '$ 600,000.00'
    """


    entidade = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Entidade'), null=True)
    natureza_gasto = models.ForeignKey('outorga.Natureza_gasto', verbose_name=_(u'Pasta'))
    descricao = models.CharField(_(u'Descrição'), max_length=255, help_text=_(u'ex. Locação e armazenamento especializado na Granero Tech.'))
    justificativa = models.TextField(_(u'Justificativa'))
    quantidade = models.IntegerField(_(u'Quantidade'))
    obs = models.TextField(_(u'Observação'), blank=True)
    valor = models.DecimalField(_(u'Valor Concedido'), max_digits=12, decimal_places=2, help_text=_(u'ex. 150500.50'))

    # Retorna a descrição e o termo, se existir.
    def __unicode__(self):
        return u'%s' % (self.descricao)


    # Retorna o Termo se o pedido de concessão estiver conectado a um termo.
    def mostra_termo(self):
        return '%s' % self.natureza_gasto.mostra_termo()
    mostra_termo.short_description = _(u'Termo')


    # Retorna a descrição do item do pedido de concessão.
    def mostra_descricao(self):
        return u'%s' % self.descricao
    mostra_descricao.short_description = _(u'Descrição')


    # Retorna a modalidade do Item do Pedido de Concessão.
    def mostra_modalidade(self):
        return u'%s' % self.natureza_gasto.modalidade.sigla
    mostra_modalidade.short_description = _(u'Mod')


    # Retorna a quantidade.
    def mostra_quantidade(self):
        if self.quantidade > 0:
            return self.quantidade
        return '-'
    mostra_quantidade.short_description=_(u'Qtde')


    # Calcula o valor total realizado de um determinado item.
    def calcula_total_despesas(self):
       
        total = Decimal('0.00')
        if hasattr(self, 'origemfapesp_set'):
	    for of in self.origemfapesp_set.all():
    		for fp in of.pagamento_set.all():
		    #if fp.extrato:
		       total += fp.valor_fapesp
        return total


    # Define um atributo com o valor total realizado
    valor_realizado_acumulado = property(calcula_total_despesas)


    # Valor realizado por mês
    def calcula_realizado_mes(self, dt, after=False):
        total = Decimal('0.00')
        if hasattr(self, 'origemfapesp_set'):
	    for of in self.origemfapesp_set.all():
	        if after:
		    if self.natureza_gasto.modalidade.moeda_nacional:
   		        pgs = of.pagamento_set.filter(conta_corrente__data_oper__gte=dt)
                    else:
			pgs = of.pagamento_set.filter(protocolo__data_vencimento__gte=dt)
		else:
                    if self.natureza_gasto.modalidade.moeda_nacional:
    		        pgs = of.pagamento_set.filter(conta_corrente__data_oper__month=dt.strftime('%m'), conta_corrente__data_oper__year=dt.strftime('%Y'))
                    else:
                        pgs = of.pagamento_set.filter(protocolo__data_vencimento__month=dt.strftime('%m'), protocolo__data_vencimento__year=dt.strftime('%Y'))
		for fp in pgs:
		       total += fp.valor_fapesp
        return total

    # Mostra o valor realizado acumulado formatado conforme a moeda da modalidade
    def mostra_valor_realizado(self):
        if not self.valor_realizado_acumulado:
            return '-'

        total = self.natureza_gasto.formata_valor(self.valor_realizado_acumulado)
	#if self.valor_realizado_acumulado > self.valor:
        #    return '<span style="color: red">%s</span>' % (total)
	return total
    mostra_valor_realizado.allow_tags = True
    mostra_valor_realizado.short_description=_(u'Total Realizado')

    def saldo(self):
        return self.valor - self.valor_realizado_acumulado

    # Pagina com todos os protocolos ligados a este item
    def protocolos_pagina(self):
        return '<a href="/protocolo/protocolo/?fontepagadora__origem_fapesp__item_outorga__id=%s">Despesas</a>' % self.id
    protocolos_pagina.short_description = _(u'Lista de despesas')
    protocolos_pagina.allow_tags = True

    def pagamentos_pagina(self):
    	return '<a href="/financeiro/pagamento/?origem_fapesp__item_outorga=%s">Despesas</a>' % self.id
    pagamentos_pagina.short_description = _(u'Lista de pagamentos')
    pagamentos_pagina.allow_tags = True

    # Define a descrição (singular e plural) e a ordenação pela data de solicitação do pedido de concessão.
    class Meta:
        verbose_name = _(u'Item do Orçamento')
        verbose_name_plural = _(u'Itens do Orçamento')
        ordering = ('-natureza_gasto__termo__ano', 'descricao')



class Arquivo(models.Model):

    """
    Uma instância dessa classe representa um arquivo de um pedido de concessão.

    O método '__unicode__'	Retorna o nome do arquivo.
    O método 'concessao'	Retorna o método '__unicode__' do modelo Outorga.
    A class 'Meta'		Define a ordenação dos dados pelo 'id' e a unicidade dos dados pelos campos 'arquivo' e 'outorga'.
    """


    arquivo = models.FileField(upload_to=upload_dir)
    outorga = models.ForeignKey('outorga.Outorga', related_name='arquivos')


    # Retorna o nome do arquivo.
    def __unicode__(self):
        if self.arquivo.name.find('/') == -1:
            return u'%s' % self.arquivo.name
        else:
            return u'%s' % self.arquivo.name.split('/')[-1]


    # Retorna o pedido de concessão.
    def concessao(self):
        return self.outorga
    concessao.short_description = _(u'Pedido de Concessão')


    # Retorna o termo do pedido de concessão.
    def mostra_termo(self):
        return self.outorga.mostra_termo()
    mostra_termo.short_description = _(u'Termo')
    

    # Define a ordenação dos dados e a unicidade dos dados.
    class Meta:
        ordering = ('id', )
        unique_together = ('arquivo', 'outorga')



class Acordo(models.Model):

      """
      Acordos como, por exemplo, entre a ANSP e a Telefônica.

      O método '__unicode__'	Retorna a descrição do acordo.

      >>> a, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')

      >>> a.__unicode__()
      'Acordo entre Instituto UNIEMP e SAC'

      """

      estado = models.ForeignKey('outorga.Estado')
      descricao = models.TextField(verbose_name=_(u'Descrição'))
      itens_outorga = models.ManyToManyField('outorga.Item', through='outorga.OrigemFapesp')


      # Retorna a descrição.
      def __unicode__(self):
	  return u"%s" % self.descricao

      class Meta:
      	  ordering = ('descricao',)

class OrigemFapesp(models.Model):
      """
      Uma instância dessa classe representa a associação de uma acordo a um item da Outorga


      Cria Termo
      >>> e, created = Estado.objects.get_or_create(nome='Vigente')
      >>> t, create = Termo.objects.get_or_create(ano=2008, processo=22222, digito=2, defaults={'inicio': datetime.date(2008,1,1), 'estado'= e})


      Cria Outorga
      >>> c1, created = Categoria.objects.get_or_create(nome='Inicial')
      >>> c2, created = Categoria.objects.get_or_create(nome='Aditivo')

      >>> o1, created = Outorga.objects.get_or_create(termo=t, categoria=c1, data_solicitacao=datetime.date(2007,12,1), defaults={'termino': datetime.date(2008,12,31), 'data_presta_contas': datetime.date(2008,2,28)})
      >>> o2, created = Outorga.objects.get_or_create(termo=t, categoria=c2, data_solicitacao=datetime.date(2008,4,1), defaults={'termino': datetime.date(2008,12,31), 'data_presta_contas': datetime.date(2008,2,28)})


      Cria Natureza de gasto
      >>> m1, created = Modalidade.objects.get_or_create(sigla='STE', defaults={'nome': 'Servicos de Terceiro no Exterior', 'moeda_nacional': False})

      >>> n1, created = Natureza_gasto.objects.get_or_create(modalidade=m1, outorga=o1)
      >>> n2, created = Natureza_gasto.objects.get_or_create(modalidade=m1, outorga=o2)


      Cria Item de Outorga
       from identificacao.models import Entidade, Contato, Identificacao

      >>> ent1, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'SAC do Brasil', 'cnpj': '00.000.000/0000-00', 'ativo': True, 'fisco': True, 'url': ''})

      >>> i1, created = Item.objects.get_or_create(entidade=ent1, natureza_gasto=n1, descricao='Serviço de Conexão Internacional', defaults={'justificativa': 'Link Internacional', 'quantidade': 12, 'valor_unit': 250000})
      >>> i2, created = Item.objects.get_or_create(entidade=ent1, natureza_gasto=n2, descricao='Serviço de Conexão Internacional', defaults={'justificativa': 'Ajuste na cobrança do Link Internacional', 'quantidade': 6, 'valor_unit': 50000, 'item: i2})

      >>> a, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')

      >>> of, created = OrigemFapesp.objects.get_or_create(acordo=a, item_outorga=i1)


      >>> of.__unicode__()
      'Acordo entre Instituto UNIEMP e SAC - Serviço de Conexão Internacional'

      """

      acordo = models.ForeignKey('outorga.Acordo')
      item_outorga = models.ForeignKey('outorga.Item', verbose_name=_(u'Item de Outorga'))


      # Retorna o acordo e o item de Outorga da Origem FAPESP.
      def __unicode__(self):
	  return u"%s - %s" % (self.acordo, self.item_outorga)


      # Define a descrição do modelo.
      class Meta:
          verbose_name = _(u'Origem FAPESP')
          verbose_name_plural = _(u'Origem FAPESP')
	  ordering = ('item_outorga',)

      def gasto(self):
          g = self.pagamento_set.all().aggregate(Sum('valor_fapesp'))
	  return g['valor_fapesp__sum'] or Decimal('0.0')


class Contrato(models.Model):

      """
      Uma instância dessa classe representa um contrato. (Ex. Instituto Uniemp e Telefônica)


      Cria um Contrato
       from identificacao.models import Entidade, Contato, Identificacao

      >>> ent, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'SAC do Brasil', 'cnpj': '00.000.000/0000-00', 'ativo': True, 'fisco': True, 'url': ''})

      >>> ct, created = Contrato.objects.get_or_create(data_inicio=datetime.date(2008,1,1), auto_renova=True, limite_rescisao=datetime.date(2008,1,11), entidade=ent)

      >>> ct.__unicode__()
      'SAC - 01/01/2008'

      >>> ct.existe_arquivo()
      ' '
      """

      numero = models.CharField(_(u'Número'), max_length=20)
      descricao = models.TextField(_(u'Descrição'), blank=True)
      data_inicio = NARADateField(_(u'Início'))
      auto_renova = models.BooleanField(_(u'Auto renovação?'))
      limite_rescisao = NARADateField(_(u'término'), null=True, blank=True)
      entidade = models.ForeignKey('identificacao.Entidade')
      anterior = models.ForeignKey('outorga.Contrato', verbose_name=_('Contrato anterior'), null=True, blank=True)
      arquivo = models.FileField(upload_to='contrato')


      # Retorna a entidade e a data de ínicio do Contrato.
      def __unicode__(self):
	  inicio = self.data_inicio.strftime("%d/%m/%Y")
	  if self.entidade:
	      return u"%s - %s" % (self.entidade, inicio)
	  else:
	      return inicio


      # Retorna um ícone se o contrato tiver anexo.
      def existe_arquivo(self):
          a = '<center><a href="/site-media/contrato/%s"><img src="/media/img/arquivo.png" /></a></center>'
          if self.arquivo:
              aq = str(self.arquivo).split('/')[1]
              return '<center>%s</center>' % (a % aq)
          return ' '
      existe_arquivo.allow_tags = True
      existe_arquivo.short_description = _(u'Arquivo')


class TipoContrato(models.Model):
      nome = models.CharField(max_length=30)

      def __unicode__(self):
      	  return self.nome

      class Meta:
      	  verbose_name = u'Tipo de documento'
	  verbose_name_plural = u'Tipos de documento'
          ordering = ('nome',)

class OrdemDeServico(models.Model):

      """
      Uma instância dessa classe representa uma ordem de serviço de um Contrato.

    
      Cria um Contrato
       from identificacao.models import Entidade, Contato, Identificacao

      >>> ent, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'SAC do Brasil', 'cnpj': '00.000.000/0000-00', 'ativo': True, 'fisco': True, 'url': ''})

      >>> ct, created = Contrato.objects.get_or_create(data_inicio=datetime.date(2008,1,1), auto_renova=True, limite_rescisao=datetime.date(2008,1,11), entidade=ent)


      Cria uma Ordem de Serviço
      >>> a, created = Acordo.objects.get_or_create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')

      >>> os, created = OrdemDeServico.objects.get_or_create(acordo=a, contrato=ct, data_inicio=datetime.date(2008,2,1), data_rescisao=datetime.date(2008,11,1), antes_rescisao=2, descricao='OS 34567 - Contratação de mais um link')

 
      >>> os.__unicode__()
      'OS 34567 - Contratação de mais um link'

      >>> os.mostra_prazo()
      '2 meses'

      >>> os.existe_arquivo()
      ' '
      """

      numero = models.CharField(_(u'Número'), max_length=20)
      tipo = models.ForeignKey('outorga.TipoContrato')
      acordo = models.ForeignKey('outorga.Acordo')
      contrato = models.ForeignKey('outorga.Contrato')
      data_inicio = NARADateField(_(u'Início'))
      data_rescisao = NARADateField(_(u'Término'), null=True, blank=True)
      antes_rescisao = models.IntegerField(_(u'Prazo p/ solicitar rescisão'), null=True, blank=True)
      descricao = models.TextField(_(u'Descrição'))
      #arquivo = models.FileField(upload_to='OS', null=True, blank=True)
      pergunta = models.ManyToManyField('memorando.Pergunta', null=True, blank=True)
      substituicoes = models.TextField(null=True, blank=True)

      # Retorna a descrição.
      def __unicode__(self):
	  return u"%s %s" % (self.tipo, self.numero)


      # Retorna o prazo para solicitar recisão (campo 'antes_rescisao').
      def mostra_prazo(self):
	  if self.antes_rescisao < 1:
	      return '-'
	  if self.antes_rescisao > 1:
              return u'%s meses' % self.antes_rescisao
          return u'%s meses' % self.antes_rescisao
      mostra_prazo.short_description = _(u'Prazo p/ solicitar rescisão')


      # Retorna um ícone se a ordem de serviço tiver anexo.
      def existe_arquivo(self):
	  a = '<center><a href="/admin/outorga/arquivoos/?os__id__exact=%s"><img src="/media/img/arquivo.png" /></a></center>' % self.id
	  if self.arquivos.count() > 0:
	      return a
	  else:
	      return ' '
      existe_arquivo.allow_tags = True
      existe_arquivo.short_description = _(u'Arquivo')

      def entidade(self):
          return self.contrato.entidade

      def primeiro_arquivo(self):
          osf = self.arquivos.all()
          if osf.count() > 0: return osf[0].arquivo
          return None

      class Meta:
	  verbose_name = _(u'Alteração de contrato (OS)')
	  verbose_name_plural = _(u'Alteração de contratos (OS)')
          ordering = ('tipo', 'numero')


class ArquivoOS(models.Model):
      """
      Arquivos de ordem de serviço	
      """    
      arquivo = models.FileField(upload_to=upload_dir_os)
      data = models.DateField()
      historico = models.TextField()
      os = models.ForeignKey('outorga.OrdemDeServico', related_name='arquivos')

      def __unicode__(self):
	  if self.arquivo.name.find('/') == -1:
	      return u'%s' % self.arquivo.name
	  else:
	      return u'%s' % self.arquivo.name.split('/')[-1]
	  
	  
