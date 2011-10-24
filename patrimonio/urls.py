from django.conf.urls.defaults import *

urlpatterns = patterns('patrimonio.views',
    (r'escolhe_termo$', 'escolhe_termo'),
    (r'escolhe_protocolo$', 'escolhe_protocolo'),
    (r'escolhe_pagamento$', 'escolhe_pagamento'),
    (r'escolhe_entidade$', 'escolhe_entidade'),
    (r'patrimonio_existente$', 'patrimonio_existente'),
    (r'relatorio/por_estado$', 'por_estado'),
    (r'relatorio/por_local$', 'por_local'),
)

