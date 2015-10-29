from django.conf.urls import *

urlpatterns = patterns('repositorio.views',
                       (r'seleciona_patrimonios$', 'ajax_seleciona_patrimonios'),
                       (r'ajax_repositorio_tipo_nomes$', 'ajax_repositorio_tipo_nomes'),
                       (r'relatorio/repositorio$', 'relatorio_repositorio'),
                       (r'relatorio/repositorio/(?P<pdf>\d)$', 'relatorio_repositorio'),
                       )