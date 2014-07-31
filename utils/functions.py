# -*- coding: utf-8 -*-

import settings
from datetime import date, timedelta, datetime
import calendar
import httplib
import json as simplejson
import os
import cgi
import cStringIO as StringIO

import weasyprint

from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


"""
Funções para uso da biblioteca PisaPDF
"""

"""
Utilizado para resolver o acesso a imagens relativas.
Ele resolve automaticamente, se for utilizado os prefixos definidos em STATIC_URL e MEDIA_URL

Ex. de uso no template:
{% load static %}
url('{% get_media_prefix %}{{papelaria.papel_timbrado_retrato_a4}}');

"""
def fetch_resources(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % \
                    (sUrl, mUrl))
    return path


def render_to_pdf(template_src, context_dict, request=None, context_instance=None, filename='file.pdf', attachments=[]):
    import ho.pisa as pisa
    from sx.pisa3.pisa_pdf import pisaPdf

    template = loader.get_template(template_src)

    if request: 
        context = RequestContext(request)
    else: 
        context = Context()
    
    context.update(context_dict)
    html  = template.render(context)
    pdf = pisaPDF()
    pdf_princ = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), link_callback=fetch_resources)
    pdf.addDocument(pdf_princ)
    a = 0
    for f,d,t in attachments:
        a += 1
        pdf.addDocument(pisa.pisaDocument(StringIO.StringIO((u'<div style="text-align:center; font-size:22px; padding-top:12cm;"><strong>Anexo %s<br />%s</strong></div>' % (a,d)).encode('utf-8'))))
        if t == 1: pdf.addFromFile(open(f, "rb"))
        elif t == 2: pdf.addFromString(f)
    if not pdf_princ.err:
        response = HttpResponse(mimetype='application/pdf')
        response.write(pdf.getvalue())
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))


"""
Funções para uso da biblioteca WeasyPrint
"""

def weasy_fetcher(url,**kwargs):
    """
    Definição de URLs relativas;
    Para acessar imagens do MEDIA, utilizar media:
    Para os do STATIC, utilizar static:
    
    Ex: 
    url('media:{{papelaria.papel_timbrado_paisagem_a4}}');
    
    """
    if url.startswith('static:'):
        url = url[len('static:'):]
        return weasyprint.default_url_fetcher('file://' + os.path.join(settings.STATIC_ROOT, url))
    elif url.startswith('media:'):
        url = url[len('media:'):]
        return weasyprint.default_url_fetcher('file://' + os.path.join(settings.MEDIA_ROOT, url))
    else:
        return weasyprint.default_url_fetcher(url)


def render_to_pdf_weasy(template_src, context_dict, request=None, filename='file.pdf'):
    # Renderiza o HTML
    template = loader.get_template(template_src)
    if request: 
        context = RequestContext(request)
        base_url = request.build_absolute_uri() 
    else: 
        context = Context()
        base_url = ''
    
    context.update(context_dict)
    html  = template.render(context)
    
    response = HttpResponse(mimetype="application/pdf")
    
    # Necessário passar o base_url para poder resolver os caminhos relativos de imagens
    weasyprint.HTML(string=html, url_fetcher=weasy_fetcher).write_pdf(response)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response



def render_to_pdfxhtml2pdf(template_src, context_dict, context_instance=None, filename='file.pdf', attachments=[]):
    from xhtml2pdf import pisa
    from xhtml2pdf.pdf import pisaPDF
    # Renderiza o HTML
    template = loader.get_template(template_src)
    context = context_instance or Context()
    context.update(context_dict)
    html  = template.render(context)
    pdf = pisaPDF()
    pdf_princ = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8"))) #, link_callback=fetch_resources)
    pdf.addDocument(pdf_princ)
    a = 0
    for f,d,t in attachments:
        a += 1
        pdf.addDocument(pisa.pisaDocument(StringIO.StringIO((u'<div style="text-align:center; font-size:22px; padding-top:12cm;"><strong>Anexo %s<br />%s</strong></div>' % (a,d)).encode('utf-8'))))
        if t == 1: pdf.addFromFile(open(f, "rb"))
        elif t == 2: pdf.addFromString(f)
        
    if not pdf_princ.err:
        response = HttpResponse(mimetype='application/pdf')
        response.write(pdf.getvalue())
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))


def render_wk_to_pdf(template_src, context_dict, context_instance=None, filename=None, attachments=[], request=None, header_template=None, footer_template=None):
    from wkhtmltopdf.views import PDFTemplateResponse
    
    """
    Renderiza o HTML utilizando o wkHTMLtoPDF, por linha de comando, utilizando a engine QT com webkit
    """
    context = context_instance or Context()
    context.update(context_dict)
    context_dict.update({'request': request})
    
    result = StringIO.StringIO()
    
    if header_template == None:
        header_template = 'wkhtmltopdf_header_template.html'
    
    if footer_template == None:
        footer_template = 'wkhtmltopdf_footer_template.html'
    
    today = datetime.today()
    fileDate = "%s-%s-%s." % (today.year, today.month, today.day)
    
    if not filename:
        localFilename = 'file.pdf'
    else:
        localFilename = filename
    localFilename = localFilename.replace('.', fileDate, 1)
             
    cmd_options = {'orientation': 'landscape'}
     
    response = PDFTemplateResponse(request=request,
                                   template=template_src,
                                   context=context,
                                   filename=localFilename,
                                   footer_template=footer_template,
                                   header_template=header_template,
                                   show_content_in_browser=False, cmd_options=cmd_options)

    return response



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
    conn.request('GET', '/bancos.asp')
    dados = conn.getresponse().read()
    conn.close()
    p1 = dados.find('table')
    bancos = []
    numero = None
    dados = dados[p1:]
    dados = dados.split('blank">\r\n')
    for l in dados[1:]:
        n = l.find('\r')
        m = l[:n]
        if numero is not None:
            try:
               bancos.append((int(numero), m.strip().decode('iso-8859-1').encode('utf-8')))
            except:
               pass
            numero = None
        else:
            numero = m.strip()

    return bancos

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


def working_days(year, month):
    fromdate = date(year, month, 1)
    dias_mes = calendar.monthrange(year, month)[1]
    daygenerator = (fromdate + timedelta(x + 1) for x in range(dias_mes))
    return sum(day.weekday() < 5 for day in daygenerator)


def clone_objects(objects):
    def clone(from_object):
        args = dict([(fld.name, getattr(from_object, fld.name))
                for fld in from_object._meta.fields
                        if fld is not from_object._meta.pk]);

        return from_object.__class__.objects.create(**args)

    if not hasattr(objects,'__iter__'):
       objects = [ objects ]

    # We always have the objects in a list now
    objs = []
    for object in objects:
        obj = clone(object)
        obj.save()
        objs.append(obj)

def clone_objects(objects):
    def clone(from_object):
        args = dict([(fld.name, getattr(from_object, fld.name))
                for fld in from_object._meta.fields
                        if fld is not from_object._meta.pk]);

        return from_object.__class__.objects.create(**args)

    if not hasattr(objects,'__iter__'):
       objects = [ objects ]

    # We always have the objects in a list now
    objs = []
    for object in objects:
        obj = clone(object)
        obj.save()
        objs.append(obj)

import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
