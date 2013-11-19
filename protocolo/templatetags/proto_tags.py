# -*- coding: utf-8 -*-

from django.template import Library
from protocolo.models import Protocolo, Cotacao
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from decimal import Decimal
from django.shortcuts import get_object_or_404
from membro.models import Membro
import math


import logging



register = Library()

@register.inclusion_tag('admin/protocolo/protocolo/vencendo.html')
def mostra_vencer():
    choices =  [p for p in Protocolo.objects.all() if p.pagamentos_amanha()]
    return {'existe': len(choices), 'choices' : choices}

@register.simple_tag
def detalha_externo(field):
    
    try:
        rel = field.field.widget.rel.to
        if rel in field.field.widget.admin_site._registry:
            url = "'../../../%s/%s/'" % (rel._meta.app_label, rel._meta.object_name.lower())
            return mark_safe('<a href="javascript:void(0);" id="detail_%s" onclick="window.open(%s+document.forms[0][\'%s\'].value+\'/\');">%s</a>' %
                (rel._meta.object_name.lower(), url, field.html_name, 'Detalhe'))
        else:
            return ''
    except:
        return ''

@register.simple_tag
def link_cotacao(pk):
    try:
        p = Protocolo.objects.get(pk=pk)
    except Protocolo.DoesNotExist:
        return ''
    
    try:
        c = p.cotacao
    except Cotacao.DoesNotExist:
        return ''
    
    return mark_safe('<a href="/protocolo/%s/cotacoes">%s</a>' % (pk, _(u'Ver cotações')))

@register.inclusion_tag('admin/relatorios.html')
def lista_relatorios():
    gerenciais = []
    administrativos = []
    tecnicos = []
    verificacoes = []
    
    administrativos.append({'url':'/financeiro/relatorios/pagamentos_mes', 'nome':u'Pagamentos por mês'})
    administrativos.append({'url':'/financeiro/relatorios/pagamentos_parcial', 'nome':u'Pagamentos por parcial'})
    gerenciais.append({'url':'/financeiro/relatorios/gerencial', 'nome':u'Gerencial'})
    gerenciais.append({'url':'/financeiro/relatorios/acordos', 'nome':u'Acordos'})
    administrativos.append({'url':'/financeiro/relatorios/parciais', 'nome':u'Diferenças totais'})
    administrativos.append({'url':'/financeiro/relatorios/caixa', 'nome':u'Diferenças de caixa'})
    administrativos.append({'url':'/financeiro/extrato', 'nome':u'Extrato da conta corrente'})
    administrativos.append({'url':'/financeiro/extrato_mes', 'nome':u'Extrato da conta corrente por mês'})
    administrativos.append({'url':'/financeiro/extrato_tarifas', 'nome':u'Extrato de tarifas por mês'})
    administrativos.append({'url':'/financeiro/extrato_financeiro', 'nome':u'Extrato do financeiro por mês'})
    administrativos.append({'url':'/financeiro/extrato_financeiro_parciais', 'nome':u'Extrato do financeiro por parcial'})
    administrativos.append({'url':'/financeiro/relatorios/prestacao', 'nome':u'Prestação de contas'})
    administrativos.append({'url':'/protocolo/descricao', 'nome':u'Protocolos por descrição'})
    gerenciais.append({'url':'/outorga/relatorios/contratos', 'nome':u'Contratos'})
    tecnicos.append({'url':'/identificacao/relatorios/arquivos', 'nome':u'Documentos por entidade'})
    administrativos.append({'url':'/memorando/relatorio', 'nome':u'Memorandos FAPESP'})
    gerenciais.append({'url':'/outorga/relatorios/lista_acordos', 'nome':u'Concessões por  acordo'})
    administrativos.append({'url':'/outorga/relatorios/item_modalidade', 'nome':u'Itens do orçamento por modalidade'})
    tecnicos.append({'url':'/patrimonio/relatorio/por_estado', 'nome':u'Patrimônio por estado do item'})
    tecnicos.append({'url':'/patrimonio/relatorio/por_local', 'nome':u'Patrimônio por localização'})
    tecnicos.append({'url':'/patrimonio/relatorio/por_local_termo', 'nome':u'Patrimônio por localização e termo'})
    tecnicos.append({'url':'/patrimonio/relatorio/por_tipo', 'nome':u'Patrimônio por tipo'})
    administrativos.append({'url':'/identificacao/agenda', 'nome':u'Agenda'})
    administrativos.append({'url':'/identificacao/ecossistema/par', 'nome':u'Ecossistema'})
    administrativos.append({'url':'/membro/mensalf', 'nome':u'Controle de horário mensal'})
    gerenciais.append({'url':'/outorga/relatorios/acordo_progressivo', 'nome':u'Gerencial progressivo'})
    gerenciais.append({'url':'/processo/processos', 'nome':u'Processos'})
    gerenciais.append({'url':'/rede/custo_terremark', 'nome':u'Custos dos recursos contratados'})
    tecnicos.append({'url':'/rede/planejamento', 'nome':u'Planejamento por ano'})
    tecnicos.append({'url':'/rede/planejamento2', 'nome':u'Serviços contratados por processo'})
    tecnicos.append({'url':'/rede/info', 'nome':u'Dados cadastrais dos participantes'})
    administrativos.append({'url':'/patrimonio/relatorio/por_termo', 'nome':u'Patrimônio por termo de outorga'})
    tecnicos.append({'url':'/patrimonio/racks', 'nome':u'Racks (em construção)'})
    tecnicos.append({'url':'/patrimonio/relatorio/por_marca', 'nome':u'Patrimônio por marca'})
    administrativos.append({'url':'/logs', 'nome':u'Registro de uso do sistema por ano'})
    tecnicos.append({'url':'/rede/blocosip', 'nome':u'Lista de blocos IP'})
    tecnicos.append({'url':'/patrimonio/relatorio/por_tipo_equipamento2', 'nome':u'Patrimônio por tipo de equipamento'})
    administrativos.append({'url':'/patrimonio/relatorio/presta_contas', 'nome':u'Prestação de contas patrimonial (em construção)'})
    tecnicos.append({'url':'/patrimonio/relatorio/por_tipo_equipamento', 'nome':u'Busca por tipo de equipamento'})
    
    verificacoes.append({'url':'/verificacao/relatorio/equipamento_consolidado', 'nome':u'Verificação de equipamentos'})
    verificacoes.append({'url':'/verificacao/relatorio/patrimonio_consolidado', 'nome':u'Verificação de patrimônio'})
    verificacoes.append({'url':'/carga/', 'nome':u'Carga de planilha de patrimônio'})

    gerenciais.sort(key=lambda x: x['nome'])
    administrativos.sort(key=lambda x: x['nome'])
    tecnicos.sort(key=lambda x: x['nome'])
    verificacoes.sort(key=lambda x: x['nome'])
    
    return {'relatorios':[{'nome':u'gerenciais', 'rel':gerenciais}, 
                          {'nome':u'administrativos', 'rel':administrativos}, 
                          {'nome':u'técnicos', 'rel':tecnicos},
                          {'nome':u'de verificações (Acesso restrito)', 'rel':verificacoes}], 
            }



