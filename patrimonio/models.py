# -*- coding: utf-8 -*-


from django.db import models
from utils.models import NARADateField
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.db.models import Q
import datetime
import re
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)




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
    checado = models.BooleanField(default=False)
    apelido = models.CharField(max_length=30, null=True, blank=True)
    descricao = models.TextField(_(u'Descrição NF'))
    ean = models.CharField(u'EAN', max_length=45, null=True, blank=True)
    tem_numero_fmusp = models.BooleanField('Tem número de patrimônio FMUSP?', default=False)
    numero_fmusp = models.IntegerField('Número de patrimônio FMUSP', null=True, blank=True)
    entidade_procedencia = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Procedência'), null=True, blank=True, help_text=u"Representa a Entidade que fornece este patrimônio.")

# Campos duplicados que existem no Model de Equipamento
    tipo = models.ForeignKey('patrimonio.Tipo')
    descricao_tecnica = models.TextField(u'Descrição técnica', null=True, blank=True)
    part_number = models.CharField(null=True, blank=True, max_length=50)
    # Patrimonio não tem mais marca. Utilizar o campo equipamento.entidade_fabricante.sigla
    #marca = models.CharField(_(u'Marca/Editora'), null=True, blank=True, max_length=100)
    modelo = models.CharField(null=True, blank=True, max_length=100)
    imagem = models.ImageField(upload_to='patrimonio', null=True, blank=True)
    isbn = models.CharField(_(u'ISBN'), null=True, blank=True, max_length=20)
    titulo_autor = models.CharField(_(u'Título e autor'), null=True, blank=True, max_length=100)
    especificacao = models.FileField(u'Especificação', upload_to='patrimonio', null=True, blank=True)
    ncm = models.CharField(u'NCM/SH', null=True, blank=True, max_length=30)
    tamanho = models.DecimalField(u'Tamanho (em U)', max_digits=5, decimal_places=2, blank=True, null=True)

    revision = models.CharField(u'Revision', null=True, blank=True, max_length=30)
    version = models.CharField(u'Version', null=True, blank=True, max_length=30)
    ocst = models.CharField(u'O/CST', null=True, blank=True, max_length=30)
    cfop = models.CharField(u'CFOP', null=True, blank=True, max_length=30)
    garantia_termino = NARADateField(_(u'Data de término da garantia'))

    def __unicode__(self):
        if self.pagamento:
            return u'%s - %s  - %s - %s' % (self.pagamento.protocolo.num_documento, self.apelido, self.ns, self.descricao)
        else:
            return u'%s - %s - %s' % (self.apelido, self.ns, self.descricao)

    def save(self, *args, **kwargs):
        super(Patrimonio, self).save(*args, **kwargs)
        
        # Rogerio: após salvar o patrimonio, verifica se os patrimonios filhos estão
        # no mesmo endereço e posição.
        # Se não estiverem, cria um novo histórico de endereço para todos os filhos
        if Patrimonio.objects.filter(patrimonio=self).exists():
            filhos = Patrimonio.objects.filter(patrimonio=self)
            
            for filho in filhos:
                # Rogerio: se não tiver endereço, não faz nada com os patrimonios filhos,
                # já que não podemos remover os endereços
                #
                # Também não modificamos se o filho possui um histórico com data mais atual
                if self.historico_atual and self.historico_atual.data >= filho.historico_atual.data:
                    if not filho.historico_atual or \
                        (self.historico_atual.endereco != filho.historico_atual.endereco) or \
                            (self.historico_atual.posicao != filho.historico_atual.posicao):
                        
                        novoHistorico = HistoricoLocal.objects.create(memorando=self.historico_atual.memorando,
                                                       patrimonio=filho,
                                                       endereco=self.historico_atual.endereco,
                                                       estado=self.historico_atual.estado,
                                                       descricao="Movimentado junto com o patrimonio %s [%s]"%(self.id, self.historico_atual.descricao),
                                                       data=self.historico_atual.data,
                                                       posicao=self.historico_atual.posicao,
                                                       )


    def marca(self):
        retorno = ''
        if self.equipamento and self.equipamento.entidade_fabricante and self.equipamento.entidade_fabricante.sigla:
            retorno = self.equipamento.entidade_fabricante.sigla
        return retorno
    marca.short_description = u'Marca'
    
    @cached_property
    def historico_atual(self):
        ht = self.historicolocal_set.order_by('-data')
        if not ht: return None
        return ht[0]
   

    def posicao(self):
        ht = self.historico_atual
        if not ht: return u''
        return u'%s - %s' % (ht.endereco.complemento, ht.posicao)

    # Retorna os patrimônios de um termo.
    @classmethod
    def patrimonios_termo(cls, t):
        return cls.objects.filter(pagamento_protocolo__termo=t)

    def nf(self):
        if self.pagamento is not None and self.pagamento.protocolo is not None:
            return u'%s' % self.pagamento.protocolo.num_documento
        else:
            return ''
    nf.short_description = u'NF'

    # retorna modalidade, parcial e pagina para exibicao no admin
    def auditoria(self):
        if not self.pagamento:
            return ''
        if not self.pagamento.origem_fapesp:
            return ''
        modalidade = self.pagamento.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
        return u'%s (%s/%s)' % (modalidade, self.pagamento.parcial(), self.pagamento.pagina())
    auditoria.short_description = u'Material (par/pág)'

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
        ordering = ('-data', 'id')
        unique_together = (('patrimonio', 'endereco', 'descricao', 'data'), )

    @cached_property
    def posicao_rack(self):
        retorno = None
        if self.posicao:
            rack_str = self.posicao.split('.')
            
            if len(rack_str) == 1:
                rack_str = self.posicao.split('-')

            if len(rack_str) >= 2:
                retorno = rack_str[0]
        return retorno

    @cached_property
    def posicao_rack_letra(self):
        retorno = None
        if self.posicao:
            rack_str = self.posicao.split('.')
            
            if len(rack_str) == 1:
                rack_str = self.posicao.split('-')

            if len(rack_str) >= 2:
                eixoLetra = re.findall(r'[a-zA-Z]+', rack_str[0])
                if len(eixoLetra) == 1:
                    retorno = eixoLetra[0]
                    
        return retorno
    
    @cached_property
    def posicao_rack_numero(self):
        retorno = None
        if self.posicao:
            rack_str = self.posicao.split('.')
            if len(rack_str) == 1:
                rack_str = self.posicao.split('-')
                
            if len(rack_str) >= 2:
                eixoNumero = re.findall(r'\d+', rack_str[0])
                if len(eixoNumero) == 1:
                    retorno = eixoNumero[0]
        return retorno
        
    @cached_property
    def posicao_furo(self):
        retorno = -1
        if self.posicao:
            # verifica se possui a posição já configurada
            if self.posicao.isdigit():
                retorno = int(self.posicao)
            else:
                # verifica se é possível recuperar a posição de furo de uma string como R042.F085.TD
                furo_str = self.posicao.split('.F')
                if len(furo_str) > 1:
                    pos_str = furo_str[1].split('.')
                    if len(pos_str) >= 1 and pos_str[0].isdigit():
                        retorno = int(pos_str[0])
                    else:
                        pos_str = furo_str[1].split('-')
                        if len(pos_str) > 1:
                            retorno = int(pos_str[0])
        
        return retorno

    @cached_property
    def posicao_colocacao(self):
        retorno = None
        if self.posicao:
            # verifica se é possível recuperar a posição TD de uma string como R042.F085.TD ou R042.F085-TD 
            furo_str = self.posicao.split('.F')
            if len(furo_str) >= 2:
                pos_str = furo_str[1].split('.')
                if len(pos_str) >= 2:
                    retorno = pos_str[1]
                else:
                    pos_str = furo_str[1].split('-')
                    if len(pos_str) > 1:
                        retorno = pos_str[1]
                        
            else:
                # verifica se é possível recuperar a posição piso de uma string como R042.piso
                pos_str = self.posicao.split('.')
                if len(pos_str) == 2:
                    retorno = pos_str[1]
                else:
                    # verifica se é possível recuperar a posição piso de uma string como R042-piso
                    pos_str = self.posicao.split('-')
                    if len(pos_str) == 2:
                        retorno = pos_str[1]
            
        return retorno

    
