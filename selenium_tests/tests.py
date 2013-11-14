# -*- coding: utf-8 -*-
from utils.SeleniumServerTestCase import SeleniumServerTestCase
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class PollsTest(SeleniumServerTestCase):
    
    def setUp(self):
        super(PollsTest, self).setUp()
        
    def tearDown(self):
        super(PollsTest, self).tearDown()
    
    def test_home_page(self):
        self.browser.get(self.sistema_url + '/admin/')
         
        elemHeader = self.browser.find_element_by_css_selector('div#container h1')
        self.assertEquals(elemHeader.text, u'Administração do Site')
 
        
    def test_controle_500(self):
        req = self.browser.get(self.sistema_url + '/membro/mensalf?ano=2012&mes=1&')
        self.assertTrue(self.test_500())
        self.assertFalse(self.test_404())
        
    def test_controle_404(self):
        self.browser.get(self.sistema_url + '/admin/asdfasdfasdf/')
        self.assertTrue(self.test_404())
        self.assertFalse(self.test_500())



