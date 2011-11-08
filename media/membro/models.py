# -*- coding: utf-8 -*-


from django.db import models
from utils.models import NARADateField
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from dateutil.relativedelta import *

import datetime


#from utils.models import CPFField


#######
class CPFField(models.CharField):
    """
    """
    empty_strings_allowed = False
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        models.CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        from django.contrib.localflavor.br.forms import BRCPFField
        defaults = {'form_class': BRCPFField}
        defaults.update(kwargs)
        return super(models.CharField, self).formfield(**defaults)
######


class Classificacao(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
    	return self.nome

    class Meta:
    	verbose_name = _(u'Classificação')
	verbose_name_plural = _(u'Classificações')

class TipoAssinatura(models.Model):

    """
    Uma instância dessa classe é um tipo de assinatura.

    O método '__unicode__'	Retorna o nome.
    A 'class Meta'		Define a descrição (singular e plural) do modelo e a ordenação  dos dados pelo nome.

    >>> ta, created = TipoAssinatura.objects.get_or_create(nome='Cheque')

    >>> ta.__unicode__()
    u'Cheque'
    """


    nome = models.CharField(_(u'Nome'), max_length=20, help_text=_(u' '), unique=True)


    # Retorna o nome
    def __unicode__(self):
        return u'%s' % self.nome


    # Define a descrição do modelo e a ordenação dos dados pelo nome.
    class Meta:
        verbose_name = _(u'Tipo de Assinatura')
        verbose_name_plural = _(u'Tipos de Assinatura')
        ordering = ("nome", )



class Equipe(models.Model):

    """
    Uma instância dessa classe representa uma equipe de uma entidade.

    O método '__unicode__'		Retorna a entidade e a área.
    A classmethod 'equipes_entidade' 	Retorna as equipes de uma entidade.
    A class 'Meta'			Ordena os dados pelos campos 'entidade' e 'nome' e define que um membro deve ser único pelos campos
					'entidade' e 'nome'.

    >>> from identificacao.models import Entidade

    >>> ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome': 'Academic Network at São Paulo', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> ep, created = Equipe.objects.get_or_create(entidade=ent, area='NARA')

    >>> ep.__unicode__()
    u'ANSP_NARA'

    >>> Equipe.equipes_entidade(ent)
    [<Equipe: ANSP_NARA>]
    """

    entidade = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Entidade'))
    area = models.CharField(_(u'Area'), max_length=50, help_text=_(u'ex. NARA'))
    obs = models.TextField(_(u'Observação'), blank=True)
    membros = models.ManyToManyField('membro.Membro', through='Tarefa')


    # Retorna a sigla da entidade e a área.
    def __unicode__(self):
        return '%s_%s' % (self.entidade.sigla, self.area)


    # Define a ordenação dos dados e a unicidade dos dados.
    class Meta:
        ordering = ('entidade', 'area')
        unique_together = (('entidade', 'area'),)



class Tarefa(models.Model):

    """
    Uma instância dessa classe representa uma conexão entre os modelos equipe e membro.

    O método '__unicode__'		Retorna os campos 'equipe' e 'membro'.
    A classmethod 'membros_equipe'	Retorna as membros de uma equipe.
    A classmethod 'equipes_membro	Retorna as equipes de um membro.
    A class 'Meta'			Ordena os dados pelos campos 'equipe' e 'membro', define o nome do modelo (singular e plural) o a unicidade 
					de uma tarefa pelos campos 'equipe', 'membro' e 'funcao.

    >>> from identificacao.models import Entidade

    >>> ent, created = Entidade.objects.get_or_create(sigla='NEXTEL', defaults={'nome': 'NEXTEL do Brasil Ltda.', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> ent2, created = Entidade.objects.get_or_create(sigla='GTECH', defaults={'nome': 'Graneiro Tech', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> ep, created = Equipe.objects.get_or_create(entidade=ent, area='Diretoria')

    >>> ep2, created = Equipe.objects.get_or_create(entidade=ent2, area='Recursos Humanos')

    >>> mb, created = Membro.objects.get_or_create(nome='Soraya Gomes', funcionario=True, defaults={'cargo': 'Secretaria', 'email': 'soraya@gomes.com', 'cpf': '000.000.000-00'})

    >>> mb2, created = Membro.objects.get_or_create(nome='Jonas Alves', funcionario=True, defaults={'cargo': 'Auxiliar Administrativo', 'email': 'jonas@alves.com', 'cpf': '000.000.000-00'})

    >>> tf, created = Tarefa.objects.get_or_create(equipe=ep, membro=mb, funcao='Preparar memorandos')

    >>> tf2, created = Tarefa.objects.get_or_create(equipe=ep, membro=mb2, funcao='Arquivar documentos')

    >>> tf3, created = Tarefa.objects.get_or_create(equipe=ep2, membro=mb, funcao='Preparar folha de pagamento')

    >>> tf.__unicode__()
    u'NEXTEL_Diretoria_Soraya Gomes'

    >>> Tarefa.membros_equipe(ep)
    [<Tarefa: NEXTEL_Diretoria_Jonas Alves>, <Tarefa: NEXTEL_Diretoria_Soraya Gomes>]

    >>> Tarefa.equipes_membro(mb)
    [<Tarefa: GTECH_Recursos Humanos_Soraya Gomes>, <Tarefa: NEXTEL_Diretoria_Soraya Gomes>]
    """

    equipe = models.ForeignKey('membro.Equipe', verbose_name=_(u'Equipe'))
    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Membro'))
    funcao= models.CharField(_(u'Função'), max_length=100, help_text=_(u'ex. Arquivar documentos'))


    # Retorna a equipe e o membro.
    def __unicode__(self):
        return u'%s_%s' % (self.equipe, self.membro.nome)


    # Define a ordenação e a unicidade dos dados.
    class Meta:
        ordering = ('equipe', 'membro')
        verbose_name = _(u'Identificação do Membro')
        verbose_name_plural = _(u'identificação do Membros')
        unique_together = (('equipe', 'membro', 'funcao'), )



class Membro(models.Model):

    """
    Uma instância dessa classe representa um membro de uma equipe.

    O método '__unicode__'	Retorna os campos 'nome' e 'cargo'.
    O método 'existe_ramal' 	Retorna o campo 'ramal' se estiver preenchido.
    O método 'existe_curriculo' Retorna um ícone com link para o currículo lattes se o campo 'url_lattes' se estiver preenchido.
    A class 'Meta' 		Define a ordenação dos dados pelos campos 'equipe' e 'membro' e define que um membro deve ser único
    				pelos campos 'equipe', 'nome' e 'funcao'.

    >>> from identificacao.models import Entidade

    >>> ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome': 'Academic Network at São Paulo', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> ep, created = Equipe.objects.get_or_create(entidade=ent, area='NARA')

    >>> mb, created = Membro.objects.get_or_create(nome='Joice Gomes', funcionario=True, defaults={'cargo': 'Secretaria', 'email': 'soraya@gomes.com', 'cpf': '000.000.000-00', 'data_admissao': datetime.date(2008,1,1), 'data_demissao': datetime.date(2009,1,1), 'ramal': 23})

    >>> mb.__unicode__()
    'Joice Gomes (Secretaria)' 

    >>> mb.existe_curriculo()
    ''

    >>> mb.existe_ramal()
    23
    """


    nome = models.CharField(_(u'Nome'), max_length=50, help_text=_(u'ex. Caio Andrade'))
    rg = models.CharField(_(u'RG'), max_length=12, help_text=_(u'ex. 00.000.000-0'), blank=True, null=True)
    cpf = CPFField(_(u'CPF'), blank=True, null=True, help_text=_(u'ex. 000.000.000-00'))
    cargo = models.CharField(_(u'Cargo'), max_length=100, blank=True, help_text=_(u'ex. Analista de Sistemas'))
    data_admissao = NARADateField(_(u'Admissão'), help_text=_(u'Data de Admissão'), blank=True, null=True)
    funcionario = models.BooleanField(_(u'Funcionário'))
    email = models.CharField(_(u'E-mail'), max_length=50, blank=True, help_text=_(u'ex. nome@empresa.br'))
    ramal = models.IntegerField(_(u'Ramal'), blank=True, null=True)
    obs = models.TextField(_(u'Observação'), blank=True)
    data_demissao = NARADateField(_(u'Demissão'), help_text=_(u'Data de Demissão'), blank=True, null=True)
    url_lattes = models.URLField(_(u'Currículo Lattes'), verify_exists=True, blank=True, help_text=_(u'URL do Currículo Lattes'))
    foto = models.ImageField(upload_to='membro', blank=True, null=True)
    data_nascimento = NARADateField(_(u'Nascimento'), help_text=_(u'Data de nascimento'), blank=True, null=True)
    classificacao = models.ForeignKey('membro.Classificacao', verbose_name=_(u'Classificação'), blank=True, null=True)


    # Retorna o nome e o cargo.
    def __unicode__(self):
        if self.cargo:
            return '%s (%s)' % (self.nome, self.cargo)
        return '%s' % (self.nome)


    # Verifica se o campo ramal está preenchido.
    def existe_ramal(self):
        if self.ramal:
            return self.ramal
        return ''
    existe_ramal.short_description = _(u'Ramal')


    # Retorna um ícone com o link para o currículo lattes.
    def existe_curriculo(self):
        if self.url_lattes:
            a = '<center><a href="%s"><img src="/site-media/eye.png" /></a></center>' % (self.url_lattes)
            return a
        return ''
    existe_curriculo.allow_tags = True
    existe_curriculo.short_description = _(u'Currículo Lattes')


    # Define a ordenação e unicidade dos dados.
    class Meta:
        ordering = ('nome', )
        unique_together = (('nome', 'funcionario'), )



class Usuario(models.Model):

    """
    Uma instância dessa classe representa um usuário de um sistema.

    O método '__unicode__'		Retorna o campo 'username'.
    A classmethod 'usuarios_sistema'	Retorna os usuários de um sistema.
    A class 'Meta' 			Define a descrição do modelo (singuar e plural), ordena os dados pelos campos 'username' e 
					a unicidade de um usuário pelos campos 'membro', 'username' e 'sistema'.

    >>> from identificacao.models import Entidade

    >>> ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome': 'Academic Network at São Paulo', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> ep, created = Equipe.objects.get_or_create(entidade=ent, area='NARA')

    >>> mb, created = Membro.objects.get_or_create(nome='Soraya Gomes', funcionario=True, defaults={'cargo': 'Secretaria', 'email': 'soraya@gomes.com', 'cpf': '000.000.000-00'})

    >>> usr, created = Usuario.objects.get_or_create(membro=mb, username='soraya', sistema='Administrativo')

    >>> usr.__unicode__()
    'soraya'

    >>> Usuario.usuarios_sistema(usr.sistema)
    [<Usuario: soraya>]
    """

    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Membro'), limit_choices_to=Q(funcionario=True))
    username = models.CharField(_(u'Usuário'), max_length=20, help_text=_(u'Nome de usuário no sistema'))
    sistema = models.CharField(_(u'Sistema'), max_length=50, help_text=_(u'Nome do Sistema'))


    # Retorna o usuário.
    def __unicode__(self):
        return '%s' % (self.username)


    # Define a descrição do modelo, a ordenação e a unicidade dos dados.
    class Meta:
        verbose_name = _(u'Usuário')
        verbose_name_plural = _(u'Usuários')
        ordering = ('username', )
        unique_together = (('membro', 'username', 'sistema'),)



class Assinatura(models.Model):

    """
    Uma instância dessa classe representa uma assinatura de um membro.

    O método '__unicode__'		Retorna os campos 'membro' e 'tipo_assinatura'.
    A classmethod 'assinaturas_membro'	Retorna as assinaturas de um membro específico.
    A class 'Meta'			Define a ordenação dos dados pelo 'nome' e unicidade pelos campos 'tipo_assinatura' e 'membro'.

    >>> from identificacao.models import Entidade

    >>> ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome': 'Academic Network at São Paulo', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> ep, created = Equipe.objects.get_or_create(entidade=ent, area='NARA')

    >>> mb, created = Membro.objects.get_or_create(nome='Soraya Gomes', funcionario=True, defaults={'cargo': 'Secretaria', 'email': 'soraya@gomes.com', 'cpf': '312.617.028-00'})

    >>> ta, created = TipoAssinatura.objects.get_or_create(nome='Cheque')

    >>> a, created = Assinatura.objects.get_or_create(membro=mb, tipo_assinatura=ta)

    >>> a.__unicode__()
    u'Soraya Gomes | Cheque'

    >>> Assinatura.assinaturas_membro(a.membro)
    [<Assinatura: Soraya Gomes | Cheque>]
    """

    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Membro'), limit_choices_to=Q(funcionario=True))
    tipo_assinatura = models.ForeignKey('membro.TipoAssinatura', verbose_name=_(u'Tipo de Assinatura'))


    # Retorna o membro e o tipo de assinatura.
    def __unicode__(self):
        return u'%s | %s' % (self.membro.nome, self.tipo_assinatura)


    # Define a ordenação e a unicidade dos dados.
    class Meta:
        ordering = ('membro', )
        unique_together = (('membro', 'tipo_assinatura'),)



class Ferias(models.Model):

    """
    Uma instância dessa classe representa as férias de um membro.

    O método '__unicode__'		Retorna o membro e o período de férias (campos 'membro', 'periodo_escolha_inic' e 'periodo_escolha_term').
    O método 'dt_trab'			Retorna as datas de início e término do perído de trabalho no formato dd/mm/aaaa.
    O método 'dt_ferias'		Retorna as datas de início e término do perído de férias no formato dd/mm/aaaa.
    O método 'qtde_dias'		Retorna a diferença (em dias) entre os campos 'periodo_escolha_inic' e 'periodo_escolha_term'.
    A classmethod 'ferias_membro'	Retorna as férias de um membro.
    A class 'Meta'			Define a descrição do modelo (singular e plural), ordenação dos dados pelo campo 'periodo_escolha_inic' 
    					e a unicidade dos dados pelos campos 'membro', 'periodo_trab_inicio' e 'periodo_trab_termino'.

    >>> from identificacao.models import Entidade

    >>> ent, created = Entidade.objects.get_or_create(sigla='ANSP', defaults={'nome': 'Academic Network at São Paulo', 'cnpj': '', 'ativo': True, 'fisco': True })

    >>> ep, created = Equipe.objects.get_or_create(entidade=ent, area='NARA')

    >>> mb, created = Membro.objects.get_or_create(nome='Soraya Gomes', funcionario=True, defaults={'cargo': 'Secretaria', 'email': 'soraya@gomes.com', 'cpf': '000.000.000-00'})

    >>> f, created = Ferias.objects.get_or_create(membro=mb, periodo_compl_trab_inicio=datetime.date(2008,1,1),  periodo_compl_trab_termino=datetime.date(2009,1,1), defaults={'periodo_escolha_inic': datetime.date(2009,5,1), 'periodo_escolha_term': datetime.date(2009,5,30)})

    >>> Ferias.ferias_membro(mb)
    [<Ferias: Soraya Gomes (Secretaria) | Férias: 01/05/2009 - 30/05/2009>]
    """


    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Membro'), limit_choices_to=Q(funcionario=True))
    trab_inicio = NARADateField(_(u'Início'), help_text=_(u'Início do período de trabalho'))
    completo = models.BooleanField(_(u'Completo'), help_text=_(u'Período aquisitivo completo?'), default=True)
    periodo_escolha_inic = NARADateField(_(u'Início'), help_text=_(u'Início das férias (oficial)'), blank=True, null=True)
    periodo_escolha_term = NARADateField(_(u'Término'), help_text=_(u'Término das férias (oficial)'), blank=True, null=True)
    obs = models.TextField(_(u'Observação'), blank=True)


    # Retorna o membro e o período de férias.
    def __unicode__(self):
        if self.periodo_escolha_inic and self.periodo_escolha_term:
            return u'%s | Férias: %s - %s' % (self.membro, self.periodo_escolha_inic, self.periodo_escolha_term)
        else:
            return u'%s | Férias: Não definida' % (self.membro)

    @property
    def trab_termino(self):
	return self.trab_inicio+relativedelta(days=+365)

    # Retorna quantos dias de férias foi solicitado.
    def qtde_dias(self):
        if self.periodo_escolha_inic and self.periodo_escolha_term:
            dias = self.periodo_escolha_term - self.periodo_escolha_inic
            dias = dias.days + 1
            return '%s dias' % dias
        return ''
    qtde_dias.short_description = _(u'Dias solicitados')


    # Define a descrição do modelo, ordenação e a unicidade dos dados.
    class Meta:
        verbose_name = _(u'Férias')
        verbose_name_plural = _(u'Férias')
        ordering = ('-periodo_escolha_inic', )
        unique_together = (('membro', 'trab_inicio'),)


class ControleFerias(models.Model):
    """
    Controle efetivo das férias, com as datas reais de saída e retorno
    """
    ferias = models.ForeignKey('membro.Ferias')
    inicio = NARADateField()
    termino = NARADateField()
    justificiativa = models.TextField()

    def __unicode__(self):
	return "%s - %s", (self.inicio, self.termino)


class DispensasLegais(models.Model):
    """
    Dispensas legais, como por exemplo dispensa médica, para trabalho em eleição, luto, casamento, etc
    """
    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Membro'), limit_choices_to=Q(funcionario=True))
    justificativa = models.TextField()
    inicio_direito = NARADateField()
    dias_uteis = models.IntegerField()
    inicio_realizada = NARADateField()
    cumprida = models.BooleanField()
    atestado = models.BooleanField()
    arquivo = models.FileField(upload_to='/dispensas/')

    def __unicode__(self):
	return "%s - %s" % (self.membro, self.justificativa)

class Banco(models.Model):

    """
    Tabela para guardar os números e nomes dos bancos, com atualização automática periódica.

    O método '__unicode__'	Retorna o nome e o número do banco.
    A class 'Meta'		Define a ordenação dos dados pelo nome do banco.

    >>> b = Banco(numero=151, nome='Nossa Caixa')
    >>> b.save()

    >>> b.__unicode__()
    u'Nossa Caixa (151)'
    """

    numero = models.IntegerField()
    nome = models.CharField(max_length=100)


    # Define a ordenação dos dados pelo nome.
    class Meta:
        ordering = ('nome',)


    # Retorna o nome e o número do banco.
    def __unicode__(self):
        return u'%s (%03d)' % (self.nome, self.numero)



class DadoBancario(models.Model):

    """
    Uma instância dessa classe representa os dados bancários de uma entidade ou um contato.

    O método '__unicode__'	Retorna os dados bancários (banco + agência + conta).
    O método 'agencia_digito'	Retorna o número da agência + o dígito.
    O método 'conta_digito'	Retorna o número da conta + o dígito.
    A class 'Meta'		Define a descrição do modelo (singular e plural), a ordenação dos dados pelo 'banco' e a unicidade dos
				dados pelos campos 'banco', 'agencia', 'ag_digito', 'conta', 'cc_digito'.

    >>> mb, created = Membro.objects.get_or_create(nome='Soraya Gomes', funcionario=True, defaults={'cargo': 'Secretaria', 'email': 'soraya@gomes.com', 'cpf': '000.000.000-00'})

    >>> b = Banco(numero=151, nome='Nossa Caixa')
    >>> b.save()

    >>> db, created = DadoBancario.objects.get_or_create(membro=mb, banco=b, agencia=1690, ag_digito=4, conta=123439, cc_digito='x')

    >>> db.agencia_digito()
    '1690-4'

    >>> db.conta_digito()
    '123439-x'
    """


    membro = models.OneToOneField('membro.Membro', verbose_name=_(u'Membro'))
    banco = models.ForeignKey('membro.Banco', verbose_name=_(u'Banco'))
    agencia = models.IntegerField(_(u'Ag.'), help_text=_(u'ex. 0909'))
    ag_digito = models.IntegerField(' ', blank=True, null=True, help_text=_(u'ex. 9'))
    conta = models.IntegerField(_(u'CC'), help_text=_(u'ex. 01222222'))
    cc_digito = models.CharField(' ', max_length=1, blank=True, help_text=_(u'ex. x'))


    # Retorna o banco, a agência e o número da conta.
    def __unicode__(self):
        if self.ag_digito:
            ag = '%s-%s' % (self.agencia, self.ag_digito)
        else:
            ag = '%s' % (self.agencia)

        if self.cc_digito:
            cc = '%s-%s' % (self.conta, self.cc_digito)
        else:
            cc = '%s' % (self.conta)

        return u'%s AG. %s CC %s' % (self.banco, ag, cc)


    # Define a descrição do modelo, a ordenação dos dados pelo banco e a unicidade dos dados.
    class Meta:
        verbose_name = _(u'Dados bancários')
        verbose_name_plural = _(u'Dados bancários')
        ordering = ('banco', )
        unique_together = (('banco', 'agencia', 'ag_digito', 'conta', 'cc_digito'),)


    # Retorna o número da agência completo (agência + dígito)
    def agencia_digito(self):
        if self.agencia or self.ag_digito:
            if self.ag_digito:
                return '%s-%s' % (self.agencia, self.ag_digito)
            else:
                return self.agencia
        return ' '
    agencia_digito.short_description = _(u'Agência')


    # Retorna o número da conta completo (conta + dígito)
    def conta_digito(self):
        if self.conta or self.cc_digito:
            if self.cc_digito:
                return '%s-%s' % (self.conta, self.cc_digito)
            else:
                return self.conta
        return ' '
    conta_digito.short_description = _(u'Conta')

