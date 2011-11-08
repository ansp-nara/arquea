# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib import auth
from django.http import HttpResponse, Http404, HttpResponseRedirect
from haystack.views import SearchView
from identificacao.models import Contato, Entidade
from membro.models import Membro, Classificacao
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from datetime import datetime
from string import ascii_lowercase
from cms.models import Page
from utils.functions import formata_moeda
import matplotlib
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def sample_view(request, **kw):
    kw['user'] = request.user
    context = RequestContext(request, kw)
    return render_to_response("home.html", context)

def login(request):
    if request.method == 'POST':

        next = request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
	        return HttpResponseRedirect(next)

    else:
        context = RequestContext(request)
        return render_to_response('login.html', context) 

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required
def agenda(request, char='a', pess='fis'):
    context = RequestContext(request)
    if pess == 'fis':
	contatos = Contato.objects.filter(ativo=True, nome__istartswith=char)
    else:
        contatos = Entidade.objects.filter(ativo=True, nome__istartswith=char)

    paginator = Paginator(contatos, 10)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        contacts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        contacts = paginator.page(paginator.num_pages)



    context.update({'agenda': contacts, 'pess': pess, 'letters':ascii_lowercase, 'char':char})
    return render_to_response('agenda-results.html', context)

class PageSearchView(SearchView):
    
    def get_results(self):
	res = super(PageSearchView, self).get_results()

	results = []
        slugs = []
 
	try:
            for p in res:
                slug = p.object.get_slug()
	        if not slug in slugs:
		    slugs.append(slug)
		    results.append(p)

	    return results
        except:
            return res

@login_required
def membros(request, class_id=1):
    context = RequestContext(request)
	
    if request.method == 'GET':
        cls = Classificacao.objects.all()
        context.update({'membros':Membro.objects.filter(classificacao__id=class_id), 'cls':cls, 'atual':int(class_id)})
	return render_to_response('membros.html',context)
    else:
	raise Http404

@login_required
def custeio(request, tipo='nara'):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)
    context = RequestContext(request)

    if tipo == 'links':
        dados_custeio = rpc_srv.custo_links
        page_id = 'custo_links'
    elif tipo == 'suporte':
        dados_custeio = rpc_srv.custo_suporte
        page_id = 'custo_suporte'
    elif tipo == 'nara':
        dados_custeio = rpc_srv.custeio
        page_id = 'custeio'

    if request.GET.has_key('termo'):
        termo_id = request.GET.get('termo') 
        context.update({'acordo':dados_custeio(termo_id), 'termo':termo_id})
        return render_to_response('custeio.html', context)
    else:
        body = ''
        graficos = ''
        try:
            page = Page.objects.get(reverse_id=page_id)
            ph = page.placeholders.get(slot='body')
            pl1 = ph.get_plugins_list()[0]
            t = pl1.text
            body = t.body
            pl2 = ph.get_plugins_list()[1]
            t = pl2.text
            graficos = t.body
        except:
            pass
        context.update({'termos':rpc_srv.termos(), 'body':body, 'graficos':graficos})
        return render_to_response('escolhe_termo.html', context)

@login_required
def ferias(request):
    import xmlrpclib
    if request.method == 'POST':
        raise Http404

    ano = request.GET.get('ano')
    if not ano:
        raise Http404

    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)
    context = RequestContext(request)
    context.update({'ferias':rpc_srv.ferias(int(ano)), 'ano':ano})
    return render_to_response('ferias.html', context)

def format(valor, moeda='', maior=''):
    DIVISAO = ['','MIL', 'MI', 'BI']
    div = 0
    if not maior: maior = valor

    while maior > 5000:
       valor = valor/1000.
       maior = maior/1000.
       div += 1

    v = str(valor)
    d = None
    try:
        i,d = v.split('.')
        d = d[:2]
    except:
        i = v
    r = []
    k = len(i)
    while k > 0:
       j = k-3
       if j < 0: j = 0
       r.append(i[j:k])
       k -= 3
    r.reverse()
    i = '.'.join(r)
    if d:
        return '%s%s,%s %s' % (moeda,i,d, DIVISAO[div])
    else:
        return i

def retorna_imagem(pl):
    response = HttpResponse(mimetype='image/png')
    pl.savefig(response, format='png')

    return response

