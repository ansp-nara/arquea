# -*- coding: utf-8 -*-


from django.db import models
from utils.models import CNPJField
from utils.models import NARADateField
from django.utils.translation import ugettext_lazy as _
from datetime import datetime


# Create your models here.



class Contato(models.Model):

    """
    Uma instância dessa classe representa um contato.

    O método '__unicode__'	Retorna o nome.
    O método 'contato_ent'	Retorna as entidades do contato.
    A 'class Meta'		Ordena os dados pelo campo 'nome'.

    >>> ent1, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'Global Crossing', 'cnpj': '00.000.000/0000-00', 'ativo': False, 'fisco': True, 'url': '', 'asn': 123})

    >>> ent2, created = Entidade.objects.get_or_create(sigla='GTECH', defaults={'nome': 'Graneiro Tech', 'cnpj': '00.000.000/0000-00', 'ativo': False, 'fisco': True, 'url': '', 'asn': 321})

    >>> c, created = Contato.objects.get_or_create(nome='Joao', defaults={'email':'joao@joao.com.br', 'tel': '', 'ativo': True})

    >>> iden1, created = Identificacao.objects.get_or_create(entidade=ent1, contato=c, defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True})

    >>> iden2, created = Identificacao.objects.get_or_create(entidade=ent2, contato=c, defaults={'funcao': 'Gerente', 'area': '', 'ativo': True})

    >>> c.__unicode__()
    'Joao'

    >>> c.contato_ent()
    u'GTECH, SAC'
    """


    nome = models.CharField(_(u'Nome'), max_length=100, help_text=_(u'ex. João Andrade'), unique=True)
    email = models.CharField(_(u'E-mail'), max_length=100, blank=True, help_text=_(u'ex. joao@joao.br'))
    ativo = models.BooleanField(_(u'Ativo'))
    tel = models.CharField(_(u'Telefone'), max_length=100, help_text=_(u'ex. Com. (11)2222-2222, Cel. (11)9999-9999, Fax (11)3333-3333, ...'))


    # Retorna o nome.
    def __unicode__(self):
        return self.nome


    # Retorna as entidades do contato.
    def contato_ent(self):
        ident = self.identificacao_set.all()
        ent = []
        for i in ident:
            if i.endereco.entidade not in ent:
                ent.append(i.endereco.entidade)
        l = [e.sigla for e in ent]
        e = ', '.join(l)
        return u'%s' % (e)
    contato_ent.short_description = _(u'Entidade')


    # Define a ordenação dos dados pelo nome.
    class Meta:
        ordering = ('nome', )


class TipoDetalhe(models.Model):
    nome = models.CharField(max_length=40)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)

