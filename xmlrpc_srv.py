# Patchless XMLRPC Service for Django
# Kind of hacky, and stolen from Crast on irc.freenode.net:#django
# Self documents as well, so if you call it from outside of an XML-RPC Client
# it tells you about itself and its methods
#
# Brendan W. McAdams <brendan.mcadams@thewintergrp.com>

# SimpleXMLRPCServer lets us register xml-rpc calls w/o
# running a full XMLRPC Server.  It's up to us to dispatch data

from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
from django.db.models import Sum
from membro.models import *
import xmlrpclib
from django.views.decorators.csrf import csrf_exempt
from outorga.models import Termo, OrigemFapesp, Acordo, Modalidade, Natureza_gasto
from decimal import Decimal
from financeiro.models import Pagamento
from datetime import datetime,timedelta

# Create a Dispatcher; this handles the calls and translates info to function maps
#dispatcher = SimpleXMLRPCDispatcher() # Python 2.4
dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None) # Python 2.5

 
@csrf_exempt
def rpc_handler(request):
        """
        the actual handler:
        if you setup your urls.py properly, all calls to the xml-rpc service
        should be routed through here.
        If post data is defined, it assumes it's XML-RPC and tries to process as such
        Empty post assumes you're viewing from a browser and tells you about the service.
        """

        if len(request.POST):
                response = HttpResponse(mimetype="application/xml")
                response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
        else:
                response = HttpResponse()
                response.write("<b>This is an XML-RPC Service.</b><br>")
                response.write("You need to invoke it using an XML-RPC Client!<br>")
                response.write("The following methods are available:<ul>")
                methods = dispatcher.system_listMethods()

                for method in methods:
                        # right now, my version of SimpleXMLRPCServer always
                        # returns "signatures not supported"... :(
                        # but, in an ideal world it will tell users what args are expected
                        sig = dispatcher.system_methodSignature(method)

                        # this just reads your docblock, so fill it in!
                        help =  dispatcher.system_methodHelp(method)

                        response.write("<li><b>%s</b>: [%s] %s" % (method, sig, help))

                response.write("</ul>")
                response.write('<a href="http://www.djangoproject.com/"> <img src="http://media.djangoproject.com/img/badges/djangomade124x25_grey.gif" border="0" alt="Made with Django." title="Made with Django."></a>')

        response['Content-length'] = str(len(response.content))
        return response

def membros():
    """
    Retorna uma lista dos membros que devem aparecer no site da ANSP, com nome, cargo, email,
    url para o curriculo Lattes e foto.
    """
    import re
    mb = []
    for m in Membro.objects.filter(site=True,historico__termino__isnull=True):
        c = Cargo.objects.filter(nome=m.cargo_atual())
        if c:
            mb.append((m,c[0].hierarquia or 9999999))
        else:
            mb.append((m,9999999))
    mb.sort(key=lambda x: x[1])
    retorno = []
    for m,h in mb:
        membro = {'nome':m.nome, 'cargo':m.cargo_atual(), 'email':m.email, 'lattes':m.url_lattes}
        if m.foto:
	    fname = '_'.join(m.nome.split()[:4]).lower()
	    fname = re.sub('[^\w]', '', fname)
	    membro.update({'foto':xmlrpclib.Binary(m.foto.file.read()), 'fname':fname})
	retorno.append(membro)    
    return retorno

dispatcher.register_function(membros, 'membros')


def termos():
    """
    Uma lista dos termos de outorga
    """
    retorno = []
    for t in Termo.objects.all():
        retorno.append({'id':t.id, 'termo':t.__unicode__(), 'ano':t.ano})

    return retorno

dispatcher.register_function(termos, 'termos')