@login_required
def barra_modalidades(request, mod_id):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)

    dados = rpc_srv.modalidade(mod_id)
    tam = len(dados['valores'][0])
    bottom = [0] * tam
    colors = ['r', 'g', 'b', 'y', 'k', 'c', 'm']    

    plt.clf()
    graphs = []
    for dd,c,t in zip(dados['valores'],colors,dados['termos']):
        graphs.append((plt.bar(np.arange(0,0.35*tam,0.35), dd, width=0.35, bottom=bottom, color=c)[0], t))
        bottom = map(lambda x,y: x+y, bottom, dd)

    plt.title('Gastos para a modalidade %s' % dados['modalidade'])
    leg = zip(*graphs)
    plt.legend(leg[0], leg[1], loc='upper left')
    meses = ['jan','jul']
    anos = range(2005, 2005*tam/12 + 1)
    ticks = []
    ind = np.arange(0,tam*0.35,2.1)
    for i in range(len(ind)):
        m = meses[i%2]
        a = anos[i/2]
        ticks.append('%s %s' % (m,a))
    plt.xticks(ind+0.175, ticks, rotation=35, ha='right')

    return retorna_imagem(plt)

@login_required
def linha_modalidades(request, acima):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)

    modalidades = rpc_srv.modalidades()
    colors = ['r', 'g', 'b', 'y', 'k', 'c', 'm', 'r']
    plt.clf()
    graphs = []
    acima = int(acima)

    for m,c in zip(modalidades,colors):
        dados = rpc_srv.modalidade(m['id'])
        tam = len(dados['valores'][0])
        valores = [0.0] * tam
        for v in dados['valores']:
            valores = map(lambda x,y: x+y, valores, v)

        pl = True
        if acima > 0:
            if max(valores) < 500000: pl = False
        else:
            if max(valores) >= 500000: pl = False
    
        if pl:
            graphs.append((plt.plot(np.arange(0,0.35*tam,0.35), valores, c+'-'), dados['modalidade']))

    plt.title('Gastos por modalidade')
    leg = zip(*graphs)
    plt.legend(leg[0], leg[1], loc='0', prop={'size':7})
    meses = ['jan','jul']
    anos = range(2005, 2005*tam/12 + 1)
    ticks = []
    ind = np.arange(0,tam*0.35,2.1)
    for i in range(len(ind)):
        m = meses[i%2]
        a = anos[i/2]
        ticks.append('%s %s' % (m,a))
    plt.xticks(ind+0.175, ticks, rotation=35, ha='right')

    return retorna_imagem(plt)


@login_required
def barra_acordos(request, a_id):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)

    dados = rpc_srv.acordo(a_id)
    tam = len(dados['valores'][0])
    bottom = [0] * tam
    colors = ['r', 'g', 'b', 'y', 'k', 'c', 'm']    

    plt.clf()
    graphs = []
    for dd,c,t in zip(dados['valores'],colors,dados['termos']):
        graphs.append((plt.bar(np.arange(0,0.35*tam,0.35), dd, width=0.35, bottom=bottom, color=c)[0], t))
        bottom = map(lambda x,y: x+y, bottom, dd)

    plt.title('Gastos para o acordo %s' % dados['acordo'])
    leg = zip(*graphs)
    plt.legend(leg[0], leg[1], loc='0', prop={'size':7})
    meses = ['jan','jul']
    anos = range(2005, 2005*tam/12 + 1)
    ticks = []
    ind = np.arange(0,tam*0.35,2.1)
    for i in range(len(ind)):
        m = meses[i%2]
        a = anos[i/2]
        ticks.append('%s %s' % (m,a))
    plt.xticks(ind+0.175, ticks, rotation=35, ha='right')

    return retorna_imagem(plt)

