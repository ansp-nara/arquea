from django.conf.urls import *

urlpatterns = patterns('carga.views',
                       
    (r'upload_planilha_patrimonio$', 'upload_planilha_patrimonio'),
    (r'list_planilha_patrimonio$', 'list_planilha_patrimonio'),
    (r'$', 'list_planilha_patrimonio'),
)

