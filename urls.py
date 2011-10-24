from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

admin.site.root_path = "/admin/" # there is probably a bug in django...

urlpatterns = patterns('',
    # Example:
    # (r'^sistema/', include('sistema.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^protocolo/', include('sistema.protocolo.urls')),
    (r'^patrimonio/', include('sistema.patrimonio.urls')),
    (r'^financeiro/', include('sistema.financeiro.urls')),
    (r'^outorga/', include('sistema.outorga.urls')),
    (r'^memorando/', include('sistema.memorando.urls')),
    (r'^identificacao/', include('sistema.identificacao.urls')),
    (r'^monitor/', include('sistema.monitor.urls')),
#    (r'^rede/', include('sistema.rede.urls')),
    (r'^accounts/login/$', 'django_cas.views.login'),
    (r'^accounts/logout/$', 'django_cas.views.logout'),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^xml_rpc_srv$', 'xmlrpc_srv.rpc_handler', {'SSL':False}),
    (r'^verifica$', 'utils.views.verifica', {'SSL':False}),
    (r'^', include(admin.site.urls)),
)
