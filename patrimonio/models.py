# -*- coding: utf-8 -*-


from django.db import models
from utils.models import NARADateField
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
import datetime


# Create your models here.



class Estado(models.Model):

    # Declaração de variáveis estáticas
    PATRIMONIO_ATIVO = 22



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
    pagamento = models.ForeignKey('financeiro.Pagamento', null=True, blank=True)
    ns = models.CharField(_(u'Número de série'), null=True, blank=True, max_length=50)
    complemento = models.CharField('Compl', max_length=100, null=True, blank=True)
    valor = models.DecimalField(u'Vl unit', max_digits=12, decimal_places=2, null=True, blank=True)
    procedencia = models.CharField(_(u'Procedência'), null=True, blank=True, max_length=100)
    obs = models.TextField(null=True, blank=True)
    agilis = models.BooleanField(_(u'Agilis?'), default=True)
    equipamento = models.ForeignKey('patrimonio.Equipamento', null=True, blank=True)
    checado = models.BooleanField()
    apelido = models.CharField(max_length=30, null=True, blank=True)
    descricao = models.TextField(_(u'Descrição NF'))
    ean = models.CharField(u'EAN', max_length=45, null=True, blank=True)
    tem_numero_fmusp = models.BooleanField('Tem número de patrimônio FMUSP?', default=False)
    numero_fmusp = models.IntegerField('Número de patrimônio FMUSP', null=True, blank=True)

# Campos duplicados que existem no Model de Equipamento
    tipo = models.ForeignKey('patrimonio.Tipo')
    descricao_tecnica = models.TextField(u'Descrição técnica', null=True, blank=True)
    part_number = models.CharField(null=True, blank=True, max_length=50)
    marca = models.CharField(_(u'Marca/Editora'), null=True, blank=True, max_length=100)
    modelo = models.CharField(null=True, blank=True, max_length=100)
    imagem = models.ImageField(upload_to='patrimonio', null=True, blank=True)
    isbn = models.CharField(_(u'ISBN'), null=True, blank=True, max_length=20)
    titulo_autor = models.CharField(_(u'Título e autor'), null=True, blank=True, max_length=100)
    especificacao = models.FileField(u'Especificação', upload_to='patrimonio', null=True, blank=True)
    ncm = models.CharField(u'NCM/SH', null=True, blank=True, max_length=30)
    tamanho = models.DecimalField(u'Tamanho (em U)', max_digits=5, decimal_places=2, blank=True, null=True)

    def __unicode__(self):
        if self.pagamento:
            return '%s - %s  - %s - %s' % (self.pagamento.protocolo.num_documento, self.apelido, self.ns, self.descricao)
        else:
            return '%s - %s - %s' % (self.apelido, self.ns, self.descricao)

    def historico_atual(self):
        ht = self.historicolocal_set.order_by('-data')
        if not ht: return None
        return ht[0]
   

    def posicao(self):
        ht = self.historico_atual()
        if not ht: return ''
        return '%s - %s' % (ht.endereco.complemento, ht.posicao)

    # Retorna os patrimônios de um termo.
    @classmethod
    def patrimonios_termo(cls, t):
        return cls.objects.filter(pagamento_protocolo__termo=t)

    def nf(self):
        if self.pagamento is not None and self.pagamento.protocolo is not None:
            return '%s' % self.pagamento.protocolo.num_documento
        else:
            return ''
    nf.short_description = u'NF'

    # Define a descrição do modelo.
    class Meta:
        verbose_name = _(u'Patrimônio')
        verbose_name_plural = _(u'Patrimônio')
	ordering = ('tipo', 'descricao')

    # retorna modalidade, parcial e pagina para exibicao no admin
    def auditoria(self):
        if not self.pagamento:
            return ''
        if not self.pagamento.origem_fapesp:
            return ''
        modalidade = self.pagamento.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
        return '%s (%s/%s)' % (modalidade, self.pagamento.parcial(), self.pagamento.pagina())
    auditoria.short_description = u'Material (par/pág)'


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


    memorando = models.ForeignKey('memorando.MemorandoSimples', null=True, blank=True)
    patrimonio = models.ForeignKey(Patrimonio, verbose_name=_(u'Patrimônio'))
    endereco = models.ForeignKey('identificacao.EnderecoDetalhe', verbose_name=_(u'Localização'))
    estado =  models.ForeignKey(Estado, verbose_name=_(u'Estado do Patrimônio'))
    descricao = models.TextField(_(u'Ocorrência'), help_text=_(u'ex. Empréstimo'))
    data = models.DateField(_(u'Data'))
    posicao = models.CharField(u'Posição', max_length=50, null=True, blank=True)
    pai = models.ForeignKey(Patrimonio, null=True, blank=True, related_name='filhos')

    # Retorna a data o patrimônio e o endereco.
    def __unicode__(self):
        return u'%s - %s | %s' % (self.data.strftime('%d/%m/%Y'), self.patrimonio, self.endereco or '')



    # Define a descrição do modelo e a ordenação dos dados pelo campo 'nome'.
    class Meta:
        verbose_name = _(u'Histórico Local')
        verbose_name_plural = _(u'Histórico Local')
        ordering = ('-data', )
        unique_together = (('patrimonio', 'endereco', 'descricao', 'data'), )


    def posicao_int(self):
        try:
            return int(self.posicao)
        except:
            try:
                return int(self.posicao.split('.F')[1].split('.')[0])
            except:
		return -1

