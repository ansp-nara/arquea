import httplib
from django.core import serializers
from django.utils import simplejson
import os
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template import Context, loader, RequestContext
from django.http import HttpResponse

def render_to_pdf(template_src, context_dict, context_instance=None, filename='file.pdf'):
    template = loader.get_template(template_src)
    context = context_instance or Context()
    context.update(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))

def formata_moeda(n, s_d):
    if s_d == '.':
       s_i = ','
    else:
       s_i = '.'
    f = str(n)
    num = f.split('.')
    i = num[0]
    if len(num) > 1:
	d = num[1]
    else:
	d = '0'
    if len(d) == 1: d = d+'0'
    ii = list(i)
    j = 3
    while len(ii) > j:
        ii.insert(-j,s_i)
        j += 4
    r = ''.join(ii)
    return s_d.join((r,d))

def pega_bancos():
    conn = httplib.HTTPConnection('www.febraban.org.br')
    conn.request('GET', '/buscabanco/agenciasBancos.asp')
    dados = conn.getresponse().read()
    conn.close()
    p = 11119
    bancos = []
    while p > 11118:
        pnum = p+9
        p1 = dados.find('class="link">', pnum)
        pnome = p1+19
        p2 = dados.find('\n', pnome)
	try:
            bancos.append((dados[pnum:pnum+3],unicode(dados[pnome:p2-2], 'latin-1')))
	except:
	    print dados[pnome:p2-2]
        p = dados.find('Estilo2', p2)

    bb = []
    for b in bancos:
        try:
            bb.append((int(b[0]),b[1]))
        except:
            pass

    return bb

def pega_lista(request, obj, filtro):
    if request.method == 'POST':
        id = request.POST.get('id');
        kwargs = {filtro:id}
        lista = obj.objects.filter(**kwargs)
        retorno = []
	for o in lista:
	    retorno.append({'pk':o.pk, 'valor':o.__unicode__()})
        if lista.count() > 0:
            json = simplejson.dumps(retorno)
        else:
            retorno = [{"pk":"0","valor":"Nenhum registro"}]
            json = simplejson.dumps(retorno)
    return json