@login_required
def grafico_barra(request, termo_id):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)    

    resumo = rpc_srv.resumo_termo(termo_id)
    log = request.GET.get('log') or False

    width = 0.28 if log else 0.35

    ind = np.arange(len(resumo['modalidades']))
    plt.clf()
    c = plt.bar(ind, resumo['concedido'], width, color='b', log=log)
    r = plt.bar(ind+width, resumo['realizado'], width, color='g', log=log)
    if log:
        s = plt.bar(ind+2*width, resumo['saldo'], width, color='y', log=log)
    else:
        s = plt.bar(ind+width, resumo['saldo'], width, bottom=resumo['realizado'], color='y', log=log)

    plt.ylabel('Valor em reais')
    
    locs, labels = plt.yticks()
    plt.yticks(locs, map(format, locs, ['R$ ']*len(locs), [max(locs)]*len(locs)))
    if not log:
        plt.xticks(ind+width, resumo['modalidades'])
    else:
        plt.xticks(ind+1.5*width, resumo['modalidades'])
    plt.legend((c[0], r[0], s[0]), ('Concedido', 'Realizado', 'Saldo'), loc=0)

    return retorna_imagem(plt)

@login_required
def grafico_pizza(request, termo_id):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)    

    resumo = rpc_srv.resumo_termo(termo_id)

    concedido = []
    modalidades = []
    n = len(resumo['concedido'])
    for i in range(n/2):
        concedido.append(resumo['concedido'][i])
        concedido.append(resumo['concedido'][n-1-i])
        modalidades.append(resumo['modalidades'][i])
        modalidades.append(resumo['modalidades'][n-1-i])

    if n%2 == 1:
        concedido.append(resumo['concedido'][n/2])
        modalidades.append(resumo['modalidades'][n/2])
        
    plt.clf()
    plt.pie(concedido, labels=modalidades, autopct='%.1f%%')

    return retorna_imagem(plt)

@login_required
def resumo_termo(request):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)    
    context = RequestContext(request)

    if request.GET.has_key('termo'):
        termo_id = request.GET.get('termo')
        context.update({'termo_id':termo_id, 'termo':rpc_srv.termo(termo_id)})
        return render_to_response('resumo_termo.html', context)
    else:
        context.update({'termos':rpc_srv.termos()})
        return render_to_response('escolhe_termo.html', context)

@login_required
def tempo_modalidade(request):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)    
    context = RequestContext(request)

    if request.GET.has_key('modalidade'):
        mod_id = request.GET.get('modalidade')
        context.update({'mod_id':mod_id})
        return render_to_response('tempo_modalidade.html', context)
    else:
        context.update({'modalidades':rpc_srv.modalidades()})
        return render_to_response('escolhe_modalidade.html', context)

@login_required
def tempo_acordo(request):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)    
    context = RequestContext(request)

    if request.GET.has_key('acordo'):
        ac_id = request.GET.get('acordo')
        context.update({'ac_id':ac_id})
        return render_to_response('tempo_acordo.html', context)
    else:
        context.update({'acordos':rpc_srv.acordos()})
        return render_to_response('escolhe_acordo.html', context)

def linha_modalidades2(acima):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)

    modalidades = rpc_srv.modalidades()
    colors = ['r', 'g', 'b', 'y', 'k', 'c', 'm', 'r']
    plt.clf()
    graphs = []
    acima = int(acima)
    dpi = 100
    fig = plt.figure(dpi=dpi)
    hg = fig.get_figheight() * dpi
    for m,c in zip(modalidades,colors):
        dados = rpc_srv.modalidade(m['id'])
        tam = len(dados['valores'][0])
        valores = [0.0] * tam
        for v in dados['valores']:
            valores = map(lambda x,y: x+y, valores, v)

        pl = True
        if acima > 0:
            if max(valores) < 500000: pl = False
        else:
            if max(valores) >= 500000: pl = False
    
        if pl:
            graphs.append((plt.plot(np.arange(0,0.35*tam,0.35), valores, c+'-')[0], dados['modalidade']))

    plt.title('Gastos por modalidade')
    leg = zip(*graphs)
    plt.legend(leg[0], leg[1], loc='0', prop={'size':7})
    meses = ['jan','jul']
    anos = range(2005, 2005*tam/12 + 1)
    ticks = []
    ind = np.arange(0,tam*0.35,2.1)
    for i in range(len(ind)):
        m = meses[i%2]
        a = anos[i/2]
        ticks.append('%s %s' % (m,a))
    plt.xticks(ind+0.175, ticks, rotation=35, ha='right')
   
    posicoes = []
    for g in leg[0]:
        g._transform_path()
        path, affine = g._transformed_path.get_transformed_points_and_affine()
        path = affine.transform_path(path)
        posicoes.append(map(tuple,path.vertices))
   
    fig.savefig('/var/www/media/graficos/lmod.png')
    plt.close(fig)

    return (posicoes, hg)