class EnderecoDetalhe(models.Model):
    endereco = models.ForeignKey('identificacao.Endereco', null=True, blank=True)
    tipo = models.ForeignKey('identificacao.TipoDetalhe')
    complemento = models.TextField()
    detalhe = models.ForeignKey('identificacao.EnderecoDetalhe', verbose_name=u'ou Detalhe pai', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.endereco == None and self.detalhe == None:
            return
        if self.endereco != None and self.detalhe != None:
            return
        super(EnderecoDetalhe,self).save(*args,**kwargs)


    def __unicode__(self):
        return self.complemento


class Endereco(models.Model):

    """
    Uma instância dessa classe representa um endereco de uma identificação.

    O método '__unicode__'	Retorna os campos 'rua', 'num' e 'compl' (se existir).
    A 'class Meta'		Define a descrição do modelo (singular e plural), a ordenação dos dados e a unicidade que um endereço pelos 
			    	campos 'identificacao', 'rua', 'num', 'compl', 'bairro', 'cidade', 'cep', 'estado' e 'pais'.

    >>> ent, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'Global Crossing', 'cnpj': '00.000.000/0000-00', 'ativo': False, 'fisco': True, 'url': '', 'asn': 123})

    >>> c, created = Contato.objects.get_or_create(nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': '', 'ativo': True})

    >>> iden, created = Identificacao.objects.get_or_create(entidade=ent, contato=c, defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True})

    >>> end, created = Endereco.objects.get_or_create(identificacao=iden, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010', estado='SP', pais='Brasil')

    >>> end.__unicode__()
    'Dr. Ovidio, 215'
    """

    entidade = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Entidade'))
    rua = models.CharField(_(u'Logradouro'), max_length=100, help_text=_(u'ex. R. Dr. Ovídio Pires de Campos'))
    num = models.IntegerField(_(u'Num.'), help_text=_(u'ex. 215'))
    compl = models.CharField(_(u'Complemento'), max_length=100, blank=True, help_text=_(u'ex. 2. andar - Prédio da PRODESP'))
    bairro = models.CharField(_(u'Bairro'), max_length=50, blank=True, help_text=_(u'ex. Cerqueira César'))
    cidade =  models.CharField(_(u'Cidade'), max_length=50, blank=True, help_text=_(u'ex. São Paulo'))
    cep = models.CharField(_(u'CEP'), max_length=8, blank=True, help_text=_(u'ex. 05403010'))
    estado = models.CharField(_(u'Estado'), max_length=50, blank=True, help_text=_(u'ex. SP'))
    pais = models.CharField(_(u'País'), max_length=50, blank=True, help_text=_(u'ex. Brasil'))
    data_inatividade = models.DateField(_(u'Data de inatividade'), blank=True, null=True)

    # Retorna os campos rua, num e compl (se existir).
    def __unicode__(self):
        if self.compl:
            return u'%s - %s, %s, %s' % (self.entidade.sigla, self.rua, self.num, self.compl)
        else:
            return u'%s - %s, %s' % (self.entidade.sigla, self.rua, self.num)
    __unicode__.short_description = _(u'Logradouro')


    # Define a descricao do modelo, a ordenação dos dados pela cidade e a unicidade dos dados.
    class Meta:
        verbose_name = _(u'Endereço')
        verbose_name_plural = _(u'Endereços')
        ordering = ('entidade', )
        unique_together = (('rua', 'num', 'compl', 'bairro', 'cidade', 'cep', 'estado', 'pais'),)



class ASN(models.Model):
    """
    Tabela com os ASs da Internet
    """

    numero = models.IntegerField(u'Número do AS')
    entidade = models.ForeignKey('identificacao.Entidade', null=True, blank=True)
    pais = models.CharField(u'País', null=True, blank=True, max_length=3)

    def __unicode__(self):
	if self.entidade:
	    return '%s - %s' % (self.numero, self.entidade)
        else: return self.numero

    class Meta:
        verbose_name = (u'ASN')
        verbose_name_plural = (u'ASNs')
        ordering = ('numero',)

class Entidade(models.Model):

    """
    Uma instância dessa classe representa uma entidade cadastrada no sistema.

    O método '__unicode__'	Retorna a sigla da entidade.
    O método 'sigla_nome'	Retorna a sigla e o nome da entidade.
    O método 'save'		Faz a validação do CNPJ e converte todos os caracteres da sigla para maiúsculo.
    A 'class Meta' 		Define a ordenação dos dados pela sigla.

    A unicidade dos dados é feita através do campo 'sigla'.

    >>> from utils.models import CNPJField

    >>> e, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'Global Crossing', 'cnpj': '00.000.000/0000-00', 'ativo': False, 'fisco': True, 'url': '', 'asn': 123})

    >>> e.sigla_nome()
    u'SAC - Global Crossing'
    """

    entidade = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Faz parte de'), null=True, blank=True, related_name='entidade_em')
    nome = models.CharField(_(u'Nome'), max_length=255, help_text=_(u'Razão Social (ex. Telecomunicações de São Paulo S.A.)'))
    url = models.URLField(_(u'URL'), verify_exists=True, blank=True, help_text=_(u'ex. www.telefonica.com.br'))
    sigla = models.CharField(_(u'Sigla'), max_length=20, help_text=_(u'Nome Fantasia (ex. TELEFÔNICA)'), unique=True)
    pertence = models.BooleanField(u'Pertence à ANSP?')
    cnpj = CNPJField(_(u'CNPJ'), blank=True, help_text=_(u'ex. 00.000.000/0000-00'))
    fisco = models.BooleanField(_(u'Fisco'), help_text=_(u'ex. Ativo no site da Receita Federal?'))


    # Retorna a sigla.
    def __unicode__(self):
        return self.sigla

    def sigla_completa(self):
        if self.entidade:
           return u'%s - %s' % (self.entidade.sigla_completa(), self.sigla)
        else:
           return u'%s' % self.sigla
    sigla_completa.short_description = _(u'Faz parte de')

    # Retorna a sigla e o nome.
    def sigla_nome(self):
        return u'%s - %s' % (self.sigla, self.nome)
    sigla_nome.short_description = _(u'Entidade')


    # Grava o CNPJ no banco de dados com as devidas pontuações e converte a sigla em letras maiúsculas.
    def save(self, force_insert=False, force_update=False):
        if self.cnpj and len(self.cnpj) < 18:
            a = list(self.cnpj)
            p = [(2,'.'), (6,'.'), (10,'/'), (15,'-')]
            for i in p:
                if i[1] != a[i[0]]:
                    a.insert(i[0],i[1])
            self.cnpj = ''.join(a)
        self.sigla = self.sigla.upper()
        super(Entidade,self).save(force_insert, force_update)


    # Define a ordenação dos dados pela sigla.
    class Meta:
        ordering = ('sigla', )

class EntidadeHistorico(models.Model):
    inicio = models.DateField()
    termino = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(_(u'Ativo'))
    obs = models.TextField(_(u'Observação'), blank=True, null=True)
    entidade = models.ForeignKey('identificacao.Entidade')
    tipo = models.ForeignKey('identificacao.TipoEntidade')

    def __unicode__(self):
        return '%s %s %s' % (self.entidade.sigla, self.tipo.nome, self.inicio)


class Identificacao(models.Model):

    """
    Uma instância dessa classe representa uma identificação de uma empresa, fornecedor ou contato.

    O método 'formata_historico'	Retorna o histórico no formato dd/mm/aa hh:mm
    O método '__unicode__'		Retorna sigla da entidade e o nome do contato.
    A 'class Meta'			Define a descrição do modelo (singular e plural), a ordenação dos dados pela entidade e a unicidade dos
    					dados pelos campos contato, entidade.

    >>> ent, created = Entidade.objects.get_or_create(sigla='SAC', defaults={'nome': 'Global Crossing', 'cnpj': '00.000.000/0000-00', 'ativo': False, 'fisco': True, 'url': '', 'asn': 123})

    >>> c, created = Contato.objects.get_or_create(nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': '', 'ativo': True})

    >>> iden, created = Identificacao.objects.get_or_create(entidade=ent, contato=c, defaults={'funcao':'Tecnico', 'area':'', 'ativo': True})

    >>> iden.__unicode__()
    u'SAC_Joao'
    """


#    monitor = models.ForeignKey('rede.Monitor', verbose_name=_(u'Monitor'))
    endereco = models.ForeignKey('identificacao.Endereco', verbose_name=_(u'Entidade'))
    contato = models.ForeignKey('identificacao.Contato', verbose_name=_(u'Contato'))
    historico = models.DateTimeField(_(u'Histórico'), default=datetime.now(), editable=False)
    area = models.CharField(_(u'Área'), max_length=50, blank=True, help_text=_(u'ex. Administração'))
    funcao = models.CharField(_(u'Função'), max_length=50, blank=True, help_text=_(u'ex. Gerente Administrativo'))
    ativo = models.BooleanField(_(u'Ativo'))


    # Define a descrição do modelo, a ordenação dos dados pela entidade e a unicidade dos dados.
    class Meta:
        verbose_name = _(u'Identificação')
        verbose_name_plural = _(u'Identificações')
        ordering = ('endereco', 'contato')
        unique_together = (('endereco', 'contato'),)


    # Retorna a sigla da entidade e o nome do contato.
    def __unicode__(self):
        if self.area:
            return u'%s - %s - %s' % (self.endereco.entidade, self.area, self.contato.nome)
        else:
            return u'%s - %s' % (self.endereco.entidade, self.contato.nome)


    # Retorna o histórico formatado.
    def formata_historico(self):
        return self.historico.strftime('%d/%m/%y %H:%M')
    formata_historico.short_description = _(u'Histórico')

class TipoArquivoEntidade(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome
  
    class Meta:
        ordering = ('nome',)

class ArquivoEntidade(models.Model):
    arquivo = models.FileField(upload_to='entidade')
    entidade = models.ForeignKey('identificacao.Entidade')
    data = models.DateField()
    tipo = models.ForeignKey('identificacao.TipoArquivoEntidade')
  
    def __unicode__(self):
	return '%s - %s' % (self.entidade.sigla, self.arquivo.name)

    class Meta:
        ordering = ('tipo', '-data')

class TipoEntidade(models.Model):
    nome = models.CharField(max_length=20)
    
    def __unicode__(self):
	return self.nome

    class Meta:
        ordering = ('nome',)
	
class PapelEntidade(models.Model):
    data = models.DateField()
    tipo = models.ForeignKey('identificacao.TipoEntidade')
    entidade = models.ForeignKey('identificacao.Entidade')
      
    def __unicode__(self):
        return '%s - %s' % (self.entidade, self.tipo)
	 

class Agenda(models.Model):
    nome = models.CharField(max_length=40)
    entidades = models.ManyToManyField('identificacao.Entidade', through='Agendado')

    def __unicode__(self):
        return u'%s' % self.nome

class Agendado(models.Model):
    agenda = models.ForeignKey('identificacao.Agenda')
    entidade = models.ForeignKey('identificacao.Entidade')
    ativo = models.BooleanField()

    def __unicode__(self):
        return u'%s - %s' % (self.agenda.nome, self.entidade.sigla)

class Acesso(models.Model):
    identificacao = models.ForeignKey('identificacao.Identificacao', verbose_name=u'Identificação')
    niveis = models.ManyToManyField('identificacao.NivelAcesso', verbose_name=u'Níveis de acesso')
    liberacao = models.DateField(u'Liberação')
    encerramento = models.DateField(null=True, blank=True)
    obs = models.TextField()
    detalhe = models.ManyToManyField('identificacao.EnderecoDetalhe', null=True, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.identificacao, self.nivel)

class NivelAcesso(models.Model): 
    nivel = models.IntegerField(u'Nível')
    explicacao = models.TextField('Explicação')

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = u'Nível de acesso'
        verbose_name_plural = u'Níveis de acesso'