def custo_acordos(termo_id, acordos):
    retorno = []
    for o in OrigemFapesp.objects.filter(acordo__in=acordos,item_outorga__natureza_gasto__termo__id=termo_id):
        it = {'desc':o.item_outorga.__unicode__(), 'id':o.id}
        total = Decimal('0.0')
        pg = []
        for p in o.pagamento_set.order_by('conta_corrente__data_oper'):
            pags = {'id':p.id, 'cod':p.conta_corrente.cod_oper, 'data':p.conta_corrente.data_oper.strftime('%d/%m'), 'descricao':p.protocolo.descricao2.descricao, 'referente':p.protocolo.referente, 'valor':float(p.valor_fapesp), 'tipo':p.protocolo.tipo_documento.nome, 'numero':p.protocolo.num_documento} # 'docs':p.auditoria_set.all()}
            audits = []
            for a in p.auditoria_set.all():
                url = ''
                if a.arquivo: url = a.arquivo.url
                audits.append({'tipo':a.tipo.nome, 'parcial':a.parcial, 'pagina':a.pagina, 'url':url})
            pags.update({'docs':audits})
            pg.append(pags)
            total += p.valor_fapesp

        it.update({'total':float(total), 'pg':pg})
        retorno.append(it)
    return retorno

def custo_links(termo_id):
    acordos = Acordo.objects.filter(descricao__startswith="Links por")
    return custo_acordos(termo_id, acordos)

dispatcher.register_function(custo_links, 'custo_links')

def custo_suporte(termo_id):
    acordos = Acordo.objects.filter(descricao__startswith="Suporte t")
    return custo_acordos(termo_id, acordos)

dispatcher.register_function(custo_suporte, 'custo_suporte')

def custeio(termo_id):
    """
    Gastos com custeio do nara para um determinado processo
    """
    acordos = Acordo.objects.filter(descricao__startswith="Custeio NARA")
    return custo_acordos(termo_id, acordos)

dispatcher.register_function(custeio, 'custeio')

def termo(termo_id):
    try:
        t = Termo.objects.get(id=termo_id)
        return t.__unicode__()
    except:
        return None

dispatcher.register_function(termo, 'termo')

def ferias(ano):
    retorno = []

    for f in Ferias.objects.filter(inicio__year=ano-1):
        oficial = []
        informal = []
        for c in f.controleferias_set.filter(oficial=True):
            oficial.append({'inicio':c.inicio.strftime('%d/%m/%Y'), 'termino':c.termino.strftime('%d/%m/%Y')})
        for c in f.controleferias_set.filter(oficial=False):
            informal.append({'inicio':c.inicio.strftime('%d/%m/%Y'), 'termino':c.termino.strftime('%d/%m/%Y')})
        retorno.append({'nome':f.membro.nome, 'oficial':oficial, 'informal':informal})
    
    return retorno

dispatcher.register_function(ferias, 'ferias')

def resumo_termo(termo_id):
    termo = Termo.objects.get(id=termo_id)

    concedido = []
    realizado = []
    saldo = []
    modalidades = []
    for ng in termo.natureza_gasto_set.filter(modalidade__moeda_nacional=True): 
        modalidades.append(ng.modalidade.sigla)
        concedido.append(float(ng.valor_concedido))
        realizado.append(float(ng.total_realizado))
        saldo.append(float(ng.valor_concedido - ng.total_realizado))

    #realizado = map(lambda x: 0.0 if x < 0.01 else x, realizado)
    #saldo = map(lambda x: 0.0 if x < 0.01 else x, saldo)
    return {'modalidades':modalidades, 'concedido':concedido, 'realizado':realizado, 'saldo':saldo}
dispatcher.register_function(resumo_termo, 'resumo_termo')

def modalidades():
    """
    Uma lista de todas as modalidades
    """
    modalidades = Modalidade.objects.all()
    retorno = []
    for m in modalidades:
        retorno.append({'id':m.id, 'modalidade':m.sigla})

    return retorno 
dispatcher.register_function(modalidades, 'modalidades')

def meses_entre(inicio, fim):
    meses = []
    cursor = inicio
    while cursor <= fim:
        if '%s%02d' % (cursor.year,cursor.month) not in meses:
            meses.append('%s%02d' % (cursor.year,cursor.month))
        cursor += timedelta(weeks=1)
    return meses
    
