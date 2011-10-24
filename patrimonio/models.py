# -*- coding: utf-8 -*-


from django.db import models
from utils.models import NARADateField
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
import datetime


# Create your models here.



class Estado(models.Model):

    """
    Uma instância dessa classe representa um estado do patrimônio ou do equipamento.
    Exemplo de estado do Patrimônio: Emprestado, Mautenção, Doado, ...
    Exemplo de estado do Equipamento: Defeito, Obsoleto, Ativo, ...

    O método '__unicode__'	Retorna o nome.
    A class 'Meta'		Define a ordem de apresentação dos dados pelo nome.

    >>> e, created = Estado.objects.get_or_create(nome='Doado')

    >>> e.__unicode__()
    u'Doado'
    """


    nome = models.CharField(_(u'Nome'), max_length=30, help_text=_(u'ex. Doado'), unique=True)


    # Retorna o nome
    def __unicode__(self):
        return u'%s' % self.nome


    # Define a ordenação dos dados pelo nome
    class Meta:
        ordering = ("nome", )



class Tipo(models.Model):

    """
    Uma instância dessa classe é um tipo de licença (ex. Free).

    O método '__unicode__'	Retorna o nome.
    A class 'Meta'		Define a ordem de apresentação dos dados pelo nome.

    >>> t, created = Tipo.objects.get_or_create(nome='Free')

    >>> t.__unicode__()
    u'Free'
    """


    nome = models.CharField(_(u'Nome'), max_length=30, help_text=_(u'ex. Open Source'), unique=True)


    # Retorna o nome
    def __unicode__(self):
        return u'%s' % self.nome


    # Define a ordenação dos dados pelo nome
    class Meta:
        ordering = ("nome", )



class Patrimonio(models.Model):

    """
    Uma instância dessa classe representa um patrimônio.

    """

    patrimonio = models.ForeignKey('patrimonio.Patrimonio', null=True, blank=True, verbose_name=_(u'Contido em'), related_name='contido')
    pagamento = models.ForeignKey('financeiro.Pagamento')
    tipo = models.ForeignKey('patrimonio.Tipo')
    descricao = models.TextField(_(u'Descrição'))
    part_number = models.CharField(null=True, blank=True, max_length=50)
    marca = models.CharField(_(u'Marca ou Editora'), null=True, blank=True, max_length=100)
    modelo = models.CharField(null=True, blank=True, max_length=100)
    ns = models.CharField(_(u'Número de série'), null=True, blank=True, max_length=50)
    valor = models.DecimalField(u'Valor de compra', max_digits=12, decimal_places=2)
    imagem = models.ImageField(upload_to='patrimonio', null=True, blank=True)
    procedencia = models.CharField(_(u'Procedência'), null=True, blank=True, max_length=100)
    obs = models.TextField(null=True, blank=True)
    isbn = models.CharField(_(u'ISBN'), null=True, blank=True, max_length=20)
    titulo_autor = models.CharField(_(u'Título e autor'), null=True, blank=True, max_length=100)

    def __unicode__(self):
        return '%s' % self.descricao

    def historico_atual(self):
        ht = self.historicolocal_set.order_by('-data')
        if not ht: return None
        return ht[0]
   

    # Retorna os patrimônios de um termo.
    @classmethod
    def patrimonios_termo(cls, t):
        return cls.objects.filter(pagamento_protocolo__termo=t)


    def nf(self):
        return '%s' % self.pagamento.protocolo.num_documento

    # Define a descrição do modelo.
    class Meta:
        verbose_name = _(u'Patrimônio')
        verbose_name_plural = _(u'Patrimônio')
	ordering = ('tipo', 'descricao')



