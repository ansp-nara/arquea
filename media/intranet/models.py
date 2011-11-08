# -*- coding: utf-8 -*-
from django.db import models
import xmlrpclib
from django.conf import settings
import datetime

# Create your models here.

#class Documento(models.Model):
#    descricao = models.CharField(max_length=60)
#    arquivo = models.FileField(upload_to='documentos')
#
#    def __unicode__(self):
#	return self.descricao

class LinkExterno(models.Model):
    descricao = models.CharField(max_length=20)
    url = models.URLField()

    def __unicode__(self):
	return self.descricao


    class Meta:
	verbose_name = u'Link Externo'
        verbose_name_plural = u'Links Externos'
	ordering = ('id',)


class LatestPosts(models.Model):
     autor = models.CharField(max_length=60)
     titulo = models.CharField(max_length=100)
     data = models.DateField()
     link = models.URLField(verify_exists=False)
     ci = models.BooleanField(default=False)

     @classmethod
     def atualiza(cls, count1, count2):
	sp = xmlrpclib.ServerProxy(settings.WP_XML_URL)
	autores = sp.wp.getAuthors(settings.WP_BLOG_ID, settings.WP_ADMIN_USER, settings.WP_ADMIN_PASS)
	authors = {}
    	for a in autores:
              authors[a['user_id']] = a['display_name']

        all = sp.mt.getRecentPostTitles(settings.WP_BLOG_ID, settings.WP_ADMIN_USER, settings.WP_ADMIN_PASS, count1+40)
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

        cm = cm[:count2]
        posts = posts[:count1]

        i = 1
        for p in posts:
            criado = p['dateCreated'].__str__()
            post, cr = cls.objects.get_or_create(id=i, defaults={'autor':authors[p['userid']], 'titulo':p['title'], 'data':datetime.date(int(criado[0:4]), int(criado[4:6]), int(criado[6:8])), 
		  				          'link':'http://%s/wp-login.php?redirect_to=/%s%s' % (settings.WP_DOMAIN, '%3Fp%3D', p['postid'],)})
            if not cr:
		post.autor = authors[p['userid']]
		post.titulo = p['title']
		post.data = datetime.date(int(criado[0:4]), int(criado[4:6]), int(criado[6:8]))
		post.link = 'http://%s/wp-login.php?redirect_to=/%s%s' % (settings.WP_DOMAIN, '%3Fp%3D', p['postid'],)
                post.ci = False
		post.save()
            i += 1

        for p in cm:
            criado = p['dateCreated'].__str__()
            post, cr = cls.objects.get_or_create(id=i, defaults={'autor':authors[p['userid']], 'titulo':p['title'], 'data':datetime.date(int(criado[0:4]), int(criado[4:6]), int(criado[6:8])), 
                                                          'link':'http://%s/wp-login.php?redirect_to=/%s%s' % (settings.WP_DOMAIN, '%3Fp%3D', p['postid'],), 'ci':True})
            if not cr:
                post.autor = authors[p['userid']]
                post.titulo = p['title']
                post.data = datetime.date(int(criado[0:4]), int(criado[4:6]), int(criado[6:8]))
                post.link = 'http://%s/wp-login.php?redirect_to=/%s%s' % (settings.WP_DOMAIN, '%3Fp%3D', p['postid'],)
		post.ci = True
                post.save()
            i += 1

class Reuniao(models.Model):
    titulo = models.CharField(max_length=100)
    link = models.URLField(verify_exists=False)

    def __unicode__(self):
 	return self.titulo

    @classmethod
    def atualiza(cls):
        sp = xmlrpclib.ServerProxy(settings.WP_XML_URL)
 	all = sp.mt.getRecentPostTitles(settings.WP_BLOG_ID, settings.WP_ADMIN_USER, settings.WP_ADMIN_PASS, 50)
        for p in all:
            ct = sp.mt.getPostCategories(p['postid'], settings.WP_ADMIN_USER, settings.WP_ADMIN_PASS)
            for c in ct:
                if c['categoryId'] == settings.WP_CAT_REU:
		    try:
                        cls.objects.get(id=int(p['postid']))
                    except cls.DoesNotExist:
			r = cls(id=int(p['postid']), titulo=p['title'], link='http://%s/wp-login.php?redirect_to=%s%s' % (settings.WP_DOMAIN, '%3Fp%3D', p['postid'],))
                        r.save()	


class Parceiro(models.Model):
    nome = models.CharField(max_length=20)
    descricao = models.CharField(max_length=60)
    texto_pt_br = models.TextField(u'Texto em português')
    logo = models.ImageField(upload_to='parceiros')
    url = models.URLField()

    def __unicode__(self):
        return self.nome



