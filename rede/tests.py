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