class HistoricoLocal(models.Model):

    """
    Uma instância dessa classe representa o histórico de um patrimônio.

    O método '__unicode__' 	Retorna os campos 'data', 'patrimonio', 'endereco'.
    A class 'Meta' 		Define a descrição do modelo (singular e plural), a ordenação dos dados pelo campo 'data' e a unicidade
    				dos dados pelos campos 'patrimonio', 'endereco', 'descricao' e 'data'.

    >>> from protocolo.models import TipoDocumento, Origem, Protocolo, ItemProtocolo
    >>> from protocolo.models import Estado as EstadoProtocolo
    >>> from identificacao.models import Entidade, Contato, Endereco, Identificacao
    >>> from membro.models import Membro
    >>> from outorga.models import Termo

    >>> ent, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'Global Crossing', 'cnpj': '00.000.000/0000-00', 'ativo': False, 'fisco': True, 'url': '', 'asn': 123})

    >>> c, created = Contato.objects.get_or_create(nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': '', 'ativo': True})

    >>> iden, created = Identificacao.objects.get_or_create(entidade=ent, contato=c, defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True})

    >>> end, created = Endereco.objects.get_or_create(identificacao=iden, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')


    >>> tp, created = Tipo.objects.get_or_create(nome='Free')

    >>> td, created = TipoDocumento.objects.get_or_create(nome='Fatura')

    >>> e, created = Estado.objects.get_or_create(nome='Vigente')

    >>> ep, created = EstadoProtocolo.objects.get_or_create(nome='Pago')

    >>> ent1, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome': 'Academic Network at São Paulo', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> og, created = Origem.objects.get_or_create(nome='Sedex')

    >>> mb, created = Membro.objects.get_or_create(nome='Gerson Gomes', funcionario=True, defaults={'cargo': 'Outorgado', 'email': 'gerson@gomes.com', 'cpf': '000.000.000-00'})

    >>> t, created = Termo.objects.get_or_create(ano=2008, processo=52885, digito=8, defaults={'data_concessao': datetime.date(2008,1,1), 'data_assinatura': datetime.date(2009,1,15), 'membro': mb})

    >>> p = Protocolo(termo=t, tipo_documento=td, num_documento=2008, estado=ep, identificacao=iden, data_chegada=datetime.datetime(2008,9,30,10,10), data_validade=datetime.date(2009,8,25), data_vencimento=datetime.date(2008,9,30), descricao="Aditivo Material Permanente", origem=og)
    >>> p.save()

    >>> ip = ItemProtocolo(protocolo=p, descricao='Hardware para rede', quantidade=1, valor_unitario='2358.90')
    >>> ip.save()

    >>> bb, created = Biblioteca.objects.get_or_create(obs='Codigo XXX')

    >>> rt, created = Roteador.objects.get_or_create(ns='AF345678GB3489X', marca='Foundry', modelo='NetIron400', community= 'ANSP', defaults={'itemprotocolo': ip, 'estado': e, 'part_number': ' ', 'nome': 'Roteador'})

    >>> hl, created = HistoricoLocal.objects.get_or_create(patrimonio=rt, endereco= end, descricao='Emprestimo', data= datetime.date(2009,2,5))

    >>> hl.__unicode__()
    u'05/02/09 - NetIron400_AF345678GB3489X | Community: ANSP | Dr. Ovidio, 215'

    >>> HistoricoLocal.historico_patrimonio(rt)
    [<HistoricoLocal: 05/02/09 - Equipamento: Roteador | Foundry_NetIron400 - AF345678GB3489X | Dr. Ovidio, 215>]
    """


    patrimonio = models.ForeignKey(Patrimonio, verbose_name=_(u'Patrimônio'))
    endereco = models.ForeignKey('identificacao.EnderecoDetalhe', verbose_name=_(u'Localização'))
    descricao = models.TextField(_(u'Ocorrência'), help_text=_(u'ex. Empréstimo'))
    data = models.DateField(_(u'Data'))
    estado =  models.ForeignKey(Estado, verbose_name=_(u'Estado do Patrimônio'))
    memorando = models.ForeignKey('memorando.MemorandoSimples', null=True, blank=True)

    # Retorna a data o patrimônio e o endereco.
    def __unicode__(self):
        return u'%s - %s | %s' % (self.data.strftime('%d/%m/%Y'), self.patrimonio, self.endereco)



    # Define a descrição do modelo e a ordenação dos dados pelo campo 'nome'.
    class Meta:
        verbose_name = _(u'Histórico Local')
        verbose_name_plural = _(u'Histórico Local')
        ordering = ('-data', )
        unique_together = (('patrimonio', 'endereco', 'descricao', 'data'), )



