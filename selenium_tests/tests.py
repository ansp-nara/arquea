# -*- coding: utf-8 -*-
from utils.SeleniumServerTestCase import SeleniumServerTestCase
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class HomeTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(HomeTest, self).setUp()
        
    def tearDown(self):
        super(HomeTest, self).tearDown()
    
    def test_home_page(self):
        self.browser.get(self.sistema_url + '/admin/')
         
        elemHeader = self.browser.find_element_by_css_selector('div#container h1')
        self.assertEquals(elemHeader.text, u'Administração do Site')
 
        
    def test_controle_500(self):
        url = self.sistema_url + '/membro/mensalf?ano=2012&mes=1&'
        req = self.browser.get(url)
        self.assertTrue(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
                
    def test_controle_404(self):
        url = self.sistema_url + '/admin/asdfasdfasdf/'
        self.browser.get(url)
        self.assertTrue(self.is_http_404(), u'Requisicao %s etornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)


class AuthTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(AuthTest, self).setUp()
        
    def tearDown(self):
        super(AuthTest, self).tearDown()
    
    def test__auth__assinatura__lista(self):
        url = self.sistema_url + '/admin/membro/assinatura/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__auth__assinatura__registro(self):
        url = self.sistema_url + '/admin/membro/assinatura/4/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)


class MembroTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(MembroTest, self).setUp()
        
    def tearDown(self):
        super(MembroTest, self).tearDown()
    
    def test__cargo__lista(self):
        url = self.sistema_url + '/admin/membro/cargo/'
        logger.debug(url)
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
"""
    def test__cargo__registro(self):
        url = self.sistema_url + '/admin/membro/cargo/45/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
    
    def test__controles__lista(self):
        url = self.sistema_url + '/admin/membro/controle/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__controles__registro_filtro(self):
        url = self.sistema_url + '/admin/membro/controle/?membro__id__exact=2'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__controles__registro(self):
        url = self.sistema_url + '/admin/membro/controle/2242/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__dispensas__lista(self):
        url = self.sistema_url + '/admin/membro/dispensalegal/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__membro__registro(self):
        url = self.sistema_url + '/admin/membro/dispensalegal/21/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__ferias__lista(self):
        url = self.sistema_url + '/admin/membro/ferias/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__ferias__busca(self):
        url = self.sistema_url + '/admin/membro/ferias/?q=anna'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__ferias__registro(self):
        url = self.sistema_url + '/admin/membro/ferias/12/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__membro__lista(self):
        url = self.sistema_url + '/admin/membro/membro/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__membro__lista_paginacao(self):
        url = self.sistema_url + '/admin/membro/membro/?p=2'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__membro__busca(self):
        url = self.sistema_url + '/admin/membro/membro/?q=paulo'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__membro__registro(self):
        url = self.sistema_url + '/admin/membro/membro/45/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__tipo_dispensa__lista(self):
        url = self.sistema_url + '/admin/membro/tipodispensa/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__tipo_dispensa__registro(self):
        url = self.sistema_url + '/admin/membro/tipodispensa/10/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__tipo_de_assinatura__lista(self):
        url = self.sistema_url + '/admin/membro/tipoassinatura/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__tipo_de_assinatura__registro(self):
        url = self.sistema_url + '/admin/membro/tipoassinatura/2/'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)


class IdentificacaoTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(IdentificacaoTest, self).setUp()
        
    def tearDown(self):
        super(IdentificacaoTest, self).tearDown()
    
    def test__relatorio_tecnico__documentos_por_entidade__lista(self):
        url = self.sistema_url + '/identificacao/relatorios/arquivos'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
"""

class FinanceiroTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(FinanceiroTest, self).setUp()
        
    def tearDown(self):
        super(FinanceiroTest, self).tearDown()
    
    def test__relatorio_gerencial__acordo__filtro_inicial(self):
        """
        Verifica se o filtro de acordo lista ao menos os últimos 5 acordos
        """
        self.browser.get(self.sistema_url + '/financeiro/relatorios/acordos')
         
        elem = self.browser.find_element_by_css_selector('select#id_termo')
        
        self.assertTrue(elem.text.find('13/11711-5') >= 0)
        self.assertTrue(elem.text.find('11/52044-6') >= 0)
        self.assertTrue(elem.text.find('10/52277-8') >= 0)
        self.assertTrue(elem.text.find('09/11388-4') >= 0)
        self.assertTrue(elem.text.find('08/52885-8') >= 0)
        
    def test__relatorio_gerencial__acordo__lista(self):
        """
        Verifica se o relatorio foi aberto
        """
        self.browser.get(self.sistema_url + '/financeiro/relatorios/acordos?termo=21')
         
        elem = self.browser.find_element_by_css_selector('div#content.colM h1')
        self.assertTrue(elem.text.find('13/11711-5') >= 0)
        
        elem = self.browser.find_element_by_css_selector('tr#tr_1_2.nivel1 td')
        self.assertTrue(elem.text.find(u'Colaboração') >= 0)
        
        elem = self.browser.find_element_by_css_selector('.nivel3 td a')
    
    def test__relatorio_gerencial__gerencial__filtro_inicial(self):
        url = self.sistema_url + '/financeiro/relatorios/gerencial'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_gerencial__gerencial__lista(self):
        url = self.sistema_url + '/financeiro/relatorios/gerencial?termo=21'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)


class OutorgaTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(OutorgaTest, self).setUp()
        
    def tearDown(self):
        super(OutorgaTest, self).tearDown()
    
    def test__relatorio_gerencial__concessoes_por_acordo__lista(self):
        url = self.sistema_url + '/outorga/relatorios/lista_acordos'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_gerencial__gerencial_progressivo__lista(self):
        url = self.sistema_url + '/outorga/relatorios/acordo_progressivo'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)


class RedeTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(RedeTest, self).setUp()
        
    def tearDown(self):
        super(RedeTest, self).tearDown()
    
    def test__relatorio_gerencial__custo_de_recursos_contratados__lista(self):
        url = self.sistema_url + '/rede/custo_terremark'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__dados_cadastrais_dos_participantes__lista(self):
        url = self.sistema_url + '/rede/info'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__dados_cadastrais_dos_participantes__lista_info_tec(self):
        url = self.sistema_url + '/rede/info_tec/3'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__lista_de_bloco_ip__filtro_inicial(self):
        url = self.sistema_url + '/rede/blocosip'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_todos(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=0&proprietario=0&usuario=0&designado=0'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_anunciante(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=32&proprietario=0&usuario=0&designado=0'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_proprietario(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=0&proprietario=32&usuario=0&designado=0'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_usuario(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=0&proprietario=0&usuario=215&designado=0'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_designado(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=0&proprietario=0&usuario=0&designado=215'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_anunciante_designado(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=32&proprietario=32&usuario=0&designado=215'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_anunciante_usuario(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=32&proprietario=32&usuario=215&designado=0'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_todos_filtros(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=32&proprietario=32&usuario=215&designado=215'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__planejamento_por_ano__filtro_inicial(self):
        url = self.sistema_url + '/rede/planejamento'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__planejamento_por_ano__busca(self):
        url = self.sistema_url + '/rede/planejamento?anoproj=2013%2F1&os='
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__planejamento_por_ano__busca_os(self):
        url = self.sistema_url + '/rede/planejamento?anoproj=2013%2F1&os=109'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__servicos_contratados_por_processo__filtro_inicial(self):
        url = self.sistema_url + '/rede/planejamento2'
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)

    def test__relatorio_tecnico__servicos_contratados_por_processo__lista(self):
        url = self.sistema_url + '/rede/planejamento2?entidade=1&termo=17&beneficiado='
        req = self.browser.get(url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)


class ProcessoTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(ProcessoTest, self).setUp()
        
    def tearDown(self):
        super(ProcessoTest, self).tearDown()
    
    def test__relatorio_gerencial__processos__lista(self):
        url = self.sistema_url + '/processo/processos'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)


class PatrimonioTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(PatrimonioTest, self).setUp()
        
    def tearDown(self):
        super(PatrimonioTest, self).tearDown()

    def test__relatorio_tecnico__busca_por_tipo_de_equpamento__filtro_inicial(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__busca_por_tipo_de_equpamento__busca_todos(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento?tipo=0&estado=0&partnumber=0'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__busca_por_tipo_de_equpamento_busca_por_tipo_estado(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento?tipo=1&estado=22&partnumber=0'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__busca_por_tipo_de_equpamento__busca_por_tipo(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento?tipo=1&estado=0&partnumber=0'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__busca_por_tipo_de_equpamento__busca_partnumber(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento?tipo=0&estado=0&partnumber=0350WYC%2F0+CN'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__patrimonio_por_estado_do_item__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_estado'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__patrimonio_por_localizacao__filtro_inicial(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_local'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__patrimonio_por_localizacao__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_local?entidade=1&endereco=60&detalhe=24&detalhe1=&detalhe2='
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__patrimonio_por_marca__filtro_inicial(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_marca'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__patrimonio_por_marca__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_marca?marca=3Com'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__patrimonio_por_tipo__filtro_inicial(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__patrimonio_por_tipo__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo?tipo=42'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__patrimonio_por_tipo_de_equipamento__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento2'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__racks__filtro_inicial(self):
        url = self.sistema_url + '/patrimonio/racks'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__racks__lista(self):
        url = self.sistema_url + '/patrimonio/racks?dc=13'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)

    def test__relatorio_tecnico__racks__lista(self):
        url = self.sistema_url + '/patrimonio/racks?dc=13'
        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)'%url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)'%url)


