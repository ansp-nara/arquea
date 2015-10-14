# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, patterns, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

admin.site.root_path = "/admin/" # there is probably a bug in django...

urlpatterns = patterns('',
    # Example:
    # (r'^sistema/', include('foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^protocolo/', include('protocolo.urls')),
    (r'^patrimonio/', include('patrimonio.urls')),
    (r'^financeiro/', include('financeiro.urls')),
    (r'^outorga/', include('outorga.urls')),
    (r'^memorando/', include('memorando.urls')),
    (r'^monitor/', include('monitor.urls')),
    (r'^identificacao/', include('identificacao.urls')),
    (r'^membro/', include('membro.urls')),
    (r'^rede/', include('rede.urls')),
    (r'^processo/', include('processo.urls')),
    (r'^verificacao/', include('verificacao.urls')),
    (r'^repositorio/', include('repositorio.urls')),
    (r'^carga/', include('carga.urls')),
    (r'^utils/', include('utils.urls')),
    (r'^configuracao/', include('configuracao.urls')),
    
    (r'^accounts/login/$', 'django_cas_ng.views.login'),
    (r'^accounts/logout/$', 'django_cas_ng.views.logout'),
    (r'^xml_rpc_srv$', 'xmlrpc_srv.rpc_handler', {'SSL':False}),
    (r'^verifica$', 'utils.views.verifica', {'SSL':False}),
    (r'^sempermissao$', TemplateView.as_view(template_name="401.html")),


    # necessário instalar o django_localflavor
    # No Django 1.6 o django.contrib.localflavor foi desabilitado
    
    # necessário instalar o django_wkhtmltopdf para conversão de PDF

    # necessário instalar/atualizar o django_tinymce
    (r'^tinymce/', include('tinymce.urls')),
    # necessário instalar o django_ckeditor_updated (para o Django 1.6)
    #(r'^ckeditor/', include('ckeditor.urls')),
    # Utilizar com o CKEditor > 5.0
    (r'^ckeditor/', include('ckeditor_uploader.urls')),

    
    (r'^', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 

