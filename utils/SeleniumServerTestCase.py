# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.conf import settings
from selenium import webdriver, selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class SeleniumServerTestCase(LiveServerTestCase):
    def setUp(self):
        # Only display possible problems
        selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        selenium_logger.setLevel(logging.WARNING)

        # configura a url do sistema que vai ser testada
        self.sistema_url = 'http://' + settings.SELENIUM_SISTEMA_HOST +''
        
        # iniciando conexão com o Selenium Server
        server_url = "http://%s:%s/wd/hub" % (settings.SELENIUM_HOST , settings.SELENIUM_PORT)
        dc = DesiredCapabilities.HTMLUNIT
        self.browser = webdriver.Remote(server_url, dc)
        
        self.login()

    def tearDown(self):
        self.browser.quit()
        
    def login(self):
        """
        Faz o handshake com o CAS para fazer o login no Sistema
        """
        self.browser.get('https://cas.ansp.br/cas/login?service=http%3A%2F%2F' + settings.SELENIUM_SISTEMA_HOST + '%2Faccounts%2Flogin%2F%3Fnext%3D%252Fadmin%252F')

        # She sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        
        elem = self.browser.find_element_by_id("id_username").send_keys(settings.SELENIUM_SISTEMA_USERNAME)
        elem = self.browser.find_element_by_id("id_password").send_keys(settings.SELENIUM_SISTEMA_PASS)
        
        self.browser.find_element_by_id("login-form").submit();

    def is_http_404(self):
        elemHeader = None
        
        try:
            # DESENVOLVIMENTO
            elemHeader = self.browser.find_element_by_css_selector('div#summary h1')
        except:
            try:
                # PRODUCAO
                elemHeader = self.browser.find_element_by_css_selector('div#content.colM h2')
            except:
                print

        # Teste de 404 para ambientes de desenvolvimento
        if elemHeader and elemHeader.text.find('Page not found') >=0:
            return True
        # Teste de 404 para ambientes de produção
        elif elemHeader and elemHeader.text.find(u"não existe no sistema.") >=0:
            return True
                
    def is_http_500(self):
        elemHeaderDesenv = None
        elemHeaderProd = None
        
        try:
            # DESENVOLVIMENTO
            elemHeaderDesenv = self.browser.find_element_by_css_selector('div#traceback')
        except:
            try:
                # PRODUCAO
                elemHeaderProd = self.browser.find_element_by_css_selector('div#content.colM')
            except:
                print

        # Teste de 500 para ambientes de desenvolvimento
        if elemHeaderDesenv:
            return True
        # Teste de 500 para ambientes de produção
        elif elemHeaderProd and elemHeaderProd.text.find('Ocorreu um erro no sistema') >=0:
            return True

