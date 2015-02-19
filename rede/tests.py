# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from identificacao.models import ASN, Entidade
from rede.models import BlocoIP, RIR


class BlocoIPModelTest(TestCase):
    def setUp(self):
        asn_entidade = Entidade.objects.create(sigla='ANSP_ASN', nome='nome ANSP_ASN', cnpj='', fisco= True, url='')
        asn = ASN.objects.create(numero=1234, entidade=asn_entidade, pais="BR")
        
        proprietario_entidade = Entidade.objects.create(sigla='ANSP_PROP', nome='nome ANSP_PROP', cnpj='', fisco= True, url='')
        proprietario = ASN.objects.create(numero=4321, entidade=proprietario_entidade, pais="BR")
        
        designado = Entidade.objects.create(sigla='ANSP_DESIGNADO', nome='nome ANSPP_DESIGNADO', cnpj='', fisco= True, url='')
        usuario = Entidade.objects.create(sigla='ANSP_USUARIO', nome='nome ANSP_USUARIO', cnpj='', fisco= True, url='')
        
        rir = RIR.objects.create(nome="RIR1")
        
        ipv4 = BlocoIP.objects.create(ip='192.168.1.0', mask='20',
                                      asn=asn, proprietario=proprietario, superbloco=None,
                                      designado=designado, usuario=usuario, rir=rir,
                                      obs="OBS ipv4 - n1", transito=True)

        ipv6 = BlocoIP.objects.create(ip='2001:0db8::7344', mask='20',
                                      asn=asn, proprietario=proprietario, superbloco=None,
                                      designado=designado, usuario=usuario, rir=rir,
                                      obs="OBS ipv6 - n1", transito=True)

    def test_unicode(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEquals('192.168.1.0/20', p.__unicode__())

    def test_cidr(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEquals('192.168.1.0/20', p.cidr())

    def test_netmask(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEquals('255.255.240.0', p.netmask())

    def test_ipv4(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertTrue(p.is_IPV4())
        self.assertFalse(p.is_IPV6())

    def test_ipv6(self):
        p = BlocoIP.objects.get(ip='2001:0db8::7344')
        self.assertTrue(p.is_IPV6())
        self.assertFalse(p.is_IPV4())

    def test_AS(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEquals(1234, p.AS())

    def test_prop(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEquals('ANSP_PROP', p.prop().entidade.sigla)

    def test_usu(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEquals('ANSP_USUARIO', p.usu())

    def test_desig(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEquals('ANSP_DESIGNADO', p.desig())

    def test_leaf(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertTrue(p.leaf())

    def test_superbloco(self):
        asn_entidade = Entidade.objects.create(sigla='SUPERBLOCO_ANSP_ASN', nome='nome ANSP_ASN', cnpj='', fisco= True, url='')
        asn = ASN.objects.create(numero=1234, entidade=asn_entidade, pais="BR")
        
        proprietario_entidade = Entidade.objects.create(sigla='SUPERBLOCO_ANSP_PROP', nome='nome ANSP_PROP', cnpj='', fisco= True, url='')
        proprietario = ASN.objects.create(numero=4321, entidade=proprietario_entidade, pais="BR")
        
        designado = Entidade.objects.create(sigla='SUPERBLOCO_ANSP_DESIGNADO', nome='nome ANSPP_DESIGNADO', cnpj='', fisco= True, url='')
        usuario = Entidade.objects.create(sigla='SUPERBLOCO_ANSP_USUARIO', nome='nome ANSP_USUARIO', cnpj='', fisco= True, url='')
        
        rir = RIR.objects.create(nome="SUPERBLOCO_RIR1")
        
        ipv4_superbloco = BlocoIP.objects.create(ip='192.168.0.0', mask='20',
                                      asn=asn, proprietario=proprietario, superbloco=None,
                                      designado=designado, usuario=usuario, rir=rir,
                                      obs="OBS ipv4 - superbloco", transito=True)

        p = BlocoIP.objects.get(ip='192.168.1.0')
        p.superbloco = ipv4_superbloco
        p.save()
        
        ipv4_superbloco = BlocoIP.objects.get(ip='192.168.0.0')
        self.assertFalse(ipv4_superbloco.leaf())


class ViewPermissionDeniedTest(TestCase):
    """
    Teste das permissões das views. Utilizando um usuário sem permissão de superusuário.
    """
    fixtures = ['auth_user.yaml', 'treemenus.yaml',]
    
    def setUp(self):
        super(ViewPermissionDeniedTest, self).setUp()
        self.response = self.client.login(username='john', password='123456')

    def test_planejamento(self):
        url = reverse("rede.views.planejamento")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_planilha_informacoes_gerais(self):
        url = reverse("rede.views.planilha_informacoes_gerais")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_planejamento2(self):
        url = reverse("rede.views.planejamento2")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_blocosip(self):
        url = reverse("rede.views.blocosip")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_blocosip_ansp(self):
        url = reverse("rede.views.blocosip_ansp")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_blocosip_transito(self):
        url = reverse("rede.views.blocosip_transito")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_blocosip_inst_transito(self):
        url = reverse("rede.views.blocosip_inst_transito")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_blocosip_inst_ansp(self):
        url = reverse("rede.views.blocosip_inst_ansp")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_custo_terremark(self):
        url = reverse("rede.views.custo_terremark")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_relatorio_recursos_operacional(self):
        url = reverse("rede.views.relatorio_recursos_operacional")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)


class ViewTest(TestCase):
 
    # Fixture para carregar dados de autenticação de usuário
    fixtures = ['auth_user_superuser.yaml', 'treemenus.yaml',]
    
    def setUp(self):
        super(ViewTest, self).setUp()
        # Comando de login para passar pelo decorator @login_required
        self.response = self.client.login(username='john', password='123456')

    def setUpBlocoIP(self):
        # Registro 1
        asn_entidade = Entidade.objects.create(sigla='ANSP_ASN_1', nome='nome ANSP_ASN_1', cnpj='', fisco= True, url='')
        asn = ASN.objects.create(numero=1234, entidade=asn_entidade, pais="BR")
        
        proprietario_entidade = Entidade.objects.create(sigla='ANSP_PROP_1', nome='nome ANSP_PROP_1', cnpj='', fisco= True, url='')
        proprietario = ASN.objects.create(numero=4321, entidade=proprietario_entidade, pais="BR")
        
        designado = Entidade.objects.create(sigla='ANSP_DESIGNADO_1', nome='nome ANSP_DESIGNADO_1', cnpj='', fisco= True, url='')
        usuario = Entidade.objects.create(sigla='ANSP_USUARIO_1', nome='nome ANSP_USUARIO_1', cnpj='', fisco= True, url='')
        
        rir = RIR.objects.create(nome="RIR_1")
        
        ipv4 = BlocoIP.objects.create(ip='192.168.1.0', mask='20',
                                      asn=asn, proprietario=proprietario, superbloco=None,
                                      designado=designado, usuario=usuario, rir=rir,
                                      obs="OBS ipv4 - n1", transito=True)
        
        # Registro 2
        asn_entidade = Entidade.objects.create(sigla='ANSP_ASN_2', nome='nome ANSP_ASN_2', cnpj='', fisco= True, url='')
        asn = ASN.objects.create(numero=1234, entidade=asn_entidade, pais="BR")
        
        proprietario_entidade = Entidade.objects.create(sigla='ANSP_PROP_2', nome='nome ANSP_PROP_2', cnpj='', fisco= True, url='')
        proprietario = ASN.objects.create(numero=4321, entidade=proprietario_entidade, pais="BR")
        
        designado = Entidade.objects.create(sigla='ANSP_DESIGNADO_2', nome='nome ANSPP_DESIGNADO_2', cnpj='', fisco= True, url='')
        usuario = Entidade.objects.create(sigla='ANSP_USUARIO_2', nome='nome ANSP_USUARIO_2', cnpj='', fisco= True, url='')
        
        rir = RIR.objects.create(nome="RIR_2")
        

        ipv6 = BlocoIP.objects.create(ip='2001:0db8::7344', mask='20',
                                      asn=asn, proprietario=proprietario, superbloco=None,
                                      designado=designado, usuario=usuario, rir=rir,
                                      obs="OBS ipv6 - n1", transito=True)


    def _test_view__blocosip__breadcrumb(self, response):
        # assert breadcrumb
        self.assertContains(response, u'<a href="/rede/blocosip">Lista de Blocos IP</a>')

    def _test_view__blocosip__filtros__cabecalhos(self, response):
        # assert breadcrumb
        self.assertContains(response, u'<select name="anunciante" id="id_anunciante">')
        self.assertContains(response, u'<select name="proprietario" id="id_proprietario">')
        self.assertContains(response, u'<select name="usuario" id="id_usuario">')
        self.assertContains(response, u'<select name="designado" id="id_designado">')
        self.assertContains(response, u'<select name="designado" id="id_designado">')
        self.assertContains(response, u'<input type="checkbox" id="id_porusuario" name="porusuario">')

    
    def test_view__blocosip(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica.
        """
        self.setUpBlocoIP()
        
        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {})
        
        self.assertTrue(200, response.status_code)
        
        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)


    def test_view__blocosip__resultado_sem_filtro(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica.
        """
        self.setUpBlocoIP()
        
        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {'anunciante':'0', 'proprietario':'0', 'usuario':'0', 'designado':'0'})
        
        self.assertTrue(200, response.status_code)
        
        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)
        
        # asssert dos dados do relatório. Verificação dos cabeçalhos das colunas.
        self.assertContains(response, u"""<div class="col1">
   Bloco IP
   </div>""")
        self.assertContains(response, u'<div class="colunas">AS anunciante</div>')
        self.assertContains(response, u'<div class="colunas">AS proprietário</div>')
        self.assertContains(response, u'<div class="colunas">Usado por</div>')
        self.assertContains(response, u'<div class="colunas">Designado para</div>')
        self.assertContains(response, u'<div class="colunas">RIR</div>')
        self.assertContains(response, u'<div class="obs">Obs</div>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'<div class="col1"><a href="/admin/rede/blocoip/1/"')
        self.assertContains(response, u'192.168.1.0/20')
        self.assertContains(response, u'<div class="colunas">1234 - ANSP_ASN_1</div>')
        self.assertContains(response, u'<div class="colunas">4321 - ANSP_PROP_1</div>')
        self.assertContains(response, u'<div class="colunas">ANSP_USUARIO_1</div>')
        self.assertContains(response, u'<div class="colunas">ANSP_DESIGNADO_1</div>')
        self.assertContains(response, u'<div class="colunas">RIR_1</div>')
        self.assertContains(response, u'<div class="obs">OBS ipv4 - n1</div>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'<div class="col1"><a href="/admin/rede/blocoip/2/"')
        self.assertContains(response, u'2001:db8::7344/20')
        self.assertContains(response, u'<div class="colunas">1234 - ANSP_ASN_2</div>')
        self.assertContains(response, u'<div class="colunas">4321 - ANSP_PROP_2</div>')
        self.assertContains(response, u'<div class="colunas">ANSP_USUARIO_2</div>')
        self.assertContains(response, u'<div class="colunas">ANSP_DESIGNADO_2</div>')
        self.assertContains(response, u'<div class="colunas">RIR_2</div>')
        self.assertContains(response, u'<div class="obs">OBS ipv6 - n1</div>')


    def test_view__blocosip__filtro_anunciante(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por anunciante.
        """
        self.setUpBlocoIP()
        
        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {'anunciante':'1', 'proprietario':'0', 'usuario':'0', 'designado':'0'})
        
        self.assertTrue(200, response.status_code)
        
        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="1" selected>1234 - ANSP_ASN_1</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'192.168.1.0/20')
        self.assertNotContains(response, u'2001:db8::7344/20')
        

    def test_view__blocosip__filtro_proprietario(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por proprietario.
        """
        self.setUpBlocoIP()
        
        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {'anunciante':'0', 'proprietario':'2', 'usuario':'0', 'designado':'0'})
        
        self.assertTrue(200, response.status_code)
        
        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="2" selected>4321 - ANSP_PROP_1</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'192.168.1.0/20')
        self.assertNotContains(response, u'2001:db8::7344/20')


    def test_view__blocosip__filtro_usuario(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por usuario.
        """
        self.setUpBlocoIP()
        
        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {'anunciante':'0', 'proprietario':'0', 'usuario':'4', 'designado':'0'})
        
        self.assertTrue(200, response.status_code)
        
        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="4" selected>ANSP_USUARIO_1</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'192.168.1.0/20')
        self.assertNotContains(response, u'2001:db8::7344/20')


    def test_view__blocosip__filtro_designado(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por designado.
        """
        self.setUpBlocoIP()
        
        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {'anunciante':'0', 'proprietario':'0', 'usuario':'0', 'designado':'3'})
        
        self.assertTrue(200, response.status_code)
        
        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="3" selected>ANSP_DESIGNADO_1</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'192.168.1.0/20')
        self.assertNotContains(response, u'2001:db8::7344/20')