def modalidade(mod_id):
    """
    Dados sobre uma modalidade ao longo dos processos
    """
    meses = meses_entre(datetime(2005,1,1),datetime.now()) 
    mod = Modalidade.objects.get(id=mod_id) 
    retorno = []
    termos = []
    for t in Termo.objects.filter(ano__gte=2004).order_by('ano'):
        termos.append(t.__unicode__())
        termo = []
        for m in meses:
            ano = m[:4]
            mes = m[4:]
            v = Pagamento.objects.filter(protocolo__termo=t, conta_corrente__data_oper__year=ano, conta_corrente__data_oper__month=mes, origem_fapesp__item_outorga__natureza_gasto__modalidade=mod).aggregate(Sum('valor_fapesp'))
            termo.append(float(v['valor_fapesp__sum']) if v['valor_fapesp__sum'] else 0.0)
        retorno.append(termo)

    return {'modalidade':mod.sigla, 'valores':retorno, 'termos':termos}
dispatcher.register_function(modalidade, 'modalidade')

def acordos():
    """
    Retorna uma lista de todos os acordos
    """
    retorno = []
    for a in Acordo.objects.all():
        retorno.append({'id':a.id, 'acordo':a.__unicode__()})

    return retorno
dispatcher.register_function(acordos, 'acordos')

def nome_acordo(a_id):
    """
    Retorna o nome do acordo dado seu id
    """
    try:
        ac = Acordo.objects.get(id=a_id)
    except:
        return ''
    return ac.descricao
dispatcher.register_function(nome_acordo, 'nome_acordo')

def acordo(a_id):
    """
    Dados sobre uma modalidade ao longo dos processos
    """
    meses = meses_entre(datetime(2005,1,1),datetime.now())
    ac = Acordo.objects.get(id=a_id)
    retorno = []
    termos = []
    for t in Termo.objects.filter(ano__gte=2004).order_by('ano'):
        termos.append(t.__unicode__())
        termo = []
        for m in meses:
            ano = m[:4]
            mes = m[4:]
            v = Pagamento.objects.filter(protocolo__termo=t, conta_corrente__data_oper__year=ano, conta_corrente__data_oper__month=mes, origem_fapesp__acordo=ac).aggregate(Sum('valor_fapesp'))
            termo.append(float(v['valor_fapesp__sum']) if v['valor_fapesp__sum'] else 0.0)
        retorno.append(termo)

    return {'acordo':ac.__unicode__(), 'valores':retorno, 'termos':termos}
dispatcher.register_function(acordo, 'acordo')

def acordo_modalidades(a_id):
    """
    Gasto mensal em um acordo separado por modalidade
    """
    meses = meses_entre(datetime(2005,1,1),datetime.now())
    ac = Acordo.objects.get(id=a_id)

    retorno = []
    modalidades = []
    for mod in Modalidade.objects.all():
        modalidades.append(mod.sigla)
        modalidade = []
        for m in meses:
            ano = m[:4]
            mes = m[4:]
            v = Pagamento.objects.filter(conta_corrente__data_oper__year=ano, conta_corrente__data_oper__month=mes, origem_fapesp__acordo=ac, origem_fapesp__item_outorga__natureza_gasto__modalidade=mod).aggregate(Sum('valor_fapesp'))
            modalidade.append(float(v['valor_fapesp__sum']) if v['valor_fapesp__sum'] else 0.0)
        retorno.append(modalidade)

    return {'acordo':ac.__unicode__(), 'valores':retorno, 'modalidades':modalidades}
dispatcher.register_function(acordo_modalidades, 'acordo_modalidades')


def patrimonio(p_id):

    try:
        patrimonio = Patrimonio.objects.get(id=p_id)
	patrimonio = patrimonio.apelido
    except:
	patrimonio = u'Não cadastrado'

    return patrimonio
dispatcher.register_function(patrimonio, 'patrimonio')

