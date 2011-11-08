from django import template
import xmlrpclib
from django.conf import settings
from photologue.models import Photo, Gallery
from intranet.models import *

register = template.Library()

@register.inclusion_tag('posts.html')
def latest_posts(count=1, ci=False):
    return {'posts':LatestPosts.objects.filter(ci=ci).order_by('-data')[:count]}

@register.inclusion_tag('lista_reunioes.html')
def reunioes():
    return {'posts':Reuniao.objects.order_by('-id')}

def latest_posts_old(count=1, ci=False):
    sp = xmlrpclib.ServerProxy(settings.WP_XML_URL)
    autores = sp.wp.getAuthors(settings.WP_BLOG_ID, settings.WP_ADMIN_USER, settings.WP_ADMIN_PASS)
    authors = {}
    for a in autores:
        authors[a['user_id']] = a['display_name']

    all = sp.mt.getRecentPostTitles(settings.WP_BLOG_ID, settings.WP_ADMIN_USER, settings.WP_ADMIN_PASS, count+10)
    posts = []
    cm = []
    for p in all:
        ispost = True
        ct = sp.mt.getPostCategories(p['postid'], settings.WP_ADMIN_USER, settings.WP_ADMIN_PASS)
	for c in ct:
	    if c['categoryId'] == settings.WP_CAT_COM:
               ispost = False
	       break
        if ispost:
           posts.append(p)
        else:
           cm.append(p)

    if ci:
       posts = cm[:count]
    else:
       posts = posts[:count]
	
    retorno = []
    for p in posts:
        criado = p['dateCreated'].__str__()
        date = '%s/%s/%s' % (criado[6:8], criado[4:6], criado[0:4])
        retorno.append({'title':p['title'], 'url':'http://%s/wp-login.php?redirect_to=/%3Fp%3D%s' % (settings.WP_DOMAIN, p['postid'],), 'author':authors[p['userid']], 'date':date})

    return {'posts': retorno}  


@register.inclusion_tag('gallery.html')
def latest_photos(count=1):

    galleries = Gallery.objects.all()
    photos = []
    for g in galleries:
        if g.photos.count() > 0:
           photos.append((g.photos.order_by('-date_added')[0], g.get_absolute_url()))

    retorno = []
    for p in photos[:count]:
	retorno.append({'thumbnail':p[0].get_home_thumbnail_url(), 'url':p[1]})

    return {'photos': retorno}


@register.inclusion_tag('links.html')
def links_uteis():

    return {'links': LinkExterno.objects.all()}
   

@register.filter(name='moeda')
def moeda(value, sep=','):
    try:
        v = str(value)
        v = Decimal(v)
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


@register.filter
def distinct(value):

    try:
	pass
    except:
	return value 

@register.inclusion_tag('parcerias_lista.html')
def mostra_parceiros(lang='pt-br'):
    parceiros = Parceiro.objects.all()
    return {'parcerias':parceiros}


@register.inclusion_tag('grafico_acordos.html')
def grafico_acordos(acordo=1):
    import xmlrpclib
    from dateutil import relativedelta
    import datetime
    now = datetime.datetime.now().date()

    rpc_srv = xmlrpclib.ServerProxy("http://10.0.1.18/xml_rpc_srv", allow_none=True)

    dados = rpc_srv.acordo(acordo)
    valores = [reduce(lambda x,y:x+y, l) for l in zip(*dados['valores'])]
    meses = []
    data = datetime.date(2005,1,1)
    um_mes = relativedelta.relativedelta(months=1)
    while data < now:
        meses.append(data)
        data += um_mes

    return {'dados':zip(map(lambda d:'%02d/%s' % (d.month, d.year), meses),valores), 'acordo':rpc_srv.nome_acordo(acordo)}
