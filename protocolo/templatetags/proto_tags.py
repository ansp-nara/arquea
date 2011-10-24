# -*- coding: utf-8 -*-

from django.template import Library
from protocolo.models import Protocolo, Cotacao
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from decimal import Decimal

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
    relatorios = []
    relatorios.append({'url':'/financeiro/relatorios/pagamentos_mes', 'nome':u'Pagamentos por mês'})
    relatorios.append({'url':'/financeiro/relatorios/pagamentos_parcial', 'nome':u'Pagamentos por parcial'})
    relatorios.append({'url':'/financeiro/relatorios/gerencial', 'nome':u'Gerencial'})
    relatorios.append({'url':'/financeiro/relatorios/acordos', 'nome':u'Acordos'})
    relatorios.append({'url':'/financeiro/relatorios/parciais', 'nome':u'Diferenças totais'})
    relatorios.append({'url':'/financeiro/relatorios/caixa', 'nome':u'Diferenças de caixa'})
    relatorios.append({'url':'/financeiro/extrato', 'nome':u'Extrato da conta corrente'})
    relatorios.append({'url':'/financeiro/extrato_mes', 'nome':u'Extrato da conta corrente por mês'})
    relatorios.append({'url':'/financeiro/extrato_tarifas', 'nome':u'Extrato de tarifas por mês'})
    relatorios.append({'url':'/financeiro/extrato_financeiro', 'nome':u'Extrato do financeiro por mês'})
    relatorios.append({'url':'/financeiro/extrato_financeiro_parciais', 'nome':u'Extrato do financeiro por parcial'})
    relatorios.append({'url':'/financeiro/relatorios/prestacao', 'nome':u'Prestação de contas'})
    relatorios.append({'url':'/protocolo/descricao', 'nome':u'Protocolos por descrição'})
    relatorios.append({'url':'/outorga/relatorios/contratos', 'nome':u'Contratos'})
    relatorios.append({'url':'/identificacao/relatorios/arquivos', 'nome':u'Medições de serviços'})
    relatorios.append({'url':'/memorando/relatorio', 'nome':u'Memorandos FAPESP'})
    return {'relatorios':relatorios}


@register.filter(name='moeda')
def moeda(value, nac=1):
    if nac:
        sep = ','
    else:
        sep = '.'

    try:
        v = Decimal(value)
    except:
        return value

    i, d = str(value).split('.')
    s = ''
    if i[0] == '-':
       s = '- '
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
    return '%s %s %s' % (m, s, sep.join((i,d)))

