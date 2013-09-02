# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('verificacao.views',
    (r'relatorio/equipamento_consolidado$', 'equipamento_consolidado'),
    (r'relatorio/equipamento_part_number_modelo_vazio$', 'equipamento_part_number_modelo_vazio'),
    (r'relatorio/equipamento_part_number_vazio$', 'equipamento_part_number_vazio'),
    (r'relatorio/equipamento_part_number_modelo_diferente$', 'equipamento_part_number_modelo_diferente'),
    
    (r'relatorio/patrimonio_consolidado$', 'patrimonio_consolidado'),
    (r'relatorio/patrimonio_equipamento_vazio$', 'patrimonio_equipamento_vazio'),
    (r'relatorio/patrimonio_equipamento_part_number_diferente$', 'patrimonio_equipamento_part_number_diferente'),
    (r'relatorio/patrimonio_equipamento_descricao_diferente$', 'patrimonio_equipamento_descricao_diferente'),
    
    (r'relatorio/patrimonio_equipamento_marca_diferente$', 'patrimonio_equipamento_marca_diferente'),
    (r'relatorio/patrimonio_equipamento_modelo_diferente$', 'patrimonio_equipamento_modelo_diferente'),
    (r'relatorio/patrimonio_equipamento_ncm_diferente$', 'patrimonio_equipamento_ncm_diferente'),
    (r'relatorio/patrimonio_equipamento_tamanho_diferente$', 'patrimonio_equipamento_tamanho_diferente'),
    (r'verificacao/copy_attribute_to_patrimonio$', 'copy_attribute_to_patrimonio'),
    
    
    
)