class Direcao(models.Model):
	origem = models.CharField(max_length=15)
	destino = models.CharField(max_length=15)
	
	def __unicode__(self):
		return u'%s - %s' % (self.origem, self.destino)
		
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
        return u'%s' % self.nome

    class Meta:
	ordering = ('nome',)

class Equipamento(models.Model):
    tipo = models.ForeignKey('patrimonio.TipoEquipamento', null=True, blank=True)
    descricao = models.TextField(_(u'Descrição'))
    part_number = models.CharField(null=True, blank=True, max_length=50)
    
    # TERMINADA A ASSOCIAÇÃO COM A ENTIDADE, DESABILITAR O CAMPO MARCA(CHARFIELD)
    #marca = models.CharField(_(u'Marca ou Editora'), null=True, blank=True, max_length=100)
    entidade_fabricante = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Marca/Editora'), null=True, blank=True, help_text=u"Representa a Entidade que fabrica este equipamento.")
    
    modelo = models.CharField(null=True, blank=True, max_length=100)
    ncm = models.CharField(u'NCM/SH', null=True, blank=True, max_length=30)
    ean = models.CharField(u'EAN', max_length=45, null=True, blank=True)
    tamanho = models.DecimalField(u'Tamanho (em U)', max_digits=5, decimal_places=2, null=True, blank=True)
    dimensao = models.ForeignKey('patrimonio.Dimensao', null=True, blank=True)
    especificacao = models.FileField(u'Especificação', upload_to='patrimonio', null=True, blank=True)
    imagem = models.ImageField(u'Imagem do equipamento', upload_to='patrimonio', null=True, blank=True)
    convencoes = models.ManyToManyField('patrimonio.Distribuicao', verbose_name=u'Convenções')
    titulo_autor = models.CharField(_(u'Título e autor'), null=True, blank=True, max_length=100)
    isbn = models.CharField(_(u'ISBN'), null=True, blank=True, max_length=20)

    def __unicode__(self):
        return u'%s - %s' % (self.descricao, self.part_number)

    class Meta:
	ordering = ('descricao',)
