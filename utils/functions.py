import httplib
from django.core import serializers
from django.utils import simplejson
import os
import ho.pisa as pisa
from sx.pisa3.pisa_pdf import *
import cStringIO as StringIO
import cgi
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
import settings

def render_to_pdf(template_src, context_dict, context_instance=None, filename='file.pdf', attachments=[]):
    template = loader.get_template(template_src)
    context = context_instance or Context()
    context.update(context_dict)
    html  = template.render(context)
    pdf = pisaPDF()
    pdf_princ = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8"))) #, link_callback=fetch_resources)
    pdf.changeDocument(pdf_princ)
    a = 0
    for f,d,t in attachments:
        a += 1
        pdf.changeDocument(pisa.pisaDocument(StringIO.StringIO((u'<div style="text-align:center; font-size:22px; padding-top:12cm;"><strong>Anexo %s<br />%s</strong></div>' % (a,d)).encode('utf-8'))))
        if t == 1: pdf.changeFromFile(open(f, "rb"))
        elif t == 2: pdf.changeFromString(f)
    if not pdf_princ.err:
        response = HttpResponse(mimetype='application/pdf')
        response.write(pdf.getvalue())
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))

def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

    return path

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

