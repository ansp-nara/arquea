from django.conf.urls import *

urlpatterns = patterns('patrimonio.views',
    (r'escolhe_termo$', 'escolhe_termo'),
    (r'escolhe_protocolo$', 'escolhe_protocolo'),
    (r'escolhe_pagamento$', 'escolhe_pagamento'),
    (r'escolhe_entidade$', 'escolhe_entidade'),
)