@register.filter(name='moeda_css')
def moeda_css(value, nac=1):
    """
    Novo metodo para formatar o valor em moeda, com valor negativo em cor vermelha em css 
    """
    return moeda(value, nac, False, True)

@register.filter(name='moeda_valor')
def moeda_valor(value, nac=1):
    """
    Novo metodo para formatar o valor em moeda, mas remover o prefixo da moeda (ex: R$)
    """
    return moeda(value, nac, True, False)

@register.filter(name='moeda_valor_css')
def moeda_valor_css(value, nac=1):
    """
    Novo metodo para formatar o valor em moeda, mas remover o prefixo da moeda (ex: R$), com valor negativo em cor vermelha em css
    """
    return moeda(value, nac, True, True)
    
@register.filter(name='moeda')
def moeda(value, nac=True, nosep=False, css=False):
    logger = logging.getLogger('prototags')
    


    if nac:
        sep = ','
    else:
        sep = '.'

    try:
        v = Decimal(value)
    except:
        return value

    i, d = str(value).split('.')
    
    # Corrigindo o tamanho da decimal para 2 dígitos
    if len(d) > 2: d = d[:2]
    if len(d) == 1: d = d[:1] + '0'
    
    s = '%s'
    ## Verifica se adiciona () para números negativos
    ## Se for especificado como CSS, o tratamento ocorre no final
    if i[0] == '-':
        i = i[1:len(i)]

    res = []
    p = len(i)
    while p > 2:
        res.append(i[p-3:p])
        p -= 3
    if p > 0:
        res.append(i[0:p])

    si = '.'
    m = 'R$'
    if sep == '.':
        si = ','
        m = 'US$'
        
    res.reverse()
    i = si.join(res)
    
    # valor com os separadores
    valor = s % (sep.join((i,d)))
    
    # tratamento de negativos
    if v < 0:
        if css == False:
            valor = '(%s)'%valor
        else:
            valor = '-%s'%valor

    # Juntando o número, separador de dígito, e digitos
    # Adiciona, ou não, o valor de moeda
    retorno = None
    if nosep:
        retorno = valor
    else:
        retorno = '%s %s' % (m, valor)
    
    # Faz o tratamento de negativo utilizando CSS com cor vermelha
    if css and v < 0:
        retorno = '<span style="color: red">%s</span>' % (retorno) 
    
    return mark_safe(retorno)
    
    

@register.inclusion_tag('membro/controle.html')
def controle_horario(user):
    try:
        membro = Membro.objects.get(contato__email=user.email)
    except Membro.DoesNotExist:
        return {'acao':None}

    controles = membro.controle_set.all()
    acao = u'entrada'
    if controles:
        controle = controles[0]
        if controle.saida == None: acao = u'saída'

    return {'acao':acao, 'user':user.first_name}


@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )