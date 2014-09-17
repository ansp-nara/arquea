from django.conf.urls import *

urlpatterns = patterns('repositorio.views',
    (r'seleciona_patrimonios$', 'ajax_seleciona_patrimonios'),

)