class Direcao(models.Model):
	origem = models.CharField(max_length=15)
	destino = models.CharField(max_length=15)
	
	def __unicode__(self):
		return '%s - %s' % (self.origem, self.destino)
		
	class Meta:
		verbose_name = u'Direção'
		verbose_name_plural = u'Direções'
	
class DistribuicaoUnidade(models.Model):
	nome = models.CharField(max_length=45)
	sigla = models.CharField(max_length=4)
	
	def __unicode__(self):
		return u'%s - %s' % (self.sigla, self.nome)
		
class Distribuicao(models.Model):
	inicio = models.IntegerField()
	final = models.IntegerField()
	unidade = models.ForeignKey('patrimonio.DistribuicaoUnidade')
	direcao = models.ForeignKey('patrimonio.Direcao')
	
	def __unicode__(self):
		return u'%s - %s' % (self.inicio, self.final)
		
	class Meta:
		verbose_name = u'Distribuição'
		verbose_name_plural = u'Distribuições'

class UnidadeDimensao(models.Model):
	nome = models.CharField(max_length=15)
	
	def __unicode__(self):
		return u'%s' % self.nome
		
	class Meta:
		verbose_name = u'Unidade da dimensão'
		verbose_name_plural = u'Unidades das dimensões'
		
class Dimensao(models.Model):
	altura = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
	largura = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
	profundidade = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
	peso = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
	unidade = models.ForeignKey('patrimonio.UnidadeDimensao')
	
	def __unicode__(self):
		return u'%s x %s x %s %s - %s kg' % (self.altura, self.largura, self.profundidade, self.unidade, self.peso)
	
	class Meta:
		verbose_name = u'Dimensão'
		verbose_name_plural = u'Dimensões'

class TipoEquipamento(models.Model):
    nome = models.CharField(max_length=45)

    def __unicode__(self):
        return '%s' % self.nome

    class Meta:
	ordering = ('nome',)

class Equipamento(models.Model):
    descricao = models.TextField(_(u'Descrição'))
    part_number = models.CharField(null=True, blank=True, max_length=50)
    marca = models.CharField(_(u'Marca ou Editora'), null=True, blank=True, max_length=100)
    modelo = models.CharField(null=True, blank=True, max_length=100)
    imagem = models.ImageField(u'Imagem do equipamento', upload_to='patrimonio', null=True, blank=True)
    isbn = models.CharField(_(u'ISBN'), null=True, blank=True, max_length=20)
    ncm = models.CharField(u'NCM/SH', null=True, blank=True, max_length=30)
    titulo_autor = models.CharField(_(u'Título e autor'), null=True, blank=True, max_length=100)
    tamanho = models.DecimalField(u'Tamanho (em U)', max_digits=5, decimal_places=2, null=True, blank=True)
    especificacao = models.FileField(u'Especificação', upload_to='patrimonio', null=True, blank=True)
    tipo = models.ForeignKey('patrimonio.TipoEquipamento', null=True, blank=True)
    convencoes = models.ManyToManyField('patrimonio.Distribuicao', verbose_name=u'Convenções')
    dimensao = models.ForeignKey('patrimonio.Dimensao', null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.descricao, self.part_number)

    class Meta:
	ordering = ('descricao',)
