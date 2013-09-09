from django.conf.urls.defaults import *

urlpatterns = patterns('membro.views',
    (r'controle$', 'controle'),
    (r'mensal/(?P<ano>\d+)/(?P<mes>\d+)$', 'mensal'),
    (r'detalhes$', 'detalhes'),
    (r'obs/(?P<id>\d+)$', 'observacao'),
    (r'mensalf$', 'mensal_func'),
    (r'ajax_controle_mudar_almoco$', 'controle_mudar_almoco'),

    (r'ajax_controle_avancar_bloco$', 'controle_avancar_bloco'),
    (r'ajax_controle_voltar_bloco$', 'controle_voltar_bloco'),
    (r'ajax_controle_adicionar_tempo_final$', 'controle_adicionar_tempo_final'),
    (r'ajax_controle_adicionar_tempo_inicial$', 'controle_adicionar_tempo_inicial'),
    
    
)