@login_required
def tempo_modalidade2(request):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)    
    context = RequestContext(request)

    posicoes, altura = linha_modalidades2(1)
    context.update({'posicoes':posicoes, 'altura':altura})
    return render_to_response('linha_modalidades.html', context)


@login_required
def acordo_modalidades(request):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)    
    context = RequestContext(request)

    if request.GET.has_key('acordo'):
        ac_id = request.GET.get('acordo')
        context.update({'ac_id':ac_id})
        return render_to_response('acordo_modalidades.html', context)
    else:
        context.update({'acordos':rpc_srv.acordos()})
        return render_to_response('escolhe_acordo.html', context)

@login_required
def linhas_ac_mod(request, a_id):
    import xmlrpclib
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)    
    context = RequestContext(request)

    dados = rpc_srv.acordo_modalidades(a_id)
    tam = len(dados['valores'][0])
    colors = ['r', 'g', 'b', 'y', 'k', '#ff00ff', '#ffafaf', '#00b200', '#b27a7a', '#00ffff']
    plt.clf()

    graphs = []
    for mod,c, m in zip(dados['valores'], colors, dados['modalidades']):
        graphs.append((plt.plot(np.arange(0,0.35*tam,0.35), mod, color=c)[0], m))

    plt.title('Gastos por modalidade')
    leg = zip(*graphs)
    plt.legend(leg[0], leg[1], loc='0', prop={'size':7})

    meses = ['jan','jul']
    anos = range(2005, 2005*tam/12 + 1)
    ticks = []
    ind = np.arange(0,tam*0.35,2.1)
    for i in range(len(ind)):
        m = meses[i%2]
        a = anos[i/2]
        ticks.append('%s %s' % (m,a))
    plt.xticks(ind+0.175, ticks, rotation=35, ha='right')

    return retorna_imagem(plt)


@login_required
def grafico_pizza_teste(request, termo_id):
    import xmlrpclib
    from pygooglechart import PieChart3D
    context = RequestContext(request)

    chart = PieChart3D(650, 350)
    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)

    resumo = rpc_srv.resumo_termo(termo_id)

    concedido = []
    modalidades = []
    n = len(resumo['concedido'])
    for i in range(n/2):
        concedido.append(resumo['concedido'][i])
        concedido.append(resumo['concedido'][n-1-i])
        modalidades.append(resumo['modalidades'][i])
        modalidades.append(resumo['modalidades'][n-1-i])

    if n%2 == 1:
        concedido.append(resumo['concedido'][n/2])
        modalidades.append(resumo['modalidades'][n/2])

    chart.add_data(concedido)
    chart.set_pie_labels(modalidades)
    chart.set_colours(('ff0000', 'ffff00', '00ff00') )
    context.update({'img':chart.get_url()})

    return render_to_response('teste_pizza.html', context)

@login_required
def grafico_pizza_teste2(request, termo_id):
    import xmlrpclib
    context = RequestContext(request)

    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)

    resumo = rpc_srv.resumo_termo(termo_id)

    concedido = []
    modalidades = []
    n = len(resumo['concedido'])
    for i in range(n/2):
        concedido.append(resumo['concedido'][i])
        concedido.append(resumo['concedido'][n-1-i])
        modalidades.append(resumo['modalidades'][i])
        modalidades.append(resumo['modalidades'][n-1-i])

    if n%2 == 1:
        concedido.append(resumo['concedido'][n/2])
        modalidades.append(resumo['modalidades'][n/2])

    context.update({'dados':zip(modalidades, concedido), 'formatado': map(lambda x: 'R$ %s' % formata_moeda(x, ','), concedido)})
    return render_to_response('teste_pizza2.html', context)

@login_required
def grafico_coluna_teste(request, termo_id):
    import xmlrpclib
    context = RequestContext(request)

    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)

    resumo = rpc_srv.resumo_termo(termo_id)

    concedido = resumo['concedido']
    modalidades = resumo['modalidades']
    realizado = resumo['realizado']

    context.update({'dados':zip(modalidades, concedido, realizado)})
    return render_to_response('resumo_termo_gchart.html', context)

