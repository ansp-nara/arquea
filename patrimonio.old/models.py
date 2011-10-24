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

    O método '__unicode__'		Retorna o método __unicode__ de um dos modelos 'Licenca', 'Publicacao' ou 'Equipamento'.
    O método 'fornecedor'		Retorna a sigla da entidade, o tipo do protocolo e o número documento.
    A classmethod 'patrimonios_termo' 	Retorna os patrimônios de um termo.
    A class 'Meta' 			Define a descrição do modelo (singular e plural).

    >>> from protocolo.models import TipoDocumento, Origem, Protocolo, ItemProtocolo
    >>> from protocolo.models import Estado as EstadoProtocolo
    >>> from identificacao.models import Entidade, Contato, Endereco, Identificacao
    >>> from outorga.models import Termo
    >>> from membro.models import Membro

    >>> td, created = TipoDocumento.objects.get_or_create(nome='Anexo 9')

    >>> e1, created = Estado.objects.get_or_create(nome='Ativo')
    >>> e2, created = Estado.objects.get_or_create(nome='Manuteção')

    >>> ep, created = EstadoProtocolo.objects.get_or_create(nome='Pago')

    >>> ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome': 'Academic Network at São Paulo', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> c, created = Contato.objects.get_or_create(nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})

    >>> og, created = Origem.objects.get_or_create(nome='Sedex')

    >>> iden, created = Identificacao.objects.get_or_create(entidade=ent, contato=c, defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True})

    >>> end, created = Endereco.objects.get_or_create(identificacao=iden, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')

    >>> mb, created = Membro.objects.get_or_create(nome='Gerson Gomes', funcionario=True, defaults={'cargo': 'Outorgado', 'email': 'gerson@gomes.com', 'cpf': '000.000.000-00'})

    >>> t, created = Termo.objects.get_or_create(ano=2008, processo=52885, digito=8, defaults={'data_concessao': datetime.date(2008,1,1), 'data_assinatura': datetime.date(2009,1,15), 'membro': mb})

    >>> p = Protocolo(termo=t, tipo_documento=td, num_documento=2008, estado=ep, identificacao=iden, data_chegada=datetime.datetime(2008,9,30,10,10), data_validade=datetime.date(2009,8,25), data_vencimento=datetime.date(2008,9,30), descricao="Aditivo Material Permanente", origem=og)
    >>> p.save()

    >>> ip = ItemProtocolo(protocolo=p, descricao='Impressoras', quantidade=2, valor_unitario='1500.50')
    >>> ip.save()

    >>> Patrimonio.patrimonios_termo(t)
    [<Patrimonio: Licença: XXXX>, <Patrimonio: Equipamento: Roteador | Foundry_NetIron400 - AF345678GB3489X>, <Patrimonio: Equipamento: Roteador Wireless | Foundry_IronPoint 200 - WR345678GB3489X>]
    """


    #itemprotocolo = models.ForeignKey('protocolo.ItemProtocolo', verbose_name=_(u'Item do Protocolo'), limit_choices_to=Q(protocolo__estado__nome=u'Concluído') & (Q(protocolo__tipo_documento__nome=u'Fatura') | Q(protocolo__tipo_documento__nome=u'Nota Fiscal')))
    #itemprotocolo = models.ForeignKey('protocolo.ItemProtocolo', verbose_name=_(u'Item do Protocolo'), limit_choices_to={'protocolo__id':99999999})
    pagamento = models.ForeignKey('financeiro.Pagamento')
    #estado =  models.ForeignKey(Estado, verbose_name=_(u'Estado do Patrimônio'))
    valor = models.DecimalField(u'Valor de compra', max_digits=12, decimal_places=2)


    # Retorna o método __unicode__ de suas subclasses (Licenca, Publicacao ou Equipamento).
    def __unicode__(self):
        try:
            return u'Licença: %s' % (self.licenca)
        except Licenca.DoesNotExist:
            try:
                return u'Publicação: %s' % (self.publicacao)
            except Publicacao.DoesNotExist:
                try:
                    return u'Equipamento: %s' % (self.equipamento)
                except Equipamento.DoesNotExist:
                    try:
		        return u'Móvel: %s' % (self.movel)
		    except Movel.DoesNotExist:
		        pass


    # Retorna o Fornecedor, o tipo e o número do documento (protocolo).
    def fornecedor(self):
        return u'%s_%s' % (self.pagamento.protocolo.entidade(), self.pagamento.protocolo.doc_num())
    fornecedor.short_description = _(u'Fornecedor')


    # Retorna o estado
    def mostra_estado(self):
        return self.estado.nome
    mostra_estado.short_description = _(u'Estado do Patrimônio')

    # Retorna os patrimônios de um termo.
    @classmethod
    def patrimonios_termo(cls, t):
        return cls.objects.filter(itemprotocolo__protocolo__termo=t)


    # Define a descrição do modelo.
    class Meta:
        verbose_name = _(u'Patrimônio')
        verbose_name_plural = _(u'Patrimônio')



class Licenca(Patrimonio):

    """
    Uma instância dessa classe herda os campos da classe Patrimonio e representa uma licença.

    O método '__unicode__'	Retorna o 'nome' da Licença.
    A class 'Meta'		Define a descrição do modelo (singular e plural) e a ordenação dos dados pelo campo 'nome'.

    >>> from protocolo.models import TipoDocumento, Origem, Protocolo, ItemProtocolo
    >>> from protocolo.models import Estado as EstadoProtocolo
    >>> from identificacao.models import Entidade, Contato, Endereco, Identificacao
    >>> from outorga.models import Termo
    >>> from membro.models import Membro

    >>> tp, created = Tipo.objects.get_or_create(nome='Provisória')

    >>> td, created = TipoDocumento.objects.get_or_create(nome='Fatura')

    >>> e, created = Estado.objects.get_or_create(nome='Vigente')

    >>> ep, created = EstadoProtocolo.objects.get_or_create(nome='Pago')

    >>> ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome': 'Academic Network at São Paulo', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> c, created = Contato.objects.get_or_create(nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})

    >>> og, created = Origem.objects.get_or_create(nome='Sedex')

    >>> iden, created = Identificacao.objects.get_or_create(entidade=ent, contato=c, defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True})

    >>> end, created = Endereco.objects.get_or_create(identificacao=iden, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')

    >>> mb, created = Membro.objects.get_or_create(nome='Gerson Gomes', funcionario=True, defaults={'cargo': 'Outorgado', 'email': 'gerson@gomes.com', 'cpf': '000.000.000-00'})

    >>> t, created = Termo.objects.get_or_create(ano=2008, processo=52885, digito=8, defaults={'data_concessao': datetime.date(2008,1,1), 'data_assinatura': datetime.date(2009,1,15), 'membro': mb})

    >>> p = Protocolo(termo=t, tipo_documento=td, num_documento=2008, estado=ep, identificacao=iden, data_chegada=datetime.datetime(2008,9,30,10,10), data_validade=datetime.date(2009,8,25), data_vencimento=datetime.date(2008,9,30), descricao="Aditivo Material Permanente", origem=og)
    >>> p.save()

    >>> ip = ItemProtocolo(protocolo=p, descricao='Licença para Software', quantidade=1, valor_unitario='2358.90')
    >>> ip.save()

    >>> bb, created = Biblioteca.objects.get_or_create(obs='Codigo XXX')

    >>> li, created = Licenca.objects.get_or_create(itemprotocolo=ip, nome='XXXX', qtde_usuarios=20, tipo= tp, defaults={'estado': e, 'biblioteca': bb, 'obs': ''})

    >>> li.nome
    'XXXX'

    >>> li.fornecedor()
    u'ANSP_Fatura 2008'
    """


    nome = models.CharField(_(u'Nome'), max_length=100, help_text=_(u'Nome da licença'))
    qtde_usuarios = models.IntegerField(_(u'Quantidade'), help_text=_(u'Quantidade de Usuários'))
    tipo = models.ForeignKey(Tipo, verbose_name=_(u'Tipo de Licença'))
    obs = models.TextField(_(u'Observação'), blank=True)


    # Retorna a descrição do patrimônio e o nome da licença.
    def __unicode__(self):
        return u'%s' % (self.nome)


    # Retorna a Biblioteca
    def mostra_biblioteca(self):
        if self.biblioteca: return self.biblioteca.obs
    mostra_biblioteca.short_description = _(u'Biblioteca')


    # Retorna o tipo de licença.
    def mostra_tipo(self):
        return self.tipo.nome
    mostra_biblioteca.short_description = _(u'Biblioteca')


    # Define a descrição do modelo, a ordenação dos dados pelo campo 'nome'.
    class Meta:
        verbose_name = _(u'Licença')
        verbose_name_plural = _(u'Licenças')
        ordering = ('nome', )



class Publicacao(Patrimonio):

    """
    Uma instância dessa classe herda os campos da classe Patrimonio e representa uma publicação (ex. livros).

    O método '__unicode__'	Retorna os campos 'autor' e 'titulo'.
    A class 'Meta'		Define a descrição do modelo (singular e plural) e a ordenação dos dados pelos campos 'autor' e 'titulo'.

    >>> from protocolo.models import TipoDocumento, Origem, Protocolo, ItemProtocolo
    >>> from protocolo.models import Estado as EstadoProtocolo
    >>> from identificacao.models import Entidade, Contato, Endereco, Identificacao
    >>> from outorga.models import Termo
    >>> from membro.models import Membro

    >>> td, created = TipoDocumento.objects.get_or_create(nome='Anexo 9')

    >>> e, created = Estado.objects.get_or_create(nome='Ativo')

    >>> ep, created = EstadoProtocolo.objects.get_or_create(nome='Pago')

    >>> ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome': 'Academic Network at São Paulo', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> c, created = Contato.objects.get_or_create(nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})

    >>> og, created = Origem.objects.get_or_create(nome='Sedex')

    >>> iden, created = Identificacao.objects.get_or_create(entidade=ent, contato=c, defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True})

    >>> end, created = Endereco.objects.get_or_create(identificacao=iden, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')

    >>> mb, created = Membro.objects.get_or_create(nome='Gerson Gomes', funcionario=True, defaults={'cargo': 'Outorgado', 'email': 'gerson@gomes.com', 'cpf': '000.000.000-00'})

    >>> t, created = Termo.objects.get_or_create(ano=2008, processo=52885, digito=8, defaults={'data_concessao': datetime.date(2008,1,1), 'data_assinatura': datetime.date(2009,1,15), 'membro': mb})

    >>> p = Protocolo(termo=t, tipo_documento=td, num_documento=2008, estado=ep, identificacao=iden, data_chegada=datetime.datetime(2008,9,30,10,10), data_validade=datetime.date(2009,8,25), data_vencimento=datetime.date(2008,9,30), descricao="Aditivo Material Permanente", origem=og)
    >>> p.save()

    >>> ip = ItemProtocolo(protocolo=p, descricao='Livro', quantidade=1, valor_unitario='340.79')
    >>> ip.save()

    >>> bb, created = Biblioteca.objects.get_or_create(obs='Codigo YYY')

    >>> pb, created = Publicacao.objects.get_or_create(itemprotocolo=ip, isbn= 'BG7890CT7854', defaults={'estado': e, 'biblioteca': bb, 'titulo': 'Redes', 'autor': 'ALVES, Mario', 'editora': 'Saraiva', 'obs': ''})

    >>> pb.__unicode__()
    u'ALVES, Mario. Redes'
    """

    titulo = models.CharField(_(u'Título'), max_length=100, help_text=_(u'ex. Título do Livro'))
    autor = models.CharField(_(u'Autor'), max_length=100, help_text=_(u'ex. ALVES, Mario'))
    editora = models.CharField(_(u'Editora'), max_length=100, help_text=_(u'ex. Editora LTC'))
    isbn = models.CharField(_(u'ISBN'), max_length=20, help_text=_(u' '))
    obs = models.TextField(_(u'Observação'), blank=True)


    # Retorna o autor e o título do livro.
    def __unicode__(self):
        return u'%s. %s' % (self.autor, self.titulo)


    # Define a descrição do modelo, a ordenação dos dados pelo campo 'autor'.
    class Meta:
        verbose_name = _(u'Publicação')
        verbose_name_plural = _(u'Publicações')
        ordering = ('autor', 'titulo')



class Equipamento(Patrimonio):

    """
    Uma instância dessa classe herda os campos da classe Patrimonio e representa um equipamento.

    O método '__unicode__'	Retorna os campos 'nome', 'marca', 'modelo' e 'ns'.
    A class 'Meta'		Define a descrição do modelo (singular e plural) e a ordenação dos dados pelos campos 'marca' e 'modelo'.

    >>> from protocolo.models import TipoDocumento, Origem, Protocolo, ItemProtocolo
    >>> from protocolo.models import Estado as EstadoProtocolo
    >>> from identificacao.models import Entidade, Contato, Endereco, Identificacao
    >>> from membro.models import Membro
    >>> from outorga.models import Termo

    >>> td, created = TipoDocumento.objects.get_or_create(nome='Anexo 9')

    >>> e, created = Estado.objects.get_or_create(nome='Emprestado')

    >>> ep, created = EstadoProtocolo.objects.get_or_create(nome='Pago')

    >>> eq, created = Estado.objects.get_or_create(nome='Ativo')

    >>> ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome': 'Academic Network at São Paulo', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> c, created = Contato.objects.get_or_create(nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})

    >>> og, created = Origem.objects.get_or_create(nome='Sedex')

    >>> iden, created = Identificacao.objects.get_or_create(entidade=ent, contato=c, defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True})

    >>> end, created = Endereco.objects.get_or_create(identificacao=iden, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')

    >>> mb, created = Membro.objects.get_or_create(nome='Gerson Gomes', funcionario=True, defaults={'cargo': 'Outorgado', 'email': 'gerson@gomes.com', 'cpf': '000.000.000-00'})

    >>> t, created = Termo.objects.get_or_create(ano=2008, processo=52885, digito=8, defaults={'data_concessao': datetime.date(2008,1,1), 'data_assinatura': datetime.date(2009,1,15), 'membro': mb})

    >>> p = Protocolo(termo=t, tipo_documento=td, num_documento=2008, estado=ep, identificacao=iden, data_chegada=datetime.datetime(2008,9,30,10,10), data_validade=datetime.date(2009,8,25), data_vencimento=datetime.date(2008,9,30), descricao="Aditivo Material Permanente", origem=og)
    >>> p.save()

    >>> ip = ItemProtocolo(protocolo=p, descricao='Hardware para Rede', quantidade=1, valor_unitario='20500.59')

    >>> ip.save()

    >>> eq, created = Equipamento.objects.get_or_create(ns='WR345678GB3489X', marca='Foundry', modelo='IronPoint 200', defaults={'itemprotocolo': ip, 'estado': e, 'part_number': ' ', 'nome': 'Roteador Wireless', 'estado_equipamento': eq})

    >>> eq.__unicode__()
    u'Roteador Wireless | Foundry_IronPoint 200 - WR345678GB3489X'
    """

    ns = models.CharField(_(u'NS'), max_length=50, help_text=_(u'Número de Série'))
    part_number = models.CharField(_(u'Part Number'), max_length=50, help_text=_(u' '), blank=True)
    marca = models.CharField(_(u'Marca'), max_length=100, help_text=_(u'ex. Foundry'))
    modelo = models.CharField(_(u'Modelo'), max_length=100, help_text=_(u'ex. NetIron 400'))
    nome = models.CharField(_(u'Descricao'), max_length=50, help_text=_(u' '))
    equipamento_esta = models.ForeignKey('patrimonio.Patrimonio', verbose_name=_(u'Contido em'), blank=True, null=True, related_name='equipamento_em') 


    # Retorna o nome do equipamento, a marca, o modelo e o número de série.
    def __unicode__(self):
        return u'%s | %s_%s - %s' % (self.nome, self.marca, self.modelo, self.ns)


    # Define a descrição do modelo e a ordenação dos dados pelos campos 'marca' e 'modelo'.
    class Meta:
        verbose_name = _(u'Equipamento')
        verbose_name_plural = _(u'Equipamentos')
        ordering = ('marca', 'modelo')


class Movel(Patrimonio):
    descricao = models.CharField(_(u'Descrição'), max_length=50)
    imagem = models.ImageField(upload_to='moveis', null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.descricao

    class Meta:
        verbose_name = _(u'Móvel')
	verbose_name_plural = _(u'Móveis')

class MonitoramentoInterno(Equipamento):

    """
    Uma instância dessa classe herda os campos da classe Equipamento e representa um roteador, switch ou qualquer outro equipamento
    monitorado internamente por SNMP.

    O método '__unicode__'	Retorna os campos 'modelo', 'ns' e 'community'.
    A class 'Meta'		Define a descrição do modelo (singular e plural) e a ordenação dos dados pelos campos 'modelo' e 'community'.

    >>> from protocolo.models import TipoDocumento, Origem, Protocolo, ItemProtocolo
    >>> from protocolo.models import Estado as EstadoProtocolo
    >>> from identificacao.models import Entidade, Contato, Endereco, Identificacao
    >>> from membro.models import Membro
    >>> from outorga.models import Termo

    >>> td, created = TipoDocumento.objects.get_or_create(nome='Anexo 9')

    >>> e, created = Estado.objects.get_or_create(nome='Emprestado')

    >>> ep, created = EstadoProtocolo.objects.get_or_create(nome='Pago')

    >>> eq, created = Estado.objects.get_or_create(nome='Ativo')

    >>> ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome': 'Academic Network at São Paulo', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> c, created = Contato.objects.get_or_create(nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})

    >>> og, created = Origem.objects.get_or_create(nome='Sedex')

    >>> iden, created = Identificacao.objects.get_or_create(entidade=ent, contato=c, defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True})

    >>> end, created = Endereco.objects.get_or_create(identificacao=iden, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')

    >>> mb, created = Membro.objects.get_or_create(nome='Gerson Gomes', funcionario=True, defaults={'cargo': 'Outorgado', 'email': 'gerson@gomes.com', 'cpf': '000.000.000-00'})

    >>> t, created = Termo.objects.get_or_create(ano=2008, processo=52885, digito=8, defaults={'data_concessao': datetime.date(2008,1,1), 'data_assinatura': datetime.date(2009,1,15), 'membro': mb})

    >>> p = Protocolo(termo=t, tipo_documento=td, num_documento=2008, estado=ep, identificacao=iden, data_chegada=datetime.datetime(2008,9,30,10,10), data_validade=datetime.date(2009,8,25), data_vencimento=datetime.date(2008,9,30), descricao="Aditivo Material Permanente", origem=og)
    >>> p.save()

    >>> ip = ItemProtocolo(protocolo=p, descricao='Hardware para rede', quantidade=1, valor_unitario='20500.59')
    >>> ip.save()

    >>> rt, created = Roteador.objects.get_or_create(ns='AF345678GB3489X', marca='Foundry', modelo='NetIron400', community= 'ANSP', defaults={'itemprotocolo': ip, 'estado': e, 'estado_equipamento': eq, 'part_number': ' ', 'nome': 'Roteador'})

    >>> rt.__unicode__()
    u'NetIron400_AF345678GB3489X | Community: ANSP'
    """


    community = models.CharField(_(u'Community'), max_length=100, help_text=_(u'ex. ANSP'))


    # Retorna o modelo, o número de série e a community.
    def __unicode__(self):
        return u'%s_%s | Community: %s' % (self.modelo, self.ns, self.community)


    # Define a descrição do modelo e a ordenação dos dados pelos campos 'modelo' e 'community'.
    class Meta:
        ordering = ('modelo', 'community')
        verbose_name = _(u'Monitoramento interno')
        verbose_name_plural = _(u'Monitoramentos internos')

class MonitoramentoExterno(models.Model):
    
    identificacao = models.ForeignKey('identificacao.Identificacao')
    equipamento = models.ForeignKey('patrimonio.Equipamento')
    read_only = models.BooleanField(default=False)

    def __unicode__(self):
	return "%s - %s" % (self.identificacao.entidade, self.equipamento)

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
    endereco = models.ForeignKey('identificacao.EnderecoDetalhe', verbose_name=_(u'Detalhe do endereço'))
    descricao = models.TextField(_(u'Descrição'), help_text=_(u'ex. Empréstimo'))
    data = models.DateField(_(u'Data'))
    estado =  models.ForeignKey(Estado, verbose_name=_(u'Estado do Patrimônio'))

    # Retorna a data o patrimônio e o endereco.
    def __unicode__(self):
        return u'%s - %s | %s' % (self.data.strftime('%d/%m/%Y'), self.patrimonio, self.endereco)



    # Define a descrição do modelo e a ordenação dos dados pelo campo 'nome'.
    class Meta:
        verbose_name = _(u'Histórico Local')
        verbose_name_plural = _(u'Histórico Local')
        ordering = ('-data', )
        unique_together = (('patrimonio', 'endereco', 'descricao', 'data'), )


